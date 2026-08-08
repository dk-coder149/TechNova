import numpy as np
import pandas as pd
from faker import Faker
from tqdm import tqdm
from config import NUM_PAYMENTS
from utils.file_utils import save_to_csv

fake = Faker()

def generate_payments():
    methods = ['Cash', 'UPI', 'Card', 'Net Banking', 'Wallet']
    method_probs = [0.15, 0.50, 0.20, 0.10, 0.05]
    
    statuses = ['Paid', 'Pending', 'Failed', 'Refunded']
    status_probs = [0.88, 0.05, 0.05, 0.02]
    
    dates = [fake.date_between(start_date='-2y', end_date='today') for _ in range(NUM_PAYMENTS)]
    
    df = pd.DataFrame({
        "payment_id": np.arange(1, NUM_PAYMENTS + 1),
        "payment_method": np.random.choice(methods, size=NUM_PAYMENTS, p=method_probs),
        "payment_status": np.random.choice(statuses, size=NUM_PAYMENTS, p=status_probs),
        "payment_date": dates
    })
    
    save_to_csv(df, "payments.csv")
    return df