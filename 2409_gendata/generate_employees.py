# generate_employees.py

from faker import Faker
from tqdm import tqdm
import csv
import random
from config import NUM_EMPLOYEES, FIELD_DISTRIBUTIONS
from regions import korea_regions
from utils import weighted_choice

def generate_employees():
    print("직원 데이터를 생성 및 저장 중...")
    fake = Faker('ko_KR')
    positions = FIELD_DISTRIBUTIONS['employee_positions']
    branches = FIELD_DISTRIBUTIONS.get('employee_branches', None)
    fieldnames = ["employee_id", "name", "branch", "position", "contact_info", "hire_date"]

    with open('employees.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for i in tqdm(range(1, NUM_EMPLOYEES + 1), desc="직원 데이터 생성"):
            hire_date = fake.date_between(start_date='-10y', end_date='today')
            position = weighted_choice(positions)
            branch = weighted_choice(branches) if branches else random.choice(list(korea_regions.keys()))

            employee = {
                "employee_id": i,
                "name": fake.name(),
                "branch": branch,
                "position": position,
                "contact_info": fake.phone_number(),
                "hire_date": hire_date.strftime('%Y-%m-%d')
            }
            writer.writerow(employee)
    print("직원 데이터 저장 완료.")
