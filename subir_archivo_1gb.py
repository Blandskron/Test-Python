import os
import requests

# Función para generar un archivo de 1GB con ceros
def generar_archivo_1gb(file_name):
    try:
        with open(file_name, "wb") as f:
            # Mueve el puntero a 1GB menos 1 byte
            f.seek(1 * 1024 * 1024 * 1024 - 1)
            # Escribe un byte al final para definir el tamaño
            f.write(b"\0")
        print(f"Archivo '{file_name}' de 1GB generado exitosamente.")
    except Exception as e:
        print("Error al generar el archivo:", e)

# Función para cargar el archivo al servidor
def cargar_archivo(file_path):
    # URL del endpoint de carga
    url = "http://localhost:8085/api/documents/create"

    try:
        # Abre el archivo en modo binario
        with open(file_path, "rb") as file:
            # Prepara los datos para enviar
            files = {"file": file}

            # Realiza la solicitud POST
            response = requests.post(url, files=files)

            # Imprime el resultado
            if response.status_code == 200:
                print("Archivo subido exitosamente:", response.text)
            else:
                print(f"Error al subir archivo: {response.status_code} - {response.text}")
    except Exception as e:
        print("Error durante la carga del archivo:", e)

# Nombre del archivo de 1GB
file_name = "archivo_prueba_1gb.dat"

# Generar el archivo de 1GB
generar_archivo_1gb(file_name)

# Cargar el archivo al servidor
cargar_archivo(file_name)
