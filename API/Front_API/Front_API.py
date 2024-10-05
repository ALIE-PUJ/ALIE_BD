from flask import Flask, request, jsonify, send_file
from flask_cors import CORS, cross_origin # CORS for angular
import psycopg2
from io import BytesIO
import uuid
import os
import time
import threading

# Esperar a que la base de datos esté lista
print("Esperando a que la base de datos esté lista... 5 segundos")
time.sleep(5)

# Inicializacion de Flask
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["*"]}}) # Habilita CORS para la APP Flask. Necesario para que funcione adecuadamente con Angular

# Importe de librerías propias
from Libraries.DeepTranslator_Translate import *
from Libraries.Tagging import *
from Libraries.PineconeFiles import *



# Database connection
# Busca la variable de entorno USER; si no existe, asigna "root"
userDB = os.getenv('COCKROACHDB_USER', 'root')
# Busca la variable de entorno PASS; si no existe, asigna una cadena vacía
passw = os.getenv('COCKROACHDB_PASS', 'pass')
# Busca la variable de entorno HOST; si no existe, asigna postgres
cdb_host = os.getenv('COCKROACHDB_HOST', 'postgres')
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





# ENDPOINTS



# Tagging

# /tag
# Example payload: 
'''
{
    "auth_token": "XXX",
    "user_message": "Hola, que hora es?",
    "agent_message": "Son las 3 de la tarde.",
    "sentiment_tag": "pos"
}
'''
@app.route('/api/front/tag', methods=['POST'])
def tag():
    # Obtén los datos del cuerpo de la solicitud
    data = request.json

    # Verifica que todos los campos necesarios estén presentes
    if not all(key in data for key in ('auth_token', 'user_message', 'agent_message', 'sentiment_tag')):
        return jsonify(success=False, message="Faltan campos requeridos"), 400

    auth_token = data['auth_token']
    user_message = data['user_message']
    agent_message = data['agent_message']
    sentiment_tag = data['sentiment_tag']

    # Print payload
    print("/tag payload. auth_token: {}, user_message: {}, agent_message: {}, sentiment_tag: {}".format(auth_token, user_message, agent_message, sentiment_tag))

    # Verifica que el estado sea 'pos' o 'neg'
    if sentiment_tag not in ('pos', 'neg'):
        return jsonify(success=False, message="Estado inválido"), 400

    # Logica de negocio (Tagging)
    user_language = detect_language(user_message) # Detecta el idioma del mensaje del usuario

    tag_document = save_tag_to_mongo(user_message, agent_message, sentiment_tag, user_language)

    if tag_document is None:
        return jsonify(success=False, message="Error al guardar el documento en MongoDB"), 500
    else:
        return jsonify(success=True, message="Documento guardado correctamente", tag_document=tag_document)
    




# Files

@app.route('/api/front/files/submit', methods=['POST'])
def submit_file():
    data = request.form
    file = request.files.get('file')
    categoria = data.get('categoria')
    auth_token = data.get('auth_token')

    if not auth_token:
        return jsonify(success=False, message="Falta el token de autenticación"), 401

    if not categoria or not file:
        return jsonify(success=False, message="Faltan campos requeridos"), 400

    if not file.filename.lower().endswith('.pdf'):
        return jsonify(success=False, message="El archivo debe ser un PDF"), 400

    try:
        archivo_binario = file.read()
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO Archivo (nombre, categoria, archivo)
                VALUES (%s, %s, %s)
            """, (file.filename, categoria, archivo_binario))
            connection.commit()

            # Actualizar pinecone en un hilo
            print("Actualizando Pinecone en un hilo...")
            threading.Thread(target=export_and_upload_to_pinecone, args=()).start()
            
        return jsonify(success=True), 200
    except Exception as e:
        connection.rollback()
        print(f"Error: {e}")
        return jsonify(success=False, message="Error al guardar el archivo"), 500

@app.route('/api/front/files/list', methods=['GET'])
def list_files():
    auth_token = request.args.get('auth_token')
    if not auth_token:
        return jsonify(success=False, message="Falta el token de autenticación"), 401

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT nombre, categoria FROM Archivo")
            files = cursor.fetchall()

        file_list = [{'name': file[0], 'category': file[1]} for file in files]
        return jsonify(success=True, files=file_list), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify(success=False, message="Error al obtener los archivos"), 500

@app.route('/api/front/files/delete', methods=['DELETE'])
def delete_file():
    file_name = request.args.get('name')
    auth_token = request.args.get('auth_token')
    if not auth_token:
        return jsonify(success=False, message="Falta el token de autenticación"), 401
    if not file_name:
        return jsonify(success=False, message="Falta el nombre del archivo"), 400

    try:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM Archivo WHERE nombre = %s", (file_name,))
            rows_deleted = cursor.rowcount
            connection.commit()

            # Actualizar pinecone en un hilo
            print("Actualizando Pinecone en un hilo...")
            threading.Thread(target=export_and_upload_to_pinecone, args=()).start()


        if rows_deleted > 0:
            return jsonify(success=True), 200
        else:
            return jsonify(success=False, message="Archivo no encontrado"), 404
    except Exception as e:
        connection.rollback()
        print(f"Error: {e}")
        return jsonify(success=False, message="Error al eliminar el archivo"), 500

@app.route('/api/front/files/view', methods=['GET'])
def view_file():
    file_name = request.args.get('name')
    auth_token = request.args.get('auth_token')
    if not auth_token:
        return jsonify(success=False, message="Falta el token de autenticación"), 401
    if not file_name:
        return jsonify(success=False, message="Falta el nombre del archivo"), 400

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT archivo FROM Archivo WHERE nombre = %s", (file_name,))
            archivo = cursor.fetchone()

        if archivo:
            pdf_data = archivo[0]
            return send_file(BytesIO(pdf_data), 
                             download_name=file_name, 
                             as_attachment=False, 
                             mimetype='application/pdf')
        else:
            return jsonify(success=False, message="Archivo no encontrado"), 404
    except Exception as e:
        print(f"Error: {e}")
        return jsonify(success=False, message="Error al obtener el archivo"), 500





# Chats

@app.route('/api/front/chat/guardar', methods=['POST'])
def guardar_chat():
    data = request.get_json()

    if not all(key in data for key in ('auth_token', 'mensajes_agente', 'mensajes_usuario', 'mensajes_supervision', 'user_id')):
        return jsonify(success=False, message="Faltan campos requeridos"), 400

    auth_token = data['auth_token']
    nombre = data.get('nombre')  # El nombre puede estar presente o no
    mensajes_agente = data['mensajes_agente']
    mensajes_usuario = data['mensajes_usuario']
    mensajes_supervision = data['mensajes_supervision']
    user_id = data['user_id']
    intervenido = data.get('intervenido', False)  # Nuevo campo para indicar intervención

    # Generar un memory_key único si no se proporciona
    memory_key = data.get('memory_key', str(uuid.uuid4()))

    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Chat WHERE memory_key = %s", (memory_key,))
        chat = cursor.fetchone()

        if chat:
            # Si el chat existe, actualizamos los campos
            query = """
                UPDATE Chat 
                SET mensajes_agente = array_cat(mensajes_agente, %s), 
                    mensajes_usuario = array_cat(mensajes_usuario, %s),
                    mensajes_supervision = array_cat(mensajes_supervision, %s),
                    intervenido = %s
            """
            if nombre:
                query += ", nombre = %s"
                query += " WHERE memory_key = %s"
                cursor.execute(query, (mensajes_agente, mensajes_usuario, mensajes_supervision, intervenido, nombre, memory_key))
            else:
                query += " WHERE memory_key = %s"
                cursor.execute(query, (mensajes_agente, mensajes_usuario, mensajes_supervision, intervenido, memory_key))

        else:
            # Nuevo chat
            if not nombre:
                cursor.execute("SELECT COUNT(*) FROM Chat")
                chat_count = cursor.fetchone()[0] + 1
                nombre = f'Chat {chat_count}'  

            query = """
                INSERT INTO Chat (memory_key, nombre, mensajes_agente, mensajes_usuario, mensajes_supervision, user_id, archivado, intervenido)
                VALUES (%s, %s, %s, %s, %s, %s, FALSE, %s)
            """
            cursor.execute(query, (memory_key, nombre, mensajes_agente, mensajes_usuario, mensajes_supervision, user_id, intervenido))

        connection.commit()
        cursor.close()
        return jsonify(success=True, memory_key=memory_key, nombre=nombre)
    except Exception as e:
        print(e)
        return jsonify(success=False, message="Error en el servidor")




@app.route('/api/front/chat/get', methods=['POST'])
def get_chat():
    data = request.get_json()

    if not all(key in data for key in ('auth_token', 'memory_key')):
        return jsonify(success=False, message="Faltan campos requeridos"), 400

    auth_token = data['auth_token']
    memory_key = data['memory_key']

    try:
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM Chat WHERE memory_key = %s", (memory_key,))
        chat = cursor.fetchone()
        cursor.close()

        if chat:
            return jsonify({
                'memory_key': chat[0],
                'nombre': chat[1],
                'mensajes_agente': chat[2],
                'mensajes_usuario': chat[3],
                'mensajes_supervision': chat[4],
                'archivado': chat[5],
                'intervenido': chat[6],  # Return intervention status
                'success': True
            })
        else:
            return jsonify(success=False, message="Chat no encontrado"), 404
    except Exception as e:
        print(e)
        return jsonify(success=False, message="Error en el servidor")


@app.route('/api/front/chat/list_intervention', methods=['POST'])
def list_intervention_chats():
    data = request.get_json()

    if 'auth_token' not in data:
        return jsonify(success=False, message="Faltan campos requeridos"), 400

    auth_token = data['auth_token']

    try:
        cursor = connection.cursor()
        # Filter for only the chats marked as intervenido
        cursor.execute("SELECT memory_key, nombre FROM Chat WHERE intervenido = TRUE")
        chats = cursor.fetchall()
        cursor.close()

        chat_list = [{'memory_key': chat[0], 'nombre': chat[1]} for chat in chats]
        return jsonify(chat_list)
    except Exception as e:
        print(e)
        return jsonify(success=False)



@app.route('/api/front/chat/list', methods=['POST'])
def list_chats_by_user():
    data = request.get_json()


    if not all(key in data for key in ('auth_token', 'user_id')):
        return jsonify(success=False, message="Faltan campos requeridos"), 400

    auth_token = data['auth_token']
    user_id = data['user_id']

    try:
        cursor = connection.cursor()
        cursor.execute("SELECT memory_key, nombre FROM Chat WHERE user_id = %s", (user_id,))
        chats = cursor.fetchall()
        cursor.close()

        chat_list = [{'memory_key': chat[0], 'nombre': chat[1]} for chat in chats]
        return jsonify(chat_list)
    except Exception as e:
        print(e)
        return jsonify(success=False)


@app.route('/api/front/chat/list_all', methods=['POST'])
def list_all_chats():
    data = request.get_json()

    if 'auth_token' not in data:
        return jsonify(success=False, message="Faltan campos requeridos"), 400

    auth_token = data['auth_token']

    try:
        cursor = connection.cursor()
        cursor.execute("SELECT memory_key, nombre, intervenido FROM Chat")
        chats = cursor.fetchall()
        cursor.close()

       
        chat_list = [{'memory_key': chat[0], 'nombre': chat[1], 'intervenido': chat[2]} for chat in chats]
        return jsonify(chat_list)
    except Exception as e:
        print(e)
        return jsonify(success=False)


@app.route('/api/front/chat/delete', methods=['POST'])
def delete_chat():
    data = request.get_json()

    if not all(key in data for key in ('auth_token', 'memory_key')):
        return jsonify(success=False, message="Faltan campos requeridos"), 400

    auth_token = data['auth_token']
    memory_key = data['memory_key']

    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM Chat WHERE memory_key = %s", (memory_key,))
        connection.commit()
        cursor.close()

        if cursor.rowcount > 0:
            return jsonify(success=True)
        else:
            return jsonify(success=False, message="Chat no encontrado"), 404
    except Exception as e:
        print(e)
        return jsonify(success=False)

@app.route('/api/front/chat/archive', methods=['POST'])
def archive_chat():
    data = request.get_json()

    if not all(key in data for key in ('auth_token', 'memory_key')):
        return jsonify(success=False, message="Faltan campos requeridos"), 400

    auth_token = data['auth_token']
    memory_key = data['memory_key']

    try:
        cursor = connection.cursor()
        cursor.execute("UPDATE Chat SET archivado = TRUE WHERE memory_key = %s", (memory_key,))
        connection.commit()
        cursor.close()

        if cursor.rowcount > 0:
            return jsonify(success=True)
        else:
            return jsonify(success=False, message="Chat no encontrado"), 404
    except Exception as e:
        print(e)
        return jsonify(success=False)


@app.route('/api/front/chat/update_intervention', methods=['POST'])
def update_intervention_status():
    data = request.get_json()

    if not all(key in data for key in ('auth_token', 'memory_key', 'intervenido')):
        return jsonify(success=False, message="Faltan campos requeridos"), 400

    auth_token = data['auth_token']
    memory_key = data['memory_key']
    intervenido = data['intervenido']  

    try:
        cursor = connection.cursor()
        query = "UPDATE Chat SET intervenido = %s WHERE memory_key = %s"
        cursor.execute(query, (intervenido, memory_key))
        connection.commit()
        cursor.close()

        return jsonify(success=True)
    except Exception as e:
        print(e)
        return jsonify(success=False, message="Error en el servidor")


# Main runner
if __name__ == '__main__':
    # Actualizar pinecone en un hilo
    print("Actualizando Pinecone en un hilo...")
    threading.Thread(target=export_and_upload_to_pinecone, args=()).start()

    # Iniciar la aplicación flask
    app.run(host='0.0.0.0', port=5000)