import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime
import plotly.express as px

st.set_page_config(page_title="Escala de Creatividad de Gough", layout="centered")

st.title("🧠 Escala de Creatividad de Gough (1976) - Adaptada con Escala Likert")

menu = st.sidebar.radio("Selecciona una sección:", ["Cuestionario", "Análisis de grupo"])

if menu == "Cuestionario":
    nombre = st.text_input("Escribe tu nombre o iniciales (opcional):")

    st.write("Responde cada afirmación según tu grado de acuerdo. Usa la escala Likert de 1 a 5:")
    st.write("1 = Totalmente en desacuerdo, 5 = Totalmente de acuerdo")

    # Preguntas integradas directamente en el código
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

    # Crear diccionario para almacenar respuestas
    respuestas = {}

    # Mostrar preguntas agrupadas por dimensión
    dim_scores = {}
    contador = 1
    for dimension, preguntas in preguntas_por_dimension.items():
        st.subheader(dimension)
        score_total = 0
        for pregunta in preguntas:
            respuesta = st.radio(
                f"{contador}. {pregunta}",
                options=[1, 2, 3, 4, 5],
                index=2,
                key=f"preg_{contador}"
            )
            respuestas[contador] = respuesta
            score_total += respuesta
            contador += 1
        dim_scores[dimension] = score_total / len(preguntas)

    # Calcular puntaje global promedio
    puntaje_total = np.mean(list(respuestas.values()))

    st.markdown("---")
    st.subheader("🔍 Resultado general")
    st.write(f"**Puntaje promedio global:** {puntaje_total:.2f} (escala 1 a 5)")

    # Interpretación general
    if puntaje_total >= 4.0:
        interpretacion = "Alto perfil creativo"
        st.success(interpretacion)
    elif puntaje_total >= 3.0:
        interpretacion = "Perfil moderadamente creativo"
        st.info(interpretacion)
    elif puntaje_total >= 2.0:
        interpretacion = "Perfil con rasgos creativos limitados"
        st.warning(interpretacion)
    else:
        interpretacion = "Tendencia a evitar comportamientos creativos"
        st.error(interpretacion)

    # Mostrar resultados por dimensión
    st.subheader("📊 Perfil por dimensión")
    for dim, score in dim_scores.items():
        st.write(f"**{dim}:** {score:.2f}")

    # Consejos personalizados
    st.markdown("### 💡 Sugerencias personalizadas")
    if dim_scores.get("Capacidad para resolver problemas", 0) >= 4:
        st.write("- Tienes un pensamiento resolutivo. Usa retos o acertijos para mantener tu mente activa.")
    if dim_scores.get("Capacidad para desafiar normas", 0) >= 4:
        st.write("- Tiendes a cuestionar estructuras. Usa eso para proponer ideas disruptivas en tu entorno.")
    if dim_scores.get("Tendencia a ajustarse a normas sociales y evitar riesgos creativos", 0) >= 3.5:
        st.write("- Podrías estar evitando riesgos. Intenta un proyecto sin buscar aprobación externa.")
    if dim_scores.get("Seguridad en sí mismo para resolver problemas", 0) >= 4:
        st.write("- Tu autoconfianza puede potenciar tus decisiones creativas. Lidera desde tu autenticidad.")
    if dim_scores.get("Apertura a nuevas experiencias", 0) >= 4:
        st.write("- Eres receptivo a lo nuevo. Prueba actividades artísticas o improvisación para nutrir tu creatividad.")

    # Radar chart
    st.subheader("📈 Visualización de tu perfil")
    labels = list(dim_scores.keys())
    values = list(dim_scores.values())
    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    values += values[:1]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.fill(angles, values, color='skyblue', alpha=0.4)
    ax.plot(angles, values, color='blue', linewidth=2)
    ax.set_yticks([1, 2, 3, 4, 5])
    ax.set_yticklabels(['1', '2', '3', '4', '5'])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)
    ax.set_title("Radar de Dimensiones Creativas", y=1.1)
    st.pyplot(fig)

    # Guardar resultados
    if st.button("💾 Guardar mis respuestas"):
        df_resultado = pd.DataFrame([{
            "Nombre": nombre if nombre else "Anónimo",
            "Fecha": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            "Puntaje Global": puntaje_total,
            "Interpretación": interpretacion,
            **dim_scores
        }])
        df_resultado.to_csv("resultados_creatividad_likert.csv", mode='a', header=False, index=False)
        st.success("Resultados guardados correctamente.")

elif menu == "Análisis de grupo":
    st.header("📂 Análisis grupal de resultados")
    archivo = st.file_uploader("Carga el archivo CSV de respuestas", type=["csv"])

    if archivo is not None:
        df = pd.read_csv(archivo)

        st.write("Vista previa de datos:")
        st.dataframe(df.head())

        dimensiones = [
            "Capacidad para resolver problemas",
            "Seguridad en sí mismo para resolver problemas",
            "Capacidad para desafiar normas",
            "Apertura a nuevas experiencias",
            "Tendencia a ajustarse a normas sociales y evitar riesgos creativos"
        ]

        df_melted = df.melt(
            id_vars=["Nombre"],
            value_vars=dimensiones,
            var_name="Dimensión",
            value_name="Puntaje"
        )

        fig = px.box(
            df_melted,
            x="Dimensión",
            y="Puntaje",
            points="all",
            color="Dimensión",
            hover_data=["Nombre"],
            title="Distribución de puntajes por dimensión"
        )

        st.plotly_chart(fig, use_container_width=True)



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
            umbral = st.slider("Filtra por puntaje global mínimo:", 1.0, 5.0, 3.5, 0.1)
            filtrado = df[df["Puntaje Global"] >= umbral]

            st.write(f"{len(filtrado)} alumns con puntaje global ≥ {umbral}")

            for idx, row in filtrado.iterrows():
                st.markdown(f"**{row['Nombre']} ({row['Puntaje Global']}):**")
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


####################################################################################################################

import streamlit as st
import pandas as pd
import numpy as np
import datetime


st.title("🗣️ Escala de Habilidades Sociales (EHS) - Gismero 2010")

nombre = st.text_input("Nombre o identificar del estudiante:")

st.write("Responde a cada afirmación según el grado con el que te identifiques. Usa la siguiente escala:")
st.markdown("""
1 = Nunca<br>
2 = Casi nunca<br>
3 = A veces<br>
4 = Casi siempre<br>
5 = Siempre
""", unsafe_allow_html=True)

# Lista de ítems representativos (pueden ser adaptados fielmente si se cuenta con todos)
items = [
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

# Diccionario para acumular puntuaciones por dimensión
respuestas = {}
resultados_dim = {}

for idx, (dim, texto) in enumerate(items):
    valor = st.slider(f"{idx+1}. {texto}", 1, 5, 3, key=f"pregu_{idx+1}")
    if dim not in respuestas:
        respuestas[dim] = []
    respuestas[dim].append(valor)

# Calcular promedios por dimensión
for dim, vals in respuestas.items():
    resultados_dim[dim] = round(np.mean(vals), 2)

puntaje_global = round(np.mean(list(resultados_dim.values())), 2)

st.markdown("---")
st.subheader("📊 Resultado del perfil social")
st.write(f"**Puntaje global:** {puntaje_global} (escala 1-5)")

# Mostrar resultados por dimensión
for dim, score in resultados_dim.items():
    st.write(f"**{dim}:** {score}")

# Interpretación general
st.markdown("### 🧾 Interpretación global")
if puntaje_global >= 4:
    st.success("Perfil altamente habilidoso socialmente.")
elif puntaje_global >= 3:
    st.info("Perfil social moderado. Algunas áreas pueden requerir fortalecimiento.")
elif puntaje_global >= 2:
    st.warning("Perfil con posibles dificultades en habilidades sociales.")
else:
    st.error("Perfil con alta necesidad de intervención en habilidades sociales.")

# Guardar resultados
if st.button("💾 Guardar resultados"):
    df_resultado = pd.DataFrame([{
        "Nombre": nombre if nombre else "Anónimo",
        "Fecha": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        "Puntaje Global": puntaje_global,
        **resultados_dim
    }])
    df_resultado.to_csv("resultados_EHS_Gismero.csv", mode='a', header=False, index=False)
    st.success("Resultados guardados correctamente.")

