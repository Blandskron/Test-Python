import requests
import random
import uuid
import time
import logging
from config import BASE_URL 

# Configuración de logging
logging.basicConfig(filename='api_requests.log', level=logging.INFO, format='%(asctime)s - %(message)s')


def generate_random_update_data():
    """
    Genera datos aleatorios para actualizar un usuario.
    """
    return {
        "identification": str(random.randint(100000, 999999)),
        "name": f"Updated-{uuid.uuid4().hex[:5]}",
        "email": f"updated{random.randint(1000, 9999)}@example.com",
        "password": "updated_password123"
    }

def send_put_request(user_id, update_data):
    """
    Envía una solicitud PUT para actualizar un usuario existente.
    """
    try:
        start_time = time.time()
        response = requests.put(f"{BASE_URL}{user_id}", json=update_data, headers={"accept": "*/*"})
        end_time = time.time()

        if response.status_code == 200:
            message = f"[SUCCESS] User {user_id} updated: {response.json()} (Time: {end_time - start_time:.2f}s)"
            print(message)
            logging.info(message)  # Registra en el archivo
        else:
            message = f"[ERROR] PUT request failed for User {user_id} with status {response.status_code}: {response.text}"
            print(message)
            logging.error(message)  # Registra errores en el archivo
        return response.status_code
    except requests.exceptions.RequestException as e:
        message = f"[EXCEPTION] PUT request failed for User {user_id}: {e}"
        print(message)
        logging.exception(message)  # Registra excepciones en el archivo
        return None

def update_users(user_ids):
    """
    Actualiza múltiples usuarios.
    """
    for user_id in user_ids:
        update_data = generate_random_update_data()
        send_put_request(user_id, update_data)

if __name__ == "__main__":
    # IDs de usuarios existentes para actualizar
    existing_user_ids = [1, 2, 3, 4, 5]
    update_users(existing_user_ids)
