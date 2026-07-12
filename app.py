import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
from mplsoccer import Radar, PyPizza

# 1. CONFIGURACIÓN DE LA PÁGINA Y LOOK PREMIUM
st.set_page_config(page_title="cdfelite | Advanced Football Analytics", page_icon="⚽", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0f1116; color: #ffffff; }
    .sidebar .sidebar-content { background-color: #161920; }
    h1, h2, h3 { color: #00ffcc !important; font-family: 'Inter', sans-serif; }
    </style>
    """, unsafe_allow_html=True)

# 2. NAVEGACIÓN LATERAL
st.sidebar.title("📊 cdfelite Navigation")
page = st.sidebar.radio("Go to:", ["Home", "Player Scout Report (Pizza & Radar)", "3D Data Dashboard"])

st.sidebar.markdown("---")
st.sidebar.caption("📅 Data Source: Live FBref Data")
st.sidebar.caption("🚀 Developed by @cdfgnz")

# 3. MÓDULO: HOME (PÁGINA DE BIENVENIDA)
if page == "Home":
    col1, col2 = st.columns([1, 2])
    with col1:
        st.write("### 🌐 Global Coverage")
        map_data = pd.DataFrame({
            'lat': [40.4167, 51.5074, 48.8566, 52.5200, -34.6037],
            'lon': [-3.7037, -0.1278, 2.3522, 13.4050, -58.3816],
            'League': ['La Liga', 'Premier League', 'Ligue 1', 'Bundesliga', 'Liga Profesional']
        })
        fig_map = px.scatter_geo(map_data, lat='lat', lon='lon', hover_name='League', projection="orthographic")
        fig_map.update_geos(projection_type="orthographic", showcountries=True, landcolor="#1e222b", oceancolor="#0f1116")
        fig_map.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color="white", margin=dict(l=0, r=0, t=0, b=0))
        st.plotly_chart(fig_map, use_container_width=True)

    with col2:
        st.title("⚽ Welcome to cdfelite")
        st.markdown("#### *Unlock the Power of Football Analytics – Dive into the Numbers Behind the Game!*")
        st.write("cdfelite transforms raw FBref event data into high-fidelity visual intelligence. "
                 "Skip complex spreadsheets and generate elite data visualisations instantly.")

# 4. MÓDULO: PLAYER SCOUT REPORT
elif page == "Player Scout Report (Pizza & Radar)":
    st.title("🔍 Advanced Percentile Reports")
    
    player_input = st.text_input("Search Player (Connected to FBref Pipeline):", "Vinicius Jr")
    chart_style = st.radio("Select Chart Visual Style:", ["Percentile Pizza Chart", "Tactical Radar Chart"])
    
    # Simulación de la respuesta automatizada de FBref
    params = ["Non-Penalty Goals", "Shots Total", "Assists", "Shot-Creating Actions", "Touches (Box)", "Progressive Carries"]
    percentiles = [97, 94, 82, 89, 91, 96] 
    
    if player_input:
        st.markdown("---")
        
        if chart_style == "Percentile Pizza Chart":
            baker = PyPizza(params=params, background_color="#0f1116", straight_line_color="#2a303c",
                            last_circle_color="#00ffcc", other_circle_color="#2a303c")
            fig, ax = baker.make_pizza(percentiles, figsize=(8, 8), color_blank_space="same",
                                        slice_colors=["#00ffcc"] * 6, value_colors=["#0f1116"] * 6,
                                        value_bck_colors=["#00ffcc"] * 6, text_props=dict(color="white", fontsize=10, weight="bold"))
            
            # 🔥 MARCAS DE AGUA INTEGRADAS PARA TWITTER 🔥
            fig.text(0.5, 0.95, f"{player_input} - Performance Profile", ha="center", color="white", fontsize=20, weight="bold")
            fig.text(0.5, 0.91, "Data Source: FBref / Opta | cdfelite engine", ha="center", color="#8892b0", fontsize=11, style="italic")
            fig.text(0.88, 0.94, "cdfelite", color="#00ffcc", fontsize=15, weight="bold", ha="right")
            fig.text(0.88, 0.05, "Created by: @cdfgnz", color="#8892b0", fontsize=11, weight="bold", ha="right")
            st.pyplot(fig)
            
        else:
            radar = Radar(params, [0]*6, [100]*6, num_rings=4, ring_width=1, center_circle=True)
            fig, ax = radar.setup_axis()
            fig.patch.set_facecolor('#0f1116')
            ax.set_facecolor('#0f1116')
            radar.draw_circles(ax=ax, facecolor='#161920', edgecolor='#2a303c')
            radar.draw_radar(percentiles, ax=ax, kwargs_radar={'facecolor': '#00ffcc', 'alpha': 0.6})
            radar.draw_range_labels(ax=ax, color='#ffffff', fontsize=10)
            radar.draw_param_labels(ax=ax, color='#ffffff', fontsize=11, weight='bold')
            
            # 🔥 MARCAS DE AGUA INTEGRADAS PARA TWITTER 🔥
            ax.text(0.5, 1.15, f"{player_input} - Tactical Analysis", transform=ax.transAxes, color='white', fontsize=18, ha='center', weight='bold')
            ax.text(0.98, 1.14, "cdfelite", transform=ax.transAxes, color='#00ffcc', fontsize=14, ha='right', weight='bold')
            ax.text(0.98, -0.05, "Analysis by: @cdfgnz", transform=ax.transAxes, color='#8892b0', fontsize=11, ha='right', weight='bold')
            st.pyplot(fig)
            
        st.success("📸 Graphic ready! Right-click, save the image, and post directly to Twitter.")

# 5. MÓDULO: 3D DATA DASHBOARD
elif page == "3D Data Dashboard":
    st.title("📊 Multi-Dimensional Analytics")
    mock_db = pd.DataFrame({
        'Player': [f'Scouted Player {i}' for i in range(1, 31)],
        'Goals per 90': np.random.uniform(0.1, 0.8, 30),
        'Assists per 90': np.random.uniform(0.05, 0.5, 30),
        'Expected Goals (xG)': np.random.uniform(0.1, 0.7, 30),
        'Position': np.random.choice(['FW', 'MF'], 30)
    })
    fig_3d = px.scatter_3d(mock_db, x='Goals per 90', y='Assists per 90', z='Expected Goals (xG)', color='Position', hover_name='Player', color_discrete_sequence=['#00ffcc', '#ff007f'])
    fig_3d.update_layout(scene=dict(xaxis=dict(backgroundcolor="#161920", textcolor="white"), yaxis=dict(backgroundcolor="#161920", textcolor="white"), zaxis=dict(backgroundcolor="#161920", textcolor="white")), paper_bgcolor='#0f1116', font_color="white")
    st.plotly_chart(fig_3d, use_container_width=True)