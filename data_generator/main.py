import time
from utils.random_utils import set_seed
from generators.categories_generator import generate_categories
from generators.products_generator import generate_products
from generators.customers_generator import generate_customers
from generators.employees_generator import generate_employees
from generators.payments_generator import generate_payments
from generators.orders_generator import generate_orders
from generators.order_items_generator import generate_order_items
from generators.inventory_generator import generate_inventory

def main():
    start_time = time.time()
    print("🚀 Starting Enterprise Dataset Generation...\n")
    
    set_seed(42)
    
    print("1/8 Generating Categories...")
    categories_df = generate_categories()
    
    print("2/8 Generating Products...")
    products_df = generate_products(categories_df)
    
    print("3/8 Generating Customers...")
    customers_df = generate_customers()
    
    print("4/8 Generating Employees...")
    employees_df = generate_employees()
    
    print("5/8 Generating Payments...")
    payments_df = generate_payments()
    
    print("6/8 Generating Orders...")
    orders_df = generate_orders(payments_df)
    
    print("7/8 Generating Order Items...")
    order_items_df = generate_order_items(products_df)
    
    print("8/8 Generating Inventory...")
    inventory_df = generate_inventory()
    
    elapsed = round(time.time() - start_time, 2)
    print(f"\n✅ Dataset Generation Completed Successfully in {elapsed} seconds!")
    print("📁 Check the 'output/' folder for all CSV files.")

if __name__ == "__main__":
    main()

# from generators.categories_generator import generate_categories


# def main():

#     generate_categories()


# if __name__ == "__main__":
#     main()