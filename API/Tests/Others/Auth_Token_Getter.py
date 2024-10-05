import requests

# Datos de autenticación
BASE_URL = 'http://localhost:2001/api/auth'  # La URL de la API de autenticación
USERNAME = "luis.bravo@javeriana.edu.com"
PASSWORD = "123456"

def login_and_get_header():
    """
    Inicia sesión, obtiene el token de autenticación, y devuelve un encabezado de autorización.
    
    :return: dict - encabezado con el token de autorización y 'accept': 'application/json'
    """
    # Definir payload para iniciar sesión
    payload = {
        "email": USERNAME,
        "contrasena": PASSWORD
    }

    # Hacer la solicitud POST al endpoint /login
    response = requests.post(f'{BASE_URL}/login', json=payload)

    # Verificar que la solicitud fue exitosa
    if response.status_code == 200:
        # Extraer token de la respuesta
        response_data = response.json()
        token = response_data['token']
        print(f"Token obtenido: {token}")

        # Crear el header con el token y el campo 'accept'
        headers = {
            'Authorization': f'Bearer {token}',
            'accept': 'application/json'
        }

        # Retornar el header para usarlo en otras solicitudes
        return headers
    else:
        # Si falla el login, imprimir el error y devolver None
        print(f"Error al iniciar sesión: {response.status_code} - {response.text}")
        return None

# Ejemplo de uso
if __name__ == '__main__':

    '''
    headers = login_and_get_header()
    if headers:
        print("Header de autorización creado con éxito:", headers)
        # Ahora puedes usar 'headers' en otras solicitudes de la API
    else:
        print("No se pudo crear el header de autorización.")
    '''
