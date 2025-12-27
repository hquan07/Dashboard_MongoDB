import dash
import dash_bootstrap_components as dbc
from pages.app import app
from data.data_loader import load_and_clean_data
from pages.dashboard import get_layout
from callbacks.dashboard_callbacks import register_callbacks

try:
    df = load_and_clean_data('/home/hquan07/Dashboard/data/user_profiles_368_vn34_genderfix - profile.csv')
    print(f"✅ Data loaded successfully: {len(df)} records")
    print(f"   Columns: {', '.join(df.columns.tolist())}")
except Exception as e:
    print(f"❌ Error loading data: {e}")
    print("   Creating sample data for demonstration...")

    import pandas as pd
    import numpy as np

    np.random.seed(42)
    n = 100

    locations = ['Hà Nội', 'TP.HCM', 'Đà Nẵng', 'Cần Thơ', 'Hải Phòng',
                 'Nghệ An', 'Thanh Hóa', 'Bình Dương', 'Đồng Nai', 'Quảng Ninh']
    diseases = ['Tiểu đường', 'Cao huyết áp', 'Hen suyễn', 'Không có',
                'Tim mạch', 'Đau dạ dày', 'Viêm gan', 'Suy thận']
    age_groups = ['Dưới 18', '18-30', '31-45', '46-60', 'Trên 60']
    genders = ['Nam', 'Nữ']

    df = pd.DataFrame({
        'location': np.random.choice(locations, n),
        'commonDiseases': np.random.choice(diseases, n),
        'age_group': np.random.choice(age_groups, n),
        'gender': np.random.choice(genders, n),
        'BMI': np.random.normal(24, 4, n).clip(15, 40)
    })

    print(f"✅ Sample data created: {len(df)} records")

app.layout = get_layout(df)

register_callbacks(app, df)

print("\n" + "=" * 60)
print("🚀 Health Insights Pro - Starting...")
print("=" * 60)
print(f"📊 Dashboard ready with {len(df)} health records")
print(f"🌐 Server: http://localhost:8050")
print("=" * 60 + "\n")

if __name__ == '__main__':
    app.run(debug=True, port=8050)