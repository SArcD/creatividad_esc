import streamlit as st
import pandas as pd
import numpy as np
import datetime
import plotly.express as px
import matplotlib.pyplot as plt

st.set_page_config(page_title="Escalas Psicológicas Combinadas", layout="centered")

st.title("🧠 Escalas Combinadas: Habilidades Sociales, Síntomas Depresivos y Creatividad")

menu = st.sidebar.radio("Selecciona una escala:", [
    "Escala de Habilidades Sociales",
    "PHQ-9 (Depresión)",
    "Escala de Creatividad"])

nombre = st.text_input("Nombre o identificador del estudiante:")

# ================================
# FUNCIÓN GENERAL DE RADAR PLOT
# ================================
def plot_radar(labels, values, title):
    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    values += values[:1]
    angles += angles[:1]
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.fill(angles, values, alpha=0.25)
    ax.plot(angles, values, linewidth=2)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)
    ax.set_yticks([1, 2, 3, 4, 5])
    ax.set_yticklabels(['1', '2', '3', '4', '5'])
    ax.set_title(title, y=1.1)
    st.pyplot(fig)

# =====================================
# ESCALA DE HABILIDADES SOCIALES (GISMERO)
# =====================================
def escala_ehs(nombre):
    st.subheader("Escala de Habilidades Sociales - Gismero (2010)")
    dimensiones = {
        "Autoexpresión en situaciones sociales": [
            "Me resulta difícil comenzar una conversación con personas desconocidas.",
            "Evito hablar en público siempre que puedo.",
            "Siento ansiedad cuando tengo que hacer una llamada importante."
        ],
        "Defensa de los propios derechos": [
            "Me cuesta decir que no cuando alguien me pide un favor.",
            "A menudo cedo incluso cuando no estoy de acuerdo.",
            "Evito conflictos aunque no esté conforme."
        ],
        "Expresión de enfado o disconformidad": [
            "Reprimo mi enfado para evitar problemas.",
            "Prefiero callar antes que discutir.",
            "Me cuesta expresar molestia cuando algo no me gusta."
        ],
        "Hacer peticiones": [
            "Me cuesta pedir ayuda cuando la necesito.",
            "Evito pedir favores por miedo a molestar.",
            "Prefiero arreglármelas solo antes que pedir algo."
        ],
        "Iniciar interacciones positivas con el sexo opuesto": [
            "Me resulta difícil iniciar conversaciones con personas que me atraen.",
            "Evito el contacto visual con personas que me interesan.",
            "Me pongo nervioso/a al hablar con alguien que me gusta."
        ],
        "Interacción con personas de estatus elevado": [
            "Me intimidan las figuras de autoridad.",
            "Me pongo nervioso/a ante personas importantes.",
            "Me cuesta expresar mis ideas frente a personas influyentes."
        ]
    }
    respuestas = {}
    dim_scores = {}
    contador = 1
    for dim, preguntas in dimensiones.items():
        st.subheader(dim)
        suma = 0
        for preg in preguntas:
            resp = st.radio(f"{contador}. {preg}", options=[1, 2, 3, 4, 5], index=2, key=f"ehs_{contador}")
            respuestas[contador] = resp
            suma += resp
            contador += 1
        dim_scores[dim] = suma / len(preguntas)

    st.markdown("---")
    st.subheader("📊 Resultados por dimensión")
    for k, v in dim_scores.items():
        st.write(f"**{k}:** {v:.2f}")
    plot_radar(list(dim_scores.keys()), list(dim_scores.values()), f"Radar de Habilidades Sociales - {nombre}")

# =====================================
# ESCALA PHQ-9 (DEPRESIÓN)
# =====================================
def escala_phq9(nombre):
    st.subheader("PHQ-9 - Evaluación de Síntomas Depresivos")
    preguntas = [
        "Poco interés o placer en hacer cosas",
        "Sentirse decaído, deprimido o sin esperanzas",
        "Dificultad para dormir o dormir en exceso",
        "Sentirse cansado o con poca energía",
        "Falta de apetito o comer en exceso",
        "Sentirse mal consigo mismo o que es un fracaso",
        "Dificultad para concentrarse",
        "Moverse o hablar muy lento o estar inquieto",
        "Pensamientos de que estaría mejor muerto"
    ]
    respuestas = []
    for i, pregunta in enumerate(preguntas):
        resp = st.radio(f"{i+1}. {pregunta}", [0, 1, 2, 3], index=0, key=f"phq9_{i}")
        respuestas.append(resp)

    total = sum(respuestas)
    st.subheader("🔍 Interpretación del puntaje total")
    st.write(f"**Puntaje total:** {total}")
    if total <= 4:
        st.success("Mínima o sin depresión")
    elif total <= 9:
        st.info("Leve")
    elif total <= 14:
        st.info("Moderada")
    elif total <= 19:
        st.warning("Moderadamente severa")
    else:
        st.error("Severa")

# =====================================
# ESCALA DE CREATIVIDAD DE GOUGH
# =====================================
def escala_creatividad(nombre):
    st.subheader("Escala de Creatividad - Gough (adaptada)")
    dimensiones = {
        "Capacidad para resolver problemas": [
            "Soy capaz de encontrar soluciones cuando enfrento dificultades.",
            "Disfruto analizar situaciones para entender cómo resolverlas.",
            "Busco diferentes enfoques antes de tomar una decisión.",
            "Puedo adaptarme cuando las cosas no salen como esperaba.",
            "Me esfuerzo por mejorar continuamente mis métodos de trabajo."
        ],
        "Seguridad en sí mismo para resolver problemas": [
            "Confío en mi capacidad para superar retos complejos.",
            "Creo en mis habilidades para tomar buenas decisiones.",
            "Me mantengo firme incluso cuando otros dudan de mí.",
            "No me intimidan los problemas difíciles.",
            "Me siento seguro al proponer ideas nuevas."
        ],
        "Capacidad para desafiar normas": [
            "Estoy dispuesto a cuestionar reglas establecidas.",
            "No tengo miedo de expresar opiniones impopulares.",
            "Me atrevo a proponer cambios aunque sean disruptivos.",
            "Creo que romper esquemas puede ser positivo.",
            "A veces rompo las reglas si creo que es lo correcto."
        ],
        "Apertura a nuevas experiencias": [
            "Me interesa conocer culturas y formas de vida diferentes.",
            "Disfruto aprender cosas nuevas cada día.",
            "Estoy dispuesto a probar actividades desconocidas.",
            "Me atrae explorar lo inesperado.",
            "Me adapto fácilmente a cambios."
        ],
        "Tendencia a ajustarse a normas sociales y evitar riesgos creativos": [
            "Prefiero seguir lo que dicta la mayoría.",
            "Evito tomar decisiones que puedan parecer arriesgadas.",
            "Me siento más cómodo repitiendo lo que ya ha funcionado.",
            "Dudo en proponer ideas que no han sido probadas.",
            "Prefiero mantenerme dentro de lo convencional."
        ]
    }
    respuestas = {}
    dim_scores = {}
    contador = 1
    for dim, preguntas in dimensiones.items():
        st.subheader(dim)
        suma = 0
        for preg in preguntas:
            resp = st.radio(f"{contador}. {preg}", options=[1, 2, 3, 4, 5], index=2, key=f"crea_{contador}")
            respuestas[contador] = resp
            suma += resp
            contador += 1
        dim_scores[dim] = suma / len(preguntas)

    puntaje_total = np.mean(list(respuestas.values()))
    st.subheader("🔍 Resultado general")
    st.write(f"**Puntaje promedio global:** {puntaje_total:.2f}")
    if puntaje_total >= 4.0:
        st.success("Alto perfil creativo")
    elif puntaje_total >= 3.0:
        st.info("Perfil moderadamente creativo")
    elif puntaje_total >= 2.0:
        st.warning("Perfil con rasgos creativos limitados")
    else:
        st.error("Tendencia a evitar comportamientos creativos")

    st.subheader("📊 Perfil por dimensión")
    for k, v in dim_scores.items():
        st.write(f"**{k}:** {v:.2f}")
    plot_radar(list(dim_scores.keys()), list(dim_scores.values()), f"Radar Creatividad - {nombre}")



# ==========================
# ANÁLISIS COLECTIVO POR ESCALA
# ==========================
st.markdown("---")
st.subheader("📁 Análisis colectivo por escala")
opcion = st.radio("Selecciona escala para cargar respuestas en CSV:", [
    "Escala de Habilidades Sociales",
    "PHQ-9",
    "Escala de Creatividad"
], horizontal=True)

archivo = st.file_uploader("Carga un archivo CSV con respuestas", type=["csv"])

if archivo:
    df = pd.read_csv(archivo)
    dimensiones = []

    if opcion == "Escala de Habilidades Sociales":
        dimensiones = [
            "Autoexpresión en situaciones sociales",
            "Defensa de los propios derechos",
            "Expresión de enfado o disconformidad",
            "Hacer peticiones",
            "Iniciar interacciones positivas con el sexo opuesto",
            "Interacción con personas de estatus elevado"
        ]
    elif opcion == "PHQ-9":
        dimensiones = ["PHQ-9 Total"]
        df["PHQ-9 Total"] = df[[f"i{i}" for i in range(1, 10)]].sum(axis=1)
    elif opcion == "Escala de Creatividad":
        dimensiones = [
            "Capacidad para resolver problemas",
            "Seguridad en sí mismo para resolver problemas",
            "Capacidad para desafiar normas",
            "Apertura a nuevas experiencias",
            "Tendencia a ajustarse a normas sociales y evitar riesgos creativos"
        ]

    st.subheader("📊 Boxplot colectivo")
    df_melt = df.melt(id_vars=["Nombre"], value_vars=dimensiones, var_name="Dimensión", value_name="Puntaje")
    fig = px.box(df_melt, x="Dimensión", y="Puntaje", points="all", color="Dimensión", hover_name="Nombre")
    st.plotly_chart(fig, use_container_width=True)

    # RADARES
    st.markdown("---")
    st.subheader("🔍 Visualización individual o por perfil")

    opciones_filtrado = st.radio("Selecciona el tipo de filtro:", ["Por nombre", "Por perfil similar"])

    if opciones_filtrado == "Por nombre":
        seleccion = st.selectbox("Selecciona un nombre:", df["Nombre"].unique())
        alumno = df[df["Nombre"] == seleccion].iloc[0]

        st.write(f"### Perfil de {seleccion}")
        labels = dimensiones
        values = [alumno[dim] for dim in dimensiones]
        angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
        values += values[:1]
        angles += angles[:1]

        fig2, ax2 = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
        ax2.fill(angles, values, color='lightcoral', alpha=0.4)
        ax2.plot(angles, values, color='red', linewidth=2)
        ax2.set_yticks([1, 2, 3, 4, 5])
        ax2.set_yticklabels(['1', '2', '3', '4', '5'])
        ax2.set_xticks(angles[:-1])
        ax2.set_xticklabels(labels)
        ax2.set_title(f"Radar de {seleccion}", y=1.1)
        st.pyplot(fig2)

    elif opciones_filtrado == "Por perfil similar":
        if opcion == "PHQ-9":
            umbral = st.slider("Filtra por PHQ-9 Total mínimo:", 0, 27, 10, 1)
            filtrado = df[df["PHQ-9 Total"] >= umbral]
        else:
            df["Puntaje Global"] = df[dimensiones].mean(axis=1)
            umbral = st.slider("Filtra por puntaje global mínimo:", 1.0, 5.0, 3.5, 0.1)
            filtrado = df[df["Puntaje Global"] >= umbral]

        st.write(f"{len(filtrado)} alumn@s con puntaje ≥ {umbral}")

        for idx, row in filtrado.iterrows():
            st.markdown(f"**{row['Nombre']} ({row[dimensiones].mean():.2f}):**")
            values = [row[dim] for dim in dimensiones]
            angles = np.linspace(0, 2 * np.pi, len(dimensiones), endpoint=False).tolist()
            values += values[:1]
            angles += angles[:1]
            fig3, ax3 = plt.subplots(figsize=(5, 5), subplot_kw=dict(polar=True))
            ax3.fill(angles, values, color='skyblue', alpha=0.3)
            ax3.plot(angles, values, color='blue')
            ax3.set_xticks(angles[:-1])
            ax3.set_xticklabels(dimensiones)
            ax3.set_yticks([1, 2, 3, 4, 5])
            ax3.set_yticklabels(['1', '2', '3', '4', '5'])
            ax3.set_title(row['Nombre'])
            st.pyplot(fig3)

