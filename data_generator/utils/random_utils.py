import random
import numpy as np

def set_seed(seed=42):
    random.seed(seed)
    np.random.seed(seed)

def generate_phone_number():
    return f"+91{random.randint(6000000000, 9999999999)}"