import streamlit as st
from PIL import Image
from io import BytesIO
from fpdf import FPDF
import os

# Título de la aplicación
st.title("Conversor de Imágenes a PDF")

# Entrada para el nombre del archivo
file_name = st.text_input("Introduce el nombre del archivo PDF (sin extensión):", "")

# Subida de imágenes
uploaded_files = st.file_uploader("Sube una o varias imágenes", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

if uploaded_files:
    images = []
    for uploaded_file in uploaded_files:
        image = Image.open(uploaded_file)
        images.append(image)

    if not file_name.strip():
        st.error("Por favor, introduce un nombre válido para el archivo.")
    else:
        # Crear el PDF
        pdf = FPDF()
        pdf.set_auto_page_break(0)

        for i, img in enumerate(images):
            if img.mode != "RGB":
                img = img.convert("RGB")
            
            temp_filename = f"temp_image_{i}.jpg"
            img.save(temp_filename)

            pdf.add_page()
            pdf.image(temp_filename, x=10, y=10, w=190)

            os.remove(temp_filename)

        # Guardar el PDF en un buffer
        pdf_buffer = BytesIO()
        pdf_content = pdf.output(dest='S').encode('latin1')
        pdf_buffer.write(pdf_content)
        pdf_buffer.seek(0)

        # Descargar el archivo PDF
        st.success("¡PDF generado exitosamente!")
        st.download_button(
            label="Descargar PDF",
            data=pdf_buffer,
            file_name=f"{file_name}.pdf",
            mime="application/pdf"
        )