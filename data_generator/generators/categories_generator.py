import pandas as pd
from config import NUM_CATEGORIES
from utils.file_utils import save_to_csv

CATEGORIES_LIST = [
    "Electronics", "Mobile & Accessories", "Computers & Laptops", "Home Appliances",
    "Kitchenware", "Men's Fashion", "Women's Fashion", "Kids & Toys", "Footwear",
    "Beauty & Personal Care", "Books & Stationery", "Sports & Fitness", "Automotive",
    "Furniture", "Home Decor", "Groceries", "Snacks & Beverages", "Pet Supplies",
    "Jewelry & Watches", "Luggage & Bags", "Gaming", "Cameras & Audio", "Health & Wellness",
    "Garden & Outdoor", "Office Supplies", "Smart Home", "Baby Care", "Musical Instruments",
    "Crafts & Sewing", "Industrial & Tools"
]

def generate_categories():
    categories = CATEGORIES_LIST[:NUM_CATEGORIES]
    df = pd.DataFrame({
        "category_id": range(1, len(categories) + 1),
        "category_name": categories
    })
    save_to_csv(df, "categories.csv")
    return df