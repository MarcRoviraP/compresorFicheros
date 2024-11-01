import tkinter as tk
from tkinter import filedialog
from tkinterdnd2 import DND_FILES, TkinterDnD
import os
from PIL import Image

rutas = []

# Función para manejar el evento de arrastrar y soltar
def on_drop(event):
    file_paths = event.data.split()  # Dividir para obtener una lista de rutas
    for path in file_paths:
        rutas.append(path)
        listbox.insert(tk.END, path)  # Insertar cada ruta en la lista

# Configurar la ventana principal
root = TkinterDnD.Tk()
root.title("Image Compressor")
root.geometry("600x400")

# Crear una lista para mostrar las rutas de los archivos
listbox = tk.Listbox(root, width=80, height=20)
listbox.pack(pady=20)

# Configurar el widget para permitir arrastrar y soltar
listbox.drop_target_register(DND_FILES)
listbox.dnd_bind('<<Drop>>', on_drop)

btnConvertir = tk.Button(root, text="Convert", command=lambda: convertir())
btnConvertir.pack(pady=10)

#Accion al pulsar encima del listbox

listbox.bind("<Button-1>", lambda x: asignar())

def asignar():
    global listbox
    resultado = list(filedialog.askopenfilenames())
    print(resultado)
    for file in resultado:

        listbox.insert(tk.END, file)
        rutas.append(file)

def guardarEn():
    global rutaGuardar
    rutaGuardar = filedialog.askdirectory()
    print(rutaGuardar)

# Función para convertir las imágenes
def convertir():
    global rutas  # Declarar que se usa la variable global `rutas`
    if not rutas:
        return
    guardarEn()
    for ruta in rutas:
        # Si la ruta es un directorio, añadir las rutas de los archivos que contiene
        if os.path.isdir(ruta):
            for i in os.listdir(ruta):
                if os.path.isdir(f"{ruta}/{i}"):
                    continue
                rutas.append(f"{ruta}/{i}")
            continue

        llista = ruta.split("/")
        extensio = llista[-1].split(".")[1]

        if extensio in ["png", "jpg", "jpeg", "webp"]:
            img = Image.open(ruta)
            img.save(rutaGuardar + f"/compressed_{llista[-1]}", optimize=True, quality=60)

    rutas.clear()
    # Vaciar la listbox
    listbox.delete(0, tk.END)

# Ejecutar la aplicación
root.mainloop()
