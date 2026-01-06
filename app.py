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
            try:
                return json.load(f)
            except:
                return {}
    return {}

def guardar_datos(historial):
    with open(ARCHIVO_DATOS, "w") as f:
        json.dump(historial, f, indent=4)

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Habit Tracker Grid", layout="wide")

# --- INICIALIZACIÓN ---
historial = cargar_datos() # <--- ¡Esta es la línea que faltaba!
hoy_dt = datetime.now()
hoy_str = hoy_dt.strftime("%Y-%m-%d")

# Generar exactamente los últimos 7 días terminando HOY
dias_semana = []
for i in range(6, -1, -1):
    fecha = (hoy_dt - timedelta(days=i)).strftime("%Y-%m-%d")
    dias_semana.append(fecha)

# Obtener lista maestra de hábitos
if historial and hoy_str in historial:
    lista_habitos_maestra = list(historial[hoy_str].keys())
elif historial:
    ultima_fecha = sorted(historial.keys())[-1]
    lista_habitos_maestra = list(historial[ultima_fecha].keys())
else:
    lista_habitos_maestra = ["Beber Agua", "Hacer Ejercicio", "Programar"]

# Asegurarse de que cada día de la semana tenga sus datos
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

# --- CUERPO PRINCIPAL ---
st.title("📅 Mi Habit Tracker")

# Estilo CSS para cuadraditos grandes y verdes
st.markdown("""
    <style>
    .stCheckbox {
        display: flex;
        justify-content: center;
    }
    input[type=checkbox] {
        transform: scale(1.8);
    }
    </style>
    """, unsafe_allow_html=True)

# Traducción de días
traduccion_dias = {"Mon": "Lun", "Tue": "Mar", "Wed": "Mie", "Thu": "Jue", "Fri": "Vie", "Sat": "Sab", "Sun": "Dom"}

# Encabezados
cols = st.columns([2] + [1] * 7)
cols[0].write("**HÁBITO**")
for i, fecha_str in enumerate(dias_semana):
    f_obj = datetime.strptime(fecha_str, "%Y-%m-%d")
    nombre_esp = traduccion_dias.get(f_obj.strftime("%a"), f_obj.strftime("%a"))
    
    if fecha_str == hoy_str:
        cols[i+1].markdown(f"<div style='text-align: center;'><b>{nombre_esp}</b><br>📍</div>", unsafe_allow_html=True)
    else:
        cols[i+1].markdown(f"<div style='text-align: center;'><b>{nombre_esp}</b></div>", unsafe_allow_html=True)

st.divider()

# Filas de hábitos
for habito in lista_habitos_maestra:
    cols = st.columns([2] + [1] * 7)
    cols[0].write(f"**{habito}**")
    
    for i, dia in enumerate(dias_semana):
        clave = f"{dia}_{habito}"
        # Solo permitimos que se guarde el cambio
        estado = cols[i+1].checkbox("", value=historial[dia].get(habito, False), key=clave, label_visibility="collapsed")
        historial[dia][habito] = estado

guardar_datos(historial)

# Barra de progreso
st.divider()
total_posible = len(lista_habitos_maestra) * 7
hechos = sum(sum(h.values()) for h in [historial[d] for d in dias_semana if d in historial])
progreso = hechos / total_posible if total_posible > 0 else 0
st.subheader(f"Cumplimiento Semanal: {int(progreso * 100)}%")
st.progress(progreso)
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


