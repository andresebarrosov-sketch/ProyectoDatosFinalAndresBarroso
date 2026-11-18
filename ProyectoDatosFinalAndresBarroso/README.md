# ProyectoDatosFinalAndresBarroso

## Análisis de siniestros viales en Palmira, Colombia

Proyecto académico de ciencia de datos desarrollado para la asignatura **Fundamentos de Ciencia de Datos**. Se estudian registros de siniestros viales publicados en el portal nacional de datos abiertos y se comparan tres modelos de clasificación para distinguir registros etiquetados como `LESIONADO` y `MUERTO`.

**Autor:** Andrés Eduardo Barroso Velásquez 
**Metodología:** CRISP-DM  
**Lenguaje y herramientas:** Python, Google Colab, pandas, scikit-learn, Streamlit.

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
