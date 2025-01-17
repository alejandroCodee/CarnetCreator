import os
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import pandas as pd
import streamlit as st

# Función para crear un carnet
def crear_carnet(nombre, identidad, telefono, grupo, numero):
    ancho, alto = 400, 600
    imagen = Image.new('RGB', (ancho, alto), color=(255, 255, 255))
    draw = ImageDraw.Draw(imagen)

    # Agregar texto
    font_titulo = ImageFont.truetype("arial.ttf", 30)
    font_texto = ImageFont.truetype("arial.ttf", 20)
    draw.text((50, 50), "HILANDO OPORTUNIDADES", font=font_titulo, fill="blue")
    draw.text((50, 150), f"Nombre: {nombre}", font=font_texto, fill="black")
    draw.text((50, 200), f"ID: {identidad}", font=font_texto, fill="black")
    draw.text((50, 250), f"Teléfono: {telefono}", font=font_texto, fill="black")
    draw.text((50, 300), f"Grupo: {grupo}", font=font_texto, fill="black")
    draw.text((50, 350), f"BP-{numero}", font=font_texto, fill="black")

    # Generar un nombre único para el archivo
    ruta_carpeta = "carnets_generados"
    if not os.path.exists(ruta_carpeta):
        os.makedirs(ruta_carpeta)
    ruta_carnet = os.path.join(ruta_carpeta, f"carnet_{numero}.png")
    imagen.save(ruta_carnet)

    return ruta_carnet

# Configurar la aplicación de Streamlit
st.title("Generador de Carnets")

st.write("""
Sube un archivo Excel con las columnas **Nombre**, **Identidad**, **Teléfono**, y **Grupo**.
El sistema generará un carnet para cada persona y los guardará en una carpeta.
""")

# Subir archivo
archivo_excel = st.file_uploader("Sube un archivo Excel", type=["xlsx"])

if archivo_excel:
    # Leer el archivo Excel
    try:
        df = pd.read_excel(archivo_excel)
    except Exception as e:
        st.error(f"Error al leer el archivo Excel: {e}")
    else:
        # Validar columnas
        columnas_requeridas = {'Nombre', 'Identidad', 'Teléfono', 'Grupo'}
        if not columnas_requeridas.issubset(df.columns):
            st.error(f"El archivo Excel debe contener las columnas: {', '.join(columnas_requeridas)}")
        else:
            st.success("Archivo Excel cargado correctamente.")
            if st.button("Generar Carnets"):
                # Generar carnets
                for i, row in df.iterrows():
                    nombre = row['Nombre']
                    identidad = row['Identidad']
                    telefono = row['Teléfono']
                    grupo = row['Grupo']
                    crear_carnet(nombre, identidad, telefono, grupo, i + 1)
                st.success("¡Carnets generados exitosamente!")
                st.write("Los carnets se han guardado en la carpeta **carnets_generados**.")
