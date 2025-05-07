import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from streamlit_extras.grid import grid

# --- Page Config & Styling ---
st.set_page_config(layout="wide")
st.markdown("""
    <style>
        body {
            background-color: #ffffff;
        }
        .highlight-red {
            background-color: rgba(255, 0, 0, 0.1);
            border-left: 5px solid red;
            padding: 10px;
            border-radius: 8px;
            animation: glow 2s ease-in-out infinite alternate;
        }
        @keyframes glow {
            0% { box-shadow: 0 0 5px red; }
            100% { box-shadow: 0 0 20px red; }
        }
        .kpi-box {
            background-color: #f5f5f5;
            border-radius: 10px;
            padding: 15px;
            margin: 5px;
            text-align: center;
            box-shadow: 0 0 5px rgba(0, 0, 0, 0.1);
        }
    </style>
""", unsafe_allow_html=True)

# --- Title ---
st.markdown("""
    <h1 style='color: #0f098e;'>📊 KPI Dashboard</h1>
""", unsafe_allow_html=True)

# --- Filter UI ---
selected_perspectives = st.multiselect("Pilih Perspective:", ["FIN", "CM", "IP", "LG"], default=["IP"])
status_options = ["🔴 Merah", "🟡 Kuning", "🟢 Hijau", "⚫ Hitam"]
selected_status = st.selectbox("Pilih warna status:", status_options, index=0)

# --- Read Data ---
excel_file = "Coba excel.xlsx"
df = pd.read_excel(excel_file, sheet_name="Dulu")

status_mapping = {
    "Merah": "🔴 Merah",
    "Kuning": "🟡 Kuning",
    "Hijau": "🟢 Hijau",
    "Hitam": "⚫ Hitam"
}

# --- Filtered Data ---
filtered_df = df[df['Perspective'].isin(selected_perspectives)]
filtered_df = filtered_df[filtered_df['Traffic Light'] == selected_status.split()[1]]

# --- Top Best & Worst KPI ---
st.markdown("""
### 🔍 Highlight KPI
""")
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### ❌ Top 5 Worst KPI")
    worst = df.sort_values("%Achv", ascending=True).head(5)
    st.dataframe(worst[["KPI", "%Achv"]], use_container_width=True)

with col2:
    st.markdown("#### ✅ Top 5 Best KPI")
    best = df.sort_values("%Achv", ascending=False).head(5)
    st.dataframe(best[["KPI", "%Achv"]], use_container_width=True)

# --- Compact KPI Cards ---
st.markdown("""
### 📋 KPI Details
""")
kpi_grid = grid(3, vertical_align="top")

for i, row in filtered_df.iterrows():
    with kpi_grid.container():
        st.markdown(f"""
            <div class="highlight-red">
                <strong>{row['KPI']}</strong><br>
                🎯 Target: {row['Target Feb']}<br>
                📈 Aktual: {row['Actual Feb']}<br>
                📉 Bulan Lalu: {row['Actual Jan']}<br>
            </div>
        """, unsafe_allow_html=True)

        sparkline_fig = go.Figure(go.Scatter(
            x=["Jan", "Feb"],
            y=[row['Actual Jan'], row['Actual Feb']],
            mode="lines+markers",
            line=dict(color="#b42020"),
            marker=dict(size=6)
        ))
        sparkline_fig.update_layout(
            margin=dict(l=10, r=10, t=30, b=10),
            height=150,
            title=dict(text="Sparkline Trend", x=0.5),
            xaxis=dict(showgrid=False, zeroline=False),
            yaxis=dict(showgrid=False, zeroline=False)
        )
        st.plotly_chart(sparkline_fig, use_container_width=True)

# Optional: Summary Box with Color Count
total_counts = df.groupby('Traffic Light')['KPI'].count()
color_cols = st.columns(4)
colors = ['Merah', 'Kuning', 'Hijau', 'Hitam']
emoji = ['🔴', '🟡', '🟢', '⚫']

for i, c in enumerate(colors):
    with color_cols[i]:
        st.metric(label=f"{emoji[i]} {c}", value=total_counts.get(c, 0))
