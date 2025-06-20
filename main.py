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
    st.info(
        "🔎 **Instrucciones:** Responde según tu nivel de acuerdo con cada afirmación.\n"
        "- 1 = Muy en desacuerdo\n"
        "- 2 = En desacuerdo\n"
        "- 3 = Ni de acuerdo ni en desacuerdo\n"
        "- 4 = De acuerdo\n"
        "- 5 = Muy de acuerdo\n\n"
        "📌 **Interpretación general:**\n"
        "Puntajes más altos indican mayor competencia en habilidades sociales dentro de esa dimensión específica."
    )
    
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
#    for dim, preguntas in dimensiones.items():
#        st.subheader(dim)
#        suma = 0
#        for preg in preguntas:
#            resp = st.radio(f"{contador}. {preg}", options=[1, 2, 3, 4, 5], index=2, key=f"ehs_{contador}")
#            respuestas[contador] = resp
#            suma += resp
#            contador += 1
#        dim_scores[dim] = suma / len(preguntas)

    for dim, preguntas in dimensiones.items():
        st.subheader(dim)
        suma = 0
        for preg in preguntas:
            resp = st.radio(f"{contador}. {preg}", options=[1, 2, 3, 4, 5], index=2, key=f"ehs_{contador}")
            respuestas[contador] = resp
            resp_invertido = 6 - resp  # Invertir la escala para que 5 = alta habilidad social
            suma += resp_invertido
            contador += 1
        dim_scores[dim] = suma / len(preguntas)


    
    st.markdown("---")
    st.subheader("📈 Resultados")

    # Mostrar puntajes y diagnóstico por dimensión
    for dim, score in dim_scores.items():
        st.write(f"**{dim}:** {score:.2f}")
        if score >= 4.0:
            st.success(f"Competencia alta en {dim.lower()}.")
        elif score >= 3.0:
            st.info(f"Competencia adecuada en {dim.lower()}.")
        elif score >= 2.0:
            st.warning(f"Dificultades moderadas en {dim.lower()}.")
        else:
            st.error(f"Dificultades significativas en {dim.lower()}.")

    
    # Mostrar puntajes por dimensión
    #for dim, score in dim_scores.items():
    #    st.write(f"**{dim}:** {score:.2f}")

    # Calcular puntaje global (promedio de los promedios)
    puntaje_global = sum(dim_scores.values()) / len(dim_scores)
    st.write(f"\n**Puntaje Global:** {puntaje_global:.2f}")

    # Diagnóstico simple basado en el puntaje global
    st.markdown("### 🧠 Diagnóstico General")
    if puntaje_global >= 4.0:
        st.success("Excelente nivel de habilidades sociales. Se observa gran confianza y capacidad para interactuar en diversos contextos.")
    elif puntaje_global >= 3.0:
        st.info("Nivel adecuado de habilidades sociales. Hay buenas competencias, aunque pueden mejorarse algunos aspectos específicos.")
    elif puntaje_global >= 2.0:
        st.warning("Habilidades sociales limitadas. Se recomienda trabajar en la expresión y defensa de tus ideas en entornos sociales.")
    else:
        st.error("Dificultades significativas en habilidades sociales. Podría ser útil explorar estrategias para mejorar la comunicación interpersonal.")

    # Gráfico tipo radar
    plot_radar(list(dim_scores.keys()), list(dim_scores.values()), "Perfil de Habilidades Sociales")

    
    # --- BLOQUE DE ANÁLISIS COLECTIVO PARA EHS ---
    st.markdown("---")
    st.subheader("📂 Análisis colectivo - Habilidades Sociales")

    archivo = st.file_uploader("Carga un archivo .csv con respuestas de estudiantes (EHS)", type=["csv"], key="ehs")
    if archivo:
        df = pd.read_csv(archivo)

        # Mapear preguntas a dimensiones con nombres amigables
        mapa_dimensiones = {
            "Autoexpresión en situaciones sociales": ["Q1", "Q2", "Q3"],
            "Defensa de los propios derechos": ["Q4", "Q5", "Q6"],
            "Expresión de enfado o disconformidad": ["Q7", "Q8", "Q9"],
            "Hacer peticiones": ["Q10", "Q11", "Q12"],
            "Iniciar interacciones positivas con el sexo opuesto": ["Q13", "Q14", "Q15"],
            "Interacción con personas de estatus elevado": ["Q16", "Q17", "Q18"]
        }

        dimensiones = list(mapa_dimensiones.keys())

        # Calcular promedios por dimensión
        for nombre, preguntas in mapa_dimensiones.items():
            df[nombre] = df[preguntas].mean(axis=1)

        # Boxplot con nombres amigables
        st.write("📊 Boxplot de las dimensiones")
        df_melted = df.melt(id_vars=["Nombre"], value_vars=dimensiones, var_name="Dimensión", value_name="Puntaje")
        fig = px.box(df_melted, x="Dimensión", y="Puntaje", points="all", hover_data=["Nombre"],
                 title="Distribución por dimensión (EHS)")
        st.plotly_chart(fig)

        st.subheader("🔍 Visualización individual o por perfil")
        opciones_filtrado = st.radio("Selecciona el tipo de filtro:", ["Por nombre", "Por perfil similar"], key="ehs_filtro")

        if opciones_filtrado == "Por nombre":
            seleccion = st.selectbox("Selecciona un nombre:", df["Nombre"].unique(), key="ehs_nombre")
            alumno = df[df["Nombre"] == seleccion].iloc[0]
            plot_radar(dimensiones, [alumno[dim] for dim in dimensiones], f"Habilidades Sociales - {seleccion}")

        elif opciones_filtrado == "Por perfil similar":
            df["Puntaje Global"] = df[dimensiones].mean(axis=1)
            umbral = st.slider("Filtra por puntaje global mínimo:", 1.0, 5.0, 3.5, 0.1, key="ehs_umbral")
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

    st.info(
        "🔎 **Instrucciones:** Marca la opción que mejor describa tu experiencia en los últimos 14 días.\n"
        "- 0 = En ningún momento\n"
        "- 1 = Varios días\n"
        "- 2 = Más de la mitad de los días\n"
        "- 3 = Casi todos los días\n\n"
        "📌 **Interpretación general:**\n"
        "A mayor puntaje total, mayor presencia de síntomas depresivos."
    )

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
    st.markdown("---")
    st.subheader("📈 Resultados")

    st.write(f"**Puntaje total:** {total}")

    # Diagnóstico
    if total <= 4:
        st.success("Mínima o sin depresión")
    elif total <= 9:
        st.info("Leve")
    elif total <= 14:
        st.info("Moderada")
    elif total <= 19:
        st.warning("Moderadamente Severa")
    else:
        st.error("Severa")

    st.markdown("### 🧠 Diagnóstico General")
    st.caption("📌 El PHQ-9 no sustituye una evaluación clínica. Si experimentas malestar, considera buscar ayuda profesional.")

    # Gráfico tipo radar
    plot_radar(preguntas, respuestas, "Perfil de síntomas depresivos (PHQ-9)")


    st.markdown("---")
    st.subheader("📂 Análisis colectivo - PHQ-9")

    archivo = st.file_uploader("Carga un archivo .csv con respuestas de PHQ-9", type=["csv"], key="phq9")
    if archivo:
        df = pd.read_csv(archivo)

        # Columnas originales del archivo
        columnas_originales = [f"Pregunta_{i}" for i in range(1, 10)]

        # Nuevos nombres descriptivos por ítem
        etiquetas_descriptivas = [
            "Pérdida de interés", "Ánimo bajo", "Alteración del sueño",
            "Cansancio", "Cambios en el apetito", "Autoimagen negativa",
            "Dificultad para concentrarse", "Agitación o lentitud", "Ideación suicida"
        ]

        # Crear un diccionario para cambiar nombres
        renombrar = {f"Pregunta_{i+1}": etiquetas_descriptivas[i] for i in range(9)}
        df = df.rename(columns=renombrar)

        preguntas = etiquetas_descriptivas
        df["Puntaje Total"] = df[preguntas].sum(axis=1)

        # Derretir el DataFrame para boxplot interactivo
        df_melted = df.melt(id_vars=["Nombre", "Puntaje Total"], value_vars=preguntas,
                        var_name="Síntoma", value_name="Respuesta")

        st.write("📊 Boxplot de síntomas depresivos")
        fig = px.box(df_melted, x="Síntoma", y="Respuesta", points="all",
                 hover_data=["Nombre", "Puntaje Total"],
                 title="Distribución de respuestas (PHQ-9)")
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

    st.info("""
    A continuación encontrarás una serie de afirmaciones relacionadas con tu forma de pensar, actuar y adaptarte ante situaciones nuevas.

    Por favor, responde **qué tanto te identificas con cada afirmación** utilizando la siguiente escala:

    - **1**: Muy en desacuerdo  
    - **2**: En desacuerdo  
    - **3**: Ni de acuerdo ni en desacuerdo  
    - **4**: De acuerdo  
    - **5**: Muy de acuerdo  
    """)

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
        if v >= 4.0:
            st.success(f"Fortaleza destacada en {k.lower()}.")
        elif v >= 3.0:
            st.info(f"Competencia adecuada en {k.lower()}.")
        elif v >= 2.0:
            st.warning(f"Dificultades moderadas en {k.lower()}.")
        else:
            st.error(f"Dificultades significativas en {k.lower()}.")

    plot_radar(list(dim_scores.keys()), list(dim_scores.values()), f"Radar Creatividad - {nombre}")

    
    st.markdown("---")
    st.subheader("📂 Análisis colectivo - Creatividad")

    archivo = st.file_uploader("Carga un archivo .csv con respuestas de creatividad", type=["csv"], key="creatividad")
    if archivo:
        df = pd.read_csv(archivo)
        dimensiones = [
            "Capacidad para resolver problemas",
            "Seguridad en sí mismo para resolver problemas",
            "Capacidad para desafiar normas",
            "Apertura a nuevas experiencias",
            "Tendencia a ajustarse a normas sociales y evitar riesgos creativos"
        ]
        df["Puntaje Global"] = df[dimensiones].mean(axis=1)

        # 👉 Derretir el DataFrame para plotly
        df_melted = df.melt(id_vars=["Nombre", "Puntaje Global"],
                            value_vars=dimensiones,
                            var_name="Dimensión",
                            value_name="Puntaje")

        st.write("📊 Boxplot de dimensiones")
        fig = px.box(df_melted,
                     x="Dimensión",
                     y="Puntaje",
                     points="all",
                     hover_data=["Nombre", "Puntaje Global"],
                     title="Distribución de dimensiones creativas")
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

import streamlit as st
import numpy as np
import plotly.graph_objects as go

# Función para graficar el radar
def plot_radar(labels, values, title=""):
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values + [values[0]],
        theta=labels + [labels[0]],
        fill='toself',
        name='Puntaje'
    ))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 10])),
        showlegend=False,
        title=title
    )
    st.plotly_chart(fig)

# Función principal
def neuropsi_evaluacion(nombre):
    st.subheader("Evaluación NEUROPSI - Atención y Memoria (Versión Adaptada)")

    st.info("""
    Esta prueba simula los tres dominios principales evaluados por NEUROPSI. Por favor, califica a la persona evaluada del 0 al 10 en cada tarea descrita, donde:

    - **0**: Dificultad severa  
    - **10**: Funcionamiento completamente adecuado  
    """)

    dimensiones = {
        "Atención y funciones ejecutivas": [
            "Capacidad para enfocarse en estímulos relevantes",
            "Mantiene la atención durante tareas largas",
            "Velocidad de procesamiento mental",
            "Fluidez verbal bajo presión",
            "Capacidad para inhibir respuestas automáticas",
            "Planeación y organización de tareas"
        ],
        "Memoria": [
            "Recuerdo inmediato de listas verbales",
            "Manipulación mental de información (memoria de trabajo)",
            "Recuerdo diferido (sin claves)",
            "Reconocimiento de información previa",
            "Memoria visual de figuras y ubicaciones"
        ],
        "Lenguaje y habilidades académicas": [
            "Comprensión oral de instrucciones",
            "Expresión verbal espontánea",
            "Nombramiento de objetos o imágenes",
            "Comprensión lectora funcional",
            "Resolución de operaciones matemáticas básicas"
        ]
    }

    respuestas = {}
    dim_scores = {}
    contador = 1
    for dim, preguntas in dimensiones.items():
        st.subheader(dim)
        suma = 0
        for preg in preguntas:
            resp = st.slider(f"{contador}. {preg}", 0, 10, 5, key=f"neuropsi_{contador}")
            respuestas[contador] = resp
            suma += resp
            contador += 1
        dim_scores[dim] = suma / len(preguntas)

    puntaje_total = np.mean(list(respuestas.values()))
    st.subheader("🧾 Resultado general estimado")
    st.write(f"**Puntaje promedio global:** {puntaje_total:.2f} / 10")

    if puntaje_total >= 8.0:
        st.success("Funcionamiento cognitivo dentro del rango esperado.")
    elif puntaje_total >= 6.0:
        st.info("Funcionamiento adecuado con algunas áreas por observar.")
    elif puntaje_total >= 4.0:
        st.warning("Dificultades moderadas. Se sugiere valoración completa.")
    else:
        st.error("Dificultades significativas. Se recomienda evaluación profesional especializada.")

    st.subheader("📊 Perfil por dominio")
    for k, v in dim_scores.items():
        st.write(f"**{k}:** {v:.2f}")
        if v >= 8.0:
            st.success(f"Excelente desempeño en {k.lower()}.")
        elif v >= 6.0:
            st.info(f"Desempeño aceptable en {k.lower()}.")
        elif v >= 4.0:
            st.warning(f"Área con dificultades en {k.lower()}.")
        else:
            st.error(f"Dificultades severas en {k.lower()}.")

    plot_radar(list(dim_scores.keys()), list(dim_scores.values()), f"Perfil NEUROPSI - {nombre}")




# === LLAMADO A FUNCIONES ===
if menu == "Escala de Habilidades Sociales":
    escala_ehs(nombre)
elif menu == "PHQ-9 (Depresión)":
    escala_phq9(nombre)
elif menu == "Escala de Creatividad":
    escala_creatividad(nombre)
elif menu == "Neuropsi":
    neurop(nombre)
