import os
import json
from pymongo import MongoClient
from pymongo.errors import OperationFailure

# Programa auxiliar para conversion de Docx a JSON
import DocxToJson

def connect_to_mongodb(uri, database_name):
    client = MongoClient(uri)
    db = client[database_name]
    return db

def fetch_and_print_documents_in_collection(db_name, collection_name, mongo_uri):
    # Conectarse al servidor MongoDB
    client = MongoClient(mongo_uri)
    
    # Acceder a la base de datos
    db = client[db_name]
    
    # Acceder a la colección
    collection = db[collection_name]
    
    # Obtener todos los documentos de la colección
    documents = collection.find()
    
    # Imprimir los documentos
    for doc in documents:
        print(doc)

def create_or_access_database(uri, db_name):
    # Conectarse al servidor MongoDB
    client = MongoClient(uri)
    
    # Crear (o acceder a) la base de datos
    db = client[db_name]
    
    print(f"Base de datos '{db_name}' creada o accedida con éxito.")
    return db

def create_collection(db, collection_name):
    # Crear (o acceder a) la colección
    collection = db[collection_name]
    
    # Insertar un documento para asegurar que la colección sea creada
    if collection_name not in db.list_collection_names():
        collection.insert_one({"message": "Colección creada con éxito"})
    
    print(f"Colección '{collection_name}' creada o accedida con éxito.")
    return collection

def insert_json_files(db, folder_path, collection_name):
    """Insertar archivos JSON desde una carpeta a una colección en MongoDB."""

    # Obtener la ruta absoluta al script
    script_path = os.path.abspath(__file__)
    # Obtener el directorio del script
    script_dir = os.path.dirname(script_path)
    # Obtener la ruta absoluta a la carpeta
    full_path = os.path.join(script_dir, folder_path)

    # print("Ruta absoluta creada: ", full_path)

    # Acceder a la colección
    collection = db[collection_name]
    
    # Verificar si la carpeta existe
    if not os.path.isdir(full_path):
        print(f"La carpeta '{full_path}' no existe.")
        return

    print(f"Verificando archivos en: {full_path}")

    # Recorrer todos los archivos JSON en la carpeta
    for filename in os.listdir(full_path):
        if filename.endswith(".json"):
            file_path = os.path.join(full_path, filename)
            
            # Leer el archivo JSON
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    try:
                        data = json.load(file)
                        
                        print(f"Insertando documento '{filename}' en la colección '{collection_name}'")
                        
                        # Insertar el documento en la colección
                        collection.insert_one(data)
                    except json.JSONDecodeError as e:
                        print(f"Error al decodificar el archivo JSON '{file_path}': {e}")
                    except Exception as e:
                        print(f"Error al procesar el archivo JSON '{file_path}': {e}")
            except FileNotFoundError:
                print(f"Archivo '{file_path}' no encontrado.")
            except IOError as e:
                print(f"Error al abrir el archivo '{file_path}': {e}")

    print(f"----> Documentos insertados en la colección '{collection_name}' desde '{full_path}'.\n")


def main():
    
    # Obtener la URI de conexión desde variables de entorno
    mongo_uri = os.getenv('MONGO_URI')  # Si no se encuentra la variable de entorno, se construye la URI

    # Si la URI no se encuentra, se construye
    if not mongo_uri:
        print("URI de conexión no encontrada. Construyendo URI de conexión...")
        user = os.getenv('MONGO_USER', 'admin')  # Si no se encuentra la variable de entorno, se asigna 'admin'
        password = os.getenv('MONGO_PASS', 'admin123')  # Si no se encuentra la variable de entorno, se asigna 'admin123'
        host = os.getenv('MONGO_HOST', 'mongodb')  # 'mongodb' si se ejecuta en contenedor, 'localhost' si se ejecuta localmente
        mongo_uri = f"mongodb://{user}:{password}@{host}:27017"

    # Ahora mongo_uri contiene la URI de conexión

    # Conectarse a la base de datos
    db = connect_to_mongodb(mongo_uri, "ALIE_DB")


    # DOCUMENTOS JSON

    # Insertar documentos en las colecciones
    paths_and_collections = {
        "JSON/InformacionPrivada/Q&A": "InformacionPrivada_QA",
        "JSON/InformacionPrivada/General": "InformacionPrivada_General",
        "JSON/InformacionPublica/Q&A": "InformacionPublica_QA",
        "JSON/InformacionPublica/General": "InformacionPublica_General"
    }

    # Insertar todos los archivos JSON en las respectivas colecciones
    for relative_path, collection_name in paths_and_collections.items():
        insert_json_files(db, relative_path, collection_name)

    # Verificar el contenido de las colecciones
    '''
    print("<---> Verificacion del contenido de las colecciones")
    # Obtener todos los documentos de la colección y mostrarlos
    fetch_and_print_documents_in_collection("ALIE_DB", "InformacionPrivada_QA", mongo_uri)
    fetch_and_print_documents_in_collection("ALIE_DB", "InformacionPrivada_General", mongo_uri)
    fetch_and_print_documents_in_collection("ALIE_DB", "InformacionPublica_QA", mongo_uri)
    fetch_and_print_documents_in_collection("ALIE_DB", "InformacionPublica_General", mongo_uri)
    '''



    # SYLLABUS
    # Insertar Syllabus utilizando el programa auxiliar Docs_DB_Init/DocxToJson.py
    input_folder = "DOCX"  # Path a la carpeta que contiene los archivos .docx
    output_folder = "JSON/Syllabus"  # Path a la carpeta donde se guardarán los archivos JSON

    # Lista de palabras clave de sección a buscar
    section_keywords = [
        "Nombre Corto de la Asignatura",
        "Nombre Largo de la Asignatura",
        "Código de la asignatura",
        "Grado",
        "Descripción",
        "Número de Créditos",
        "Condiciones Académicas de Inscripción (Pre-requisitos)",
        "Período Académico de Vigencia",
        "Objetivos de Formación",
        "Resultados de Aprendizaje Esperados (RAE)",
        "Contenidos temáticos",
        "Estrategias Pedagógicas",
        "Evaluación",
        "Recursos Bibliográficos"
    ]
    
    # Procesar los archivos .docx para convertirlos en JSON
    DocxToJson.process_folder(input_folder, output_folder, section_keywords)
    # Insertar los archivos JSON generados a partir de los .docx en la base de datos
    syllabus_path_and_collection = {
        "JSON/Syllabus": "Syllabus"
    }
    # Insertar todos los archivos JSON en las respectivas colecciones
    for relative_path, collection_name in syllabus_path_and_collection.items():
        insert_json_files(db, relative_path, collection_name)
    # Verificar el contenido de la coleccion de syllabus
    '''
    print("<---> Verificacion del contenido de la colección de syllabus")
    # Obtener todos los documentos de la colección y mostrarlos
    fetch_and_print_documents_in_collection("ALIE_DB", "Syllabus", mongo_uri)
    '''

if __name__ == "__main__":
    main()