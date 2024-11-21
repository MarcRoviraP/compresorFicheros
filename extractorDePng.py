import os,shutil,time
from functools import lru_cache
start_time = time.time()

FORMATO_BUSCAR = ".png"
NOM_DESTI = f"F{FORMATO_BUSCAR}"
CARPETAS_EXCLUIR = ["Program Files", "Windows", "AppData", "usr", "bin", "lib",NOM_DESTI]


def carpetesExcluides(ruta):
    for i in CARPETAS_EXCLUIR:
        if i in ruta:
            return True
    return False

@lru_cache
def buscarEnMiInterior(ruta):
    if ruta.endswith(FORMATO_BUSCAR):
        
        accio = f"{os.getcwd()}/{NOM_DESTI}"

        try:
            # Reemplazar las barras invertidas por barras normales
            ruta = ruta.replace("\\","/")
            ruta = ruta.replace("//","/")
            accio = accio.replace("\\","/")
            shutil.copy2(ruta,accio)
            print(f"Fitxer copiat: {ruta}")
        except:
            pass
    else:
        for i in os.listdir(ruta):

            try:
                if not carpetesExcluides(ruta):
                    buscarEnMiInterior(f"{ruta}/{i}")

               
            except:
                pass



try:
    os.mkdir(NOM_DESTI)
except:
    pass



   

import winreg

def obtener_rutas_aplicaciones_windows():
    rutas_excluir = []
    claves = [
        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
        r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
    ]

    for clave in claves:
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, clave) as reg_key:
                for i in range(0, winreg.QueryInfoKey(reg_key)[0]):
                    sub_key_name = winreg.EnumKey(reg_key, i)
                    with winreg.OpenKey(reg_key, sub_key_name) as sub_key:
                        try:
                            ruta_instalacion = winreg.QueryValueEx(sub_key, "InstallLocation")[0]
                            if ruta_instalacion:
                                rutas_excluir.append(ruta_instalacion)
                        except FileNotFoundError:
                            pass
        except FileNotFoundError:
            pass

    return rutas_excluir


# Definir las unidades de disco a explorar
# En sistemas Windows
if hasattr(os, 'listdrives'):
    drives = os.listdrives()
    # Obtener rutas de aplicaciones
    rutas_aplicaciones = obtener_rutas_aplicaciones_windows()

# Remplazar las barras invertidas por barras normales
    rutas_aplicaciones = [ruta.replace("\\", "/") for ruta in rutas_aplicaciones]
    excluidas = drives + rutas_aplicaciones
else:
    drives = ['/']  # En sistemas Unix/Linux, puedes comenzar desde la raíz


for drive in drives:
    buscarEnMiInterior(drive)

print(f"Temps d'execució: {time.time() - start_time} segons")