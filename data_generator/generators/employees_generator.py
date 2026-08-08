import numpy as np
import pandas as pd
from faker import Faker
from config import NUM_EMPLOYEES
from utils.file_utils import save_to_csv

fake = Faker('en_IN')

DEPARTMENTS = ["Sales", "Customer Support", "Operations", "Logistics", "Marketing"]
DESIGNATIONS = ["Executive", "Senior Executive", "Team Lead", "Manager"]

def generate_employees():
    data = []
    for e_id in range(1, NUM_EMPLOYEES + 1):
        data.append({
            "employee_id": e_id,
            "employee_name": fake.name(),
            "department": np.random.choice(DEPARTMENTS),
            "designation": np.random.choice(DESIGNATIONS),
            "hire_date": fake.date_between(start_date='-5y', end_date='today'),
            "salary": round(float(np.random.uniform(25000, 150000)), 2)
        })
    df = pd.DataFrame(data)
    save_to_csv(df, "employees.csv")
    return df