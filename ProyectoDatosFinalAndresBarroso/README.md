# ProyectoDatosFinalAndresBarroso

## Análisis de siniestros viales en Palmira, Colombia

Proyecto académico de ciencia de datos desarrollado para la asignatura **Fundamentos de Ciencia de Datos**. Se estudian registros de siniestros viales publicados en el portal nacional de datos abiertos y se comparan tres modelos de clasificación para distinguir registros etiquetados como `LESIONADO` y `MUERTO`.

**Autor:** Andrés Barroso  
**Metodología:** CRISP-DM  
**Lenguaje y herramientas:** Python, Google Colab, pandas, scikit-learn, Streamlit.

> Si el trabajo fue realizado en grupo, agrega los nombres de los demás integrantes antes de publicar el repositorio.

## 1. Fuente de datos

- **Dataset:** [Siniestros Viales Palmira — datos.gov.co](https://www.datos.gov.co/w/sjpx-eqfp/dneh-mcp2)
- **Entidad proveedora:** Alcaldía de Palmira, Valle del Cauca.
- **Archivo utilizado:** `Siniestros_Viales_Palmira_20261026.csv`.
- **Fecha de referencia indicada en el nombre del archivo:** 26 de octubre de 2026. Confirma y registra la fecha efectiva de descarga en la entrega si fue diferente.

El CSV incluido en este repositorio contiene 2.834 filas y 19 columnas.

## 2. Objetivo y alcance

Analizar patrones temporales, geográficos y asociados al tipo de siniestro y evaluar si las variables disponibles permiten clasificar los registros como `LESIONADO` o `MUERTO`.

El modelo es exploratorio y académico. No demuestra causalidad, no predice con certeza el desenlace de un siniestro y no debe utilizarse para decisiones operativas, clínicas, jurídicas o para evaluar personas.

## 3. Estructura del repositorio

```text
ProyectoDatosFinalAndresBarroso/
├── ProyectoDatosFinalAndresBarroso.ipynb
├── app.py
├── requirements.txt
├── runtime.txt
├── README.md
├── modelo_siniestros_palmira.joblib
├── MODEL_REGENERATION_REQUIRED.txt
└── Siniestros_Viales_Palmira_20261026.csv
```

## 4. Metodología

Se sigue el proceso CRISP-DM:

1. Comprensión del problema: análisis de seguridad vial en Palmira.
2. Comprensión de los datos: estructura, tipos, faltantes, duplicados y distribuciones.
3. Preparación: limpieza, conversión de variables, revisión IQR de valores atípicos y selección de predictores.
4. Modelado: regresión logística, árbol de decisión y Random Forest.
5. Evaluación: validación cruzada estratificada por grupos y métricas Accuracy, Precision, Recall y F1.
6. Despliegue: aplicación demostrativa con Streamlit.

Los registros se agrupan por `IPAT` al separar entrenamiento y prueba, para evitar que registros vinculados al mismo siniestro queden en ambos conjuntos. La búsqueda de hiperparámetros y la selección del modelo se realizan dentro del conjunto de entrenamiento mediante F1 de la clase minoritaria `MUERTO`. El conjunto de prueba se reserva para la evaluación final.

## 5. Resultados de la ejecución disponible

La ejecución guardada en el notebook registró 9 duplicados exactos. Luego de eliminarlos y excluir `NO APLICA`, quedaron 1.851 registros para el problema binario: 1.717 `LESIONADO` (92,76 %) y 134 `MUERTO` (7,24 %).

| Modelo | Accuracy | Precision MUERTO | Recall MUERTO | F1 MUERTO | F1 macro | F1 CV MUERTO |
|---|---:|---:|---:|---:|---:|---:|
| Regresión logística | 0,666 | 0,225 | 0,753 | 0,346 | 0,561 | 0,291 |
| Random Forest | 0,591 | 0,197 | 0,805 | 0,316 | 0,512 | **0,310** |
| Árbol de decisión | 0,670 | 0,144 | 0,364 | 0,206 | 0,499 | 0,225 |

**Modelo seleccionado según validación cruzada: Random Forest**, por obtener el mayor F1 promedio para `MUERTO` (0,310). En el conjunto de prueba obtuvo F1=0,316, Recall=0,805 y Precision=0,197 para esa clase. Esto significa que detecta una proporción alta de los casos `MUERTO`, pero también genera falsas alarmas. La regresión logística tuvo F1 de prueba 0,346, pero la prueba no se utiliza para seleccionar el modelo.

Las métricas corresponden a la ejecución guardada en el notebook. Ejecuta el notebook completo para reproducir los resultados y generar el artefacto final seleccionado por validación cruzada.

## 6. Ejecutar el notebook en Google Colab

1. Descarga o sube `ProyectoDatosFinalAndresBarroso.ipynb` a Google Colab.
2. Sube `Siniestros_Viales_Palmira_20261026.csv` a la raíz de tu Google Drive (Mi unidad), o cambia la variable `ruta_csv` en la primera sección del notebook.
3. Ejecuta **Entorno de ejecución → Ejecutar todas**.
4. El notebook instala las versiones fijadas de scikit-learn y joblib, entrena los tres modelos y guarda el artefacto en:
   `Mi unidad/ProyectoDatosFinalAndresBarroso/modelo_siniestros_palmira.joblib`
5. Descarga ese modelo recién generado y reemplaza el archivo `.joblib` del repositorio antes de publicar la aplicación.

## 7. Ejecutar Streamlit localmente

Se recomienda Python 3.11. Coloca `app.py`, `requirements.txt` y el modelo `.joblib` recién generado en la misma carpeta.

```bash
python -m venv .venv
```

Activar el entorno:

**Windows**
```bash
.venv\Scripts\activate
```

**macOS / Linux**
```bash
source .venv/bin/activate
```

Instalar dependencias e iniciar la aplicación:

```bash
pip install -r requirements.txt
streamlit run app.py
```

La aplicación abrirá una dirección local que Streamlit mostrará en la terminal (normalmente `http://localhost:8501`).

## 8. Publicar en GitHub y Streamlit Community Cloud

1. Crea un repositorio público llamado `ProyectoDatosFinalAndresBarroso`.
2. Sube los archivos de esta carpeta, incluido el CSV y el modelo actualizado si las reglas de entrega lo permiten.
3. Entra a Streamlit Community Cloud e inicia sesión con GitHub.
4. Selecciona **Create app**, el repositorio, la rama y `app.py` como archivo principal.
5. Despliega y comprueba la URL pública.
6. Añade el enlace de la aplicación aquí y en la descripción del repositorio: **URL de la app:** pendiente de publicación.

No publiques claves, contraseñas ni datos personales. Si el profesor prefiere que el dataset no se replique en GitHub, elimina el CSV del repositorio y conserva el enlace oficial en este README.

## 9. Limitaciones

- La clase `MUERTO` está subrepresentada (7,24 % de los registros modelados).
- La precisión para `MUERTO` es baja; las predicciones positivas incluyen falsos positivos.
- Los registros pueden corresponder a víctimas diferentes de un mismo siniestro; por eso se agrupan por `IPAT`.
- Debe verificarse en el diccionario de datos el significado y consistencia de `IPAT` y `CONDICION DE LA VICTIMA`.
- Los valores atípicos geográficos se reportan para revisión y no se eliminan automáticamente.
- La cobertura temporal, la calidad y las definiciones dependen del registro administrativo publicado.
- Se requiere validación con datos nuevos y revisión por la entidad responsable antes de cualquier aplicación práctica.

## 10. Lista de verificación de entrega

- [ ] Confirmar la fecha efectiva de descarga y revisar la ficha del dataset.
- [ ] Ejecutar todas las celdas del notebook sin errores.
- [ ] Confirmar que el artefacto `.joblib` se regeneró con Random Forest seleccionado por F1 de validación cruzada.
- [ ] Probar `app.py` localmente con las versiones de `requirements.txt`.
- [ ] Completar los nombres de todos los integrantes, si aplica.
- [ ] Publicar el repositorio público de GitHub.
- [ ] Desplegar y probar la aplicación si el curso exige URL pública.
- [ ] Añadir el enlace de GitHub y el de Streamlit a la entrega.
- [ ] Preparar la sustentación explicando las variables, el desbalance, la validación agrupada y las limitaciones.
