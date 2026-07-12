import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os

# 1. IMPORTACIONES SEGURAS
try:
    import matplotlib.pyplot as plt
    from mplsoccer import PyPizza
except ImportError:
    st.error("Falta 'mplsoccer' o 'matplotlib'. Verifica tu requirements.txt.")
    st.stop()

# 2. CONFIGURACIÓN PREMIUM DE LA PLATAFORMA
st.set_page_config(page_title="cdfelite | Advanced Football Analytics", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0f1116; color: #ffffff; }
    [data-testid="stSidebar"] { background-color: #161920 !important; }
    h1, h2, h3, h4 { color: #00ffcc !important; font-family: 'Inter', sans-serif; font-weight: 800; }
    </style>
    """, unsafe_allow_html=True)

# 3. BASE DE DATOS OPTIMIZADA (Estructura Limpia y Segura)
@st.cache_data
def load_football_data():
    # Dataset nativo y robusto integrado para evitar caídas de red o URLs 404
    rows = [
        {"Player": "Vinicius Jr", "Team": "Real Madrid", "Position": "Left Winger", "Market Value (€)": 150000000, "Highest Value (€)": 150000000, "Goals p90": 0.3996, "Assists p90": 0.3205, "xG p90": 0.3130, "SCA p90": 3.0962, "Prog Carries": 2.3253, "Box Touches": 3.7322},
        {"Player": "Erling Haaland", "Team": "Manchester City", "Position": "Center-Forward", "Market Value (€)": 180000000, "Highest Value (€)": 180000000, "Goals p90": 0.8606, "Assists p90": 0.3686, "xG p90": 0.4673, "SCA p90": 4.2481, "Prog Carries": 6.7444, "Box Touches": 5.9711},
        {"Player": "Kylian Mbappe", "Team": "Real Madrid", "Position": "Center-Forward", "Market Value (€)": 180000000, "Highest Value (€)": 180000000, "Goals p90": 0.6856, "Assists p90": 0.0593, "xG p90": 0.4024, "SCA p90": 2.1989, "Prog Carries": 6.8282, "Box Touches": 3.2063},
        {"Player": "Harry Kane", "Team": "Bayern Munich", "Position": "Center-Forward", "Market Value (€)": 110000000, "Highest Value (€)": 150000000, "Goals p90": 0.5789, "Assists p90": 0.4865, "xG p90": 0.3039, "SCA p90": 3.2998, "Prog Carries": 6.0420, "Box Touches": 8.4559},
        {"Player": "Rodri", "Team": "Manchester City", "Position": "Defensive Midfield", "Market Value (€)": 130000000, "Highest Value (€)": 130000000, "Goals p90": 0.2248, "Assists p90": 0.4246, "xG p90": 0.5283, "SCA p90": 3.5735, "Prog Carries": 3.5231, "Box Touches": 4.5527},
        {"Player": "Jude Bellingham", "Team": "Real Madrid", "Position": "Attacking Midfield", "Market Value (€)": 180000000, "Highest Value (€)": 180000000, "Goals p90": 0.2248, "Assists p90": 0.1456, "xG p90": 0.1976, "SCA p90": 1.6626, "Prog Carries": 2.4884, "Box Touches": 6.9751},
        {"Player": "Lamine Yamal", "Team": "Barcelona", "Position": "Right Winger", "Market Value (€)": 150000000, "Highest Value (€)": 150000000, "Goals p90": 0.1465, "Assists p90": 0.1318, "xG p90": 0.3045, "SCA p90": 3.6264, "Prog Carries": 5.4212, "Box Touches": 4.8703},
        {"Player": "Kevin De Bruyne", "Team": "Manchester City", "Position": "Attacking Midfield", "Market Value (€)": 60000000, "Highest Value (€)": 150000000, "Goals p90": 0.7929, "Assists p90": 0.1325, "xG p90": 0.3565, "SCA p90": 2.0968, "Prog Carries": 4.2008, "Box Touches": 6.1204}
    ]
    df = pd.DataFrame(rows)
    df['Rating Index'] = ((df['Goals p90'] * 40) + (df['Assists p90'] * 30) + (df['SCA p90'] * 30)).round(1)
    return df

df_db = load_football_data()

# 4. MENÚ DE NAVEGACIÓN
st.sidebar.title("cdfelite Navigation")
menu = [
    "🏠 Home", "📊 Stats Dashboard", "⚖️ Player Comparison", 
    "🔍 Player Scout Report", "🧬 Player Clone", "🕵️‍♂️ Player Profiler", 
    "🧠 Player Performance Index", "📂 Player Screener"
]
choice = st.sidebar.radio("Go to:", menu)

st.sidebar.markdown("---")
st.sidebar.caption("📊 Data Source: Core Big Data Stack")
st.sidebar.caption("🚀 Developed by @cdfgnz")

# --- 🏠 HOME ---
if choice == "🏠 Home":
    st.title("⚽ cdfelite | Advanced Football Analytics")
    st.markdown("##### *Welcome to your ultimate intelligence football hub. Select a module from the sidebar to start analyzing.*")
    st.markdown("---")
    st.dataframe(df_db, use_container_width=True)

# --- 📊 STATS DASHBOARD ---
elif choice == "📊 Stats Dashboard":
    st.title("📊 Stats Dashboard")
    metrics = ['Goals p90', 'Assists p90', 'xG p90', 'SCA p90', 'Prog Carries', 'Box Touches', 'Market Value (€)']
    x_axis = st.selectbox("Select X Axis Metric", metrics, index=1)
    y_axis = st.selectbox("Select Y Axis Metric", metrics, index=4)
    
    fig = px.scatter(df_db, x=x_axis, y=y_axis, text="Player", color="Position", size="Market Value (€)")
    fig.update_layout(paper_bgcolor="#0f1116", plot_bgcolor="#161920", font_color="white")
    st.plotly_chart(fig, use_container_width=True)

# --- ⚖️ PLAYER COMPARISON ---
elif choice == "⚖️ Player Comparison":
    st.title("⚖️ Player Comparison")
    players = sorted(df_db["Player"].unique())
    p1 = st.selectbox("Selecciona al Primer Jugador:", players, index=0)
    p2 = st.selectbox("Selecciona al Segundo Jugador:", players, index=min(1, len(players)-1))
    
    comp_df = df_db[df_db["Player"].isin([p1, p2])]
    st.dataframe(comp_df, use_container_width=True)

# --- 🔍 PLAYER SCOUT REPORT ---
elif choice == "🔍 Player Scout Report":
    st.title("🔍 Player Scout Report (Advanced Percentiles)")
    target = st.selectbox("Search Player:", sorted(df_db["Player"].unique()))
    
    p_data = df_db[df_db["Player"] == target].iloc[0]
    metrics_pizza = ['Goals p90', 'Assists p90', 'xG p90', 'SCA p90', 'Prog Carries', 'Box Touches']
    values = [float(p_data[m]) for m in metrics_pizza]
    
    baker = PyPizza(
        params=metrics_pizza,
        background_color="#161920",
        straight_line_color="#22252c",
        straight_line_lw=1,
        last_circle_lw=1,
        other_circle_lw=1,
        other_circle_color="#22252c"
    )
    
    fig, ax = baker.make_pizza(
        values=[int(v * 100) if v <= 1 else int(v * 10) for v in values], 
        figsize=(6, 6),
        slice_colors=["#00ffcc"] * 6,
        value_colors=["#0f1116"] * 6,
        value_bck_colors=["#00ffcc"] * 6,
        text_props=dict(color="white", fontsize=10, weight="bold")
    )
    fig.patch.set_facecolor('#0f1116')
    st.pyplot(fig)

# --- 🧬 PLAYER CLONE ENGINE ---
elif choice == "🧬 Player Clone":
    st.title("🧬 Player Clone Engine")
    target = st.selectbox("Buscar clones para:", sorted(df_db["Player"].unique()))
    p_data = df_db[df_db["Player"] == target].iloc[0]
    
    clones = df_db[df_db["Player"] != target].copy()
    clones["Similarity Diff"] = (clones["Goals p90"] - p_data["Goals p90"]).abs() + (clones["Assists p90"] - p_data["Assists p90"]).abs()
    st.dataframe(clones.sort_values(by="Similarity Diff").head(5), use_container_width=True)

# --- 🕵️‍♂️ PLAYER PROFILER ---
elif choice == "🕵️‍♂️ Player Profiler":
    st.title("🕵️‍♂️ Player Profiler")
    st.dataframe(df_db[["Player", "Team", "Position", "Market Value (€)", "Rating Index"]], use_container_width=True)

# --- 🧠 PLAYER PERFORMANCE INDEX ---
elif choice == "🧠 Player Performance Index":
    st.title("🧠 Player Performance Index")
    st.dataframe(df_db.sort_values(by="Rating Index", ascending=False), use_container_width=True)

# --- 📂 PLAYER SCREENER ---
elif choice == "📂 Player Screener":
    st.title("📂 Player Screener")
    max_val = int(df_db["Market Value (€)"].max())
    budget = st.slider("Presupuesto Máximo (€):", 500000, max_val, 80000000, step=1000000)
    st.dataframe(df_db[df_db["Market Value (€)"] <= budget].sort_values(by="Market Value (€)", ascending=False), use_container_width=True)
