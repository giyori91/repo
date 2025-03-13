# generate_collections.py

from faker import Faker
from tqdm import tqdm
import csv
import random
import datetime
from dateutil.relativedelta import relativedelta
from config import FIELD_DISTRIBUTIONS
from utils import weighted_choice

def generate_collections(contracts, products):
    print("수금 데이터를 생성 및 저장 중...")
    fieldnames = ["collection_id", "contract_id", "collection_date", "amount", "method", "status"]
    collection_id = 1

    collection_methods = FIELD_DISTRIBUTIONS.get('collection_methods', {
        '자동이체': 0.6,
        '카드결제': 0.3,
        '현금': 0.1
    })
    collection_statuses = FIELD_DISTRIBUTIONS.get('collection_statuses', {
        '완료': 0.9,
        '연체': 0.08,
        '미납': 0.02
    })

    with open('collections.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for contract in tqdm(contracts, desc="수금 데이터 생성"):
            product = next((p for p in products if p['product_id'] == contract['product_id']), None)
            if product is None:
                continue

            monthly_payment = product['monthly_payment']
            total_payments = product['total_payments']
            contract_date = datetime.datetime.strptime(contract['contract_date'], '%Y-%m-%d').date()

            # 수금 종료일 결정
            if contract['contract_status'] == '해지' and contract['contract_termination_date']:
                end_date = datetime.datetime.strptime(contract['contract_termination_date'], '%Y-%m-%d').date()
            else:
                end_date = datetime.date.today()

            # 종료일까지의 납부일 생성
            payment_dates = []
            for n in range(total_payments):
                payment_date = contract_date + relativedelta(months=n)
                if payment_date > end_date:
                    break
                payment_dates.append(payment_date)

            # 해지일자에 가까울수록 연체 확률 증가
            num_payments = len(payment_dates)
            delinquency_start = max(0, num_payments - 3)  # 마지막 3회 납부

            for idx, payment_date in enumerate(payment_dates):
                if idx >= delinquency_start:
                    # 해지일자에 가까운 납부
                    status_choices = {
                        '완료': 0.7,
                        '연체': 0.2,
                        '미납': 0.1
                    }
                else:
                    status_choices = collection_statuses

                status = weighted_choice(status_choices)
                method = weighted_choice(collection_methods)

                collection = {
                    "collection_id": collection_id,
                    "contract_id": contract['contract_id'],
                    "collection_date": payment_date.strftime('%Y-%m-%d'),
                    "amount": monthly_payment,
                    "method": method,
                    "status": status
                }
                writer.writerow(collection)
                collection_id += 1
    print("수금 데이터 저장 완료.")
