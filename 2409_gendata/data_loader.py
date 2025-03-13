# data_loader.py

import openpyxl
import csv

def load_names_from_excel(file_path):
    wb = openpyxl.load_workbook(file_path)
    ws = wb.active
    names = []
    for row in ws['A']:
        if row.value:
            names.append(row.value.strip())
    wb.close()
    return names

def load_products_from_csv(file_path):
    products = []
    with open(file_path, 'r', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            product = {
                "product_id": int(row['product_id']),
                "company": row['company'],
                "product_name": row['product_name'],
                "description": row['description'],
                "price": int(row['price']),
                "product_type": row['product_type'],
                "monthly_payment": int(row['monthly_payment']),
                "total_payments": int(row['total_payments'])
            }
            products.append(product)
    return products
