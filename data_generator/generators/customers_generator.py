import numpy as np
import pandas as pd
from faker import Faker
from tqdm import tqdm
from config import NUM_CUSTOMERS
from utils.file_utils import save_to_csv

fake = Faker('en_IN')

INDIAN_STATES_CITIES = {
    "Maharashtra": ["Mumbai", "Pune", "Nagpur", "Nashik"],
    "Delhi": ["New Delhi", "Delhi"],
    "Karnataka": ["Bengaluru", "Mysuru", "Hubballi"],
    "Tamil Nadu": ["Chennai", "Coimbatore", "Madurai"],
    "Gujarat": ["Ahmedabad", "Surat", "Vadodara"],
    "Uttar Pradesh": ["Lakhnau", "Kanpur", "Varanasi", "Noida"],
    "Telangana": ["Hyderabad", "Warangal"],
    "West Bengal": ["Kolkata", "Howrah"]
}

def generate_customers():
    states = list(INDIAN_STATES_CITIES.keys())
    genders = ['Male', 'Female', 'Other']
    gender_probs = [0.50, 0.48, 0.02]
    
    data = {
        "customer_id": np.arange(1, NUM_CUSTOMERS + 1),
        "first_name": [],
        "last_name": [],
        "gender": np.random.choice(genders, size=NUM_CUSTOMERS, p=gender_probs),
        "age": np.random.randint(18, 70, size=NUM_CUSTOMERS),
        "email": [],
        "phone": [],
        "city": [],
        "state": [],
        "join_date": [fake.date_between(start_date='-3y', end_date='today') for _ in range(NUM_CUSTOMERS)]
    }
    
    for i in tqdm(range(NUM_CUSTOMERS), desc="Generating Customers"):
        g = data["gender"][i]
        if g == 'Male':
            fn = fake.first_name_male()
        elif g == 'Female':
            fn = fake.first_name_female()
        else:
            fn = fake.first_name()
            
        ln = fake.last_name()
        state = np.random.choice(states)
        city = np.random.choice(INDIAN_STATES_CITIES[state])
        
        data["first_name"].append(fn)
        data["last_name"].append(ln)
        data["email"].append(f"{fn.lower()}.{ln.lower()}{i+1}@example.com")
        data["phone"].append(f"+91{fake.numerify('##########')}")
        data["state"].append(state)
        data["city"].append(city)
        
    df = pd.DataFrame(data)
    save_to_csv(df, "customers.csv")
    return df