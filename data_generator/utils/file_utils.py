import os
import pandas as pd
from config import OUTPUT_FOLDER

def save_to_csv(data_dict_or_df, filename):
    filepath = os.path.join(OUTPUT_FOLDER, filename)
    if isinstance(data_dict_or_df, dict):
        df = pd.DataFrame(data_dict_or_df)
    else:
        df = data_dict_or_df
    df.to_csv(filepath, index=False)
    print(f"Saved: {filepath} ({len(df)} rows)")