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
import streamlit as st

def escala_creatividad():
    # Título e instrucciones iniciales
    st.title("Escala de Creatividad (Adaptada de Gough)")
    st.markdown("""
    **Instrucciones:** A continuación encontrarás una serie de afirmaciones relacionadas con la creatividad. 
    Lee cada afirmación y selecciona el nivel que mejor representa cuánto te identificas con ella, usando una escala de 1 a 5:
    - **1:** Muy en desacuerdo (la afirmación no te describe en absoluto).
    - **5:** Muy de acuerdo (te describes completamente con la afirmación).
    *Utiliza los valores intermedios (2, 3, 4) para matices de acuerdo o frecuencia.* 
    """)

    # Definir las preguntas agrupadas por dimensión (ejemplo; reemplazar con las reales)
    dimensiones = {
        "Dimensión 1": [
            "Me gusta proponer ideas nuevas e innovadoras.",
            "Tiende a pensar de manera poco convencional."
        ],
        "Dimensión 2": [
            "Me considero una persona curiosa.",
            "Disfruto explorando soluciones creativas a los problemas."
        ],
        "Dimensión 3": [
            "Soy persistente cuando intento resolver un desafío difícil.",
            "Me adapto fácilmente a situaciones nuevas o inesperadas."
        ]
    }

    # Diccionario para almacenar las respuestas del usuario
    respuestas = {}

    # Formulario para responder las preguntas de cada dimensión
    with st.form("form_creatividad"):
        for nombre_dim, preguntas in dimensiones.items():
            st.subheader(nombre_dim)  # Encabezado de la dimensión
            for texto_pregunta in preguntas:
                # Cada pregunta se muestra con un slider de 1 a 5
                respuesta = st.slider(texto_pregunta, min_value=1, max_value=5, value=3)
                respuestas[texto_pregunta] = respuesta
        # Botón de envío del formulario
        enviado = st.form_submit_button("Calcular resultados")

    if not enviado:
        # Si el formulario no se ha enviado, no mostrar resultados aún
        return

    # Calcular el promedio por dimensión
    promedios_dim = {}
    for nombre_dim, preguntas in dimensiones.items():
        # Extraer las respuestas de las preguntas de esta dimensión
        valores = [respuestas[texto] for texto in preguntas]
        if valores:
            promedio = sum(valores) / len(valores)
        else:
            promedio = 0
        promedios_dim[nombre_dim] = promedio

    # Calcular puntaje global (promedio de todas las respuestas)
    todos_valores = list(respuestas.values())
    if todos_valores:
        puntaje_global = sum(todos_valores) / len(todos_valores)
    else:
        puntaje_global = 0

    # Función auxiliar para interpretar el nivel según el puntaje
    def interpretar_nivel(promedio):
        """Devuelve una interpretación de nivel creativo según el valor promedio de 1 a 5."""
        if promedio >= 4.0:
            return "Nivel **alto**"
        elif promedio >= 3.0:
            return "Nivel **adecuado**"
        elif promedio >= 2.0:
            return "Nivel **limitado**"
        else:
            return "Nivel **bajo o evitativo**"

    # Mostrar diagnóstico por dimensión
    st.header("Diagnóstico por dimensión")
    for nombre_dim, promedio in promedios_dim.items():
        nivel_texto = interpretar_nivel(promedio)
        st.write(f"- **{nombre_dim}:** {nivel_texto} (promedio = {promedio:.1f})")

    # Mostrar diagnóstico global
    st.subheader("Diagnóstico general")
    nivel_global_texto = interpretar_nivel(puntaje_global)
    st.write(f"**Puntaje global de creatividad:** {puntaje_global:.1f} – {nivel_global_texto}")

    # Mostrar gráfico de radar con los promedios por dimensión
    st.subheader("Perfil de Creatividad por Dimensión")
    # Preparar datos para el radar
    etiquetas = list(promedios_dim.keys())
    valores = list(promedios_dim.values())
    # Generar el gráfico de radar utilizando la función plot_radar predefinida
    #figura_radar = plot_radar(etiquetas, valores)
    #st.pyplot(figura_radar)
    # Mostrar gráfico de radar con los promedios por dimensión
    st.subheader("Perfil de Creatividad por Dimensión")
    plot_radar(etiquetas, valores, title="Radar Creatividad")


    
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



# === LLAMADO A FUNCIONES ===
if menu == "Escala de Habilidades Sociales":
    escala_ehs(nombre)
elif menu == "PHQ-9 (Depresión)":
    escala_phq9(nombre)
elif menu == "Escala de Creatividad":
    escala_creatividad(nombre)
