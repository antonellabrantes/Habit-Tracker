import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime, timedelta

ARCHIVO_DATOS = "historial_habitos.json"

# --- FUNCIONES DE DATOS ---
def cargar_datos():
    if os.path.exists(ARCHIVO_DATOS):
        with open(ARCHIVO_DATOS, "r") as f:
            return json.load(f)
    return {}

def guardar_datos(historial):
    with open(ARCHIVO_DATOS, "w") as f:
        json.dump(historial, f, indent=4)

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Habit Tracker Grid", layout="wide") # Layout ancho para la cuadrícula

# --- INICIALIZACIÓN ---
historial = cargar_datos()
hoy_dt = datetime.now()
hoy_str = hoy_dt.strftime("%Y-%m-%d")

# Generar lista de los últimos 7 días para las columnas
dias_semana = []
for i in range(6, -1, -1):
    fecha = (hoy_dt - timedelta(days=i)).strftime("%Y-%m-%d")
    dias_semana.append(fecha)

# Obtener lista maestra de hábitos
if historial:
    ultima_fecha = sorted(historial.keys())[-1]
    lista_habitos_maestra = list(historial[ultima_fecha].keys())
else:
    lista_habitos_maestra = ["Beber Agua", "Hacer Ejercicio", "Programar"]

# Asegurarse de que cada día de la semana tenga sus datos inicializados
for dia in dias_semana:
    if dia not in historial:
        historial[dia] = {habito: False for habito in lista_habitos_maestra}

# --- BARRA LATERAL ---
st.sidebar.title("⚙️ Configuración")
nuevo_habito = st.sidebar.text_input("Añadir nuevo hábito:")
if st.sidebar.button("Añadir"):
    if nuevo_habito:
        for dia in dias_semana:
            historial[dia][nuevo_habito] = False
        guardar_datos(historial)
        st.rerun()

habito_a_borrar = st.sidebar.selectbox("Eliminar hábito:", ["---"] + lista_habitos_maestra)
if st.sidebar.button("Eliminar"):
    if habito_a_borrar != "---":
        for dia in dias_semana:
            if habito_a_borrar in historial[dia]:
                del historial[dia][habito_a_borrar]
        guardar_datos(historial)
        st.rerun()

# --- CUERPO PRINCIPAL (VISTA DE CUADRÍCULA) ---
st.title("📅 Habit Tracker - Vista Semanal")

# Crear encabezados de columnas (Hábito + los 7 días)
# Usamos una proporción de 2 para el nombre y 1 para cada cuadradito
cols = st.columns([2] + [1] * 7)
cols[0].write("**HÁBITO**")
for i, dia in enumerate(dias_semana):
    # Mostrar solo el nombre del día (Lun, Mar...)
    nombre_dia = (hoy_dt - timedelta(days=6-i)).strftime("%a")
    cols[i+1].write(f"**{nombre_dia}**")

st.divider()

# Crear las filas de la cuadrícula
for habito in lista_habitos_maestra:
    cols = st.columns([2] + [1] * 7)
    cols[0].write(f"**{habito}**") # Nombre del hábito
    
    for i, dia in enumerate(dias_semana):
        # El checkbox de cada día. Usamos una clave única combinando fecha y hábito
        clave = f"{dia}_{habito}"
        # Si es el día de hoy, permitimos editar. Si es pasado, también (opcional)
        estado = cols[i+1].checkbox(" ", value=historial[dia].get(habito, False), key=clave, label_visibility="collapsed")
        historial[dia][habito] = estado

# Guardar cambios
guardar_datos(historial)

# --- BARRA DE PROGRESO SEMANAL ---
st.divider()
total_checks = len(lista_habitos_maestra) * 7
checks_hechos = sum(sum(dia.values()) for dia in [historial[d] for d in dias_semana])
progreso_total = checks_hechos / total_checks

st.subheader(f"Cumplimiento Semanal: {int(progreso_total * 100)}%")
st.progress(progreso_total)

#if hoy not in historial:
#    historial[hoy] = {
#        "No celular 1hr AM": False,
#        "Estiramientos": False,
#        "Afirmaciones": False,
#        "Skin Care AM": False,
#        "Tarot": False, 
#        "Spray pelo": False,
#        "Leer 5 min": False,
#        "Cremas": False,
#        "No celular 1hr PM": False,
#        "Pieza ordenada PM": False, 
#        "Skin Care PM": False

#    }
