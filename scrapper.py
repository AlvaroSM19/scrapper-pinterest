import os, json, time, requests, re
from urllib.parse import quote, unquote
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

MIN_FILE_SIZE = 12000
SEARCH_SUFFIX = 'BLUE LOCK'  # Cambia aquí el término extra de búsqueda

def get_pins_data(driver):
    """Extrae src y posición de todos los pins en una sola llamada JS, inmune a StaleElement."""
    return driver.execute_script("""
        var pins = document.querySelectorAll("div[data-test-id='pin']");
        var result = [];
        for (var i = 0; i < pins.length; i++) {
            try {
                var img = pins[i].querySelector("img");
                if (!img) continue;
                result.push({ src: img.src, y: pins[i].getBoundingClientRect().top });
            } catch(e) {}
        }
        return result;
    """) or []

def download_from_pinterest(char, driver, base_name, count, target):
    driver.get(f"https://www.pinterest.com/search/pins/?q={quote(char['name'] + ' ' + SEARCH_SUFFIX)}")
    driver.execute_script("window.scrollTo(0, 800);")
    time.sleep(4)
    pins_data = sorted(get_pins_data(driver), key=lambda p: p['y'])
    for item in pins_data:
        if count >= target: break
        try:
            src = item.get('src', '')
            if not src or "75x75" in src or "avatars" in src: continue
            url = src.replace("236x", "736x").replace("474x", "736x").replace("564x", "736x")
            resp = requests.get(url, stream=True)
            if resp.status_code == 200 and int(resp.headers.get('Content-Length', 0)) > MIN_FILE_SIZE:
                with open(os.path.join(RAW_DIR, f"{base_name}_{count + 1}.jpg"), 'wb') as f:
                    for chunk in resp.iter_content(1024): f.write(chunk)
                print(f"   ✅ Pinterest #{count + 1}")
                count += 1
        except: continue
    return count

def download_from_google(char, driver, base_name, count, target):
    driver.get(f"https://www.google.com/search?q={quote(char['name'] + ' ' + SEARCH_SUFFIX + ' anime')}&tbm=isch")
    time.sleep(3)
    seen = set()
    # Extraer URLs de imágenes originales desde los links de Google Images
    links = driver.execute_script("""
        var anchors = document.querySelectorAll('a[href*="imgurl="]');
        var result = [];
        for (var i = 0; i < anchors.length; i++) {
            result.push(anchors[i].getAttribute('href') || '');
        }
        return result;
    """) or []
    for href in links:
        if count >= target: break
        try:
            match = re.search(r'imgurl=(https?://[^&]+)', href)
            if not match: continue
            url = unquote(match.group(1))
            if url in seen: continue
            seen.add(url)
            resp = requests.get(url, stream=True, timeout=8)
            if resp.status_code == 200 and int(resp.headers.get('Content-Length', 0)) > MIN_FILE_SIZE:
                with open(os.path.join(RAW_DIR, f"{base_name}_{count + 1}.jpg"), 'wb') as f:
                    for chunk in resp.iter_content(1024): f.write(chunk)
                print(f"   ✅ Google #{count + 1}")
                count += 1
        except: continue
    return count

def download_images(char, driver):
    base_name = char['image_url'].split('/')[-1].replace('.webp', '')
    if all(os.path.exists(os.path.join(RAW_DIR, f"{base_name}_{i}.jpg")) for i in range(1, N_IMAGES + 1)):
        return

    half = N_IMAGES // 2
    print(f"🔍 {char['name']} — {half} Pinterest + {N_IMAGES - half} Google")
    count = download_from_pinterest(char, driver, base_name, 0, half)
    count = download_from_google(char, driver, base_name, count, N_IMAGES)

driver = setup_driver()
for char in chars:
    for intento in range(3):  # hasta 3 reintentos por personaje
        try:
            download_images(char, driver)
            break
        except Exception as e:
            print(f"   ⚠️  Error en {char['name']} (intento {intento+1}/3): {e}")
            time.sleep(3)
driver.quit()