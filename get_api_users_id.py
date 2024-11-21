import requests
import time
import logging
from config import BASE_URL 

# Configuración de logging
logging.basicConfig(
    filename="user_get_requests.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def send_get_request(user_id):
    """
    Envía una solicitud GET al endpoint para obtener un usuario por ID.
    """
    try:
        start_time = time.time()
        response = requests.get(f"{BASE_URL}{user_id}", headers={"accept": "*/*"})
        end_time = time.time()

        if response.status_code == 200:
            message = f"[SUCCESS] User {user_id} retrieved: {response.json()} (Time: {end_time - start_time:.2f}s)"
            print(message)
            logging.info(message)
        elif response.status_code == 404:
            message = f"[NOT FOUND] User {user_id} not found (Time: {end_time - start_time:.2f}s)"
            print(message)
            logging.warning(message)
        else:
            message = f"[ERROR] GET request failed for User {user_id} with status {response.status_code}: {response.text}"
            print(message)
            logging.error(message)
        return response.status_code
    except requests.exceptions.RequestException as e:
        message = f"[EXCEPTION] GET request failed for User {user_id}: {e}"
        print(message)
        logging.exception(message)
        return None

def get_users(user_ids):
    """
    Obtiene múltiples usuarios por sus IDs.
    """
    logging.info("Starting to fetch users...")
    for user_id in user_ids:
        send_get_request(user_id)
    logging.info("Finished fetching users.")

if __name__ == "__main__":
    # IDs de usuarios a consultar
    user_ids_to_query = [1, 99999, 3]  # Incluye IDs inexistentes para probar casos 404
    get_users(user_ids_to_query)
