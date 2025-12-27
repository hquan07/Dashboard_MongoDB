import pandas as pd
import os

def load_and_clean_data(file_name):
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(base_path, 'data', file_name)
    df = pd.read_csv(path)

    if df['BMI'].dtype == 'object':
        df['BMI'] = df['BMI'].str.replace(',', '.').astype(float)

    bins = [0, 18, 31, 46, 61, 150]
    labels = ['Dưới 18', '18-30', '31-45', '46-60', 'Trên 60']
    df['age_group'] = pd.cut(df['age'], bins=bins, labels=labels, right=False)

    return df