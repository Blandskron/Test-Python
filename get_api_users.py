import requests
import concurrent.futures
import random
import time
import logging
from config import BASE_URL 

# Configuración de logging
logging.basicConfig(
    filename="massive_get_requests.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# Número de solicitudes a enviar
NUM_REQUESTS = 2

def send_request():
    """
    Envía una solicitud GET al endpoint y devuelve el resultado.
    """
    try:
        start_time = time.time()
        response = requests.get(BASE_URL, headers={"accept": "*/*"})
        end_time = time.time()

        if response.status_code == 200:
            message = f"[SUCCESS] GET request successful: {response.json()} (Time: {end_time - start_time:.2f}s)"
            print(message)
            logging.info(message)
        else:
            message = f"[ERROR] GET request failed with status code {response.status_code}: {response.text}"
            print(message)
            logging.error(message)

        return response.status_code
    except requests.exceptions.RequestException as e:
        message = f"[EXCEPTION] GET request failed: {e}"
        print(message)
        logging.exception(message)
        return None

def send_massive_requests():
    """
    Envía múltiples solicitudes concurrentes al endpoint.
    """
    logging.info("Starting massive GET requests process...")
    start_time = time.time()

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(send_request) for _ in range(NUM_REQUESTS)]
        results = [future.result() for future in concurrent.futures.as_completed(futures)]
        
        successful = results.count(200)
        failed = len(results) - successful

    end_time = time.time()
    logging.info(f"Finished sending requests: {successful} successful, {failed} failed (Time: {end_time - start_time:.2f}s)")
    print(f"Sent {NUM_REQUESTS} requests with {successful} successes and {failed} failures in {end_time - start_time:.2f} seconds.")

if __name__ == "__main__":
    send_massive_requests()
