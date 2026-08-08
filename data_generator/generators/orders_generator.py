import numpy as np
import pandas as pd
from config import NUM_ORDERS, NUM_CUSTOMERS, NUM_EMPLOYEES, NUM_PAYMENTS
from utils.file_utils import save_to_csv

def generate_orders(payments_df):
    statuses = ['Delivered', 'Pending', 'Cancelled', 'Returned', 'Shipped']
    status_probs = [0.80, 0.05, 0.05, 0.05, 0.05]
    
    df = pd.DataFrame({
        "order_id": np.arange(1, NUM_ORDERS + 1),
        "customer_id": np.random.randint(1, NUM_CUSTOMERS + 1, size=NUM_ORDERS),
        "employee_id": np.random.randint(1, NUM_EMPLOYEES + 1, size=NUM_ORDERS),
        "payment_id": np.arange(1, NUM_ORDERS + 1),  # 1-to-1 mapping
        "order_date": payments_df["payment_date"].values[:NUM_ORDERS],
        "order_status": np.random.choice(statuses, size=NUM_ORDERS, p=status_probs)
    })
    
    save_to_csv(df, "orders.csv")
    return df