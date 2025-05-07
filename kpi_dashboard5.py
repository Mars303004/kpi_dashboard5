import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# Sample KPI data
np.random.seed(42)
data = {
    'KPI Name': ['Revenue Growth', 'Customer Satisfaction', 'Efficiency Ratio'],
    'Trend Data': [
        np.random.randint(70, 120, size=12),
        np.random.randint(60, 110, size=12),
        np.random.randint(80, 130, size=12)
    ],
    'Value': [105, 88, 115]
}
df = pd.DataFrame(data)

# Fungsi untuk menentukan warna indikator
def get_color(value):
    if pd.isna(value):
        return "#000000"  # Hitam
    elif value > 100:
        return "#00aa00"  # Hijau
    elif value >= 70:
        return "#ffcc00"  # Kuning
    else:
        return "#b42020"  # Merah

# Fungsi untuk membuat sparkline dengan Plotly
def generate_sparkline(trend_data, color="#0f098e"):
    fig = go.Figure(go.Scatter(
        y=trend_data,
        mode='lines',
        line=dict(color=color, width=2),
        hoverinfo='y'
    ))
    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        height=60,
        xaxis=dict(visible=False),
        yaxis=dict(visible=False)
    )
    return fig

# Judul
st.title("📈 Dashboard KPI Interaktif")

# Tampilkan kartu KPI 2 kolom
for i in range(0, len(df), 2):
    cols = st.columns(2)
    for j in range(2):
        if i + j < len(df):
            row = df.iloc[i + j]
            color = get_color(row['Value'])
            with cols[j]:
                st.markdown(f"### {row['KPI Name']}")
                st.markdown(
                    f"<span style='color:{color}; font-size:24px; font-weight:bold'>{row['Value']}</span>",
                    unsafe_allow_html=True
                )
                spark_fig = generate_sparkline(row['Trend Data'])
                st.plotly_chart(spark_fig, use_container_width=True)

# Pilih KPI untuk detail grafik
selected_kpi = st.selectbox("📊 Pilih KPI untuk lihat detail trend:", df['KPI Name'])

# Grafik detail
selected_row = df[df['KPI Name'] == selected_kpi].iloc[0]
trend = selected_row['Trend Data']
months = [f'Bulan {i+1}' for i in range(len(trend))]

fig_detail = go.Figure(go.Scatter(
    x=months,
    y=trend,
    mode='lines+markers+text',
    text=trend,
    textposition='top center',
    line=dict(color='#0f098e', width=3),
    marker=dict(size=8, color='#b42020')
))

fig_detail.update_layout(
    title=f"Detail Trend: {selected_kpi}",
    xaxis_title="Bulan",
    yaxis_title="Nilai",
    margin=dict(l=40, r=40, t=40, b=40),
    height=400
)

st.plotly_chart(fig_detail, use_container_width=True)
