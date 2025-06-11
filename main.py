import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime

st.set_page_config(page_title="Escala de Creatividad de Gough", layout="centered")

st.title("🧠 Escala de Creatividad de Gough (1976) - Adaptada")

nombre = st.text_input("Escribe tu nombre o iniciales (opcional):")

st.write("Selecciona los adjetivos que consideres que te describen:")

# Diccionario de categorías y adjetivos adaptados a nuevas dimensiones
categorias = {
    "Capacidad para resolver problemas": ["Ingenioso", "Inventivo", "Original", "Reflexivo", "Intereses amplios"],
    "Seguridad en sí mismo para resolver problemas": ["Seguro de sí mismo", "Egocéntrico", "Atractivo/Sexy", "Humorístico"],
    "Capacidad para desafiar normas": ["Individualista", "No convencional", "Informal", "Pretencioso"],
    "Apertura a nuevas experiencias": ["Curioso", "Explorador", "Espontáneo"],
    "Tendencia a ajustarse a normas sociales y evitar riesgos creativos": ["Cauteloso", "Común", "Conservador", "Convencional", "Sumiso"]
}

# Definir adjetivos positivos y negativos
adjetivos_positivos = [
    "Ingenioso", "Inventivo", "Original", "Reflexivo", "Intereses amplios",
    "Seguro de sí mismo", "Egocéntrico", "Atractivo/Sexy", "Humorístico",
    "Individualista", "No convencional", "Informal", "Pretencioso",
    "Curioso", "Explorador", "Espontáneo"
]
adjetivos_negativos = ["Cauteloso", "Común", "Conservador", "Convencional", "Sumiso"]

seleccionados = []
resultados_dim = {}

# Mostrar adjetivos por dimensión
for categoria, adjetivos in categorias.items():
    st.subheader(categoria)
    seleccionados_cat = []
    for adj in adjetivos:
        if st.checkbox(adj, key=adj):
            seleccionados.append(adj)
            seleccionados_cat.append(adj)
    resultados_dim[categoria] = seleccionados_cat

# Calcular puntaje global
puntaje = sum([1 for a in seleccionados if a in adjetivos_positivos]) - \
          sum([1 for a in seleccionados if a in adjetivos_negativos])

st.markdown("---")
st.subheader("🔍 Resultado general")
st.write(f"**Puntaje total de creatividad:** {puntaje} (mín: -5, máx: +17)")

# Interpretación general
if puntaje >= 12:
    interpretacion = "Alto perfil creativo"
    st.success(interpretacion)
elif puntaje >= 6:
    interpretacion = "Perfil moderadamente creativo"
    st.info(interpretacion)
elif puntaje >= 0:
    interpretacion = "Perfil con rasgos creativos limitados"
    st.warning(interpretacion)
else:
    interpretacion = "Tendencia a evitar comportamientos creativos"
    st.error(interpretacion)

# Mostrar selección por dimensión y puntajes
st.subheader("📊 Perfil por dimensión")
dim_scores = {}
for cat, adjs in resultados_dim.items():
    st.write(f"**{cat}:** {', '.join(adjs) if adjs else 'Sin selección'}")
    dim_scores[cat] = len(adjs)

# Consejos personalizados
st.markdown("### 💡 Sugerencias personalizadas")
if dim_scores["Capacidad para resolver problemas"] >= 4:
    st.write("- Tienes un pensamiento resolutivo. Usa retos o acertijos para mantener tu mente activa.")
if dim_scores["Capacidad para desafiar normas"] >= 3:
    st.write("- Tiendes a cuestionar estructuras. Usa eso para proponer ideas disruptivas en tu entorno.")
if dim_scores["Tendencia a ajustarse a normas sociales y evitar riesgos creativos"] >= 3:
    st.write("- Podrías estar evitando riesgos. Intenta un proyecto sin buscar aprobación externa.")
if dim_scores["Seguridad en sí mismo para resolver problemas"] >= 3:
    st.write("- Tu autoconfianza puede potenciar tus decisiones creativas. Lidera desde tu autenticidad.")
if dim_scores["Apertura a nuevas experiencias"] >= 2:
    st.write("- Eres receptivo a lo nuevo. Prueba actividades artísticas o improvisación para nutrir tu creatividad.")

# Gráfica radar
st.subheader("📈 Visualización de tu perfil")
labels = list(dim_scores.keys())
values = list(dim_scores.values())
angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
values += values[:1]
angles += angles[:1]

fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
ax.fill(angles, values, color='skyblue', alpha=0.4)
ax.plot(angles, values, color='blue', linewidth=2)
ax.set_yticklabels([])
ax.set_xticks(angles[:-1])
ax.set_xticklabels(labels)
ax.set_title("Radar de Dimensiones Creativas", y=1.1)
st.pyplot(fig)

# Guardar resultados
if st.button("💾 Guardar mis respuestas"):
    df = pd.DataFrame([{
        "Nombre": nombre if nombre else "Anónimo",
        "Fecha": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        "Puntaje Total": puntaje,
        "Interpretación": interpretacion,
        **dim_scores
    }])
    df.to_csv("resultados_creatividad.csv", mode='a', header=False, index=False)
    st.success("Resultados guardados correctamente.")
