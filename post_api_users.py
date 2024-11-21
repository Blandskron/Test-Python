import requests
import random
import uuid
import time
import logging
from concurrent.futures import ThreadPoolExecutor
from config import BASE_URL 

# Configuración de logging
logging.basicConfig(
    filename="massive_user_registration.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# Número de usuarios a registrar
NUM_USERS = 50

def generate_random_user():
    """
    Genera un usuario con datos aleatorios.
    """
    user_data = {
        "identification": str(random.randint(100000, 999999)),  # ID aleatorio
        "name": f"User-{uuid.uuid4().hex[:5]}",  # Nombre aleatorio
        "email": f"user{random.randint(1000, 9999)}@example.com",  # Email aleatorio
        "password": "password123"  # Contraseña fija
    }
    logging.debug(f"Generated user data: {user_data}")
    return user_data

def send_post_request(user_data):
    """
    Envía una solicitud POST al endpoint con el cuerpo del usuario.
    """
    try:
        start_time = time.time()
        response = requests.post(BASE_URL, json=user_data, headers={"accept": "*/*"})
        end_time = time.time()

        if response.status_code == 201:
            message = f"[SUCCESS] User created: {response.json()} (Time: {end_time - start_time:.2f}s)"
            print(message)
            logging.info(message)
        else:
            message = f"[ERROR] Unexpected response for user: {user_data} - Status: {response.status_code}, Response: {response.text}"
            print(message)
            logging.error(message)

        return response.status_code
    except requests.exceptions.RequestException as e:
        message = f"[EXCEPTION] Failed to create user: {user_data} - Exception: {e}"
        print(message)
        logging.exception(message)
        return None

def register_massive_users():
    """
    Registra múltiples usuarios concurrentemente.
    """
    logging.info("Starting massive user registration process...")
    start_time = time.time()

    with ThreadPoolExecutor(max_workers=5) as executor:
        users = [generate_random_user() for _ in range(NUM_USERS)]
        futures = [executor.submit(send_post_request, user) for user in users]

        # Recolectar los resultados
        results = [future.result() for future in futures]
        successful = results.count(201)
        failed = len(results) - successful

    end_time = time.time()
    logging.info(f"Finished registration: {successful} successful, {failed} failed (Time: {end_time - start_time:.2f}s)")
    print(f"Registered {successful}/{NUM_USERS} users successfully in {end_time - start_time:.2f} seconds.")

if __name__ == "__main__":
    register_massive_users()
