from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin # CORS for angular

# Inicializacion de Flask
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["*"]}}) # Habilita CORS para la APP Flask. Necesario para que funcione adecuadamente con Angular

# Importe de librerías propias
from Libraries.DeepTranslator_Translate import *
from Libraries.Tagging import *



# ENDPOINTS

# /tag
# Example payload: 
'''
{
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
    if not all(key in data for key in ('user_message', 'agent_message', 'sentiment_tag')):
        return jsonify(success=False, message="Faltan campos requeridos"), 400

    user_message = data['user_message']
    agent_message = data['agent_message']
    sentiment_tag = data['sentiment_tag']

    # Print payload
    print("/tag payload. user_message: {}, agent_message: {}, sentiment_tag: {}".format(user_message, agent_message, sentiment_tag))

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
    


# Main runner
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)