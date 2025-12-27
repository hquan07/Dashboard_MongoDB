from dash import Input, Output, State, html
import dash_bootstrap_components as dbc
from components.charts import (
    create_age_chart, create_bmi_chart, create_disease_chart,
    create_province_chart, create_scatter_plot, create_timeline_chart,
    create_stats_cards_data, create_bmi_box_plot, create_disease_treemap,
    create_allergy_bar_chart, create_age_disease_stacked,
    create_registration_heatmap, create_gender_chart
)

def register_callbacks(app, df):
    @app.callback(
        [Output('age-graph', 'figure'),           # 1
         Output('bmi-graph', 'figure'),           # 2
         Output('province-graph', 'figure'),      # 3
         Output('scatter-plot', 'figure'),        # 4
         Output('scatter-legend', 'children'),    # 5
         Output('timeline-chart', 'figure'),      # 6
         Output('count-display', 'children'),     # 7
         Output('stats-cards', 'children'),       # 8
         Output('gender-pie-chart', 'figure'),    # 9
         Output('bmi-box-plot', 'figure'),        # 10
         Output('disease-treemap', 'figure'),     # 11
         Output('allergy-bar-chart', 'figure'),   # 12
         Output('age-disease-stacked', 'figure'), # 13
         Output('registration-heatmap', 'figure')],# 14
        [Input('loc-filter', 'value'),
         Input('dis-filter', 'value'),
         Input('gen-filter', 'value'),
         Input('age-filter', 'value'),
         Input('bmi-range-filter', 'value'),
         Input('reset-filters-btn', 'n_clicks')]
    )
    def update_dashboard(loc, dis, gen, age, bmi_range, reset_clicks):
        dff = df.copy()

        # 1. Logic lọc dữ liệu
        if loc: dff = dff[dff['location'].isin(loc)]
        if dis: dff = dff[dff['commonDiseases'].isin(dis)]
        if gen: dff = dff[dff['gender'].isin(gen)]
        if age: dff = dff[dff['age_group'].isin(age)]
        if bmi_range: dff = dff[(dff['BMI'] >= bmi_range[0]) & (dff['BMI'] <= bmi_range[1])]

        # 2. Lấy dữ liệu thẻ thống kê (Stats Cards)
        stats_data = create_stats_cards_data(dff)

        # 3. Trả về đúng 14 giá trị theo đúng thứ tự Output đã khai báo
        return (
            create_age_chart(dff),             # 1. age-graph
            create_bmi_chart(dff),             # 2. bmi-graph
            create_province_chart(dff),        # 3. province-graph
            create_scatter_plot(dff),          # 4. scatter-plot
            [],                                # 5. scatter-legend
            create_timeline_chart(dff),        # 6. timeline-chart
            f"{len(dff):,}",                   # 7. count-display (Nhận con số đơn thuần)
            create_stats_cards_layout(stats_data), # 8. stats-cards
            create_gender_chart(dff),          # 9. gender-pie-chart (GỌI HÀM TỪ CHARTS)
            create_bmi_box_plot(dff),          # 10. bmi-box-plot
            create_disease_treemap(dff),       # 11. disease-treemap
            create_allergy_bar_chart(dff),     # 12. allergy-bar-chart
            create_age_disease_stacked(dff),   # 13. age-disease-stacked
            create_registration_heatmap(dff)   # 14. registration-heatmap
        )

def create_stats_cards_layout(stats_data):
    """Render hàng thẻ thống kê KPI"""
    return dbc.Row([
        dbc.Col(
            html.Div([
                html.Span(s['icon'], className="text-2xl mr-3"),
                html.Div([
                    html.P(s['title'], className="text-xs text-slate-500 mb-0 uppercase font-bold"),
                    html.H4(s['value'], className="font-bold mb-0"),
                ])
            ], className="flex items-center p-4 bg-white rounded-xl border border-slate-200 shadow-sm"),
            md=3, className="mb-2"
        ) for s in stats_data
    ])