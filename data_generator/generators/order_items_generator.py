import numpy as np
import pandas as pd
from tqdm import tqdm
from config import NUM_ORDER_ITEMS, NUM_ORDERS, NUM_PRODUCTS
from utils.file_utils import save_to_csv

def generate_order_items(products_df):
    product_prices = dict(zip(products_df["product_id"], products_df["unit_price"]))
    
    order_ids = np.random.randint(1, NUM_ORDERS + 1, size=NUM_ORDER_ITEMS)
    product_ids = np.random.randint(1, NUM_PRODUCTS + 1, size=NUM_ORDER_ITEMS)
    quantities = np.random.randint(1, 6, size=NUM_ORDER_ITEMS)
    discounts = np.random.choice([0.0, 5.0, 10.0, 15.0, 20.0], size=NUM_ORDER_ITEMS, p=[0.5, 0.2, 0.15, 0.1, 0.05])
    
    selling_prices = []
    print("Calculating Selling Prices for Order Items...")
    for pid, qty, disc in zip(product_ids, quantities, discounts):
        u_price = product_prices[pid]
        s_price = round(u_price * (1 - disc / 100.0) * qty, 2)
        selling_prices.append(s_price)
        
    df = pd.DataFrame({
        "order_item_id": np.arange(1, NUM_ORDER_ITEMS + 1),
        "order_id": order_ids,
        "product_id": product_ids,
        "quantity": quantities,
        "discount": discounts,
        "selling_price": selling_prices
    })
    
    save_to_csv(df, "order_items.csv")
    return df