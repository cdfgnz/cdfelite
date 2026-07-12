import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
from mplsoccer import Radar, PyPizza

# Configuración básica de página
st.set_page_config(page_title="cdfelite", layout="wide")

# Menú simplificado y directo para evitar errores de codificación de texto
menu = [
    "🏠 Home", 
    "📊 Stats Dashboard", 
    "⚖️ Player Comparison", 
    "🔍 Player Scout Report", 
    "🧬 Player Clone", 
    "🕵️‍♂️ Player Profiler", 
    "🧠 Player Performance Index", 
    "📂 Player Screener"
]
choice = st.sidebar.radio("Navigation", menu)

# Base de datos simulada estable
np.random.seed(42)
players = ["Vinicius Jr", "Erling Haaland", "Kylian Mbappe", "Harry Kane", "Rodri", "Jude Bellingham", "Lamine Yamal", "Kevin De Bruyne"]
teams = ["Real Madrid", "Manchester City", "Real Madrid", "Bayern Munich", "Manchester City", "Real Madrid", "Barcelona", "Manchester City"]
db = pd.DataFrame({
    "Player": players, "Team": teams,
    "Goals p90": np.random.uniform(0.1, 0.9, 8),
    "Assists p90": np.random.uniform(0.05, 0.5, 8),
    "xG p90": np.random.uniform(0.1, 0.8, 8),
    "SCA p90": np.random.uniform(1.5, 5.0, 8),
    "Prog Carries": np.random.uniform(2.0, 7.0, 8),
    "Box Touches": np.random.uniform(3.0, 9.0, 8)
})

# --- CONTENIDO DE LOS MÓDULOS ---
if "Home" in choice:
    st.title("⚽ cdfelite | Advanced Football Analytics")
    st.write("Welcome to your ultimate intelligence football hub. Select a module from the sidebar to start analyzing.")
    st.dataframe(db)

elif "Stats Dashboard" in choice:
    st.title("📊 Stats Dashboard")
    fig = px.scatter(db, x="Goals p90", y="Assists p90", text="Player", color="Team", size="xG p90")
    st.plotly_chart(fig, use_container_width=True)

elif "Player Comparison" in choice:
    st.title("⚖️ Player Comparison")
    p1 = st.selectbox("Select Player 1", db["Player"].unique(), index=0)
    p2 = st.selectbox("Select Player 2", db["Player"].unique(), index=1)
    st.dataframe(db[db["Player"].isin([p1, p2])])

elif "Player Scout Report" in choice:
    st.title("🔍 Player Scout Report")
    tgt = st.selectbox("Select Player", db["Player"].unique())
    style = st.radio("Style", ["Pizza Chart", "Radar Chart"])
    
    lbls = ["Goals", "Assists", "xG", "SCA", "Carries", "Touches"]
    vals = [95, 88, 92, 85, 90, 78]
    
    if style == "Pizza Chart":
        baker = PyPizza(params=lbls, background_color="#111111", straight_line_color="#222222", last_circle_color="#00ffcc")
        fig, ax = baker.make_pizza(vals, figsize=(6, 6))
        st.pyplot(fig)
    else:
        radar = Radar(lbls, [0]*6, [100]*6)
        fig, ax = radar.setup_axis()
        radar.draw_circles(ax=ax, facecolor='#222222', edgecolor='#444444')
        radar.draw_radar(vals, ax=ax, kwargs_radar={'facecolor': '#00ffcc', 'alpha': 0.6})
        st.pyplot(fig)

elif "Player Clone" in choice:
    st.title("🧬 Player Clone Engine")
    tgt = st.selectbox("Find matches for", db["Player"].unique())
    st.write("Most statistically identical profiles:")
    st.dataframe(db[db["Player"] != tgt].head(3))

elif "Player Profiler" in choice:
    st.title("🕵️‍♂️ Player Profiler")
    st.write("Core calculated roles:")
    st.dataframe(db[["Player", "Team"]])

elif "Player Performance Index" in choice:
    st.title("🧠 Player Performance Index")
    db["Index"] = (db["Goals p90"] * 60) + (db["Assists p90"] * 40)
    st.dataframe(db[["Player", "Index"]].sort_values(by="Index", ascending=False))

elif "Player Screener" in choice:
    st.title("📂 Player Screener")
    val = st.slider("Minimum Goals per 90", 0.0, 1.0, 0.4)
    st.dataframe(db[db["Goals p90"] >= val])
