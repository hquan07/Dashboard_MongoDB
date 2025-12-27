from dash import dcc, html
import dash_bootstrap_components as dbc
from components.shadcn_ui import Card


def filter_section(df):
    """Phần bộ lọc - Cập nhật Badge Hồ sơ tìm thấy với thiết kế Indigo"""

    # Lấy giá trị BMI thấp nhất/cao nhất cho thanh trượt
    bmi_min = float(df['BMI'].min()) if 'BMI' in df.columns and len(df) > 0 else 10
    bmi_max = float(df['BMI'].max()) if 'BMI' in df.columns and len(df) > 0 else 50

    return Card([
        html.Div([
            # ... (Các bộ lọc 1, 2, 3, 4, 5 giữ nguyên) ...

            # 1. Bộ lọc Địa điểm
            html.Div([
                html.Label("📍 Tỉnh / Thành phố", className="text-xs font-bold uppercase text-blue-600 mb-2 block"),
                dcc.Dropdown(id='loc-filter',
                             options=[{'label': i, 'value': i} for i in sorted(df['location'].unique())],
                             multi=True, placeholder="Chọn địa điểm...", className="dash-dropdown")
            ], className="mb-5"),

            # 2. Bộ lọc Bệnh lý
            html.Div([
                html.Label("🏥 Tiền sử bệnh lý", className="text-xs font-bold uppercase text-blue-600 mb-2 block"),
                dcc.Dropdown(id='dis-filter',
                             options=[{'label': i, 'value': i} for i in sorted(df['commonDiseases'].unique())],
                             multi=True, placeholder="Chọn bệnh lý...", className="dash-dropdown")
            ], className="mb-5"),

            # 3. Bộ lọc Giới tính
            html.Div([
                html.Label("⚧ Giới tính", className="text-xs font-bold uppercase text-blue-600 mb-2 block"),
                dcc.Dropdown(id='gen-filter', options=[{'label': i, 'value': i} for i in sorted(df['gender'].unique())],
                             placeholder="Giới tính...", className="dash-dropdown")
            ], className="mb-5"),

            # 4. Bộ lọc Nhóm tuổi
            html.Div([
                html.Label("👤 Nhóm độ tuổi", className="text-xs font-bold uppercase text-blue-600 mb-2 block"),
                dcc.Dropdown(id='age-filter', options=[{'label': i, 'value': i} for i in
                                                       ['Dưới 18', '18-30', '31-45', '46-60', 'Trên 60']],
                             placeholder="Độ tuổi...", className="dash-dropdown")
            ], className="mb-5"),

            # 5. Bộ lọc Khoảng BMI
            html.Div([
                html.Label("📏 Khoảng BMI", className="text-xs font-bold uppercase text-blue-600 mb-2 block"),
                dcc.RangeSlider(id='bmi-range-filter', min=bmi_min, max=bmi_max, step=0.5,
                                marks={int(i): str(int(i)) for i in range(int(bmi_min), int(bmi_max) + 1, 5)},
                                value=[bmi_min, bmi_max], tooltip={"placement": "bottom", "always_visible": False},
                                className="mb-2"),
                html.Div(id='bmi-range-display', className="text-xs text-slate-500 text-center mt-2")
            ], className="mb-6"),

            # 7. Nút Reset
            html.Div([
                html.Button([html.Span("🔄 ", className="mr-1"), "Reset Filters"],
                            id="reset-filters-btn", className="w-full btn-primary text-center", n_clicks=0)
            ], className="mb-6"),

            html.Div([
                html.Div([
                    html.Div([
                        # Icon 🔍
                        html.Span("🔍", className="mr-2"),
                        # Nhãn văn bản
                        html.Span("Hồ sơ tìm thấy: ", className="font-medium opacity-80"),
                        # ID để Callback đổ dữ liệu vào
                        html.Span(id='count-display', className="font-bold ml-1 text-lg")
                    ],
                        className="""
                        inline-flex items-center justify-center 
                        px-6 py-2 rounded-full 
                        bg-indigo-600 text-white 
                        shadow-lg shadow-indigo-200/50 
                        transition-all hover:scale-105
                    """)
                ], className="flex justify-center w-full")
            ], className="pt-6 border-t border-slate-100")
        ])
    ], title="🎛️ Bảng điều khiển", description="Tùy chỉnh các tham số lọc")