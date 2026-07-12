import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
from mplsoccer import Radar, PyPizza

# ==========================================
# 1. CONFIGURACIÓN Y ESTILO VISUAL AVANZADO
# ==========================================
st.set_page_config(page_title="cdfelite | Football Intelligence Hub", page_icon="⚽", layout="wide")

# Diseño de interfaz en Modo Oscuro Premium
st.markdown("""
    <style>
    .stApp { background-color: #0f1116; color: #ffffff; }
    [data-testid="stSidebar"] { background-color: #161920 !important; }
    h1, h2, h3 { color: #00ffcc !important; font-family: 'Inter', sans-serif; font-weight: 800; }
    .module-card {
        background-color: #1c212c;
        padding: 20px;
        border-radius: 12px;
        border-left: 5px solid #00ffcc;
        margin-bottom: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. MENÚ LATERAL COMPLETO CON ICONOS
# ==========================================
st.sidebar.markdown("<h2 style='color:#00ffcc; margin-bottom:0;'>📊 cdfelite</h2>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='color:#8892b0; margin-top:0; font-size:13px;'>Advanced Analytics</p>", unsafe_allow_html=True)
st.sidebar.markdown("---")

# Diccionario de navegación calcado a la imagen (sin Help)
menu_options = {
    "🏠 Home": "Home",
    "📊 Stats Dashboard": "Stats Dashboard",
    "⚖️ Player Comparison": "Player Comparison",
    "🔍 Player Scout Report": "Player Scout Report",
    "🧬 Player Clone": "Player Clone",
    "🕵️‍♂️ Player Profiler": "Player Profiler",
    "🧠 Player Performance Index": "Player Performance Index",
    "📂 Player Screener": "Player Screener"
}

selected_icon_page = st.sidebar.radio("Navigation", list(menu_options.keys()))
page = menu_options[selected_icon_page]

st.sidebar.markdown("---")
st.sidebar.markdown("### ☕ Support cdfelite")
st.sidebar.link_button("🤝 Support on PayPal", "https://paypal.me/")
st.sidebar.caption("📅 Data Source: FBref | Developed by **@cdfgnz**")

# Base de datos simulada para alimentar los motores de búsqueda
@st.cache_data
def get_mock_database():
    np.random.seed(42)
    players = ["Vinicius Jr", "Erling Haaland", "Kylian Mbappé", "Harry Kane", "Rodri", "Jude Bellingham", "Lamine Yamal", "Kevin De Bruyne"]
    teams = ["Real Madrid", "Manchester City", "Real Madrid", "Bayern Munich", "Manchester City", "Real Madrid", "Barcelona", "Manchester City"]
    data = []
    for p, t in zip(players, teams):
        data.append({
            "Player": p, "Team": t,
            "Goals per 90": np.random.uniform(0.1, 0.9),
            "Assists per 90": np.random.uniform(0.05, 0.5),
            "Expected Goals (xG)": np.random.uniform(0.1, 0.8),
            "Shot-Creating Actions": np.random.uniform(1.5, 5.0),
            "Progressive Carries": np.random.uniform(2.0, 7.0),
            "Touches (Box)": np.random.uniform(3.0, 9.0)
        })
    return pd.DataFrame(data)

df_db = get_mock_database()

# ==========================================
# 3. MÓDULOS DE LA PLATAFORMA
# ==========================================

# --- HOME ---
if page == "Home":
    st.title("⚽ Unlock the Power of Football Analytics")
    st.markdown("#### *Transforming raw event data into elite visual intelligence.*")
    st.markdown("---")
    
    col1, col2 = st.columns([4, 5])
    with col1:
        st.write("### 🌐 Global League Coverage")
        map_data = pd.DataFrame({'lat': [40.4, 51.5, 48.8, 52.5, -34.6], 'lon': [-3.7, -0.1, 2.3, 13.4, -58.4], 'League': ['La Liga', 'Premier League', 'Ligue 1', 'Bundesliga', 'Liga Pro']})
        fig_map = px.scatter_geo(map_data, lat='lat', lon='lon', hover_name='League', projection="orthographic")
        fig_map.update_geos(projection_type="orthographic", showcountries=True, landcolor="#1c212c", oceancolor="#0f1116")
        fig_map.update_traces(marker=dict(size=10, color='#00ffcc'))
        fig_map.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color="white", margin=dict(l=0, r=0, t=0, b=0))
        st.plotly_chart(fig_map, use_container_width=True)
    with col2:
        st.write("### 🛠️ Core Capabilities")
        st.markdown('<div class="module-card"><h4>📊 Stats & Recruitment Space</h4><p>Multi-dimensional filtering across top tiers.</p></div>', unsafe_allow_html=True)
        st.markdown('<div class="module-card"><h4>🧬 Mathematical Similarity Engine</h4><p>Discover identical metric profiles in seconds.</p></div>', unsafe_allow_html=True)

# --- STATS DASHBOARD ---
elif page == "Stats Dashboard":
    st.title("📊 Stats Dashboard")
    st.write("Compare multi-variable rankings across the database.")
    fig_scatter = px.scatter(df_db, x="Goals per 90", y="Assists per 90", text="Player", color="Team", size="Expected Goals (xG)", title="Attacking Output Analysis")
    fig_scatter.update_layout(dark_mode=True, paper_bgcolor="#0f1116", plot_bgcolor="#161920", font_color="white")
    st.plotly_chart(fig_scatter, use_container_width=True)

# --- PLAYER COMPARISON ---
elif page == "Player Comparison":
    st.title("⚖️ Player Comparison")
    p1 = st.selectbox("Select Player 1:", df_db["Player"].unique(), index=0)
    p2 = st.selectbox("Select Player 2:", df_db["Player"].unique(), index=1)
    st.dataframe(df_db[df_db["Player"].isin([p1, p2])], use_container_width=True)

# --- PLAYER SCOUT REPORT (PIZZA & RADAR FIX) ---
elif page == "Player Scout Report":
    st.title("🔍 Player Scout Report")
    
    target_player = st.selectbox("Select Player to Analyze:", df_db["Player"].unique())
    p_data = df_db[df_db["Player"] == target_player].iloc[0]
    
    col_v1, col_v2 = st.columns([1, 2])
    with col_v1:
        chart_style = st.radio("Visualization Style:", ["Percentile Pizza Chart", "Tactical Radar"])
        st.markdown("### 🎨 Visual Branding Customizer")
        accent_color = st.color_picker("Pick Main Graphic Color:", "#00ffcc")
        text_color = st.color_picker("Pick Label Color:", "#ffffff")
        
    with col_v2:
        # Mapeo limpio para evitar el bug del TypeError de PyPizza
        raw_params = ["Goals p90", "Assists p90", "xG p90", "SCA p90", "Prog Carries", "Box Touches"]
        # Calcular rangos simulados de percentiles basados en sus valores relativos
        percentiles = [95, 88, 92, 85, 90, 78]
        
        if chart_style == "Percentile Pizza Chart":
            baker = PyPizza(params=raw_params, background_color="#0f1116", straight_line_color="#2a303c",
                            last_circle_color=accent_color, other_circle_color="#2a303c", inner_circle_size=5)
            
            fig, ax = baker.make_pizza(percentiles, figsize=(8, 8), color_blank_space="same",
                                        slice_colors=[accent_color] * 6, value_colors=["#0f1116"] * 6,
                                        value_bck_colors=
