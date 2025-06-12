import streamlit as st
import pandas as pd
import numpy as np
import datetime
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Escalas Psicológicas Combinadas", layout="centered")

st.title("🧠 Escalas Combinadas: Habilidades Sociales, Síntomas Depresivos y Creatividad")

menu = st.sidebar.radio("Selecciona una escala:", ["Escala de Habilidades Sociales", "PHQ-9 (Depresión)", "Escala de Creatividad"])

nombre = st.text_input("Nombre o identificador del estudiante:")

# -----------------------------
# ESCALA DE HABILIDADES SOCIALES (EHS)
# -----------------------------
if menu == "Escala de Habilidades Sociales":
    st.subheader("🗣️ Escala de Habilidades Sociales (EHS) - Gismero 2010")

    st.write("Responde a cada afirmación según el grado con el que te identifiques. Usa la siguiente escala:")
    st.markdown("""
    1 = Nunca<br>
    2 = Casi nunca<br>
    3 = A veces<br>
    4 = Casi siempre<br>
    5 = Siempre
    """, unsafe_allow_html=True)

    items_ehs = [
        ("Autoexpresión en situaciones sociales", "Me resulta difícil hablar con personas que no conozco mucho."),
        ("Autoexpresión en situaciones sociales", "Suelo ser espontáneo cuando estoy en grupo."),
        ("Defensa de los propios derechos", "Defiendo mis derechos sin sentirme culpable."),
        ("Expresión de ira o disconformidad", "Expreso mi desacuerdo aunque se enoje la otra persona."),
        ("Paralización ante situaciones nuevas", "Me paralizo cuando tengo que hablar en público."),
        ("Hacer peticiones", "Me cuesta pedir ayuda aunque la necesite."),
        ("Iniciar interacciones positivas con el sexo opuesto", "Iniciar una conversación con alguien que me gusta me pone muy nervioso."),
        ("Autoexpresión en situaciones sociales", "Suelo mantener el contacto visual cuando hablo."),
        ("Defensa de los propios derechos", "Reclamo cuando algo no me parece justo."),
        ("Hacer peticiones", "Pido favores sin sentirme incómodo."),
        ("Paralización ante situaciones nuevas", "Me cuesta desenvolverme en entrevistas u orales."),
        ("Iniciar interacciones positivas con el sexo opuesto", "No tengo problema en iniciar conversaciones amistosas con personas que me atraen.")
    ]

    opciones_likert_ehs = {"Nunca": 1, "Casi nunca": 2, "A veces": 3, "Casi siempre": 4, "Siempre": 5}
    respuestas_ehs = {}
    resultados_dim_ehs = {}

    for idx, (dim, texto) in enumerate(items_ehs):
        opcion = st.radio(f"{idx+1}. {texto}", options=list(opciones_likert_ehs.keys()), index=2, key=f"ehs_{idx+1}")
        valor = opciones_likert_ehs[opcion]
        if dim not in respuestas_ehs:
            respuestas_ehs[dim] = []
        respuestas_ehs[dim].append(valor)

    for dim, vals in respuestas_ehs.items():
        resultados_dim_ehs[dim] = round(np.mean(vals), 2)

    puntaje_global_ehs = round(np.mean(list(resultados_dim_ehs.values())), 2)

    st.subheader("📊 Resultado del perfil social")
    st.write(f"**Puntaje global EHS:** {puntaje_global_ehs} (escala 1-5)")
    for dim, score in resultados_dim_ehs.items():
        st.write(f"**{dim}:** {score}")

    # Radar
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(r=list(resultados_dim_ehs.values()),
                                  theta=list(resultados_dim_ehs.keys()),
                                  fill='toself', name=nombre if nombre else "Perfil EHS"))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[1, 5])),
                      showlegend=False,
                      title="Perfil Radar EHS")
    st.plotly_chart(fig)

    # Subir CSV y mostrar boxplots
    st.markdown("---")
    st.subheader("📂 Análisis grupal desde archivo CSV")
    archivo = st.file_uploader("Carga un archivo CSV con resultados EHS", type="csv")
    if archivo:
        df = pd.read_csv(archivo)
        cols_ehs = list(resultados_dim_ehs.keys())
        fig = px.box(df, y=cols_ehs, points="all", title="Distribución de dimensiones EHS")
        st.plotly_chart(fig)

# -----------------------------
# ESCALA PHQ-9
# -----------------------------
elif menu == "PHQ-9 (Depresión)":
    st.subheader("😟 Evaluación de síntomas depresivos (PHQ-9)")

    items_phq9 = [
        "Poco interés o placer en hacer cosas",
        "Sentirse decaído, deprimido o sin esperanzas",
        "Dificultad para dormir o dormir en exceso",
        "Sentirse cansado o con poca energía",
        "Falta de apetito o comer en exceso",
        "Sentirse mal consigo mismo o que es un fracaso o que ha fallado a su familia",
        "Dificultad para concentrarse en cosas, como leer el periódico o ver televisión",
        "Moverse o hablar tan despacio que otras personas lo podrían haber notado. O lo contrario: estar tan inquieto o agitado que se mueve mucho más de lo habitual",
        "Pensamientos de que estaría mejor muerto o de hacerse daño de alguna manera"
    ]

    opciones_phq = {
        "En ningún momento": 0,
        "Varios días": 1,
        "Más de la mitad de los días": 2,
        "Casi todos los días": 3
    }

    puntaje_phq = 0
    for i, pregunta in enumerate(items_phq9):
        opcion = st.radio(f"PHQ {i+1}. {pregunta}", options=list(opciones_phq.keys()), index=0, key=f"phq_{i+1}")
        puntaje_phq += opciones_phq[opcion]

    st.subheader("🧠 Resultado de la evaluación depresiva")
    st.write(f"**Puntaje total PHQ-9:** {puntaje_phq} (máx: 27)")

    if puntaje_phq <= 4:
        st.success("Depresión mínima o sin síntomas clínicos.")
    elif puntaje_phq <= 9:
        st.info("Síntomas leves de depresión.")
    elif puntaje_phq <= 14:
        st.warning("Depresión moderada.")
    elif puntaje_phq <= 19:
        st.warning("Depresión moderadamente severa.")
    else:
        st.error("Depresión severa.")

# -----------------------------
# ESCALA DE CREATIVIDAD DE GOUGH
# -----------------------------
elif menu == "Escala de Creatividad":
    st.subheader("🎨 Escala de Creatividad de Gough - Adaptada")

    preguntas_por_dimension = {
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

    respuestas_creatividad = {}
    dim_scores = {}
    contador = 1
    for dimension, preguntas in preguntas_por_dimension.items():
        st.subheader(dimension)
        score_total = 0
        for pregunta in preguntas:
            respuesta = st.radio(
                f"Creatividad {contador}. {pregunta}",
                options=[1, 2, 3, 4, 5],
                index=2,
                key=f"creatividad_{contador}"
            )
            respuestas_creatividad[contador] = respuesta
            score_total += respuesta
            contador += 1
        dim_scores[dimension] = score_total / len(preguntas)

    puntaje_total_creatividad = np.mean(list(respuestas_creatividad.values()))

    st.subheader("🧪 Resultado general de creatividad")
    st.write(f"**Puntaje promedio global de creatividad:** {puntaje_total_creatividad:.2f} (escala 1 a 5)")

    if puntaje_total_creatividad >= 4.0:
        st.success("Alto perfil creativo")
    elif puntaje_total_creatividad >= 3.0:
        st.info("Perfil moderadamente creativo")
    elif puntaje_total_creatividad >= 2.0:
        st.warning("Perfil con rasgos creativos limitados")
    else:
        st.error("Tendencia a evitar comportamientos creativos")

    # Radar
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(r=list(dim_scores.values()),
                                  theta=list(dim_scores.keys()),
                                  fill='toself', name=nombre if nombre else "Perfil Creatividad"))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[1, 5])),
                      showlegend=False,
                      title="Perfil Radar Creatividad")
    st.plotly_chart(fig)

    # Subir CSV y mostrar boxplot
    st.markdown("---")
    st.subheader("📂 Análisis grupal desde archivo CSV")
    archivo = st.file_uploader("Carga un archivo CSV con resultados de creatividad", type="csv")
    if archivo:
        df = pd.read_csv(archivo)
        cols = list(dim_scores.keys())
        fig = px.box(df, y=cols, points="all", title="Distribución de dimensiones creativas")
        st.plotly_chart(fig)
