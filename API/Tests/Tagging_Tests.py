# pip install pytest requests

# To run: pytest API\Tests\Tagging_Tests.py

import unittest
import requests

# Auth Headers
from Others.Auth_Token_Getter import *
headers = {} # Encabezados de la solicitud. Vacío por ahora

BASE_URL = 'http://localhost:5000/api/front/tag'  # The live API URL

class TagLiveEndpointTestCase(unittest.TestCase):
    
    def test_tag_endpoint_success(self):
        # Define payload for the request
        payload = {
            "user_message": "Hola, que hora es?",
            "agent_message": "Son las 3 de la tarde.",
            "sentiment_tag": "pos"
        }

        # Make POST request to the live /tag endpoint
        response = requests.post(BASE_URL, json=payload, headers=headers)

        # Assertions
        assert response.status_code == 200
        response_data = response.json()
        assert response_data['success'] is True
        assert 'Documento guardado correctamente' in response_data['message']
        
        # Check the tag_document structure and fields
        tag_document = response_data['tag_document']
        assert tag_document['user_prompt'] == 'Hola, que hora es?'  # Updated from 'user_message'
        assert tag_document['agent_response'] == 'Son las 3 de la tarde.'  # Updated from 'agent_message'
        assert tag_document['sentiment_tag'] == 'pos'
        assert tag_document['language'] == 'es'  # Check that the language detection worked
    
    def test_tag_endpoint_invalid_tag(self):
        # Define payload with invalid sentiment_tag
        payload = {
            "user_message": "Hola, que hora es?",
            "agent_message": "Son las 3 de la tarde.",
            "sentiment_tag": "invalid"  # Invalid sentiment_tag
        }

        # Make POST request to the live /tag endpoint
        response = requests.post(BASE_URL, json=payload, headers=headers)

        # Parse response data
        response_data = response.json()

        # Assertions
        assert response.status_code == 400
        assert response_data['success'] is False
        assert 'Estado inválido' in response_data['message']

    def test_tag_endpoint_missing_fields(self):
        # Define payload with missing fields
        payload = {
            "user_message": "Hola, que hora es?",
            # Missing 'agent_message' and 'sentiment_tag'
        }

        # Make POST request to the live /tag endpoint
        response = requests.post(BASE_URL, json=payload, headers=headers)

        # Parse response data
        response_data = response.json()

        # Assertions
        assert response.status_code == 400
        assert response_data['success'] is False
        assert 'Faltan campos requeridos' in response_data['message']

    def test_tag_endpoint_save_tag_failure(self):
        # Define payload with invalid data
        payload = {
            "user_message": "Hola, que hora es?",
            "agent_message": "Son las 3 de la tarde.",
            "sentiment_tag": "pos"
        }

        # Create a new header without the auth_token, but an invalid token
        invalid_token = "invalid_token"
        headers_specific = {
            'Authorization': f'Bearer {invalid_token}',  # Agregar "Bearer" antes del token
            'accept': 'application/json'
        }

        # Make POST request to the live /tag endpoint
        response = requests.post(BASE_URL, json=payload, headers=headers_specific)

        # Assertions - checking for failure (400 or 500)
        assert response.status_code == 401
        response_data = response.json()
        assert response_data['success'] is False
        assert 'Token de autorización inválido o faltante' in response_data['message']


if __name__ == '__main__':

    headers = login_and_get_header() # Get the auth header
    unittest.main()
