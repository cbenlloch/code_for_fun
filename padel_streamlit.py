import streamlit as st
import pandas as pd

# Aplicar CSS para fijar el logo en la esquina superior derecha
st.markdown(
    """
    <style>
        .logo-container {
            position: fixed;
            top: 10px;
            right: 20px;
            z-index: 100;
        }
        .logo-container img {
            width: 120px; /* Ajusta el tamaño del logo */
        }
    </style>
    <div class="logo-container">
        st.sidebar.image("logo.png", width=120)
    </div>
    """,
    unsafe_allow_html=True
)
# Archivo donde se guardan los resultados
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

# Aplicar CSS para fondo gris en la barra lateral
st.markdown(
    """
    <style>
        [data-testid="stSidebar"] {
            background-color: #f0f0f0;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar con selector de copa
st.sidebar.title("🏆 Selección de Copa")
opcion_copa = st.sidebar.selectbox("Elige la copa:", ["Copa Enjoy", "Copa Energy"])

# Definir archivo según selección
DATA_FILE = DATA_FILE_ENJOY if opcion_copa == "Copa Enjoy" else DATA_FILE_ENERGY
df = cargar_datos(DATA_FILE)

# Mostrar parejas según la copa seleccionada
st.title(f"Torneo de Pádel - {opcion_copa}")
st.header("Parejas Participantes")
parejas = parejas_enjoy if opcion_copa == "Copa Enjoy" else parejas_energy

for letra, pareja in parejas.items():
    st.write(f"**Pareja {letra}:** {pareja}")

# Formulario para ingresar resultados
st.header(f"Subir Resultado - {opcion_copa}")
col1, col2, col3 = st.columns(3)
with col1:
    Pareja1 = st.text_input("Pareja 1")
with col2:
    Pareja2 = st.text_input("Pareja 2")
with col3:
    resultado = st.text_input("Resultado (Ej: 6-3, 4-6, 10-7)")

if st.button("Enviar"):
    if Pareja1 and Pareja2 and resultado:
        nuevo_resultado = pd.DataFrame([[Pareja1, Pareja2, resultado]], columns=df.columns)
        df = pd.concat([df, nuevo_resultado], ignore_index=True)
        df.to_csv(DATA_FILE, index=False)
        st.success("Resultado guardado!")
        st.rerun()
    else:
        st.error("Por favor, completa todos los campos.")

# Mostrar tabla con los resultados ingresados
st.header(f"Resultados - {opcion_copa}")
st.dataframe(df)
