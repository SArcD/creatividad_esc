import streamlit as st

st.title("Escala de Creatividad de Gough (1976)")

st.write("""
Selecciona los adjetivos que crees que te describen. 
Los adjetivos están agrupados en diferentes dimensiones relacionadas con la creatividad.
""")

# Diccionario de adjetivos por dimensión
categorias = {
    "Dimensión Cognitiva": ["Ingenioso", "Inventivo", "Original", "Reflexivo", "Intereses amplios"],
    "Dimensión Afectiva/Emocional": ["Seguro de sí mismo", "Egocéntrico", "Humorístico", "Atractivo/Sexy"],
    "Dimensión de No Convencionalidad": ["Individualista", "No convencional", "Informal", "Pretencioso"],
    "Dimensión de Restricción": ["Cauteloso", "Común", "Conservador", "Convencional", "Sumiso"]
}

# Adjetivos positivos y negativos de la escala original
adjetivos_positivos = [
    "Ingenioso", "Inventivo", "Original", "Reflexivo", "Intereses amplios",
    "Seguro de sí mismo", "Egocéntrico", "Humorístico", "Atractivo/Sexy",
    "Individualista", "No convencional", "Informal", "Pretencioso"
]

adjetivos_negativos = [
    "Cauteloso", "Común", "Conservador", "Convencional", "Sumiso"
]

# Registro de respuestas
seleccionados = []
resultados_por_categoria = {}

# Mostrar los checkbox por categoría
for categoria, adjetivos in categorias.items():
    st.subheader(categoria)
    seleccionados_cat = []
    for adj in adjetivos:
        if st.checkbox(adj, key=adj):
            seleccionados.append(adj)
            seleccionados_cat.append(adj)
    resultados_por_categoria[categoria] = seleccionados_cat

# Calcular puntaje
puntaje = sum([1 for a in seleccionados if a in adjetivos_positivos]) - \
          sum([1 for a in seleccionados if a in adjetivos_negativos])

# Mostrar resultados
st.markdown("---")
st.subheader("Resultado")
st.write(f"**Puntaje total de creatividad:** {puntaje} (mín: -12, máx: +18)")

# Interpretación básica
if puntaje >= 10:
    st.success("Alto perfil creativo")
elif puntaje >= 5:
    st.info("Perfil moderadamente creativo")
elif puntaje >= 0:
    st.warning("Perfil con rasgos creativos limitados")
else:
    st.error("Tendencia a evitar comportamientos creativos")

# Mostrar selección por categoría
st.markdown("---")
st.subheader("Tu perfil por dimensión")
for cat, adjs in resultados_por_categoria.items():
    st.write(f"**{cat}:** {', '.join(adjs) if adjs else 'Sin selección'}")
