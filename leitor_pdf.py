# -*- coding: utf-8 -*-
"""Leitor_pdf

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1tDXUFMBifzOS1FYU6Tr9pH0ivKa3j3aW
"""

!apt-get install tesseract-ocr -y
!pip install pytesseract
!apt-get install poppler-utils -y
!pip install pdf2image

import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import os

def extract_text_from_pdf(pdf_path):
    """Extrai texto de um arquivo PDF usando OCR."""
    images = convert_from_path(pdf_path)
    text = "\n".join(pytesseract.image_to_string(img) for img in images)
    return text

def extract_text_from_image(image_path):
    """Extrai texto de um arquivo de imagem (PNG, JPG, etc.) usando OCR."""
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img)
    return text

def main():
    file_path = input("Digite o caminho do arquivo (PDF ou PNG): ")

    if not os.path.exists(file_path):
        print("Arquivo não encontrado!")
        return

    if file_path.lower().endswith(".pdf"):
        text = extract_text_from_pdf(file_path)
    elif file_path.lower().endswith(('.png', '.jpg', '.jpeg')):
        text = extract_text_from_image(file_path)
    else:
        print("Formato não suportado! Use PDF ou PNG/JPG.")
        return

    print("\nTexto extraído:\n")
    print(text)

    # Salvar o texto em um arquivo .txt
    output_file = file_path + ".txt"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"Texto salvo em: {output_file}")

if __name__ == "__main__":
    main()