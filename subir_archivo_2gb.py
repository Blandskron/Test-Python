import os
import requests

# Función para generar un archivo de tamaño configurable
def generar_archivo(file_name, size_gb):
    try:
        size_bytes = int(size_gb * 1024 * 1024 * 1024)  # Tamaño en bytes
        with open(file_name, "wb") as f:
            # Crear un archivo del tamaño especificado con ceros
            f.truncate(size_bytes)
        print(f"Archivo '{file_name}' de {size_gb}GB generado exitosamente.")
    except Exception as e:
        print(f"Error al generar el archivo '{file_name}':", e)

# Función para cargar el archivo al servidor en partes
def cargar_archivo(file_path, url, chunk_size=1024 * 1024):
    try:
        # Verificar si el archivo existe
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"El archivo '{file_path}' no existe.")

        # Obtener el tamaño del archivo
        file_size = os.path.getsize(file_path)
        print(f"Subiendo archivo: {file_path} ({file_size / (1024 * 1024 * 1024):.2f} GB)")

        with open(file_path, "rb") as file:
            headers = {"Content-Type": "application/octet-stream"}
            # Enviar datos en partes
            for chunk in iter(lambda: file.read(chunk_size), b""):
                response = requests.post(
                    url,
                    data=chunk,
                    headers=headers,
                    timeout=600,  # Tiempo de espera extendido (10 minutos)
                )
                if response.status_code != 200:
                    raise requests.exceptions.RequestException(
                        f"Error al subir archivo: {response.status_code} - {response.text}"
                    )

        print("Archivo subido exitosamente.")
    except requests.exceptions.Timeout:
        print("Error: La carga del archivo excedió el tiempo de espera.")
    except requests.exceptions.ConnectionError:
        print("Error: No se pudo conectar con el servidor.")
    except requests.exceptions.RequestException as e:
        print("Error durante la carga del archivo:", e)
    except Exception as e:
        print(f"Error general durante la carga del archivo '{file_path}':", e)

# Parámetros configurables
file_name = "archivo_prueba_1_9gb.dat"
file_size_gb = 1.9  # Tamaño del archivo en GB
server_url = "http://localhost:8085/api/documents/create"

# Generar el archivo
generar_archivo(file_name, file_size_gb)

# Cargar el archivo al servidor
cargar_archivo(file_name, server_url)
