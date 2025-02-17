import streamlit as st
import pandas as pd
import base64

import streamlit.components.v1 as components

# URL del logo en GitHub
logo_url = "https://raw.githubusercontent.com/cbenlloch/code_for_fun/main/logo.png.png"




  
# Archivos de datos
DATA_FILE_ENJOY = "resultados_enjoy.csv"
DATA_FILE_ENERGY = "resultados_energy.csv"

# Definir parejas
parejas_energy = {
    "A": "Gerard Oliveira – Pau Claret",
    "B": "Helena Naranjo – Lorena Martinez",
    "C": "Francisco Fortunato – Naomi Lindheimer",
    "D": "Pablo Cañaveras – Paula Penas",
    "E": "Chema Iglesias – Ausias Garcia",
    "F": "Àlex Dinaret – Raúl Cuevas",
    "G": "Oscar Machuca – Igor Almada"
}

parejas_enjoy = {
    "H": "Marcel Ferré - Marianella Abosso",
    "I": "Ferran Sanabre - Garazi Lejarza",
    "J": "Erika Tomulete - Maira Montezuma",
    "K": "Mar Sánchez - Carla Benlloch"
}

# Función para cargar datos
def cargar_datos(file):
    try:
        return pd.read_csv(file)
    except FileNotFoundError:
        return pd.DataFrame(columns=["Pareja 1", "Pareja 2", "Resultado"])       

# Aplicar estilos CSS para centrar y dar mejor aspecto a la barra lateral
st.markdown(
    """
    <style>
    [data-testid="stSidebar"] {
        background-color: #f0f0f0;  /* Color de fondo gris */
    }
    .sidebar-logo {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 10px 0; /* Espaciado arriba y abajo */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Agregar el logo en la barra lateral y centrarlo correctamente
st.sidebar.markdown(
    f"""
    <div class="sidebar-logo">
        <img src="{logo_url}" width="150">
    </div>
    """,
    unsafe_allow_html=True
)

# Sidebar con selector de copa
st.sidebar.title("🏆 Selección de Copa")
opcion_copa = st.sidebar.selectbox("Elige la copa:", ["Copa Enjoy", "Copa Energy"])

# Seleccionar el archivo y la lista de parejas según la copa
if opcion_copa == "Copa Enjoy":
    DATA_FILE = DATA_FILE_ENJOY
    parejas = parejas_enjoy
else:
    DATA_FILE = DATA_FILE_ENERGY
    parejas = parejas_energy

df = cargar_datos(DATA_FILE)

# Mostrar parejas
st.title(f"Torneo de Pádel - {opcion_copa}")
st.header("Parejas Participantes")
for letra, pareja in parejas.items():
    st.write(f"**Pareja {letra}:** {pareja}")

# 📌 **Formulario para subir resultados con Selectbox**
st.header(f"Subir Resultado - {opcion_copa}")

col1, col2, col3 = st.columns(3)

# Usamos `selectbox` en lugar de `text_input`
with col1:
    Pareja1 = st.selectbox("Pareja 1", list(parejas.values()), key="pareja1")

# Filtrar la lista para que Pareja2 no tenga la misma opción que Pareja1
opciones_pareja2 = [p for p in parejas.values() if p != Pareja1]

with col2:
    Pareja2 = st.selectbox("Pareja 2", opciones_pareja2, key="pareja2")

with col3:
    resultado = st.text_input("Resultado (Ej: 6-3, 4-6, 10-7)")

# Guardar resultado
if st.button("Enviar"):
    if Pareja1 and Pareja2 and resultado:
        nuevo_resultado = pd.DataFrame([[Pareja1, Pareja2, resultado]], columns=df.columns)
        df = pd.concat([df, nuevo_resultado], ignore_index=True)
        df.to_csv(DATA_FILE, index=False)
        st.success("Resultado guardado!")
        st.rerun()
    else:
        st.error("Selecciona parejas diferentes y escribe un resultado válido.")

# Mostrar tabla con los resultados ingresados
st.header(f"Resultados - {opcion_copa}")
st.dataframe(df)


