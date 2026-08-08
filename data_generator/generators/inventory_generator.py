import numpy as np
import pandas as pd
from faker import Faker
from config import NUM_PRODUCTS
from utils.file_utils import save_to_csv

fake = Faker()
WAREHOUSES = ["North Hub (Delhi)", "West Hub (Mumbai)", "South Hub (Bengaluru)", "East Hub (Kolkata)"]

def generate_inventory():
    data = []
    for p_id in range(1, NUM_PRODUCTS + 1):
        data.append({
            "inventory_id": p_id,
            "product_id": p_id,
            "stock_quantity": int(np.random.randint(0, 500)),
            "reorder_level": int(np.random.choice([10, 20, 50, 100])),
            "warehouse": np.random.choice(WAREHOUSES),
            "last_updated": fake.date_between(start_date='-1m', end_date='today')
        })
        
    df = pd.DataFrame(data)
    save_to_csv(df, "inventory.csv")
    return df