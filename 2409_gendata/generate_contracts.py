# generate_contracts.py

from faker import Faker
from tqdm import tqdm
import csv
import random
import datetime
from dateutil.relativedelta import relativedelta
from config import MIN_CONTRACTS_PER_CUSTOMER, MAX_CONTRACTS_PER_CUSTOMER, FIELD_DISTRIBUTIONS, CONTRACT_TERMINATION_SETTINGS, TERMINATION_REASONS
from utils import weighted_choice
import math

def generate_contracts(customers, employees, products):
    print("계약 데이터를 생성 및 저장 중...")
    fake = Faker('ko_KR')
    fieldnames = [
        "contract_id", "customer_id", "employee_id", "product_id",
        "contract_date", "expected_maturity_date", "contract_status",
        "contract_termination_date", "termination_reason",  # 'termination_reason' 필드 추가
        "sign_up_purpose", "sign_up_motivation"
    ]

    sign_up_purposes = FIELD_DISTRIBUTIONS.get('sign_up_purposes', {'장의': 0.8, '결혼': 0.2})
    sign_up_motivations = FIELD_DISTRIBUTIONS.get('sign_up_motivations', {
        '상담원 권유': 0.5,
        '내상조 그대로': 0.2,
        '지인 소개': 0.2,
        '설계사 권유': 0.1
    })
    contract_statuses = FIELD_DISTRIBUTIONS.get('contract_statuses', {
        '진행중': 0.7,
        '완료': 0.25,
        '해지': 0.05
    })

    termination_months_distribution = CONTRACT_TERMINATION_SETTINGS.get('termination_months_distribution', {
        12: 1.0  # 기본값: 12개월 후 해지
    })
    termination_settings = CONTRACT_TERMINATION_SETTINGS.get('termination_months', {})
    distribution = termination_settings.get('distribution', 'uniform')
    min_months = termination_settings.get('min_months', 1)
    max_months = termination_settings.get('max_months', None)


    contracts = []
    contract_id = 1

    with open('contracts.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for customer in tqdm(customers, desc="계약 데이터 생성"):
            num_contracts = random.randint(MIN_CONTRACTS_PER_CUSTOMER, MAX_CONTRACTS_PER_CUSTOMER)
            for _ in range(num_contracts):
                employee = random.choice(employees)
                product = random.choice(products)
                contract_date = fake.date_between(start_date=customer['join_date'], end_date='today')
                expected_maturity_date = contract_date + relativedelta(months=product['total_payments'])
                contract_status = weighted_choice(contract_statuses)
                contract = {
                    "contract_id": contract_id,
                    "customer_id": customer['customer_id'],
                    "employee_id": employee['employee_id'],
                    "product_id": product['product_id'],
                    "contract_date": contract_date.strftime('%Y-%m-%d'),
                    "expected_maturity_date": expected_maturity_date.strftime('%Y-%m-%d'),
                    "contract_status": contract_status,
                    "contract_termination_date": '',
                    "termination_reason": '',  # 초기값 설정
                    "sign_up_purpose": weighted_choice(sign_up_purposes),
                    "sign_up_motivation": weighted_choice(sign_up_motivations)
                }

                if contract_status == '해지':
                # 최대 개월 수 설정 (None이면 만기 예정일까지)
                    if max_months is None:
                        max_months_value = product['total_payments']
                    else:
                        max_months_value = max_months

                    # 해지 개월 수 결정
                    if distribution == 'uniform':
                        termination_months = random.randint(min_months, max_months_value)
                    elif distribution == 'normal':
                        mean = termination_settings.get('mean', (min_months + max_months_value) / 2)
                        stddev = termination_settings.get('stddev', (max_months_value - min_months) / 6)
                        termination_months = int(random.normalvariate(mean, stddev))
                        termination_months = max(min_months, min(termination_months, max_months_value))
                    elif distribution == 'exponential':
                        lambd = termination_settings.get('lambda', 1.0 / ((min_months + max_months_value) / 2))
                        termination_months = int(random.expovariate(lambd))
                        termination_months = max(min_months, min(termination_months, max_months_value))
                    else:
                        # 기본값으로 균등 분포 사용
                        termination_months = random.randint(min_months, max_months_value)

                    # 해지일자 계산
                    termination_date = contract_date + relativedelta(months=termination_months)
                    if termination_date > datetime.date.today():
                        termination_date = datetime.date.today()
                    contract["contract_termination_date"] = termination_date.strftime('%Y-%m-%d')

                    # 해지 사유 결정
                    termination_reason = weighted_choice(TERMINATION_REASONS)
                    contract["termination_reason"] = termination_reason
                else:
                    contract["contract_termination_date"] = ''
                    contract["termination_reason"] = ''

                writer.writerow(contract)
                contracts.append(contract)
                contract_id += 1
    print("계약 데이터 저장 완료.")
    return contracts
