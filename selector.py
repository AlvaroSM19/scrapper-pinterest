import os, json, glob, tkinter as tk
from PIL import Image, ImageTk

with open('config.json') as f: config = json.load(f)
N_IMAGES = config['images_per_character']
RAW_DIR = config['raw_dir']
FINAL_DIR = config['final_dir']

# Crear directorio si no existe
os.makedirs(FINAL_DIR, exist_ok=True)

class Selector:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1400x800")
        self.names = self.get_pending()
        self.idx = 0
        self.title_label = tk.Label(root, text="", bg="#1e293b", fg="white", font=("Arial", 13, "bold"))
        self.title_label.pack(pady=(8, 0))
        self.grid = tk.Frame(root, bg="#1e293b")
        self.grid.pack(expand=True, fill=tk.BOTH)
        self.buttons = [tk.Button(self.grid, bg="#0f172a", bd=2, cursor="hand2", command=lambda i=i: self.select(i)) for i in range(N_IMAGES)]
        for i, btn in enumerate(self.buttons):
            # Formato de grilla: 4 columnas por fila
            btn.grid(row=i//4, column=i%4, padx=5, pady=5)
            self.root.bind(str(i+1), lambda e, idx=i: self.select(idx))
        self.root.bind('<space>', lambda e: self.skip())
        self.load()

    def get_pending(self):
        return sorted([os.path.basename(f).replace("_1.jpg", "") for f in glob.glob(f"{RAW_DIR}/*_1.jpg") 
                       if not os.path.exists(os.path.join(FINAL_DIR, f"{os.path.basename(f).replace('_1.jpg', '')}.webp"))])

    def load(self):
        if self.idx >= len(self.names): self.root.quit(); return
        base = self.names[self.idx]
        self.title_label.config(text=f"{base}  ({self.idx + 1}/{len(self.names)})")
        for i in range(N_IMAGES):
            path = os.path.join(RAW_DIR, f"{base}_{i+1}.jpg")
            if os.path.exists(path):
                img = Image.open(path); img.thumbnail((300, 300))
                photo = ImageTk.PhotoImage(img)
                self.buttons[i].config(image=photo, state=tk.NORMAL); self.buttons[i].image = photo
            else: self.buttons[i].config(image='', state=tk.DISABLED)

    def select(self, idx):
        base = self.names[self.idx]
        src = os.path.join(RAW_DIR, f"{base}_{idx+1}.jpg")
        dst = os.path.join(FINAL_DIR, f"{base}.webp")
        with Image.open(src) as img:
            img.convert("RGB").save(dst, "webp", quality=100, method=6)
        self.idx += 1
        self.load()

    def skip(self): self.idx += 1; self.load()

root = tk.Tk()
Selector(root)
root.mainloop()