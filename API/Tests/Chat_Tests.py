# pip install pytest requests

# To run: pytest API\Tests\Chat_Tests.py

import unittest
import requests

# Auth Headers
from Others.Auth_Token_Getter import *
headers = {} # Encabezados de la solicitud. Vacío por ahora

BASE_URL = 'http://localhost:5000/api/front/chat'

class TestChatEndpoint(unittest.TestCase):

    # Método para configurar la clase de prueba
    @classmethod
    def setUpClass(cls):
        """Crea un chat en la base de datos y almacena su memory_key para usar en las pruebas."""
        payload = {
            'mensajes_agente': ['Hola, cómo estás?'],
            'mensajes_usuario': ['Estoy bien, gracias.'],
            'mensajes_supervision': ['Todo en orden.'],
            'user_id': 1
        }
        response = requests.post(f'{BASE_URL}/guardar', json=payload, headers=headers)
        assert response.status_code == 200, "Error al crear el chat"
        cls.memory_key = response.json()['memory_key']
        print(f"Memory Key Guardado: {cls.memory_key}")  # Para depuración


    # Pruebas para guardar chat

    def test_guardar_chat_success(self):
        """Prueba de éxito para guardar un chat con todos los campos requeridos."""
        payload = {
            'mensajes_agente': ['Hola, cómo estás?'],
            'mensajes_usuario': ['Estoy bien, gracias.'],
            'mensajes_supervision': ['Todo en orden.'],
            'user_id': 1
        }

        response = requests.post(f'{BASE_URL}/guardar', json=payload, headers=headers)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertTrue(response_data['success'])
        self.assertIn('memory_key', response_data)
        self.assertIn('nombre', response_data)

    def test_guardar_chat_missing_fields(self):
        """Prueba de error cuando faltan campos requeridos en el payload."""
        payload = {
            'mensajes_agente': ['Hola'],
            'user_id': 1
        }

        response = requests.post(f'{BASE_URL}/guardar', json=payload, headers=headers)
        self.assertEqual(response.status_code, 400)
        response_data = response.json()
        self.assertFalse(response_data['success'])
        self.assertIn('Faltan campos requeridos', response_data['message'])

    def test_guardar_chat_missing_invalid_token(self):
        """Prueba de error cuando falta el token"""
        payload = {
            'mensajes_agente': ['Hola'],
            'user_id': 1
        }

        # Create a new header without the auth_token, but an invalid token
        invalid_token = "invalid_token"
        headers_specific = {
            'Authorization': f'Bearer {invalid_token}',  # Agregar "Bearer" antes del token
            'accept': 'application/json'
        }

        response = requests.post(f'{BASE_URL}/guardar', json=payload, headers=headers_specific)

        assert response.status_code == 401
        response_data = response.json()
        assert response_data['success'] is False
        assert 'Token de autorización inválido o faltante' in response_data['message']



    # Pruebas para obtener un chat
   
    def test_get_chat_not_found(self):
        """Prueba de error cuando se intenta obtener un chat inexistente."""
        payload = {
            'memory_key': 'INVALID_MEMORY_KEY'
        }

        response = requests.post(f'{BASE_URL}/get', json=payload, headers=headers)
        self.assertEqual(response.status_code, 404)
        response_data = response.json()
        self.assertFalse(response_data['success'])
        self.assertIn('Chat no encontrado', response_data['message'])

    def test_get_chat_invalid_token(self):
        """Prueba de error cuando falta el token"""
        payload = {
            'memory_key': 'INVALID_MEMORY_KEY'
        }

        # Create a new header without the auth_token, but an invalid token
        invalid_token = "invalid_token"
        headers_specific = {
            'Authorization': f'Bearer {invalid_token}',  # Agregar "Bearer" antes del token
            'accept': 'application/json'
        }

        response = requests.post(f'{BASE_URL}/get', json=payload, headers=headers_specific)
        assert response.status_code == 401
        response_data = response.json()
        assert response_data['success'] is False
        assert 'Token de autorización inválido o faltante' in response_data['message']
    


    # Pruebas para listar chats intervenidos

    def test_list_intervention_chats(self):
        """Prueba de éxito para listar todos los chats intervenidos."""
        payload = {
        }

        response = requests.post(f'{BASE_URL}/list_intervention', json=payload, headers=headers)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertIsInstance(response_data, list)
        self.assertTrue(all('memory_key' in chat for chat in response_data))

    def test_list_intervention_chats_invalid_token(self):
        """Prueba de error cuando falta el token"""
        payload = {
        }

        # Create a new header without the auth_token, but an invalid token
        invalid_token = "invalid_token"
        headers_specific = {
            'Authorization': f'Bearer {invalid_token}',  # Agregar "Bearer" antes del token
            'accept': 'application/json'
        }

        response = requests.post(f'{BASE_URL}/list_intervention', json=payload, headers=headers_specific)
        assert response.status_code == 401
        response_data = response.json()
        assert response_data['success'] is False
        assert 'Token de autorización inválido o faltante' in response_data['message']
    


    # Pruebas para listar chats por usuario

    def test_list_chats_by_user_success(self):
        """Prueba de éxito para listar todos los chats de un usuario específico."""
        payload = {
            'user_id': 1
        }

        response = requests.post(f'{BASE_URL}/list', json=payload, headers=headers)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertIsInstance(response_data, list)
        self.assertTrue(all('memory_key' in chat for chat in response_data))

    def test_list_chats_by_user_not_found(self):
        """Prueba de error para listar chats de un usuario que no existe."""
        payload = {
            'user_id': 9999  # ID de usuario que no existe
        }

        response = requests.post(f'{BASE_URL}/list', json=payload, headers=headers)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertIsInstance(response_data, list)
        self.assertEqual(len(response_data), 0)  # Se espera una lista vacía

    def test_list_chats_by_user_invalid_token(self):
        """Prueba de error cuando falta el token"""
        payload = {
            'user_id': 1
        }

        # Create a new header without the auth_token, but an invalid token
        invalid_token = "invalid_token"
        headers_specific = {
            'Authorization': f'Bearer {invalid_token}',  # Agregar "Bearer" antes del token
            'accept': 'application/json'
        }

        response = requests.post(f'{BASE_URL}/list', json=payload, headers=headers_specific)
        assert response.status_code == 401
        response_data = response.json()
        assert response_data['success'] is False
        assert 'Token de autorización inválido o faltante' in response_data['message']



    # Pruebas para listar todos los chats

    def test_list_all_chats(self):
        """Prueba de éxito para listar todos los chats en la base de datos."""
        payload = {
        }

        response = requests.post(f'{BASE_URL}/list_all', json=payload, headers=headers)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertIsInstance(response_data, list)
        self.assertTrue(all('memory_key' in chat for chat in response_data))

    def test_list_all_chats_invalid_token(self):
        """Prueba de error cuando falta el token"""
        payload = {
        }

        # Create a new header without the auth_token, but an invalid token
        invalid_token = "invalid_token"
        headers_specific = {
            'Authorization': f'Bearer {invalid_token}',  # Agregar "Bearer" antes del token
            'accept': 'application/json'
        }

        response = requests.post(f'{BASE_URL}/list_all', json=payload, headers=headers_specific)
        assert response.status_code == 401
        response_data = response.json()
        assert response_data['success'] is False
        assert 'Token de autorización inválido o faltante' in response_data['message']



    # Pruebas para eliminar un chat

    def test_delete_chat_success(self):
        """Prueba de éxito para eliminar un chat existente."""
        payload = {
            'memory_key': self.memory_key
        }

        response = requests.post(f'{BASE_URL}/delete', json=payload, headers=headers)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertTrue(response_data['success'])

    def test_delete_chat_not_found(self):
        """Prueba de error cuando se intenta eliminar un chat inexistente."""
        payload = {
            'memory_key': 'INVALID_MEMORY_KEY'
        }

        response = requests.post(f'{BASE_URL}/delete', json=payload, headers=headers)
        self.assertEqual(response.status_code, 404)
        response_data = response.json()
        self.assertFalse(response_data['success'])
        self.assertIn('Chat no encontrado', response_data['message'])

    def test_delete_chat_invalid_token(self):
        """Prueba de error cuando falta el token"""
        payload = {
            'memory_key': self.memory_key
        }

        # Create a new header without the auth_token, but an invalid token
        invalid_token = "invalid_token"
        headers_specific = {
            'Authorization': f'Bearer {invalid_token}',  # Agregar "Bearer" antes del token
            'accept': 'application/json'
        }

        response = requests.post(f'{BASE_URL}/delete', json=payload, headers=headers_specific)
        assert response.status_code == 401
        response_data = response.json()
        assert response_data['success'] is False
        assert 'Token de autorización inválido o faltante' in response_data['message']



    # Pruebas para archivar un chat

    def test_archivar_chat_success(self):
        """Prueba de éxito para archivar un chat existente."""
        payload = {
            'memory_key': self.memory_key
        }

        response = requests.post(f'{BASE_URL}/archive', json=payload, headers=headers)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertTrue(response_data['success'])

    def test_archivar_chat_not_found(self):
        """Prueba de error cuando se intenta archivar un chat inexistente."""
        payload = {
            'memory_key': 'INVALID_MEMORY_KEY'
        }

        response = requests.post(f'{BASE_URL}/archive', json=payload, headers=headers)
        self.assertEqual(response.status_code, 404)
        response_data = response.json()
        self.assertFalse(response_data['success'])
        self.assertIn('Chat no encontrado', response_data['message'])

    def test_archivar_chat_invalid_token(self):
        """Prueba cuando falta el token"""
        payload = {
            'memory_key': self.memory_key
        }

        # Create a new header without the auth_token, but an invalid token
        invalid_token = "invalid_token"
        headers_specific = {
            'Authorization': f'Bearer {invalid_token}',  # Agregar "Bearer" antes del token
            'accept': 'application/json'
        }

        response = requests.post(f'{BASE_URL}/archive', json=payload, headers=headers_specific)
        assert response.status_code == 401
        response_data = response.json()
        assert response_data['success'] is False
        assert 'Token de autorización inválido o faltante' in response_data['message']



    # Pruebas para actualizar el estado de intervención
    
    def test_update_intervention_status_success(self):
        """Prueba de éxito para actualizar el estado de intervención de un chat existente."""
        payload = {
            'memory_key': self.memory_key,
            'intervenido': True
        }

        response = requests.post(f'{BASE_URL}/update_intervention', json=payload, headers=headers)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertTrue(response_data['success'])

    def test_update_intervention_status_not_found(self):
        """Prueba de error cuando se intenta actualizar el estado de intervención de un chat inexistente."""
        # Aquí usamos un chat existente para la prueba
        payload = {
            'memory_key': self.memory_key,
            'intervenido': False  
        }

        response = requests.post(f'{BASE_URL}/update_intervention', json=payload, headers=headers)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertTrue(response_data['success'])

    def test_update_intervention_status_invalid_token(self):
        """Prueba de error cuando falta el token"""
        payload = {
            'memory_key': self.memory_key,
            'intervenido': True
        }

        # Create a new header without the auth_token, but an invalid token
        invalid_token = "invalid_token"
        headers_specific = {
            'Authorization': f'Bearer {invalid_token}',  # Agregar "Bearer" antes del token
            'accept': 'application/json'
        }

        response = requests.post(f'{BASE_URL}/update_intervention', json=payload, headers=headers_specific)
        assert response.status_code == 401
        response_data = response.json()
        assert response_data['success'] is False
        assert 'Token de autorización inválido o faltante' in response_data['message']


if __name__ == '__main__':

    headers = login_and_get_header() # Get the auth header
    unittest.main()
