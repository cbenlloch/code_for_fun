import streamlit as st
import pandas as pd
import base64

# Función para convertir la imagen a base64 (para evitar problemas de carga)
def get_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Cargar el logo en base64
logo_base64 = get_base64("logo.png.png")

# Aplicar CSS para fijar el logo en la esquina superior derecha
st.markdown(
    f"""
    <style>
        .logo-container {{
            position: fixed;
            top: 10px;
            right: 20px;
            z-index: 100;
        }}
        .logo-container img {{
            width: 120px; /* Ajusta el tamaño del logo */
        }}
    </style>
    <div class="logo-container">
        <img src="data:image/png;base64,{logo_base64}">
    </div>
    """,
    unsafe_allow_html=True
)

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


