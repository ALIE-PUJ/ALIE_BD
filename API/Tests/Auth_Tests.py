# pip install pytest requests

# To run: pytest API\Tests\Auth_Tests.py

import unittest
import requests

# Auth Headers
from Others.Auth_Token_Getter import *
headers = {} # Encabezados de la solicitud. Vacío por ahora

BASE_URL = 'http://localhost:2000'  # La URL de la API

class VerifyTokenTestCase(unittest.TestCase):

    def test_verify_token_success(self):

        # Hacer la solicitud POST al endpoint /verify
        response = requests.post(f'{BASE_URL}/verify', headers=headers)

        # Imprimir la respuesta
        print(f"Response Status Code (Valid Token): {response.status_code}")
        print(f"Response Body (Valid Token): {response.text}")

        # Aserciones
        assert response.status_code == 200
        response_data = response.json()
        assert 'id_usuario' in response_data  # Verificar si el ID de usuario está en la respuesta
        assert 'usuario' in response_data  # Verificar si el nombre de usuario está en la respuesta
        assert response_data['usuario'] == "Luis Bravo"  # Ajustar esto según el nombre de usuario esperado

    def test_verify_token_failure(self):
        # Token inválido
        invalid_token = "invalid_token"

        headers_specific = {
            'Authorization': f'Bearer {invalid_token}',  # Agregar "Bearer" antes del token
            'accept': 'application/json'
        }

        # Hacer la solicitud POST al endpoint /verify
        response = requests.post(f'{BASE_URL}/verify', headers=headers_specific)

        # Imprimir la respuesta
        print(f"Response Status Code (Invalid Token): {response.status_code}")
        print(f"Response Body (Invalid Token): {response.text}")

        # Aserciones
        assert response.status_code == 401
        if response.content:  # Comprobar si el contenido de la respuesta no está vacío
            try:
                response_data = response.json()
                print("Response data = ", response_data)
                assert 'error' in response_data
                assert response_data['error'] == "Unauthorized"  # Verificar que el mensaje de error sea el esperado
            except ValueError: # JSON Vacio
                print("Error decoding JSON from response")
                print(response.text)  # Imprimir el contenido de la respuesta en caso de error

if __name__ == '__main__':

    headers = login_and_get_header() # Get the auth header
    unittest.main()
