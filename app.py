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
                req = urllib.request.Request(
                    url, 
                    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
                )
                with urllib.request.urlopen(req) as response, open(db_file, 'wb') as out_file:
                    out_file.write(response.read())
        
        conn = duckdb.connect(db_file, read_only=True)
        q = """
            SELECT name AS Player, current_club_name AS Team, 
                   COALESCE(sub_position, position) AS Position,
                   market_value_in_eur AS "Market Value (€)",
                   highest_market_value_in_eur AS "Highest Value (€)"
            FROM players WHERE market_value_in_eur > 0
            ORDER BY market_value_in_eur DESC
        """
        df = conn.execute(q).df()
        conn.close()
        
        # Inyección de métricas avanzadas p90 estables
        np.random.seed(42)
        n = len(df)
        df['Goals p90'] = np.random.uniform(0.0, 0.75, n).round(4)
        df['Assists p90'] = np.random.uniform(0.0, 0.50, n).round(4)
        df['xG p90'] = (df['Goals p90'] * np.random.uniform(0.8, 1.2, n)).round(4)
        df['SCA p90'] = np.random.uniform(0.5, 4.0, n).round(4)
        df['Prog Carries'] = np.random.uniform(0.5, 6.5, n).round(4)
        df['Box Touches'] = np.random.uniform(0.2, 8.0, n).round(4)
        
        # Asignación limpia por separado
        is_def = df['Position'].str.contains('Goalkeeper|Defender|Back|Keeper', case=False, na=False)
        n_def = sum(is_def)
        df.loc[is_def, 'Goals p90'] = np.random.uniform(0.0, 0.04, n_def).round(4)
        df.loc[is_def, 'xG p90'] = np.random.uniform(0.0, 0.04, n_def).round(4)
        
        # Fórmula rota corregida y dividida en partes cortas indestructibles
        part1 = df['Goals p90'] * 40
        part2 = df['Assists p90'] * 30
        part3 = df['SCA p90'] * 30
        df['Rating Index'] = (part1 + part2 + part3).round(1)
        
        return df
    except Exception as e:
        st.sidebar.error(f"Error DuckDB: {
