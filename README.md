# Buscador de Metadatos con exiftool
Este script de Python utiliza exiftool para buscar archivos en un directorio cuyos metadatos coincidan con ciertas cadenas de búsqueda. Proporciona una manera rápida y efectiva de encontrar archivos con información específica en sus metadatos, como la fecha de creación.
## Requisitos
- Python 3.x
- exiftool instalado y accesible desde la línea de comandos.

## Ejecución del script
```bash
python find_metadata.py -path <directorio_raiz> -data <cadena1> <cadena2> ... -v
```
-path: Ruta del directorio raíz donde se realizará la búsqueda.
-data: Cadenas a buscar en los metadatos de los archivos.
-v: Opcional. Muestra detalles de las coincidencias.
