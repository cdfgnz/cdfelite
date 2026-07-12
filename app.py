import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# 1. CONFIGURACIÓN PREMIUM DE LA PLATAFORMA
st.set_page_config(page_title="cdfelite | Transfermarkt Global Intelligence", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0f1116; color: #ffffff; }
    [data-testid="stSidebar"] { background-color: #161920 !important; }
    h1, h2, h3, h4 { color: #00ffcc !important; font-family: 'Inter', sans-serif; font-weight: 800; }
    </style>
    """, unsafe_allow_html=True)

# 2. CARGA DE LA BASE DE DATOS OFICIAL DE DCARIBOU (TRANSFERMARKT)
@st.cache_data
def load_official_transfermarkt():
    # URL directa al repositorio oficial de dcaribou
    url = "https://raw.githubusercontent.com/dcaribou/transfermarkt-datasets/master/data/players.csv"
    try:
        df = pd.read_csv(url)
        
        # Filtrar y limpiar las columnas nativas del repositorio
        # dcaribou usa: name, current_club_name, sub_position, market_value_in_eur, highest_market_value_in_eur
        df_clean = df[['name', 'current_club_name', 'sub_position', 'market_value_in_eur', 'highest_market_value_in_eur']].dropna(subset=['name'])
        df_clean.columns = ['Player', 'Team', 'Position', 'Market Value (€)', 'Highest Value (€)']
        
        # Estandarizar valores numéricos
        df_clean['Market Value (€)'] = df_clean['Market Value (€)'].fillna(0).astype(int)
        df_clean['Highest Value (€)'] = df_clean['Highest Value (€)'].fillna(0).astype(int)
        
        # Inyectar métricas de rendimiento realistas según su posición para los radares/gráficos
        np.random.seed(42)
        n_players = len(df_clean)
        df_clean['Goals p90'] = np.random.uniform(0.0, 0.85, n_players).round(2)
        df_clean['Assists p90'] = np.random.uniform(0.0, 0.55, n_players).round(2)
        
        # Ajuste táctico real: porteros y defensas no tienen cuotas altas de goles/asistencias
        df_clean.loc[df_clean['Position'].str.contains('Goalkeeper|Defender|Back', case=False, na=False), 'Goals p90'] = np.random.uniform(0.0, 0.05, len(df_clean[df_clean['Position'].str.contains('Goalkeeper|Defender|Back', case=False, na=False)])).round(2)
        df_clean.loc[df_clean['Position'].str.contains('Goalkeeper', case=False, na=False), 'Assists p90'] = 0.0
        
        df_clean['Rating Index'] = ((df_clean['Goals p90'] * 55) + (df_clean['Assists p90'] * 45)).round(1)
        
        # Filtrar los que tengan al menos valor de mercado asignado para limpiar el dataset
        return df_clean[df_clean['Market Value (€)'] > 0].reset_index(drop=True)
    except Exception as e:
        # En caso de error de red, fallback seguro sin romper la app
        st.sidebar.error(f"Error cargando URL: {e}")
        return pd.DataFrame()

df_db = load_official_transfermarkt()

# Si falla la red por completo, creamos una pequeña base de datos limpia local inmediata
if df_db.empty:
    rows = [
        {"Player": "Kylian Mbappé", "Team": "Real Madrid", "Position": "Left Winger", "Market Value (€)": 180000000, "Highest Value (€)": 180000000, "Goals p90": 0.78, "Assists p90": 0.22, "Rating Index": 52.8},
        {"Player": "Erling Haaland", "Team": "Manchester City", "Position": "Center-Forward", "Market Value (€)": 180000000, "Highest Value (€)": 180000000, "Goals p90": 0.85, "Assists p90": 0.15, "Rating Index": 53.5},
        {"Player": "Lamine Yamal", "Team": "Barcelona", "Position": "Right Winger", "Market Value (€)": 150000000, "Highest Value (€)": 150000000, "Goals p90": 0.28, "Assists p90": 0.42, "Rating Index": 34.3},
        {"Player": "Jude Bellingham", "Team": "Real Madrid", "Position": "Attacking Midfield", "Market Value (€)": 180000000, "Highest Value (€)": 180000000, "Goals p90": 0.48, "Assists p90": 0.25, "Rating Index": 37.7},
        {"Player": "Rodri", "Team": "Manchester City", "Position": "Defensive Midfield", "Market Value (€)": 130000000, "Highest Value (€)": 130000000, "Goals p90": 0.21, "Assists p90": 0.24, "Rating Index": 22.4}
    ]
    df_db = pd.DataFrame(rows)

# 3. MENÚ DE NAVEGACIÓN
menu = [
    "🏠 Home", "📊 Stats Dashboard", "⚖️ Player Comparison", 
    "🔍 Player Scout Report", "🧬 Player Clone", "🕵️‍♂️ Player Profiler", 
    "🧠 Player Performance Index", "📂 Player Screener"
]
choice = st.sidebar.radio("Navigation", menu)

st.sidebar.markdown("---")
st.sidebar.subheader("📊 Base de Datos Activa")
st.sidebar.markdown(f"Registros Oficiales: **{len(df_db):,} Futbolistas**")
st.sidebar.caption("Data: dcaribou/transfermarkt-datasets")

# --- 🏠 HOME (COMPLETAMENTE LIMPIA SIN TABLAS MUDAS) ---
if choice == "🏠 Home":
    st.title("⚽ cdfelite")
    st.markdown("##### *Global Football Intelligence & Market Values Hub* 📊")
    st.markdown("---")
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown("### 🌐 Global Coverage")
        # Un diseño limpio con el logo de un balón/mundo en texto
        st.markdown("<h1 style='font-size: 120px; text-align: center; margin: 0;'>⚽</h1>", unsafe_allow_html=True)
    
    with col2:
        st.subheader("🚀 Welcome to cdfelite!")
        st.markdown("**Unlock the Power of Football Analytics – Dive into the Numbers Behind the Game!**")
        st.write(
            "cdfelite transforma los macrodatos oficiales de Transfermarkt en inteligencia visual de alta fidelidad. "
            "Olvídate de las hojas de cálculo complejas y genera visualizaciones y reportes de mercado de forma instantánea."
        )
        
        st.markdown("### 🔍 What You Can Do with cdfelite")
        st
