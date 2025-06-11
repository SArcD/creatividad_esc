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
