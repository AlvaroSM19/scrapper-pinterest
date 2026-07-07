import os, json, glob, tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox

with open('config.json') as f: config = json.load(f)
N_IMAGES = config['images_per_character']
RAW_DIR = config['raw_dir']
FINAL_DIR = config['final_dir']

# Crear directorio final si no existe
os.makedirs(FINAL_DIR, exist_ok=True)

class Selector:
    def __init__(self, root):
        self.root = root
        self.root.title("Selector de Imágenes - Pinterest Scrapper")
        self.root.geometry("1400x800")
        self.root.configure(bg="#1e293b")
        
        self.names = self.get_pending()
        if not self.names:
            messagebox.showinfo("Listo", "✅ Todas las imágenes han sido seleccionadas!")
            self.root.quit()
            return
        
        self.idx = 0
        self.current_images = {}
        
        # Frame superior con información
        header = tk.Frame(root, bg="#0f172a")
        header.pack(fill=tk.X, padx=10, pady=10)
        self.label = tk.Label(header, text="", bg="#0f172a", fg="#22c55e", font=("Arial", 14, "bold"))
        self.label.pack(side=tk.LEFT)
        
        # Frame de grilla
        self.grid = tk.Frame(root, bg="#1e293b")
        self.grid.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        
        # Crear botones con mejor tamaño
        self.buttons = []
        for i in range(N_IMAGES):
            btn = tk.Button(self.grid, bg="#0f172a", bd=2, cursor="hand2", 
                          command=lambda idx=i: self.select(idx), width=20, height=15)
            btn.grid(row=i//4, column=i%4, padx=5, pady=5)
            self.buttons.append(btn)
            self.root.bind(str(i+1), lambda e, idx=i: self.select(idx))
        
        self.root.bind('<space>', lambda e: self.skip())
        self.load()

    def get_pending(self):
        if not os.path.exists(RAW_DIR):
            messagebox.showerror("Error", f"❌ Carpeta {RAW_DIR} no existe.\nEjecuta primero: python scrapper.py")
            exit()
        return sorted([os.path.basename(f).replace("_1.jpg", "") for f in glob.glob(f"{RAW_DIR}/*_1.jpg") 
                       if not os.path.exists(os.path.join(FINAL_DIR, f"{os.path.basename(f).replace('_1.jpg', '')}.webp"))])

    def load(self):
        if self.idx >= len(self.names):
            messagebox.showinfo("¡Listo!", "✅ ¡Todas las imágenes han sido seleccionadas correctamente!")
            self.root.quit()
            return
        
        base = self.names[self.idx]
        self.label.config(text=f"🎨 {base.upper()} ({self.idx + 1}/{len(self.names)}) - Presiona 1-8 para seleccionar o ESPACIO para saltar")
        
        self.current_images = {}
        for i in range(N_IMAGES):
            path = os.path.join(RAW_DIR, f"{base}_{i+1}.jpg")
            if os.path.exists(path):
                try:
                    img = Image.open(path)
                    img.thumbnail((300, 300), Image.Resampling.LANCZOS)
                    photo = ImageTk.PhotoImage(img)
                    self.current_images[i] = photo
                    self.buttons[i].config(image=photo, state=tk.NORMAL, text="")
                    self.buttons[i].image = photo
                except Exception as e:
                    print(f"Error cargando imagen {path}: {e}")
                    self.buttons[i].config(image='', state=tk.DISABLED, text=f"Error\n{i+1}")
            else:
                self.buttons[i].config(image='', state=tk.DISABLED, text=f"No existe\n{i+1}")

    def select(self, idx):
        base = self.names[self.idx]
        src_path = os.path.join(RAW_DIR, f"{base}_{idx+1}.jpg")
        dst_path = os.path.join(FINAL_DIR, f"{base}.webp")
        
        try:
            if not os.path.exists(src_path):
                messagebox.showerror("Error", f"❌ Archivo no encontrado: {src_path}")
                return
            
            with Image.open(src_path) as img:
                img_rgb = img.convert("RGB")
                img_rgb.save(dst_path, "webp", quality=85)
            
            print(f"✅ Guardada: {dst_path}")
            self.idx += 1
            self.load()
        except Exception as e:
            messagebox.showerror("Error al guardar", f"❌ Error: {str(e)}\n\nVerifica permisos en:\n{FINAL_DIR}")
            print(f"Error completo: {e}")

    def skip(self):
        self.idx += 1
        self.load()

if __name__ == "__main__":
    root = tk.Tk()
    app = Selector(root)
    root.mainloop()