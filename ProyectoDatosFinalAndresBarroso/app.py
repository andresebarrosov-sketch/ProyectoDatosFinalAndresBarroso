import streamlit as st
import joblib
import pandas as pd
import numpy as np
from pathlib import Path

st.set_page_config(page_title="ProyectoDatosFinalAndresBarroso", page_icon="🚦", layout="centered")
st.title("ProyectoDatosFinalAndresBarroso")
st.subheader("Análisis de siniestros viales en Palmira")
st.write(
    "Aplicación demostrativa del modelo de clasificación entrenado con datos abiertos "
    "de siniestros viales de Palmira. La predicción es experimental y no debe utilizarse "
    "para decisiones operativas ni para evaluar personas."
)

MODEL_PATH = Path(__file__).parent / "modelo_siniestros_palmira.joblib"

@st.cache_resource
def load_artifact(path):
    return joblib.load(path)

if not MODEL_PATH.exists():
    st.error("No se encuentra modelo_siniestros_palmira.joblib. Coloca el archivo junto a app.py.")
    st.stop()

artifact = load_artifact(MODEL_PATH)
model = artifact["model"]
meta = artifact["metadata"]
st.caption(f"Modelo seleccionado en el notebook: {artifact.get('selected_model', 'No especificado')}")
if artifact.get("selected_model") == "Regresión logística":
    st.warning(
        "Este archivo de modelo corresponde a la ejecución anterior. "
        "Ejecuta el notebook actualizado para generar el modelo seleccionado "
        "por validación cruzada y reemplaza este .joblib antes de la entrega final."
    )

# Avisar si el artefacto se creó con otra versión de scikit-learn.
saved_version = artifact.get("versions", {}).get("scikit_learn")
try:
    import sklearn
    if saved_version and saved_version != sklearn.__version__:
        st.warning(
            f"El modelo fue guardado con scikit-learn {saved_version}, "
            f"pero la aplicación usa {sklearn.__version__}. "
            "Instala las versiones de requirements.txt y vuelve a generar el modelo."
        )
except Exception:
    pass

st.subheader("Características del registro")
st.caption("Introduce valores disponibles. La aplicación no solicita identificadores ni dirección exacta.")

with st.form("prediction_form"):
    values = {}
    for col in meta["features"]:
        if col in meta["numeric_cols"]:
            default = float(meta["numeric_defaults"].get(col, 0.0))
            values[col] = st.number_input(col, value=default, format="%.4f")
        else:
            options = meta["categorical_options"].get(col, [])
            options = ["Sin dato"] + options
            selected = st.selectbox(col, options=options, index=0)
            values[col] = np.nan if selected == "Sin dato" else selected
    submitted = st.form_submit_button("Realizar predicción", type="primary")

if submitted:
    input_df = pd.DataFrame([values], columns=meta["features"])
    prediction = model.predict(input_df)[0]
    st.subheader("Resultado del modelo")
    st.metric("Clasificación estimada", str(prediction))
    if hasattr(model, "predict_proba"):
        probabilities = model.predict_proba(input_df)[0]
        classes = model.named_steps[model.steps[-1][0]].classes_
        probability_df = pd.DataFrame({"Clase": classes, "Probabilidad": probabilities})
        st.write("Probabilidades estimadas:")
        st.dataframe(probability_df.style.format({"Probabilidad": "{:.1%}"}), use_container_width=True)
    st.warning(
        "Esta salida es una clasificación estadística basada en patrones históricos. "
        "No representa una evaluación clínica, jurídica ni una predicción segura del desenlace de un siniestro."
    )

st.divider()
st.markdown("**Proyecto:** ProyectoDatosFinalAndresBarroso  \n\n**Fuente de datos:** [Siniestros Viales Palmira — datos.gov.co](https://www.datos.gov.co/w/sjpx-eqfp/dneh-mcp2)")
