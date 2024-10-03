import pytest
import requests

BASE_URL = 'http://localhost:5000/chat'

@pytest.fixture(scope='module')
def setup_chat():
    """Crea un chat en la base de datos y devuelve su memory_key para usar en las pruebas."""
    payload = {
        'auth_token': 'XXX',
        'mensajes_agente': ['Hola, cómo estás?'],
        'mensajes_usuario': ['Estoy bien, gracias.'],
        'mensajes_supervision': ['Todo en orden.'],
        'user_id': 1
    }
    response = requests.post(f'{BASE_URL}/guardar', json=payload)
    assert response.status_code == 200, "Error al crear el chat"
    memory_key = response.json()['memory_key']
    return memory_key

class TestChatEndpoint:

    # Pruebas para guardar chat
    def test_guardar_chat_success(self):
        """Prueba de éxito para guardar un chat con todos los campos requeridos."""
        payload = {
            'auth_token': 'XXX',
            'mensajes_agente': ['Hola, cómo estás?'],
            'mensajes_usuario': ['Estoy bien, gracias.'],
            'mensajes_supervision': ['Todo en orden.'],
            'user_id': 1
        }

        response = requests.post(f'{BASE_URL}/guardar', json=payload)
        assert response.status_code == 200
        response_data = response.json()
        assert response_data['success'] is True
        assert 'memory_key' in response_data
        assert 'nombre' in response_data

    def test_guardar_chat_missing_fields(self):
        """Prueba de error cuando faltan campos requeridos en el payload."""
        payload = {
            'auth_token': 'XXX',
            'mensajes_agente': ['Hola'],
            'user_id': 1
        }

        response = requests.post(f'{BASE_URL}/guardar', json=payload)
        assert response.status_code == 400
        response_data = response.json()
        assert response_data['success'] is False
        assert 'Faltan campos requeridos' in response_data['message']

    # Pruebas para obtener un chat
    def test_get_chat_success(self, setup_chat):
        """Prueba de éxito para obtener un chat existente."""
        payload = {
            'auth_token': 'XXX',
            'memory_key': setup_chat
        }

        response = requests.post(f'{BASE_URL}/get', json=payload)
        assert response.status_code == 200
        response_data = response.json()
        assert response_data['success'] is True
        assert 'memory_key' in response_data

    def test_get_chat_not_found(self):
        """Prueba de error cuando se intenta obtener un chat inexistente."""
        payload = {
            'auth_token': 'XXX',
            'memory_key': 'INVALID_MEMORY_KEY'
        }

        response = requests.post(f'{BASE_URL}/get', json=payload)
        assert response.status_code == 404
        response_data = response.json()
        assert response_data['success'] is False
        assert 'Chat no encontrado' in response_data['message']

    # Pruebas para listar chats intervenidos
    def test_list_intervention_chats(self):
        """Prueba de éxito para listar todos los chats intervenidos."""
        payload = {
            'auth_token': 'XXX'
        }

        response = requests.post(f'{BASE_URL}/list_intervention', json=payload)
        assert response.status_code == 200
        response_data = response.json()
        assert isinstance(response_data, list)
        assert all('memory_key' in chat for chat in response_data)

    # Pruebas para listar chats por usuario
    def test_list_chats_by_user_success(self):
        """Prueba de éxito para listar todos los chats de un usuario específico."""
        payload = {
            'auth_token': 'XXX',
            'user_id': 1
        }

        response = requests.post(f'{BASE_URL}/list', json=payload)
        assert response.status_code == 200
        response_data = response.json()
        assert isinstance(response_data, list)
        assert all('memory_key' in chat for chat in response_data)

    # Pruebas para listar todos los chats
    def test_list_all_chats(self):
        """Prueba de éxito para listar todos los chats en la base de datos."""
        payload = {
            'auth_token': 'XXX'
        }

        response = requests.post(f'{BASE_URL}/list_all', json=payload)
        assert response.status_code == 200
        response_data = response.json()
        assert isinstance(response_data, list)
        assert all('memory_key' in chat for chat in response_data)

    # Pruebas para eliminar un chat
    def test_delete_chat_success(self, setup_chat):
        """Prueba de éxito para eliminar un chat existente."""
        payload = {
            'auth_token': 'XXX',
            'memory_key': setup_chat
        }

        response = requests.post(f'{BASE_URL}/delete', json=payload)
        assert response.status_code == 200
        response_data = response.json()
        assert response_data['success'] is True

    def test_delete_chat_not_found(self):
        """Prueba de error cuando se intenta eliminar un chat inexistente."""
        payload = {
            'auth_token': 'XXX',
            'memory_key': 'INVALID_MEMORY_KEY'
        }

        response = requests.post(f'{BASE_URL}/delete', json=payload)
        assert response.status_code == 404
        response_data = response.json()
        assert response_data['success'] is False
        assert 'Chat no encontrado' in response_data['message']

    def test_archivar_chat_not_found(self):
        """Prueba de error cuando se intenta archivar un chat inexistente."""
        payload = {
            'auth_token': 'XXX',
            'memory_key': 'INVALID_MEMORY_KEY'
        }

        response = requests.post(f'{BASE_URL}/archive', json=payload)
        assert response.status_code == 404
        response_data = response.json()
        assert response_data['success'] is False
        assert 'Chat no encontrado' in response_data['message']

    # Pruebas para actualizar el estado de intervención
    def test_update_intervention_status_success(self, setup_chat):
        """Prueba de éxito para actualizar el estado de intervención de un chat."""
        payload = {
            'auth_token': 'XXX',
            'memory_key': setup_chat,
            'intervenido': True
        }

        response = requests.post(f'{BASE_URL}/update_intervention', json=payload)
        assert response.status_code == 200
        response_data = response.json()
        assert response_data['success'] is True
