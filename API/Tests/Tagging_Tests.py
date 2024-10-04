# pip install pytest requests

# To run: pytest API\Tests\Tagging_Tests.py

import unittest
import requests

BASE_URL = 'http://localhost:5000/tag'  # The live API URL

class TagLiveEndpointTestCase(unittest.TestCase):
    
    def test_tag_endpoint_success(self):
        # Define payload for the request
        payload = {
            "auth_token": "XXX",
            "user_message": "Hola, que hora es?",
            "agent_message": "Son las 3 de la tarde.",
            "sentiment_tag": "pos"
        }

        # Make POST request to the live /tag endpoint
        response = requests.post(BASE_URL, json=payload)

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
            "auth_token": "XXX",
            "user_message": "Hola, que hora es?",
            "agent_message": "Son las 3 de la tarde.",
            "sentiment_tag": "invalid"  # Invalid sentiment_tag
        }

        # Make POST request to the live /tag endpoint
        response = requests.post(BASE_URL, json=payload)

        # Parse response data
        response_data = response.json()

        # Assertions
        assert response.status_code == 400
        assert response_data['success'] is False
        assert 'Estado inválido' in response_data['message']

    def test_tag_endpoint_missing_fields(self):
        # Define payload with missing fields
        payload = {
            "auth_token": "XXX",
            "user_message": "Hola, que hora es?",
            # Missing 'agent_message' and 'sentiment_tag'
        }

        # Make POST request to the live /tag endpoint
        response = requests.post(BASE_URL, json=payload)

        # Parse response data
        response_data = response.json()

        # Assertions
        assert response.status_code == 400
        assert response_data['success'] is False
        assert 'Faltan campos requeridos' in response_data['message']

    ''' # Only for testing purposes, Once the token validation is implemented
    def test_tag_endpoint_save_tag_failure(self):
        # Define payload with invalid data
        payload = {
            "auth_token": "INVALID_TOKEN",  # Simulate an invalid token
            "user_message": "Hola, que hora es?",
            "agent_message": "Son las 3 de la tarde.",
            "sentiment_tag": "pos"
        }

        # Make POST request to the live /tag endpoint
        response = requests.post(BASE_URL, json=payload)

        # Assertions - checking for failure (400 or 500)
        assert response.status_code in [400, 500]
        response_data = response.json()
        assert response_data['success'] is False
        # Optionally check for an error message, depending on the API response
    '''


if __name__ == '__main__':
    unittest.main()
