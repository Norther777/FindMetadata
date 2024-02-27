import os
import subprocess
import argparse
from datetime import datetime

def buscar_strings_en_metadatos(archivo, strings_a_buscar):
    try:
        # Ejecutar exiftool para obtener los metadatos del archivo
        resultado = subprocess.check_output(["exiftool", archivo], universal_newlines=True)

        # Buscar los strings en la salida de exiftool y obtener las líneas con coincidencias
        lineas_coincidentes = [linea.strip() for linea in resultado.split('\n') if any(string.lower() in linea.lower() for string in strings_a_buscar)]

        # Obtener la fecha de creación del archivo
        fecha_creacion = obtener_fecha_creacion(archivo)
        return len(lineas_coincidentes) > 0, fecha_creacion, lineas_coincidentes
    except Exception as e:
        print(f"Error al procesar {archivo} con exiftool: {e}")
    
    return False, None, None

def obtener_fecha_creacion(archivo):
    try:
        fecha_creacion = os.path.getctime(archivo)
        return fecha_creacion
    except Exception as e:
        print(f"Error al obtener la fecha de creación de {archivo}: {e}")
        return None

def obtener_fecha_formateada(timestamp):
    try:
        fecha_creacion = datetime.fromtimestamp(timestamp)
        return fecha_creacion.strftime('%Y-%m-%d %H:%M:%S')
    except Exception as e:
        print(f"Error al formatear la fecha: {e}")
        return "Fecha no disponible"

def buscar_archivos_con_strings(directorio_raiz, strings_a_buscar, verbose):
    archivos_coincidentes = []

    for archivo in os.listdir(directorio_raiz):
        ruta_completa = os.path.join(directorio_raiz, archivo)
        if os.path.isfile(ruta_completa):  # Verificar si es un archivo (no una carpeta)
            coincidencia, fecha_creacion, lineas_coincidentes = buscar_strings_en_metadatos(ruta_completa, strings_a_buscar)
            if coincidencia:
                archivos_coincidentes.append((ruta_completa, fecha_creacion, lineas_coincidentes))

    return archivos_coincidentes

def imprimir_resultados(archivos_coincidentes, verbose):
    for archivo, fecha_creacion, lineas_coincidentes in archivos_coincidentes:
        fecha_creacion_formateada = obtener_fecha_formateada(fecha_creacion)
        print(f"Archivo: {archivo}")
        print(f"Fecha de creación: {fecha_creacion_formateada}")

        if verbose and lineas_coincidentes:
            print("Coincidencias:")
            for linea in lineas_coincidentes:
                print(linea)

        print("\n")

def main():
    parser = argparse.ArgumentParser(description='Buscar archivos con strings en metadatos de imágenes utilizando exiftool.')
    parser.add_argument('-path', type=str, help='Ruta del directorio raíz')
    parser.add_argument('-data', nargs='+', help='Strings a buscar en metadatos')
    parser.add_argument('-v', action='store_true', help='Mostrar detalles de las coincidencias (verbose)')
    args = parser.parse_args()

    directorio_raiz = args.path
    strings_a_buscar = args.data
    verbose = args.v

    archivos_coincidentes = buscar_archivos_con_strings(directorio_raiz, strings_a_buscar, verbose)

    if archivos_coincidentes:
        imprimir_resultados(archivos_coincidentes, verbose)
    else:
        print("No se encontraron archivos con los strings en los metadatos.")

if __name__ == "__main__":
    main()
