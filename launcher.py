import os
import subprocess
import threading
import minecraft_launcher_lib as ml
import json

max_a = 1

def avp(actual):
    porcentaje = int((actual / max_a) * 100)
    print(f"Progreso: {actual}/{max_a} ({porcentaje}%)", end="\r")

def ave(texto):
    print("\n>>> Estado:", texto)

def avm(new_max):
    global max_a
    max_a = new_max

pcallback = {
    "setStatus": ave,
    "setMax": avm,
    "setProgress": avp
}

carpeta = r"F:\minelauncher"
os.makedirs(carpeta, exist_ok=True)

version = "1.12.2"
print(f"Descargando Mine {version} en {carpeta}")
ml.install.install_minecraft_version(version, carpeta, callback= pcallback)

opciones = {
    "Nombre": "Username",
    "uuid": "",
    "token": "",
    "jvmarguments": ["-Xmx4G", "Xms1G"],
}

comando = ml.command.get_minecraft_command(version, carpeta, opciones)
print("abriendo chetumare")
subprocess.Popen(comando)