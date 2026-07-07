# 📖 Instrucciones de Instalación para Otros Usuarios

## ¿Qué es esto?
**Scrapper Pinterest** es una herramienta que descarga automáticamente imágenes de personajes desde Pinterest y permite seleccionar la mejor imagen de cada uno.

---

## 🚀 Pasos para Instalar y Usar

### 1️⃣ **Descargar el Proyecto**

```bash
git clone https://github.com/AlvaroSM19/scrapper-pinterest.git
cd scrapper-pinterest
```

### 2️⃣ **Instalar Python** (si no lo tienes)
- **Windows**: Descarga de https://www.python.org/ (versión 3.9+)
- **Mac**: `brew install python3`
- **Linux**: `sudo apt-get install python3`

### 3️⃣ **Instalar Dependencias**

```bash
pip install -r requirements.txt
```

**Nota para Linux/Mac (si falla tkinter):**
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# macOS
brew install python-tk
```

### 4️⃣ **Verificar Google Chrome**
La herramienta usa Chrome automatizado. Asegúrate de tener Chrome instalado en tu sistema.

---

## ⚙️ Configuración

### Editar `config.json`
```json
{
    "images_per_character": 8,      // Imágenes a descargar por personaje
    "raw_dir": "raw_images",         // Carpeta donde se guardan las descargas
    "final_dir": "final_images"      // Carpeta donde se guardan las seleccionadas
}
```

### Editar `characters.json`
Agrega los personajes que deseas:
```json
[
    {
        "name": "Ichigo Kurosaki",
        "image_url": "https://ejemplo.com/imagen.jpg"
    },
    {
        "name": "Otro Personaje",
        "image_url": "https://ejemplo.com/imagen2.jpg"
    }
]
```

---

## 🎬 Ejecutar la Herramienta

### Paso 1: Descargar Imágenes
```bash
python scrapper.py
```
✅ Abrirá Chrome automáticamente y descargará imágenes de cada personaje

### Paso 2: Seleccionar las Mejores Imágenes
```bash
python selector.py
```
✅ Se abrirá una interfaz gráfica donde puedes:
- Presionar **1-8** para seleccionar la imagen que te guste
- Presionar **ESPACIO** para saltar (no seleccionar)
- Las seleccionadas se guardan en `final_images/` en formato webp

---

## 📁 Estructura de Carpetas

Después de ejecutar los scripts, verás:
```
scrapper-pinterest/
├── raw_images/          ← Imágenes descargadas (temporales)
├── final_images/        ← Imágenes seleccionadas (finales)
├── scrapper.py         ← Script para descargar
├── selector.py         ← Script para seleccionar
├── config.json         ← Configuración
├── characters.json     ← Lista de personajes
└── requirements.txt    ← Dependencias
```

---

## ⚠️ Solución de Problemas

| Problema | Solución |
|----------|----------|
| **Error: Chrome no encontrado** | Instala Google Chrome desde chrome.google.com |
| **Error: Module not found** | Ejecuta `pip install -r requirements.txt` nuevamente |
| **Las imágenes no descargan** | Verifica tu conexión a internet y el contenido de `characters.json` |
| **Error de permisos en Windows** | Ejecuta el CMD como administrador |
| **Error de tkinter** | Ver nota en sección "Instalar Dependencias" |

---

## 🔧 Requisitos
- Python 3.9 o superior
- Google Chrome instalado
- Conexión a internet
- ~1GB de espacio libre (aproximado)

---

## 📝 Notas Importantes
- Las imágenes se descargan desde Pinterest automáticamente
- El navegador se abre automáticamente durante la descarga
- No es necesario tener sesión abierta en Pinterest
- Las imágenes finales se guardan en formato **webp** con compresión de calidad 85

---

## 🆘 ¿Problemas?
Si encuentras algún error, verifica:
1. La versión de Python (`python --version`)
2. Las dependencias (`pip list`)
3. La conexión a internet
4. Que Chrome esté instalado

¡Éxito! 🚀
