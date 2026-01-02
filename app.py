import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime

ARCHIVO_DATOS = "historial_habitos.json"

# Configuración de la página
st.set_page_config(page_title="Habit Tracker Web", layout="centered")

# --- FUNCIONES DE DATOS ---
def cargar_datos():
    if os.path.exists(ARCHIVO_DATOS):
        with open(ARCHIVO_DATOS, "r") as f:
            return json.load(f)
    return {}

def guardar_datos(historial):
    with open(ARCHIVO_DATOS, "w") as f:
        json.dump(historial, f, indent=4)

# --- LÓGICA PRINCIPAL ---
historial = cargar_datos()
hoy = datetime.now().strftime("%Y-%m-%d")

if hoy not in historial:
    historial[hoy] = {
        "Beber 2L de Agua": False,
        "Hacer Ejercicio": False,
        "Meditar 10 min": False,
        "Programar": False
    }

st.title("📊 Mi Habit Tracker Web")
st.subheader(f"Progreso para hoy: {hoy}")

# --- CHECKLIST EN LA WEB ---
for habito in historial[hoy].keys():
    # Creamos un checkbox y guardamos si cambia
    valor = st.checkbox(habito, value=historial[hoy][habito])
    historial[hoy][habito] = valor

# Guardar cambios automáticamente
guardar_datos(historial)

# --- ESTADÍSTICAS ---
st.divider()
st.subheader("Estadísticas de la semana")

if historial:
    # Transformar datos para el gráfico
    data_list = []
    for fecha, habitos in historial.items():
        porcentaje = (sum(habitos.values()) / len(habitos)) * 100
        data_list.append({"Fecha": fecha, "Cumplimiento": porcentaje})
    
    df = pd.DataFrame(data_list)
    st.bar_chart(data=df, x="Fecha", y="Cumplimiento")