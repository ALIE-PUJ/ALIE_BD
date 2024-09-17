from flask import Flask, request, jsonify

# Inicializacion de Flask
app = Flask(__name__)

# ENDPOINTS

# /tag
# Example payload: 
'''
{
    "user_message": "¿Qué hora es?",
    "agent_message": "Son las 3 de la tarde.",
    "state": "pos"
}
'''
@app.route('/tag', methods=['POST'])
def tag():
    # Obtén los datos del cuerpo de la solicitud
    data = request.json

    # Verifica que todos los campos necesarios estén presentes
    if not all(key in data for key in ('user_message', 'agent_message', 'state')):
        return jsonify(success=False, message="Faltan campos requeridos"), 400

    user_message = data['user_message']
    agent_message = data['agent_message']
    state = data['state']

    # Print payload
    print("/tag payload. user_message: {}, agent_message: {}, state: {}".format(user_message, agent_message, state))

    # Verifica que el estado sea 'pos' o 'neg'
    if state not in ('pos', 'neg'):
        return jsonify(success=False, message="Estado inválido"), 400

    # Logica de negocio (Tagging)
    # TO-DO
    
    return jsonify(success=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
