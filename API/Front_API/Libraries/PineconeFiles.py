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
import requests
import io


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



# Pinecone management

# Listar los archivos existentes en Pinecone
def list_files_in_pinecone(api_key, base_url):
    response = requests.get(base_url, headers={"Api-Key": api_key})
    if response.status_code == 200:
        files = response.json().get('files', [])
        print(f"[FILE FETCH] Respuesta completa de la API: {files}")
        return files
    else:
        print(f"Error al listar archivos. Código de estado: {response.status_code}, Respuesta: {response.text}")
        return []

# Eliminar archivo por ID
def delete_file_from_pinecone(api_key, base_url, file_id):
    delete_url = f"{base_url}/{file_id}"
    response = requests.delete(delete_url, headers={"Api-Key": api_key})
    if response.status_code == 200:
        print(f"[DELETE FILE] Archivo {file_id} eliminado exitosamente.")
    else:
        print(f"Error al eliminar archivo {file_id}. Código de estado: {response.status_code}, Respuesta: {response.text}")

# Función para verificar si existe un archivo con el nombre dado y eliminarlo
def delete_file_by_name_if_exists(api_key, base_url, file_name):
    # Listar todos los archivos existentes en Pinecone
    files = list_files_in_pinecone(api_key, base_url)
    
    # Buscar el archivo por nombre
    for file_info in files:
        if isinstance(file_info, dict) and file_info.get('name') == file_name:
            file_id = file_info.get('id')
            if file_id:
                print(f"Archivo encontrado: {file_name} con ID: {file_id}. Procediendo a eliminarlo.")
                delete_file_from_pinecone(api_key, base_url, file_id)
                return True  # Archivo encontrado y eliminado
    print(f"No se encontró ningún archivo con el nombre: {file_name}.")
    return False  # Archivo no encontrado

# Función para subir un archivo con el nombre dado
def upload_file_to_pinecone(api_key, base_url, filepath, file_name):
    try:
        # Abre el archivo y prepara para la subida
        with open(filepath, 'r', encoding='utf-8') as file:
            temp_file = io.StringIO(file.read())
            temp_file.seek(0)
        
        # Subir el archivo a Pinecone
        response = requests.post(base_url, headers={"Api-Key": api_key}, files={"file": (file_name, temp_file)})
        
        if response.status_code == 200:
            print(f"[UPLOAD FILE] Archivo '{file_name}' subido exitosamente. Respuesta: {response.text}")
        else:
            print(f"Error al subir el archivo '{file_name}'. Código de estado: {response.status_code}, Respuesta: {response.text}")
        
        temp_file.close()
    except Exception as e:
        print(f"Error al intentar subir el archivo '{file_name}': {e}")


