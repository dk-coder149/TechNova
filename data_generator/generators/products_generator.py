import random
import pandas as pd
from faker import Faker
from config import NUM_PRODUCTS
from utils.file_utils import save_to_csv

fake = Faker('en_IN')

BRANDS = ["Samsung", "Apple", "Sony", "LG", "Nike", "Adidas", "Puma", "Philips", "Boat", "OnePlus", "Tata", "Reliance"]

def generate_products(categories_df):
    cat_ids = categories_df["category_id"].tolist()
    
    data = []
    for p_id in range(1, NUM_PRODUCTS + 1):
        cat_id = random.choice(cat_ids)
        sku = f"SKU-{cat_id:02d}-{p_id:05d}"
        brand = random.choice(BRANDS)
        name = f"{brand} {fake.word().capitalize()} {fake.word().capitalize()}"
        cost_price = round(random.uniform(100, 25000), 2)
        unit_price = round(cost_price * random.uniform(1.15, 1.60), 2)
        rating = round(random.uniform(2.5, 5.0), 1)
        
        data.append({
            "product_id": p_id,
            "category_id": cat_id,
            "sku": sku,
            "product_name": name,
            "brand": brand,
            "unit_price": unit_price,
            "cost_price": cost_price,
            "rating": rating
        })
        
    df = pd.DataFrame(data)
    save_to_csv(df, "products.csv")
    return df