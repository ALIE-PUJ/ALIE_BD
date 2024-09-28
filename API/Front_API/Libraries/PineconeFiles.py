from flask import Flask, request, jsonify, send_file
from flask_cors import CORS, cross_origin # CORS for angular
import psycopg2
from io import BytesIO
import uuid
import os

# File export dependencies
import json
import PyPDF2
from io import BytesIO

# Pinecone Dependencies




# Database connection
# Busca la variable de entorno USER; si no existe, asigna "root"
userDB = os.getenv('COCKROACHDB_USER', 'root')
# Busca la variable de entorno PASS; si no existe, asigna una cadena vacía
passw = os.getenv('COCKROACHDB_PASS', 'pass')
# Busca la variable de entorno HOST; si no existe, asigna postgres
cdb_host = os.getenv('COCKROACHDB_HOST', 'localhost')
# Busca el puerto en la variable de entorno
cdb_port = os.getenv('COCKROACHDB_PORT', 5432)
# Conexion
connection = psycopg2.connect(
    host=cdb_host, # docker-compose service name. Use localhost to run locally
    port=cdb_port,
    user=userDB,
    password=passw,
    database='alie_db' # lowercase
)


# File exports to Pinecone

file_name = 'archivosSubidos_compiled.json'

def export_files_to_json():
    try:
        # Abrir conexión con la base de datos
        with connection.cursor() as cursor:
            # Obtener todos los archivos de la base de datos
            cursor.execute("SELECT nombre, categoria, archivo FROM Archivo")
            files = cursor.fetchall()

        # Crear una lista para almacenar cada archivo como un diccionario
        json_data = []
        
        for file in files:
            nombre, categoria, archivo_binario = file
            try:
                # Leer el contenido del PDF usando PyPDF2
                pdf_reader = PyPDF2.PdfReader(BytesIO(archivo_binario))
                text = ""
                for page in range(len(pdf_reader.pages)):
                    text += pdf_reader.pages[page].extract_text()

                # Crear una estructura de diccionario para el archivo
                json_data.append({
                    'name': nombre,
                    'category': categoria,
                    'content': text
                })
            except Exception as e:
                print(f"Error al leer el archivo {nombre}: {e}")
                continue  # Si hay un error con un archivo, saltamos al siguiente archivo

        # Obtener la ruta absoluta del directorio donde está el archivo .py
        script_dir = os.path.dirname(os.path.abspath(__file__))

        # Crear la ruta completa para el archivo JSON en ese directorio
        json_file_path = os.path.join(script_dir, file_name)

        # Guardar el archivo JSON en el sistema de archivos
        with open(json_file_path, 'w', encoding='utf-8') as json_file:
            json.dump(json_data, json_file, ensure_ascii=False, indent=4)

        print(f"Exportación completada. Archivo JSON guardado en: {json_file_path}")
    except Exception as e:
        print(f"Error: {e}")







export_files_to_json()
