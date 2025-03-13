# generate_customers.py

from faker import Faker
from tqdm import tqdm
import csv
import random
from config import NUM_CUSTOMERS, NAMES_FILE_PATH
from data_loader import load_names_from_excel
from regions import korea_regions

def generate_customers():
    print("고객 데이터를 생성 및 저장 중...")
    fake = Faker('ko_KR')
    fieldnames = ["customer_id", "name", "contact_info", "address", "join_date"]

    # 이름 리스트 로드
    names = load_names_from_excel(NAMES_FILE_PATH)
    if len(names) < NUM_CUSTOMERS:
        raise ValueError("이름 사전에 있는 이름의 수가 생성하려는 고객 수보다 적습니다.")

    random.shuffle(names)  # 이름 리스트를 섞습니다.

    with open('customers.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for i in tqdm(range(1, NUM_CUSTOMERS + 1), desc="고객 데이터 생성"):
            name = names.pop()  # 중복되지 않도록 이름 사용
            join_date = fake.date_between(start_date='-5y', end_date='today')

            # 시도와 시군구 생성
            sido = random.choice(list(korea_regions.keys()))
            sigungu = random.choice(korea_regions[sido])
            address = f"{sido} {sigungu}"

            customer = {
                "customer_id": i,
                "name": name,
                "contact_info": fake.phone_number(),
                "address": address,
                "join_date": join_date.strftime('%Y-%m-%d')
            }
            writer.writerow(customer)
    print("고객 데이터 저장 완료.")
