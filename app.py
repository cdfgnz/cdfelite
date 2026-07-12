import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os
import urllib.request

# 1. VERIFICACIÓN DE LIBRERÍAS
try:
    import duckdb
except ImportError:
    st.error("Falta 'duckdb' en el entorno. Ponlo en requirements.txt")
    st.stop()

try:
    import matplotlib.pyplot as plt
    from mplsoccer import PyPizza
except ImportError:
    st.error("Falta 'mplsoccer' o 'matplotlib'.")
    st.stop()

# 2. CONFIGURACIÓN VISUAL
st.set_page_config(page_title="cdfelite Analytics", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #0f1116; color: #ffffff; }
    [data-testid="stSidebar"] { background-color: #161920 !important; }
    h1, h2, h3, h4 { color: #00ffcc !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. CARGA DE DATOS DE DUCKDB
@st.cache_data(show_spinner=False)
def load_football_data():
    db_file = "transfermarkt.duckdb"
    url = "https://pub-e682421888d945d684bcae8890b0ec20.r2.dev/data/transfermarkt-datasets.duckdb"
    try:
        if not os.path.exists(db_file):
            with st.spinner("Descargando base de datos Transfermarkt..."):
                urllib.request.urlretrieve(url, db_file)
        
        conn = duckdb.connect(db_file, read_only=True)
        q = """
            SELECT name AS Player, current_club_name AS Team, 
                   COALESCE(sub_position, position) AS Position,
                   market_value_in_eur AS [Market Value (€)],
                   highest_market_value_in_eur AS [Highest Value (€)]
            FROM players WHERE market_value_in_eur > 0
            ORDER BY market_value_in_eur DESC
        """
        df = conn.execute(q).df()
        conn.close()
        
        # Inyección de métricas sintéticas estables p90
        np.random.seed(42)
        n = len(df)
        df['Goals p90'] = np.random.uniform(0.0, 0.75, n).round(4)
        df['Assists p90'] = np.random.uniform(0.0, 0.50, n).round(4)
        df['xG p90'] = (df['Goals p90'] * np.random.uniform(0.8, 1.2, n)).round(4)
        df['SCA p90'] = np.random.uniform(0.5, 4.0, n).round(4)
        df['Prog Carries'] = np.random.uniform(0.5, 6.5, n).round(4)
        df['Box Touches'] = np.random.uniform(0.2, 8.0, n).round(4)
        
        is_def = df['Position'].str.contains('Goalkeeper|Defender|Back|Keeper', case=False, na=False)
        df.loc[is_def, ['Goals p90', 'xG p90']] = np.random.uniform(0.0, 0.04, sum(is_def)).round(4)
        df['Rating Index'] = ((df['Goals p90']*40) + (df['Assists p90']*30) + (df['SCA p90']*30)).round(1)
        return df
    except Exception as e:
        st.sidebar.error(f"Error DuckDB: {str(e)}")
        return pd.DataFrame({
            "Player": ["Vinicius Jr", "Erling Haaland", "Kylian Mbappe"],
            "Team": ["Real Madrid", "Manchester City", "Real Madrid"],
            "Position": ["Left Winger", "Center-Forward", "Center-Forward"],
            "Market Value (€)": [150000000, 180000000, 180000000],
            "Highest Value (€)": [150000000, 180000000, 180000000],
            "Goals p90": [0.40, 0.86, 0.69], "Assists p90": [0.32, 0.37, 0.06],
            "xG p90": [0.31, 0.47, 0.40], "SCA p90": [3.10, 4.25, 2.20],
            "Prog Carries": [2.33, 6.74, 6.83], "Box Touches": [3.73, 5.97, 3.21],
            "Rating Index": [85.0, 92.5, 88.0]
        })

df_db = load_football_data()

# 4. MENÚ NAVEGACIÓN
st.sidebar.title("cdfelite Navigation")
menu = ["🏠 Home", "📊 Stats Dashboard", "⚖️ Player Comparison", "🔍 Player Scout Report", "🧬 Player Clone", "🕵️‍♂️ Player Profiler", "🧠 Player Performance Index", "📂 Player Screener"]
choice = st.sidebar.radio("Go to:", menu)
st.sidebar.markdown("---")
st.sidebar.caption(f"📊 base de datos: {len(df_db)} jugadores.")

# --- MÓDULOS ---
if choice == "🏠 Home":
    st.title("⚽ cdfelite | Advanced Football Analytics")
    st.markdown("##### *Welcome to your ultimate intelligence football hub.*")
    st.markdown("---")
    st.dataframe(df_db.head(15), use_container_width=True)

elif choice == "📊 Stats Dashboard":
    st.title("📊 Stats Dashboard")
    metrics = ['Goals p90', 'Assists p90', 'xG p90', 'SCA p90', 'Prog Carries', 'Box Touches', 'Market Value (€)']
    x = st.selectbox("X Axis", metrics, index=1)
    y = st.selectbox("Y Axis", metrics, index=4)
    fig = px.scatter(df_db.head(250), x=x, y=y, text="Player", color="Position", size="Market Value (€)")
    fig.update_layout(paper_bgcolor="#0f1116", plot_bgcolor="#161920", font_color="white")
    st.plotly_chart(fig, use_container_width=True)

elif choice == "⚖️ Player Comparison":
    st.title("⚖️ Player Comparison")
    players = sorted(df_db["Player"].unique())
    p1 = st.selectbox("Jugador 1:", players, index=0)
    p2 = st.selectbox("Jugador 2:", players, index=min(1, len(players)-1))
    st.dataframe(df_db[df_db["Player"].isin([p1, p2])], use_container_width=True)

elif choice == "🔍 Player Scout Report":
    st.title("🔍 Player Scout Report (Percentiles)")
    target = st.selectbox("Player:", sorted(df_db["Player"].unique()))
    p_data = df_db[df_db["Player"] == target].iloc[0]
    
    # Arreglado y compactado en una sola línea para evitar fallos de sintaxis
    m_pizza = ['Goals p90', 'Assists p90', 'xG p90', 'SCA p90', 'Prog Carries', 'Box Touches']
    vals = [int(float(p_data[m])*100) if float(p_data[m])<=1 else int(float(p_data[m])*10) for m in m_pizza]
    
    baker = PyPizza(params=m_pizza, background_color="#161920", straight_line_color="#22252c", straight_line_lw=1, last_circle_lw=1, other_circle_lw=1, other_circle_color="#22252c")
    fig, ax = baker.make_pizza(values=vals, figsize=(6, 6), slice_colors=["#00ffcc"]*6, value_colors=["#0f1116"]*6, value_bck_colors=["#00ffcc"]*6, text_props=dict(color="white", fontsize=10, weight="bold"))
    fig.patch.set_facecolor('#0f1116')
    st.pyplot(fig)

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
    max_val = int(df_db["Market Value (€)"].max())
    min_val = int(df_db["Market Value (€)"].min())
    budget = st.slider("Presupuesto Máximo (€):", min_val, max_val, int(max_val * 0.3), step=500000)
    st.dataframe(df_db[df_db["Market Value (€)"] <= budget].sort_values(by="Market Value (€)", ascending=False), use_container_width=True)
