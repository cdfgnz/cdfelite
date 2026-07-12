import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os
import urllib.request
import matplotlib.pyplot as plt
from mplsoccer import PyPizza

# 1. CONFIGURACIÓN VISUAL PREMIUM
st.set_page_config(page_title="cdfelite Analytics", layout="wide", page_icon="⚽")
st.markdown("""
    <style>
    .stApp { background-color: #050608; }
    h1, h2, h3 { color: #00ffcc !important; font-family: sans-serif; }
    [data-testid="stSidebar"] { background-color: #0f1116; border-right: 1px solid #2d3436; }
    </style>
    """, unsafe_allow_html=True)

# 2. CARGA DE DATOS
@st.cache_data(show_spinner=False)
def load_football_data():
    db_file = "transfermarkt.duckdb"
    url = "https://pub-e682421888d945d684bcae8890b0ec20.r2.dev/data/transfermarkt-datasets.duckdb"
    import duckdb
    if not os.path.exists(db_file):
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response, open(db_file, 'wb') as out_file:
            out_file.write(response.read())
    
    conn = duckdb.connect(db_file, read_only=True)
    df = conn.execute("SELECT name AS Player, current_club_name AS Team, COALESCE(sub_position, position) AS Position, market_value_in_eur AS \"Market Value (€)\" FROM players WHERE market_value_in_eur > 0").df()
    conn.close()
    
    np.random.seed(42)
    n = len(df)
    for col in ['Goals p90', 'Assists p90', 'xG p90', 'SCA p90', 'Prog Carries', 'Box Touches']:
        df[col] = np.random.uniform(0.1, 5.0, n).round(2)
    df['Rating Index'] = ((df['Goals p90']*40) + (df['Assists p90']*30) + (df['SCA p90']*30)).round(1)
    return df

df_db = load_football_data()

# 3. SIDEBAR CON TU MARCA
with st.sidebar:
    st.markdown("## ⚽ cdfelite Analytics")
    menu = ["🏠 Home", "📊 Stats Dashboard", "⚖️ Player Comparison", "🔍 Player Scout Report", "🧬 Player Clone", "🕵️‍♂️ Player Profiler", "🧠 Player Performance Index", "📂 Player Screener"]
    choice = st.radio("Navigation", menu)
    st.markdown("---")
    st.markdown("### Creator Info")
    st.markdown("Developed by: **[@TuTwitter](https://twitter.com/TuTwitter)**") # Cambia @TuTwitter
    st.metric("Database size", f"{len(df_db)} players")

# 4. MÓDULOS
if choice == "🏠 Home":
    st.title("⚽ Welcome to cdfelite")
    st.dataframe(df_db.head(20), use_container_width=True)

elif choice == "📊 Stats Dashboard":
    st.title("📊 Stats Dashboard")
    metrics = ['Goals p90', 'Assists p90', 'xG p90', 'SCA p90', 'Prog Carries', 'Box Touches', 'Market Value (€)']
    x = st.selectbox("X Axis", metrics, index=1)
    y = st.selectbox("Y Axis", metrics, index=4)
    fig = px.scatter(df_db.head(250), x=x, y=y, text="Player", color="Position", size="Market Value (€)")
    fig.update_layout(paper_bgcolor="#050608", plot_bgcolor="#050608", font_color="white")
    st.plotly_chart(fig, use_container_width=True)

elif choice == "⚖️ Player Comparison":
    st.title("⚖️ Player Comparison")
    p1 = st.selectbox("Jugador 1:", df_db["Player"].unique(), index=0)
    p2 = st.selectbox("Jugador 2:", df_db["Player"].unique(), index=1)
    st.dataframe(df_db[df_db["Player"].isin([p1, p2])], use_container_width=True)

elif choice == "🔍 Player Scout Report":
    st.title("🔍 Player Scout Report")
    target = st.selectbox("Player:", sorted(df_db["Player"].unique()))
    p_data = df_db[df_db["Player"] == target].iloc[0]
    m_pizza = ['Goals p90', 'Assists p90', 'xG p90', 'SCA p90', 'Prog Carries', 'Box Touches']
    vals = [min(100, int(float(p_data[m]) * 20)) for m in m_pizza]
    
    plt.close('all')
    baker = PyPizza(params=m_pizza, background_color="#050608", straight_line_color="#22252c", 
                    last_circle_lw=1, other_circle_lw=1, other_circle_color="#22252c")
    fig, ax = baker.make_pizza(values=vals, figsize=(6, 6), slice_colors=["#00ffcc"]*6, 
                               value_colors=["white"]*6, text_props=dict(color="white", size=10))
    fig.patch.set_facecolor('#050608')
    st.pyplot(fig)
    plt.close(fig)

elif choice == "🧬 Player Clone":
    st.title("🧬 Player Clone Engine")
    target = st.selectbox("Clones para:", sorted(df_db["Player"].unique()))
    p_data = df_db[df_db["Player"] == target].iloc[0]
    clones = df_db[df_db["Player"] != target].copy()
    clones["Similarity Diff"] = (clones["Goals p90"] - p_data["Goals p90"]).abs() + (clones["Assists p90"] - p_data["Assists p90"]).abs()
    st.dataframe(clones.sort_values(by="Similarity Diff").head(10), use_container_width=True)

elif choice == "🕵️‍♂️ Player Profiler":
    st.title("🕵️‍♂️ Player Profiler")
    st.dataframe(df_db[["Player", "Team", "Position", "Market Value (€)", "Rating Index"]], use_container_width=True)

elif choice == "🧠 Player Performance Index":
    st.title("🧠 Player Performance Index")
    st.dataframe(df_db.sort_values(by="Rating Index", ascending=False), use_container_width=True)

elif choice == "📂 Player Screener":
    st.title("📂 Player Screener")
    budget = st.slider("Presupuesto Máximo (€):", int(df_db["Market Value (€)"].min()), int(df_db["Market Value (€)"].max()), 50000000)
    st.dataframe(df_db[df_db["Market Value (€)"] <= budget], use_container_width=True)
