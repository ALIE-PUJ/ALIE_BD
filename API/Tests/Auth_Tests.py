# pip install pytest requests

# To run: pytest API\Tests\Auth_Tests.py

import unittest
import requests

BASE_URL = 'http://localhost:2000'  # La URL de la API

class VerifyTokenTestCase(unittest.TestCase):

    def test_verify_token_success(self):
        # Token válido (Ejemplo de token valido. Recuerde que cambia constantemente. Debe obtener un token valido de la API. Puede hacerlo en http://localhost:2001/swagger/#/default/post_login)
        valid_token = "eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJpZF91c3VhcmlvIjoxLCJ1c3VhcmlvIjoiTHVpcyBCcmF2byIsImVtYWlsIjoibHVpcy5icmF2b0BqYXZlcmlhbmEuZWR1LmNvbSIsImlkX2NhdGVnb3JpYSI6MiwiaWF0IjoxNzI4MTA4ODIyLCJleHAiOjE3MjgxMTI0MjJ9.buFGZ9yxtycUY9WHTHmMdjDtSbLFVkNQtgxNbs5hBNsK4VPwTKB0TmizM9cm-JdBXWrdLIfAmxbMPZVPipkXdg"
        
        headers = {
            'Authorization': f'Bearer {valid_token}',  # Agregar "Bearer" antes del token
            'accept': 'application/json'
        }

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

        headers = {
            'Authorization': f'Bearer {invalid_token}',  # Agregar "Bearer" antes del token
            'accept': 'application/json'
        }

        # Hacer la solicitud POST al endpoint /verify
        response = requests.post(f'{BASE_URL}/verify', headers=headers)

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
    unittest.main()
