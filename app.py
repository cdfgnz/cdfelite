import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from mplsoccer import Radar, PyPizza

# 1. CONFIGURACIÓN DE LA PLATAFORMA
st.set_page_config(page_title="cdfelite | Global Football Intelligence", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0f1116; color: #ffffff; }
    [data-testid="stSidebar"] { background-color: #161920 !important; }
    h1, h2, h3, h4 { color: #00ffcc !important; font-family: 'Inter', sans-serif; font-weight: 800; }
    .stSelectbox, .stSlider { color: black; }
    </style>
    """, unsafe_allow_html=True)

# 2. CONEXIÓN DIRECTA A DATOS REALES DE FBREF (WORLDFOOTBALLR PIPELINE)
@st.cache_data
def load_real_fbref_data():
    # Repositorio oficial de almacenamiento de estadísticas de las 5 grandes ligas de la temporada reciente
    url = "https://raw.githubusercontent.com/JaseZiv/worldfootballR_data/master/raw-data/fbref-data/big_5_advanced_comps.csv"
    try:
        # Cargamos el dataset masivo real
        df = pd.read_csv(url, low_memory=False)
        
        # Filtrar solo por la temporada más reciente disponible en el volcado
        if 'Season_End_Year' in df.columns:
            latest_season = df['Season_End_Year'].max()
            df = df[df['Season_End_Year'] == latest_season]
            
        # Nos aseguramos de limpiar los nombres de los jugadores (FBref a veces añade hashes o caracteres tras la barra)
        df['Player'] = df['Player'].str.split('\\').str[0]
        
        # Agrupamos y renombramos métricas estándar por 90 minutos reales
        # Mapeamos columnas típicas de estadísticas estandarizadas de worldfootballR
        rename_dict = {
            'Player': 'Player', 'Squad': 'Team', 'Comp': 'League', 'Pos': 'Position', 'Age': 'Age', 'Mins_Per_90': '90s',
            'Goals_Goals': 'Goals p90', 'Assists_Assists': 'Assists p90', 'Shots_total_Standard': 'Shots p90',
            'PasProg': 'Prog Passes p90', 'Carries_Prog': 'Prog Carries p90'
        }
        
        # En caso de que las columnas varíen según la última actualización del repositorio, buscamos alternativas seguras:
        avail_cols = {}
        for k, v in rename_dict.items():
            match = [c for c in df.columns if k.lower() in c.lower()]
            if match:
                avail_cols[match[0]] = v
                
        df_filtered = df[list(avail_cols.keys())].copy()
        df_filtered.rename(columns=avail_cols, inplace=True)
        
        # Eliminar duplicados si un jugador cambió de equipo a mitad de temporada
        df_filtered = df_filtered.drop_duplicates(subset=['Player'], keep='first')
        
        # Limpieza de valores nulos y filtrado por minutos mínimos reales (más de 3 partidos jugados completos)
        if '90s' in df_filtered.columns:
            df_filtered = df_filtered[df_filtered['90s'] >= 3.0]
            
        # Asegurar valores numéricos correctos en métricas de rendimiento
        metric_cols = [c for c in df_filtered.columns if 'p90' in c]
        for col in metric_cols:
            df_filtered[col] = pd.to_numeric(df_filtered[col], errors='coerce').fillna(0).round(2)
            
        return df_filtered.reset_index(drop=True)
    except Exception as e:
        # Si hay un problema de red o cambios en GitHub, devolvemos un DataFrame vacío para no inventar datos falsos
        return pd.DataFrame()

df_db = load_real_fbref_data()

# 3. CONTROL DE BASE DE DATOS ACTIVA
if df_db.empty:
    st.error("⚠️ Error de conexión con el repositorio de macrodatos de FBref. Por favor, reintenta o verifica la URL.")
    st.stop()

# 4. MENU LATERAL COMPLETO
menu = [
    "🏠 Home", "📊 Stats Dashboard", "⚖️ Player Comparison", 
    "🔍 Player Scout Report", "🧬 Player Clone", "🕵️‍♂️ Player Profiler", 
    "🧠 Player Performance Index", "📂 Player Screener"
]
choice = st.sidebar.radio("Navigation", menu)

st.sidebar.markdown("---")
st.sidebar.subheader("📊 Base de Datos Viva")
st.sidebar.markdown(f"Registros Reales: **{len(df_db)} Futbolistas**")
st.sidebar.caption("Fuente oficial: FBref / Opta via worldfootballR")

# --- MÓDULO 1: HOME ---
if choice == "🏠 Home":
    st.title("⚽ cdfelite")
    st.markdown("##### *Advanced Football Analytics & Scouting Hub* 📊")
    st.markdown("---")
    st.write(
        "Bienvenido a la consola avanzada de inteligencia deportiva. Este panel procesa en tiempo real "
        "las métricas de rendimiento por cada 90 minutos de juego de las principales ligas del mundo."
    )
    st.dataframe(df_db, use_container_width=True)

# --- MÓDULO 2: STATS DASHBOARD ---
elif choice == "📊 Stats Dashboard":
    st.title("📊 Stats Dashboard")
    metrics = [c for c in df_db.columns if 'p90' in c]
    
    col1, col2 = st.columns(2)
    with col1:
        x_axis = st.selectbox("Eje X (Métrica Horizontal):", metrics, index=0)
    with col2:
        y_axis = st.selectbox("Eje Y (Métrica Vertical):", metrics, index=min(1, len(metrics)-1))
        
    fig = px.scatter(
        df_db.head(500), x=x_axis, y=y_axis, text="Player", color="League" if "League" in df_db.columns else None,
        title=f"Dispersión Exclusiva de Rendimiento: {x_axis} vs {y_axis}"
    )
    fig.update_layout(paper_bgcolor="#0f1116", plot_bgcolor="#161920", font_color="white")
    st.plotly_chart(fig, use_container_width=True)

# --- MÓDULO 3: PLAYER COMPARISON (CORREGIDO SIN ERRORES DE PARÉNTESIS) ---
elif choice == "⚖️ Player Comparison":
    st.title("⚖️ Player Comparison")
    
    players = sorted(df_db["Player"].unique())
    p1 = st.selectbox("Selecciona al Primer Jugador:", players, index=0)
    p2 = st.selectbox("Selecciona al Segundo Jugador:", players, index=min(1, len(players)-1))
    
    comp_df = df_db[df_db["Player"].isin([p1, p2])]
    st.dataframe(comp_df, use_container_width=True)

# --- MÓDULO 4: PLAYER SCOUT REPORT (PIZZA & RADAR FIJOS Y SIN ERRORES DE SINTAXIS) ---
elif choice == "🔍 Player Scout Report":
    st.title("🔍 Player Scout Report")
    
    target_player = st.selectbox("Selecciona el jugador a analizar:", sorted(df_db["Player"].unique()))
    chart_style = st.radio("Estilo de Visualización Avanzada:", ["Percentile Pizza Chart", "Tactical Radar Chart"])
    
    player_stats = df_db[df_db["Player"] == target_player].iloc[0]
    metrics_list = [c for c in df_db.columns if 'p90' in c]
    
    # Calcular percentiles exactos sobre el universo real de jugadores de la liga
    percentiles = []
    for m in metrics_list:
        pct = (df_db[m] < player_stats[m]).mean() * 100
        percentiles.append(int(max(5, pct)))
        
    clean_labels = [m.replace(" p90", "") for m in metrics_list]
    
    if len(metrics_list) > 0:
        if chart_style == "Percentile Pizza Chart":
            baker = PyPizza(params=clean_labels, background_color="#0f1116", straight_line_color="#2a303c", last_circle_color="#00ffcc")
            fig, ax = baker.make_pizza(
                percentiles, figsize=(6, 6), slice_colors=["#00ffcc"] * len(metrics_list),
                value_colors=["#0f1116"] * len(metrics_list), value_bck_colors=["#00ffcc"] * len(metrics_list),
                text_props=dict(color="white", fontsize=10, weight="bold")
            )
            st.pyplot(fig)
        else:
            radar = Radar(clean_labels, [0]*len(metrics_list), [100]*len(metrics_list))
            fig, ax = radar.setup_axis()
            fig.patch.set_facecolor('#0f1116')
            ax.set_facecolor('#0f1116')
            radar.draw_circles(ax=ax, facecolor='#161920', edgecolor='#2a303c')
            radar.draw_radar(percentiles, ax=ax, kwargs_radar={'facecolor': '#00ffcc', 'alpha': 0.6})
            st.pyplot(fig)

# --- MÓDULO 5: PLAYER CLONE ENGINE ---
elif choice == "🧬 Player Clone":
    st.title("🧬 Player Clone Engine")
    target = st.selectbox("Buscar gemelos tácticos para:", sorted(df_db["Player"].unique()))
    
    metrics_list = [c for c in df_db.columns if 'p90' in c]
    target_vector = df_db[df_db["Player"] == target][metrics_list].to_numpy()
    
    # Cálculo de similitud por distancia euclidiana real
    distances = []
    for idx, row in df_db.iterrows():
        if row["Player"] == target:
            distances.append(float('inf'))
        else:
            dist = np.linalg.norm(target_vector - row[metrics_list].to_numpy())
            distances.append(dist)
            
    df_db["Similarity Distance"] = distances
    clones = df_db.sort_values(by="Similarity Distance").head(5)
    st.dataframe(clones[["Player", "Team", "League", "Position"] + metrics_list], use_container_width=True)

# --- MÓDULO 6: PLAYER PROFILER ---
elif choice == "🕵️‍♂️ Player Profiler":
    st.title("🕵️‍♂️ Player Profiler")
    st.write("Segmentación posicional del universo completo indexado en FBref:")
    st.dataframe(df_db[["Player", "Team", "Position", "League", "Age"]], use_container_width=True)

# --- MÓDULO 7: PLAYER PERFORMANCE INDEX ---
elif choice == "🧠 Player Performance Index":
    st.title("🧠 Player Performance Index")
    st.write("Clasificación algorítmica por volumen total de aportación ofensiva en jugadas de ataque:")
    
    g_col = [c for c in df_db.columns if 'goal' in c.lower() or 'gls' in c.lower()][0]
    a_col = [c for c in df_db.columns if 'assist' in c.lower() or 'ast' in c.lower()][0]
    
    df_db["Ataque Index"] = (df_db[g_col] * 0.6 + df_db[a_col] * 0.4).round(2)
    ranked = df_db.sort_values(by="Ataque Index", ascending=False)
    st.dataframe(ranked[["Player", "Team", "League", "Ataque Index"]], use_container_width=True)

# --- MÓDULO 8: PLAYER SCREENER ---
elif choice == "📂 Player Screener":
    st.title("📂 Player Screener")
    st.write("Busca talento filtrando parámetros exactos de rendimiento:")
    
    metrics_list = [c for c in df_db.columns if 'p90' in c]
    if metrics_list:
        selected_m = st.selectbox("Elige la métrica de corte:", metrics_list)
        max_val = float(df_db[selected_m].max())
        min_val = float(df_db[selected_m].min())
        
        slider_val = st.slider(f"Valor mínimo de {selected_m}:", min_val, max_val, (max_val + min_val)/4)
        filtered_df = df_db[df_db[selected_m] >= slider_val]
        st.dataframe(filtered_df, use_container_width=True)
