from dash import dcc, html
import dash_bootstrap_components as dbc
from components.filters import filter_section
from components.shadcn_ui import Card

def get_layout(df):
    return html.Div([
        # Header Section - Nền màu #33FFFF, Chữ Navy sẫm đậm nét
        html.Div([
            dbc.Container([
                html.Div([
                    html.Div("⚕️", className="text-5xl mb-3 text-[#0f172a]"),
                    html.H1("Health Insights",
                            className="text-4xl font-extrabold text-[#0f172a] mb-2"),
                    # Phụ đề font-black để đậm rõ trên nền Cyan
                    html.P("HỆ THỐNG PHÂN TÍCH HỒ SƠ NÂNG CAO",
                           className="text-[#0f172a] text-xs font-black tracking-[0.25em] mb-6"),
                    html.Div([
                        html.Div([
                            html.Span("● Live", className="text-[#16a34a] font-black mr-2"),
                            # Dòng này tự động cập nhật tổng số hồ sơ khi load trang
                            html.Span(f"| {len(df):,} Hồ sơ hệ thống", className="text-[#0f172a] font-bold")
                        ],
                            className="inline-flex items-center px-6 py-2 rounded-full bg-white/60 border border-black/10 shadow-sm text-sm")
                    ], className="flex justify-center")
                ], className="py-12 flex flex-col items-center justify-center text-center")
            ])
        ], style={'backgroundColor': '#33FFFF'},
            className="border-b border-slate-300 mb-8"),

        dbc.Container([
            dbc.Row([
                # Sidebar bộ lọc
                dbc.Col(filter_section(df), lg=3, md=4),

                # Content Area
                dbc.Col([
                    # KPI Cards được đổ dữ liệu từ Callback
                    html.Div(id='stats-cards', className="mb-6"),

                    dbc.Tabs([
                        # TAB 1: TỔNG QUAN
                        dbc.Tab(label="📊 Tổng quan", tab_id="tab-1", children=[
                            dbc.Row([
                                dbc.Col(Card(dcc.Graph(id='age-graph'), title="Phân bố Độ tuổi"), md=6),
                                dbc.Col(Card(dcc.Graph(id='gender-pie-chart'), title="Tỷ lệ Giới tính"), md=6),
                            ], className="mt-4"),
                            dbc.Row([
                                dbc.Col(Card(dcc.Graph(id='registration-heatmap'), title="Mật độ hoạt động (Đăng ký)"), md=12),
                            ], className="mt-4"),
                            dbc.Row([
                                dbc.Col(Card(dcc.Graph(id='timeline-chart'), title="Tăng trưởng hồ sơ"), md=12),
                            ], className="mt-4"),
                        ], className="p-3 bg-white border border-t-0 rounded-b-xl"),

                        # TAB 2: CHỈ SỐ SỨC KHỎE
                        dbc.Tab(label="🩺 Chỉ số Sức khỏe", tab_id="tab-2", children=[
                            dbc.Row([
                                dbc.Col(Card(dcc.Graph(id='bmi-graph'), title="Phân loại BMI"), md=6),
                                dbc.Col(Card(dcc.Graph(id='bmi-box-plot'), title="So sánh BMI theo Giới tính"), md=6),
                            ], className="mt-4"),
                            dbc.Row([
                                dbc.Col(Card([
                                    dcc.Graph(id='scatter-plot'),
                                    html.Div(id='scatter-legend', className="mt-2 text-xs flex flex-wrap justify-center")
                                ], title="Tương quan Tuổi & BMI"), md=6),
                                dbc.Col(Card(dcc.Graph(id='age-disease-stacked'), title="Bệnh lý theo Nhóm tuổi"), md=6),
                            ], className="mt-4"),
                        ], className="p-3 bg-white border border-t-0 rounded-b-xl"),

                        # TAB 3: ĐỊA PHƯƠNG & RỦI RO
                        dbc.Tab(label="📍 Địa phương & Rủi ro", tab_id="tab-3", children=[
                            dbc.Row([
                                dbc.Col(Card(dcc.Graph(id='disease-treemap'), title="Bản đồ Bệnh lý & Tỉnh thành"), md=12),
                            ], className="mt-4"),
                            dbc.Row([
                                dbc.Col(Card(dcc.Graph(id='allergy-bar-chart'), title="Top 10 Dị ứng phổ biến"), md=6),
                                dbc.Col(Card(dcc.Graph(id='province-graph'), title="Phân loại theo Tỉnh/Thành"), md=6),
                            ], className="mt-4"),
                        ], className="p-3 bg-white border border-t-0 rounded-b-xl"),
                    ], id="tabs-network", active_tab="tab-1")
                ], lg=9, md=8)
            ])
        ], fluid=True)
    ], id='main-container', className="bg-slate-50 min-h-screen pb-12")