# Scrapper Pinterest

Herramienta para descargar y seleccionar imágenes de personajes desde Pinterest.

## Instalación

### 1. Requisitos previos
- Python 3.7+
- pip (gestor de paquetes de Python)

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

**Nota para Linux/Mac:** Si tienes problemas con tkinter, instálalo con:
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# macOS
brew install python-tk
```

## Uso

### 1. Configurar el proyecto

Edita `config.json` con los parámetros deseados:
```json
{
    "images_per_character": 8,
    "raw_dir": "raw_images",
    "final_dir": "final_images"
}
```

### 2. Agregar personajes

Edita `characters.json` con los personajes:
```json
[
    {
        "name": "Nombre del Personaje",
        "image_url": "url_de_imagen_referencia"
    }
]
```

### 3. Ejecutar scrapper

```bash
python scrapper.py
```

Esto:
- Abrirá navegador Chrome automatizado
- Buscará imágenes en Pinterest para cada personaje
- Descargará y guardará las imágenes en `raw_images/`

### 4. Seleccionar imágenes

```bash
python selector.py
```

Una interfaz gráfica mostrará las imágenes descargadas donde puedes:
- Presionar números **1-8** para seleccionar una imagen
- Presionar **ESPACIO** para saltar y no seleccionar
- Las imágenes seleccionadas se guardan en `final_images/` en formato webp

## Estructura del proyecto

```
scrapper-pinterest/
├── scrapper.py          # Script para descargar imágenes
├── selector.py          # Interfaz GUI para seleccionar imágenes
├── config.json          # Configuración
├── characters.json      # Lista de personajes
├── requirements.txt     # Dependencias
├── raw_images/          # Imágenes descargadas (se crea automáticamente)
├── final_images/        # Imágenes seleccionadas (se crea automáticamente)
└── perfil_chrome/       # Perfil de navegador Chrome
```

## Troubleshooting

**Problema:** Selenium no encuentra Chrome
- **Solución:** `webdriver-manager` lo descarga automáticamente

**Problema:** Las imágenes no se descargan
- **Solución:** Verifica conexión a internet y configuración en `config.json`

**Problema:** Error de permisos en Windows
- **Solución:** Ejecuta con permisos de administrador

## Dependencias

- **selenium** - Automatización de navegador
- **webdriver-manager** - Gestión automática de ChromeDriver
- **requests** - Descargas HTTP
- **Pillow** - Procesamiento de imágenes
