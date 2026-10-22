from playwright.sync_api import expect
from faker import Faker
from datetime import datetime, timedelta

def wait_for(locator):
    expect(locator).not_to_have_count(0)

def generate_user(with_plus=True):
    fake = Faker("en_US")
    user = {
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "address": fake.street_address(),
            "city": fake.city(),
            "state": fake.state(),
            "zip_code": fake.postcode(),
            "phone_number": fake.phone_number() if with_plus else fake.phone_number().replace("+", ""),
            "ssn": fake.ssn(),
            "username": fake.user_name(),
            "password": fake.password(),
            "account": fake.numerify(text="########")
        }
    return user

def add_one_day(date):                                              #Se agrega un dia mas por el desfase temporal con el
    formated_date = datetime.strptime(date, "%m-%d-%Y")             #servidor de parabank, esto permite que coincidan las
    formated_date = formated_date + timedelta(days=1)               #fechas de las transacciones
    final_date = datetime.strftime(formated_date, "%m-%d-%Y")
    return final_date

def  substract_one_day(date):
    formated_date = datetime.strptime(date, "%m-%d-%Y")             #servidor de parabank, esto permite que coincidan las
    formated_date = formated_date - timedelta(days=1)               #fechas de las transacciones
    final_date = datetime.strftime(formated_date, "%m-%d-%Y")
    return final_date

def parse_amount(text):
    amount = float(text.replace("$", "").replace(",", ""))
    return f"{abs(amount):.2f}"

def generate_columns(line):
    return line.split("\t")
 