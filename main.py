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

    st.markdown("---")
    st.subheader("📂 Análisis colectivo - Habilidades Sociales")

    archivo = st.file_uploader("Carga un archivo .csv con respuestas de estudiantes (EHS)", type=["csv"], key="ehs")
    if archivo:
        df = pd.read_csv(archivo)
        dimensiones = [
            "Autoexpresión en situaciones sociales", "Defensa de los propios derechos",
            "Expresión de enfado o disconformidad", "Hacer peticiones",
            "Iniciar interacciones positivas con el sexo opuesto", "Interacción con personas de estatus elevado"
        ]

        st.write("📊 Boxplot de las dimensiones")
        fig = px.box(df, y=dimensiones, points="all", title="Distribución por dimensión")
        st.plotly_chart(fig)

        st.subheader("🔍 Visualización individual o por perfil")
        opciones_filtrado = st.radio("Selecciona el tipo de filtro:", ["Por nombre", "Por perfil similar"], key="ehs_filtro")

        if opciones_filtrado == "Por nombre":
            seleccion = st.selectbox("Selecciona un nombre:", df["Nombre"].unique(), key="ehs_nombre")
            alumno = df[df["Nombre"] == seleccion].iloc[0]
            plot_radar(dimensiones, [alumno[dim] for dim in dimensiones], f"Habilidades Sociales - {seleccion}")
    
        elif opciones_filtrado == "Por perfil similar":
            umbral = st.slider("Filtra por puntaje global mínimo:", 1.0, 5.0, 3.5, 0.1, key="ehs_umbral")
            df["Puntaje Global"] = df[dimensiones].mean(axis=1)
            filtrado = df[df["Puntaje Global"] >= umbral]

            st.write(f"{len(filtrado)} estudiantes con puntaje global ≥ {umbral}")
            for idx, row in filtrado.iterrows():
                st.markdown(f"**{row['Nombre']} ({row['Puntaje Global']:.2f}):**")
                plot_radar(dimensiones, [row[dim] for dim in dimensiones], row["Nombre"])



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


    st.markdown("---")
    st.subheader("📂 Análisis colectivo - PHQ-9")

    archivo = st.file_uploader("Carga un archivo .csv con respuestas de PHQ-9", type=["csv"], key="phq9")
    if archivo:
        df = pd.read_csv(archivo)
        preguntas = [
            "P1", "P2", "P3", "P4", "P5", "P6", "P7", "P8", "P9"
        ]
        df["Puntaje Total"] = df[preguntas].sum(axis=1)

        st.write("📊 Boxplot de respuestas por ítem")
        fig = px.box(df, y=preguntas, points="all", title="Distribución de respuestas (PHQ-9)")
        st.plotly_chart(fig)

        st.subheader("🔍 Visualización individual o por perfil")
        opciones_filtrado = st.radio("Selecciona el tipo de filtro:", ["Por nombre", "Por perfil similar"], key="phq9_filtro")

        if opciones_filtrado == "Por nombre":
            seleccion = st.selectbox("Selecciona un nombre:", df["Nombre"].unique(), key="phq9_nombre")
            alumno = df[df["Nombre"] == seleccion].iloc[0]
            plot_radar(preguntas, [alumno[p] for p in preguntas], f"PHQ-9 - {seleccion}")
    
        elif opciones_filtrado == "Por perfil similar":
            umbral = st.slider("Filtra por puntaje total mínimo:", 0, 27, 10, 1, key="phq9_umbral")
            filtrado = df[df["Puntaje Total"] >= umbral]
            st.write(f"{len(filtrado)} estudiantes con puntaje total ≥ {umbral}")

            for idx, row in filtrado.iterrows():
                st.markdown(f"**{row['Nombre']} ({row['Puntaje Total']}):**")
                plot_radar(preguntas, [row[p] for p in preguntas], row["Nombre"])


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

    st.markdown("---")
    st.subheader("📂 Análisis colectivo - Creatividad")

    archivo = st.file_uploader("Carga un archivo .csv con respuestas de creatividad", type=["csv"], key="creatividad")
    if archivo:
        df = pd.read_csv(archivo)
        dimensiones = [
            "Capacidad para resolver problemas", "Seguridad en sí mismo para resolver problemas",
            "Capacidad para desafiar normas", "Apertura a nuevas experiencias",
            "Tendencia a ajustarse a normas sociales y evitar riesgos creativos"
        ]
        df["Puntaje Global"] = df[dimensiones].mean(axis=1)

        st.write("📊 Boxplot de dimensiones")
        fig = px.box(df, y=dimensiones, points="all", title="Distribución de dimensiones creativas")
        st.plotly_chart(fig)

        st.subheader("🔍 Visualización individual o por perfil")
        opciones_filtrado = st.radio("Selecciona el tipo de filtro:", ["Por nombre", "Por perfil similar"], key="creatividad_filtro")

        if opciones_filtrado == "Por nombre":
            seleccion = st.selectbox("Selecciona un nombre:", df["Nombre"].unique(), key="creatividad_nombre")
            alumno = df[df["Nombre"] == seleccion].iloc[0]
            plot_radar(dimensiones, [alumno[dim] for dim in dimensiones], f"Perfil Creativo - {seleccion}")
    
        elif opciones_filtrado == "Por perfil similar":
            umbral = st.slider("Filtra por puntaje global mínimo:", 1.0, 5.0, 3.5, 0.1, key="creatividad_umbral")
            filtrado = df[df["Puntaje Global"] >= umbral]
            st.write(f"{len(filtrado)} estudiantes con puntaje global ≥ {umbral}")

            for idx, row in filtrado.iterrows():
                st.markdown(f"**{row['Nombre']} ({row['Puntaje Global']:.2f}):**")
                plot_radar(dimensiones, [row[dim] for dim in dimensiones], row["Nombre"])




# === LLAMADO A FUNCIONES ===
if menu == "Escala de Habilidades Sociales":
    escala_ehs(nombre)
elif menu == "PHQ-9 (Depresión)":
    escala_phq9(nombre)
elif menu == "Escala de Creatividad":
    escala_creatividad(nombre)
