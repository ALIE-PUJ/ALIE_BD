from flask import Flask, request, jsonify, send_file
from flask_cors import CORS, cross_origin # CORS for angular
import psycopg2
from io import BytesIO

# Inicializacion de Flask
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["*"]}}) # Habilita CORS para la APP Flask. Necesario para que funcione adecuadamente con Angular

# Importe de librerías propias
from Libraries.DeepTranslator_Translate import *
from Libraries.Tagging import *



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
@app.route('/tag', methods=['POST'])
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
    
@app.route('/files/submit', methods=['POST'])
def submit_file():
    data = request.form
    file = request.files.get('file')
    categoria = data.get('categoria')

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

        return jsonify(success=True), 200
    except Exception as e:
        connection.rollback()
        print(f"Error: {e}")
        return jsonify(success=False, message="Error al guardar el archivo"), 500


@app.route('/files/list', methods=['GET'])
def list_files():
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT nombre, categoria FROM Archivo")
            files = cursor.fetchall()

        file_list = [{'name': file[0], 'category': file[1]} for file in files]
        return jsonify(success=True, files=file_list), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify(success=False, message="Error al obtener los archivos"), 500

@app.route('/files/delete', methods=['DELETE'])
def delete_file():
    file_name = request.args.get('name')
    
    if not file_name:
        return jsonify(success=False, message="Falta el nombre del archivo"), 400
    
    try:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM Archivo WHERE nombre = %s", (file_name,))
            rows_deleted = cursor.rowcount
            connection.commit()

        if rows_deleted > 0:
            return jsonify(success=True), 200
        else:
            return jsonify(success=False, message="Archivo no encontrado"), 404
    except Exception as e:
        connection.rollback()
        print(f"Error: {e}")
        return jsonify(success=False, message="Error al eliminar el archivo"), 500


@app.route('/files/view', methods=['GET'])
def view_file():
    file_name = request.args.get('name')

    if not file_name:
        return jsonify(success=False, message="Falta el nombre del archivo"), 400

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT archivo FROM Archivo WHERE nombre = %s", (file_name,))
            archivo = cursor.fetchone()

        if archivo:
            pdf_data = archivo[0]

            # Usar el encabezado adecuado para visualización en el navegador
            return send_file(BytesIO(pdf_data), 
                             download_name=file_name, 
                             as_attachment=False, 
                             mimetype='application/pdf')
        else:
            return jsonify(success=False, message="Archivo no encontrado"), 404
    except Exception as e:
        print(f"Error: {e}")
        return jsonify(success=False, message="Error al obtener el archivo"), 500

# Main runner
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)