# pip install pytest requests

# To run: pytest API\Tests\Auth_Service_Tests.py

import unittest
import requests

BASE_URL = 'http://localhost:2001/api/auth'  # The live API URL

class UserAuthEndpointTestCase(unittest.TestCase):

    # Login

    def test_login_success_admin(self):
        # Define payload for a successful login as an admin
        payload = {
            "email": "luis.bravo@javeriana.edu.com",
            "contrasena": "123456"
        }

        # Make POST request to the /login endpoint
        response = requests.post(f'{BASE_URL}/login', json=payload)

        # Assertions
        assert response.status_code == 200
        response_data = response.json()
        assert 'user' in response_data
        assert 'token' in response_data
        assert response_data['user']['usuario'] == "Luis Bravo"  # Check the correct username
        assert response_data['user']['id_categoria'] == 2  # Category 2 is the admin category
        assert response_data['user']['email'] == "luis.bravo@javeriana.edu.com"  # Check the email

    def test_login_success_student(self):
        # Define payload for a successful login as a student
        payload = {
            "email": "pepito@javeriana.edu.com",
            "contrasena": "123456"
        }

        # Make POST request to the /login endpoint
        response = requests.post(f'{BASE_URL}/login', json=payload)

        # Assertions
        assert response.status_code == 200
        response_data = response.json()
        assert 'user' in response_data
        assert 'token' in response_data
        assert response_data['user']['usuario'] == "Pepito perez"  # Check the correct username
        assert response_data['user']['id_categoria'] == 1  # Category 1 is the student category
        assert response_data['user']['email'] == "pepito@javeriana.edu.com"  # Check the email

    def test_login_invalid_credentials(self):
        # Define payload for invalid login credentials
        payload = {
            "email": "luis.bravo@javeriana.edu.com",
            "contrasena": "wrongpassword"
        }

        # Make POST request to the /login endpoint
        response = requests.post(f'{BASE_URL}/login', json=payload)

        # Assertions
        assert response.status_code == 401
        response_data = response.json()
        assert 'message' in response_data
        assert response_data['message'] == "Credenciales inválidas"


    # Roles. Funcionalidad interna de la API
    '''
    def test_asignar_rol_success(self):
        # Define payload for assigning a role successfully
        payload = {
            "id_categoria": 2,  # Assuming category 2 exists
            "id_usuario": 2     # Assuming user 2 exists
        }

        # Make PUT request to the /asignar_rol endpoint
        response = requests.put(f'{BASE_URL}/asignar_rol', json=payload)

        # Assertions
        assert response.status_code == 200
        assert response.json() is True  # Check for true response

    def test_asignar_rol_user_not_exist(self):
        # Define payload with a non-existent user
        payload = {
            "id_categoria": 2,
            "id_usuario": 10  # Assuming user 10 does not exist
        }

        # Make PUT request to the /asignar_rol endpoint
        response = requests.put(f'{BASE_URL}/asignar_rol', json=payload)

        # Assertions
        assert response.status_code == 400
        response_data = response.json()
        assert 'message' in response_data
        assert response_data['message'] == "Error al asignar rol"

    def test_asignar_rol_role_not_exist(self):
        # Define payload with a non-existent category
        payload = {
            "id_categoria": 20,  # Assuming category 20 does not exist
            "id_usuario": 2
        }

        # Make PUT request to the /asignar_rol endpoint
        response = requests.put(f'{BASE_URL}/asignar_rol', json=payload)

        # Assertions
        assert response.status_code == 400
        response_data = response.json()
        assert 'message' in response_data
        assert response_data['message'] == "Error al asignar rol"
        '''

if __name__ == '__main__':
    unittest.main()
