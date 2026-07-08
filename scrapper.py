import os, json, time, requests
from urllib.parse import quote
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Cargar configuraciones
with open('config.json') as f: config = json.load(f)
with open('characters.json', encoding='utf-8') as f: chars = json.load(f)

N_IMAGES = config['images_per_character']
RAW_DIR = config['raw_dir']
os.makedirs(RAW_DIR, exist_ok=True)

def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={os.path.join(os.getcwd(), 'perfil_chrome')}")
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    try:
        service = Service(ChromeDriverManager().install())
        return webdriver.Chrome(service=service, options=options)
    except Exception as e:
        print(f"Error con ChromeDriver: {e}")
        print("Intentando con ruta manual de Chrome...")
        # Intentar rutas comunes de Chrome en Windows
        chrome_paths = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            os.path.expandvars(r"%ProgramFiles%\Google\Chrome\Application\chrome.exe"),
            os.path.expandvars(r"%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe"),
        ]
        for chrome_path in chrome_paths:
            if os.path.exists(chrome_path):
                options.binary_location = chrome_path
                try:
                    return webdriver.Chrome(options=options)
                except:
                    continue
        raise Exception("Chrome no encontrado en ubicaciones estándar")

MIN_FILE_SIZE = 20000  # bytes mínimos
MIN_DIMENSION = 300   # píxeles mínimos en el lado más corto
MAX_RATIO = 2.0       # descartar imágenes muy alargadas (banner, etc.)

def is_good_image(data):
    try:
        from PIL import Image
        import io
        img = Image.open(io.BytesIO(data))
        w, h = img.size
        if min(w, h) < MIN_DIMENSION: return False
        if max(w, h) / min(w, h) > MAX_RATIO: return False
        return True
    except:
        return False

def download_images(char, driver):
    base_name = char['image_url'].split('/')[-1].replace('.webp', '')
    if all(os.path.exists(os.path.join(RAW_DIR, f"{base_name}_{i}.jpg")) for i in range(1, N_IMAGES + 1)):
        return

    print(f"🔍 Buscando {N_IMAGES} imágenes para: {char['name']}")
    driver.get(f"https://www.pinterest.com/search/pins/?q={quote(char['name'] + ' demon slayer')}")
    time.sleep(5)

    # Scroll para cargar más pins y luego volver arriba
    for _ in range(4):
        driver.execute_script("window.scrollBy(0, 700);")
        time.sleep(1.2)
    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(1)

    # Obtener posición ABSOLUTA usando rect.top + scrollY para ordenar correctamente
    img_data = driver.execute_script("""
        var pins = document.querySelectorAll("div[data-test-id='pin']");
        var result = [];
        for (var i = 0; i < pins.length; i++) {
            var pin = pins[i];
            var img = pin.querySelector("img");
            if (!img) continue;
            var rect = pin.getBoundingClientRect();
            result.push({
                src: img.src || img.getAttribute('src') || '',
                naturalWidth: img.naturalWidth,
                x: rect.left,
                y: rect.top + window.scrollY
            });
        }
        return result;
    """)

    print(f"   📋 Pins encontrados: {len(img_data)}")

    # Ordenar como los ve el usuario: fila (tolerancia 40px) y columna
    img_data.sort(key=lambda p: (int(p['y'] // 40), p['x']))

    count = 0
    for item in img_data:
        if count >= N_IMAGES: break
        try:
            src = item.get('src', '')
            if not src or '75x75' in src or 'avatars' in src: continue
            if item.get('naturalWidth', 0) < 50: continue

            url = src
            for res in ["236x", "474x", "564x", "170x", "60x60"]:
                url = url.replace(res, "736x")

            resp = requests.get(url, stream=False, timeout=10)
            if resp.status_code != 200: continue

            data = resp.content
            if len(data) < MIN_FILE_SIZE: continue
            if not is_good_image(data): continue

            with open(os.path.join(RAW_DIR, f"{base_name}_{count + 1}.jpg"), 'wb') as f:
                f.write(data)
            print(f"   ✅ Guardada #{count + 1}")
            count += 1
        except: continue

    if count < N_IMAGES:
        print(f"   ⚠️  Solo {count}/{N_IMAGES} imágenes válidas para {char['name']}")

driver = setup_driver()
for char in chars:
    download_images(char, driver)
    time.sleep(2)
driver.quit()