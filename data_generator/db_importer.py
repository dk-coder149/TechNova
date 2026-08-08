import os
import pandas as pd
from sqlalchemy import create_engine

# MySQL Connection Details (Update your username and password here)
DB_USER = "root"
DB_PASS = "dileep8542"  # <-- Aapna MySQL password daalein
DB_HOST = "localhost"
DB_PORT = "3306"
DB_NAME = "retail_analytics_db"

engine = create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

OUTPUT_FOLDER = "output"

tables_in_order = [
    ("categories", "categories.csv"),
    ("products", "products.csv"),
    ("customers", "customers.csv"),
    ("employees", "employees.csv"),
    ("payments", "payments.csv"),
    ("orders", "orders.csv"),
    ("order_items", "order_items.csv"),
    ("inventory", "inventory.csv"),
]

def import_data():
    print("⏳ Starting Fast Bulk Import into MySQL Database...")
    for table_name, csv_filename in tables_in_order:
        filepath = os.path.join(OUTPUT_FOLDER, csv_filename)
        if os.path.exists(filepath):
            print(f"Importing {csv_filename} into table '{table_name}'...")
            
            # Chunking process for large tables like orders and order_items
            chunksize = 100000 
            for chunk in pd.read_csv(filepath, chunksize=chunksize):
                chunk.to_sql(table_name, con=engine, if_exists='append', index=False)
            print(f"✅ {table_name} imported successfully!")
        else:
            print(f"❌ File not found: {filepath}")

if __name__ == "__main__":
    import_data()