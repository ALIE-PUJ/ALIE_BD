# pip install pytest requests

# To run: pytest API\Tests\Files_Tests.py

import unittest
import requests
from io import BytesIO

BASE_URL = 'http://localhost:5000/files'

class FileEndpointTestCase(unittest.TestCase):

#Guardar el archivo PDF
    def test_submit_file_success(self):
        # Simula un archivo PDF
        file_data = BytesIO(b'%PDF-1.4 simulated pdf content')
        file_data.name = 'test_file.pdf'

        # Define el payload para la solicitud
        payload = {
            'categoria': 'Publico General',
            'auth_token': 'XXX'
        }

        # Hacer POST al endpoint /files/submit
        response = requests.post(f'{BASE_URL}/submit', files={'file': file_data}, data=payload)

        # Afirmaciones
        assert response.status_code == 200
        response_data = response.json()
        assert response_data['success'] is True

    def test_submit_file_missing_auth_token(self):
        # Simula un archivo PDF
        file_data = BytesIO(b'%PDF-1.4 simulated pdf content')
        file_data.name = 'test_file.pdf'

        # Define el payload con el auth_token faltante
        payload = {
            'categoria': 'Publico General'
        }

        # Hacer POST al endpoint /files/submit
        response = requests.post(f'{BASE_URL}/submit', files={'file': file_data}, data=payload)

        # Afirmaciones
        assert response.status_code == 401
        response_data = response.json()
        assert response_data['success'] is False
        assert 'Falta el token de autenticación' in response_data['message']

    def test_submit_file_invalid_format(self):
        # Simula un archivo que no es PDF
        file_data = BytesIO(b'Simulated content')
        file_data.name = 'test_file.txt'

        # Define el payload para la solicitud
        payload = {
            'categoria': 'Publico General',
            'auth_token': 'XXX'
        }

        # Hacer POST al endpoint /files/submit
        response = requests.post(f'{BASE_URL}/submit', files={'file': file_data}, data=payload)

        # Afirmaciones
        assert response.status_code == 400
        response_data = response.json()
        assert response_data['success'] is False
        assert 'El archivo debe ser un PDF' in response_data['message']


#Listar los archivos
    def test_list_files_success(self):
        # Define el parámetro auth_token
        params = {
            'auth_token': 'XXX'
        }

        # Hacer GET al endpoint /files/list
        response = requests.get(f'{BASE_URL}/list', params=params)

        # Afirmaciones
        assert response.status_code == 200
        response_data = response.json()
        assert response_data['success'] is True
        assert isinstance(response_data['files'], list)

    def test_list_files_missing_auth_token(self):
        # Hacer GET al endpoint /files/list sin auth_token
        response = requests.get(f'{BASE_URL}/list')

        # Afirmaciones
        assert response.status_code == 401
        response_data = response.json()
        assert response_data['success'] is False
        assert 'Falta el token de autenticación' in response_data['message']

#Eliminar los archivos
    def test_delete_file_success(self):
        # Subir un archivo antes de eliminar
        file_data = BytesIO(b'%PDF-1.4 simulated pdf content')
        file_data.name = 'test_file.pdf'
        payload = {
            'categoria': 'Publico General',
            'auth_token': 'XXX'
        }
        requests.post(f'{BASE_URL}/submit', files={'file': file_data}, data=payload)

        # Define los parámetros
        params = {
            'auth_token': 'XXX',
            'name': 'test_file.pdf'
        }

        # Hacer DELETE al endpoint /files/delete
        response = requests.delete(f'{BASE_URL}/delete', params=params)

        # Afirmaciones
        assert response.status_code == 200
        response_data = response.json()
        assert response_data['success'] is True

    def test_delete_file_not_found(self):
        # Define los parámetros
        params = {
            'auth_token': 'XXX',
            'name': 'non_existent_file.pdf'
        }

        # Hacer DELETE al endpoint /files/delete
        response = requests.delete(f'{BASE_URL}/delete', params=params)

        # Afirmaciones
        assert response.status_code == 404
        response_data = response.json()
        assert response_data['success'] is False
        assert 'Archivo no encontrado' in response_data['message']

    def test_delete_file_no_name(self):
        # Define los parámetros sin el nombre del archivo
        params = {'auth_token': 'XXX'}

        # Hacer DELETE al endpoint /files/delete
        response = requests.delete(f'{BASE_URL}/delete', params=params)

        # Afirmaciones
        assert response.status_code == 400
        response_data = response.json()
        assert response_data['success'] is False
        assert 'Falta el nombre del archivo' in response_data['message']

    def test_delete_file_missing_auth_token(self):
        # Intentar eliminar un archivo sin token de autorización
        params = {'name': 'test_file.pdf'}

        # Hacer DELETE al endpoint /files/delete
        response = requests.delete(f'{BASE_URL}/delete', params=params)

        # Afirmaciones
        assert response.status_code == 401
        response_data = response.json()
        assert response_data['success'] is False
        assert 'Falta el token de autenticación' in response_data['message']


#Visualizar los archivos
    def test_view_file_success(self):
        # Subir un archivo antes de intentar visualizarlo
        file_data = BytesIO(b'%PDF-1.4 simulated pdf content')
        file_data.name = 'test_file.pdf'
        payload = {
            'categoria': 'Publico General',
            'auth_token': 'XXX'
        }
        requests.post(f'{BASE_URL}/submit', files={'file': file_data}, data=payload)

        # Define los parámetros
        params = {
            'auth_token': 'XXX',
            'name': 'test_file.pdf'
        }

        # Hacer GET al endpoint /files/view
        response = requests.get(f'{BASE_URL}/view', params=params)

        # Afirmaciones
        assert response.status_code == 200
        assert response.headers['Content-Type'] == 'application/pdf'

    def test_view_file_not_found(self):
        # Define los parámetros
        params = {
            'auth_token': 'XXX',
            'name': 'non_existent_file.pdf'
        }

        # Hacer GET al endpoint /files/view
        response = requests.get(f'{BASE_URL}/view', params=params)

        # Afirmaciones
        assert response.status_code == 404
        response_data = response.json()
        assert response_data['success'] is False
        assert 'Archivo no encontrado' in response_data['message']

    def test_view_file_no_name(self):
        # Define los parámetros sin nombre de archivo
        params = {'auth_token': 'XXX'}

        # Hacer GET al endpoint /files/view
        response = requests.get(f'{BASE_URL}/view', params=params)

        # Afirmaciones
        assert response.status_code == 400
        response_data = response.json()
        assert response_data['success'] is False
        assert 'Falta el nombre del archivo' in response_data['message']

    def test_view_file_missing_auth_token(self):
        # Intentar visualizar un archivo sin token de autorización
        params = {'name': 'test_file.pdf'}

        # Hacer GET al endpoint /files/view
        response = requests.get(f'{BASE_URL}/view', params=params)

        # Afirmaciones
        assert response.status_code == 401
        response_data = response.json()
        assert response_data['success'] is False
        assert 'Falta el token de autenticación' in response_data['message']


if __name__ == '__main__':
    unittest.main()