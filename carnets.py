import os
import zipfile
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import pandas as pd
import streamlit as st

def ajustar_texto(draw, texto, font, max_ancho):
    palabras = texto.split(" ")
    lineas = []
    linea_actual = ""

    for palabra in palabras:
        if draw.textlength(linea_actual + " " + palabra, font=font) <= max_ancho:
            linea_actual += " " + palabra if linea_actual else palabra
        else:
            lineas.append(linea_actual)
            linea_actual = palabra

    if linea_actual:
        lineas.append(linea_actual)

    return lineas


def crear_carnet(nombre, identidad, telefono, grupo, numero, numero_serie):
    ancho, alto = 400, 500

    try:
        fondo = Image.open("fondo.png")
        fondo = fondo.resize((ancho, alto))
        imagen = fondo.copy()
    except FileNotFoundError:
        imagen = Image.new('RGB', (ancho, alto), color=(255, 255, 255))
        draw = ImageDraw.Draw(imagen)
        draw.text((20, 30), "FONDO NO ENCONTRADO", font=ImageFont.truetype("arialbd.ttf", 18), fill=(255, 0, 0))
        return None

    draw = ImageDraw.Draw(imagen)
    font_texto = ImageFont.truetype("arialbd.ttf", 18)
    font_carnet = ImageFont.truetype("arialbd.ttf", 16)
    negro = (0, 0, 0)
    azul_marco = (0, 43, 111)

    try:
        logo = Image.open("logo.png")
        logo = logo.resize((400, 150))
        imagen.paste(logo, (0, 0))
    except FileNotFoundError:
        draw.text((20, 30), "LOGO NO ENCONTRADO", font=font_texto, fill=(255, 0, 0))

    draw.rectangle([0, 0, ancho - 1, alto - 1], outline=azul_marco, width=4)
    draw.rectangle([20, 150, ancho - 20, alto - 20], fill=(245, 245, 245))

    max_ancho_texto = ancho - 40
    lineas_nombre = ajustar_texto(draw, f"Nombre: {nombre}", font_texto, max_ancho_texto)

    y_offset = 170
    for linea in lineas_nombre:
        draw.text((30, y_offset), linea, font=font_texto, fill=negro)
        y_offset += 30

    draw.text((30, y_offset), f"ID: {identidad}", font=font_texto, fill=negro)
    draw.text((30, y_offset + 40), f"Teléfono: {telefono}", font=font_texto, fill=negro)
    draw.text((30, y_offset + 80), f"Grupo: {grupo}", font=font_texto, fill=negro)

    numero_serie_texto = str(int(numero_serie)) if isinstance(numero_serie, float) and numero_serie.is_integer() else str(numero_serie) if pd.notna(numero_serie) else "N/A"
    draw.text((30, y_offset + 120), f"Número de Serie: {numero_serie_texto}", font=font_texto, fill=negro)
    #draw.text((30, y_offset + 160), f"#Carnet {numero}", font=font_carnet, fill=negro)

    output = BytesIO()
    imagen.save(output, format='PNG')
    return output.getvalue()


st.title("Generador de Carnets")
st.subheader("¡Es hora de tejer tu propio destino!")

archivo_excel = st.file_uploader("Sube un archivo Excel", type=["xlsx"])

if archivo_excel:
    try:
        df = pd.read_excel(archivo_excel)
    except Exception as e:
        st.error(f"Error al leer el archivo Excel: {e}")
    else:
        columnas_requeridas = {'Nombre', 'Identidad', 'Teléfono', 'Grupo', 'Numero_Serie'}
        if not columnas_requeridas.issubset(df.columns):
            st.error(f"El archivo Excel debe contener las columnas: {', '.join(columnas_requeridas)}")
        else:
            st.success("Archivo Excel cargado correctamente.")
            if st.button("Generar Carnets"):
                zip_buffer = BytesIO()
                with zipfile.ZipFile(zip_buffer, "w") as zip_file:
                    for i, row in df.iterrows():
                        contenido_carnet = crear_carnet(
                            row['Nombre'], 
                            row['Identidad'], 
                            row['Teléfono'], 
                            row['Grupo'], 
                            i + 1, 
                            row['Numero_Serie']
                        )
                        if contenido_carnet:
                            zip_file.writestr(f"carnet_{i+1}_{row['Teléfono']}.png", contenido_carnet)

                zip_buffer.seek(0)
                st.download_button(
                    label="Descargar Carnets",
                    data=zip_buffer,
                    file_name="carnets_generados.zip",
                    mime="application/zip"
                )

