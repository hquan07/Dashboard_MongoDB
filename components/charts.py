import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np


def apply_theme(fig, dark_mode=False):
    """Apply consistent theme to charts with dark mode support"""
    if dark_mode:
        colors = {
            'bg': '#1e293b',
            'paper': '#1e293b',
            'text': '#f1f5f9',
            'grid': '#334155',
        }
    else:
        colors = {
            'bg': 'rgba(0,0,0,0)',
            'paper': 'rgba(0,0,0,0)',
            'text': '#0f172a',
            'grid': '#e5e7eb',
        }

    fig.update_layout(
        font_family="Inter",
        paper_bgcolor=colors['paper'],
        plot_bgcolor=colors['bg'],
        font_color=colors['text'],
        margin=dict(
            t=80,
            b=50,
            l=50,
            r=30
        ),
        colorway=[
            "#2563eb", "#3b82f6", "#60a5fa",
            "#93c5fd", "#bfdbfe", "#6366f1", "#8b5cf6"
        ],
        hovermode='closest',
        autosize=True
    )

    fig.update_xaxes(showgrid=False, linecolor=colors['grid'], title_font=dict(size=14))
    fig.update_yaxes(showgrid=True, gridcolor=colors['grid'], title_font=dict(size=14))

    return fig


def create_age_chart(df, dark_mode=False):
    """Enhanced age distribution pie chart"""
    if 'age_group' not in df.columns or len(df) == 0:
        fig = go.Figure()
        fig.add_annotation(text="No data available", showarrow=False)
        return apply_theme(fig, dark_mode)

    age_counts = df['age_group'].value_counts().reset_index()
    age_counts.columns = ['age_group', 'count']

    fig = px.pie(
        age_counts,
        names='age_group',
        values='count',
        hole=0.4,
        color_discrete_sequence=px.colors.sequential.Blues_r
    )

    fig.update_traces(
        textposition='inside',
        textinfo='percent+label',
        hovertemplate='<b>%{label}</b><br>Số lượng: %{value}<br>Tỷ lệ: %{percent}<extra></extra>'
    )

    fig.update_layout(
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5
        )
    )

    return apply_theme(fig, dark_mode)


def create_bmi_chart(df, dark_mode=False):
    """Enhanced BMI histogram with category lines"""
    if 'BMI' not in df.columns or len(df) == 0:
        fig = go.Figure()
        fig.add_annotation(text="No BMI data available", showarrow=False)
        return apply_theme(fig, dark_mode)

    fig = go.Figure()

    # Add histogram
    fig.add_trace(go.Histogram(
        x=df['BMI'],
        nbinsx=20,
        name='BMI Distribution',
        marker_color='#2563eb',
        opacity=0.7,
        hovertemplate='BMI: %{x}<br>Count: %{y}<extra></extra>'
    ))

    # Add category reference lines
    categories = [
        (18.5, 'Underweight', '#ef4444'),
        (25, 'Normal', '#22c55e'),
        (30, 'Overweight', '#f59e0b'),
    ]

    for value, label, color in categories:
        fig.add_vline(
            x=value,
            line_dash="dash",
            line_color=color,
            annotation_text=label,
            annotation_position="top",
            line_width=2,
            opacity=0.6
        )

    fig.update_layout(
        xaxis_title="BMI",
        yaxis_title="Số lượng",
        showlegend=False,
        bargap=0.1
    )

    return apply_theme(fig, dark_mode)


def create_disease_chart(df, dark_mode=False):
    if 'commonDiseases' not in df.columns or len(df) == 0:
        return apply_theme(go.Figure(), dark_mode)

    counts = df['commonDiseases'].value_counts().reset_index().head(10)
    counts.columns = ['disease', 'count']

    fig = px.bar(
        counts,
        x='count',
        y='disease',
        orientation='h',
        color='count',
        color_continuous_scale='Blues',
        text='count'
    )

    fig.update_layout(
        yaxis={'categoryorder': 'total ascending'},
        xaxis_title="Số ca",
        yaxis_title="",
        showlegend=False,
        coloraxis_showscale=False,
        margin=dict(t=30, b=40, l=150, r=40),
        height=400
    )

    fig.update_traces(
        texttemplate='%{text}',
        textposition='outside',
        cliponaxis=False,
        marker_line_color='rgb(8,48,107)',
        marker_line_width=1.5
    )

    return apply_theme(fig, dark_mode)


def create_province_chart(df, dark_mode=False):
    if 'location' not in df.columns or len(df) == 0:
        return apply_theme(go.Figure(), dark_mode)

    prov = df['location'].value_counts().reset_index().head(10)
    prov.columns = ['location', 'count']

    fig = px.bar(
        prov,
        x='count',
        y='location',
        orientation='h',
        color='count',
        color_continuous_scale='GnBu',
        text='count'
    )

    fig.update_layout(
        yaxis={'categoryorder': 'total ascending'},
        xaxis_title="Số hồ sơ",
        yaxis_title="",
        showlegend=False,
        coloraxis_showscale=False,
        margin=dict(t=30, b=40, l=150, r=40),
        height=400
    )

    fig.update_traces(
        texttemplate='%{text}',
        textposition='outside',
        cliponaxis=False,
        marker_line_color='rgb(8,48,107)',
        marker_line_width=1
    )

    return apply_theme(fig, dark_mode)


def create_scatter_plot(df, dark_mode=False):
    """Ẩn chú thích bên trong để dành không gian cho biểu đồ"""
    if df.empty: return apply_theme(go.Figure())

    age_map = {'Dưới 18': 15, '18-30': 24, '31-45': 38, '46-60': 53, 'Trên 60': 70}
    df_plot = df.copy()
    df_plot['age_num'] = df_plot['age_group'].map(age_map)

    fig = px.scatter(
        df_plot, x='age_num', y='BMI', color='commonDiseases',
        opacity=0.7,
        labels={'age_num': 'Độ tuổi (ước tính)', 'BMI': 'Chỉ số BMI'}
    )

    fig.update_layout(
        showlegend=False,
        height=400,
        margin=dict(t=30, b=50, l=50, r=30),
        xaxis_title="Độ tuổi (ước tính)",
        yaxis_title="Chỉ số BMI"
    )

    fig.update_xaxes(title_font=dict(size=12))
    fig.update_yaxes(title_font=dict(size=12))

    return apply_theme(fig, dark_mode)


def create_timeline_chart(df, dark_mode=False):
    """Cố định chiều cao Timeline để bằng với Scatter Plot"""
    if 'age_group' not in df.columns or len(df) == 0:
        return apply_theme(go.Figure(), dark_mode)

    age_order = ['Dưới 18', '18-30', '31-45', '46-60', 'Trên 60']
    counts = [len(df[df['age_group'] == age]) for age in age_order]

    fig = go.Figure(data=[go.Bar(x=age_order, y=counts, marker_color='#2563eb')])
    fig.update_layout(height=400)
    return apply_theme(fig, dark_mode)


def create_stats_cards_data(df):
    """Generate data for statistics cards"""
    stats = []

    if 'BMI' in df.columns and len(df) > 0:
        stats.append({
            'title': 'BMI Trung bình',
            'value': f"{df['BMI'].mean():.1f}",
            'icon': '📊',
            'trend': 'stable',
            'subtitle': f'Min: {df["BMI"].min():.1f} | Max: {df["BMI"].max():.1f}'
        })

    stats.append({
        'title': 'Tổng hồ sơ',
        'value': f"{len(df):,}",
        'icon': '👥',
        'trend': 'up',
        'subtitle': f'{df["age_group"].nunique()} nhóm tuổi' if 'age_group' in df.columns else ''
    })

    if 'commonDiseases' in df.columns and len(df) > 0:
        stats.append({
            'title': 'Loại bệnh lý',
            'value': f"{df['commonDiseases'].nunique()}",
            'icon': '🏥',
            'trend': 'stable',
            'subtitle': f'Phổ biến: {df["commonDiseases"].value_counts().index[0]}' if len(df) > 0 else ''
        })

    if 'location' in df.columns and len(df) > 0:
        stats.append({
            'title': 'Vùng miền',
            'value': f"{df['location'].nunique()}",
            'icon': '📍',
            'trend': 'stable',
            'subtitle': f'Top: {df["location"].value_counts().index[0]}' if len(df) > 0 else ''
        })

    return stats


def create_bmi_box_plot(df, dark_mode=False):
    fig = px.box(df, x='gender', y='BMI', color='gender',
                 points="all", title="Phân bổ BMI theo Giới tính",
                 color_discrete_map={'Nam': '#2563eb', 'Nữ': '#ec4899'})
    return apply_theme(fig, dark_mode)


def create_disease_treemap(df, dark_mode=False):
    fig = px.treemap(df, path=['location', 'commonDiseases'],
                     title="Bản đồ Bệnh lý theo Địa phương",
                     color_continuous_scale='RdBu')
    return apply_theme(fig, dark_mode)


def create_allergy_bar_chart(df, dark_mode=False):
    counts = df['allergies'].value_counts().nlargest(10).reset_index()
    counts.columns = ['Allergy', 'Count']
    fig = px.bar(counts, y='Allergy', x='Count', orientation='h',
                 title="Top 10 Loại Dị ứng Phổ biến",
                 color='Count', color_continuous_scale='Reds')
    fig.update_layout(yaxis={'categoryorder': 'total ascending'})
    return apply_theme(fig, dark_mode)


def create_age_disease_stacked(df, dark_mode=False):
    # Group data
    temp_df = df.groupby(['age_group', 'commonDiseases']).size().reset_index(name='counts')
    fig = px.bar(temp_df, x="age_group", y="counts", color="commonDiseases",
                 title="Bệnh lý theo Nhóm tuổi", barmode="stack")
    return apply_theme(fig, dark_mode)


def create_registration_heatmap(df, dark_mode=False):
    df['createdAt'] = pd.to_datetime(df['createdAt'])
    df['day'] = df['createdAt'].dt.day_name()
    df['hour'] = df['createdAt'].dt.hour

    heatmap_data = df.groupby(['day', 'hour']).size().unstack(fill_value=0)
    # Sắp xếp thứ tự ngày
    days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    heatmap_data = heatmap_data.reindex(days_order)

    fig = px.imshow(heatmap_data, labels=dict(x="Giờ trong ngày", y="Thứ", color="Số lượng"),
                    title="Nhiệt độ Đăng ký (Hoạt động hệ thống)")
    return apply_theme(fig, dark_mode)


def create_gender_chart(df):
    """Biểu đồ tròn phân bổ giới tính với màu sắc chỉ định"""
    counts = df['gender'].value_counts().reset_index()
    counts.columns = ['gender', 'count']

    gender_colors = {
        'Nam': '#2563eb',
        'Nữ': '#f472b6'
    }

    fig = px.pie(
        counts,
        values='count',
        names='gender',
        hole=0.5,
        color='gender',
        color_discrete_map=gender_colors,
        title="<b>PHÂN BỔ GIỚI TÍNH</b>"
    )

    fig.update_traces(textposition='inside', textinfo='percent+label')
    return apply_theme(fig)