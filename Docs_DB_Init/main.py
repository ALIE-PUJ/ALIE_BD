import os
from pymongo import MongoClient
from pymongo.errors import OperationFailure

def connect_to_mongodb(uri, database_name, collection_name):
    try:
        # Conectarse al servidor MongoDB
        client = MongoClient(uri)
        
        # Acceder a la base de datos específica
        db = client[database_name]
        
        # Acceder a la colección específica
        collection = db[collection_name]
        
        return collection
    except OperationFailure as e:
        print(f"Error de autenticación: {e}")
        return None

def fetch_all_documents_in_collection(db, collection_name):
    # Acceder a la colección utilizando el nombre proporcionado
    collection = db[collection_name]
    
    # Verificar si la colección existe
    if collection_name not in db.list_collection_names():
        print(f"La colección '{collection_name}' no existe en la base de datos.")
        return []
    
    # Obtener todos los documentos de la colección
    documents = collection.find()
    
    return list(documents)


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


if __name__ == "__main__":

    # Obtener usuario y contraseña desde variables de entorno
    user = os.getenv('MONGO_USER', 'admin') # Si no se encuentra la variable de entorno, se asigna el valor 'admin'
    password = os.getenv('MONGO_PASS', 'admin123') # Si no se encuentra la variable de entorno, se asigna el valor 'admin123'
    
    # Construir la URI de conexión
    mongo_uri = f"mongodb://{user}:{password}@localhost:27017"
    
    # Nombre de la base de datos y colección
    db_name = "admin"
    collection_name = "system.users"
    
    # Crear la base de datos
    db = create_or_access_database(mongo_uri, db_name)
    
    # Obtener todos los documentos de la colección
    documents = fetch_all_documents_in_collection(db, collection_name)
    
    # Imprimir los documentos
    for doc in documents:
        print(doc)
