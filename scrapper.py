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

MIN_FILE_SIZE = 12000

def download_images(char, driver):
    base_name = char['image_url'].split('/')[-1].replace('.webp', '')
    if all(os.path.exists(os.path.join(RAW_DIR, f"{base_name}_{i}.jpg")) for i in range(1, N_IMAGES + 1)):
        return

    print(f"🔍 Buscando {N_IMAGES} imágenes para: {char['name']}")
    driver.get(f"https://www.pinterest.com/search/pins/?q={quote(char['name'] + ' demon slayer')}")
    driver.execute_script("window.scrollTo(0, 800);")
    time.sleep(4)

    pins = driver.find_elements(By.CSS_SELECTOR, "div[data-test-id='pin']")
    sorted_pins = sorted(pins, key=lambda p: p.location['y'])

    count = 0
    for pin in sorted_pins:
        if count >= N_IMAGES: break
        try:
            img = pin.find_element(By.TAG_NAME, "img")
            src = img.get_attribute('src')
            if not src or "75x75" in src or "avatars" in src: continue

            url = src.replace("236x", "736x").replace("474x", "736x").replace("564x", "736x")
            resp = requests.get(url, stream=True)
            if resp.status_code == 200 and int(resp.headers.get('Content-Length', 0)) > MIN_FILE_SIZE:
                with open(os.path.join(RAW_DIR, f"{base_name}_{count + 1}.jpg"), 'wb') as f:
                    for chunk in resp.iter_content(1024): f.write(chunk)
                print(f"   ✅ Guardada #{count + 1}")
                count += 1
        except: continue

driver = setup_driver()
for char in chars:
    download_images(char, driver)
    time.sleep(2)
driver.quit()