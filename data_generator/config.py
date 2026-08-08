from pathlib import Path

# Project Root Folder
BASE_DIR = Path(__file__).resolve().parent

# Output Folder
OUTPUT_FOLDER = BASE_DIR / "output"

# Row Counts (Optimized Lightweight Sizes for Sub-second Performance)
NUM_CATEGORIES = 30
NUM_CUSTOMERS = 10000        # Pehle 50,000 tha
NUM_EMPLOYEES = 100          # Pehle 500 tha
NUM_PRODUCTS = 1000          # Pehle 5000 tha
NUM_PAYMENTS = 50000         # Pehle 10 Lakh tha
NUM_ORDERS = 50000           # Pehle 10 Lakh tha (50k orders enough hain)
NUM_ORDER_ITEMS = 150000     # Pehle 30 Lakh tha (Ab sirf 1.5 Lakh rows hongi)
NUM_INVENTORY = 1000         # Pehle 5000 tha

# Random Seed
SEED = 42