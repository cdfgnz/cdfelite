elif choice == "🔍 Player Scout Report":
    st.title("🔍 Player Scout Report")
    target = st.selectbox("Player:", sorted(df_db["Player"].unique()))
    p_data = df_db[df_db["Player"] == target].iloc[0]
    
    m_pizza = ['Goals p90', 'Assists p90', 'xG p90', 'SCA p90', 'Prog Carries', 'Box Touches']
    
    # CORREGIDO: Forzamos matemáticamente a que los valores estén estrictamente entre 0 y 100
    vals = []
    for m in m_pizza:
        val_ins = float(p_data[m])
        calculated = int(val_ins * 100) if val_ins <= 1 else int(val_ins * 10)
        # Asegura que ningún valor rompa la lógica del gráfico (máximo 100, mínimo 0)
        final_val = max(0, min(100, calculated))
        vals.append(final_val)
    
    baker = PyPizza(params=m_pizza, background_color="#161920", straight_line_color="#22252c", straight_line_lw=1, last_circle_lw=1, other_circle_lw=1, other_circle_color="#22252c")
    
    fig, ax = baker.make_pizza(
        values=vals, 
        figsize=(6, 6), 
        slice_colors=["#00ffcc"]*6, 
        value_colors=["#0f1116"]*6, 
        text_props=dict(color="white", fontsize=10, weight="bold")
    )
    fig.patch.set_facecolor('#0f1116')
    st.pyplot(fig)
