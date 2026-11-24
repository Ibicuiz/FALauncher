import os
import sys
import subprocess
import threading
import webview
import minecraft_launcher_lib

if getattr(sys, "frozen", False):
    RESOURCE_DIR = sys._MEIPASS
else:
    RESOURCE_DIR = os.path.dirname(os.path.abspath(__file__))

MINECRAFT_DIR = os.path.join(os.path.expanduser("~"), "Documents", "FALauncher")
FONDOS_DIR = os.path.join(RESOURCE_DIR, "ui", "fondos")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FONDOS_DIR = os.path.join(BASE_DIR, "ui", "fondos")


class Api:
    def __init__(self):
        self._ventana = None
        self._max_pasos = 1

    def _set_status(self, texto):
        if self._ventana:
            limpio = texto.replace("'", "\\'")
            self._ventana.evaluate_js(f"actualizarEstado('{limpio}')")

    def _set_max(self, nuevo_max):
        self._max_pasos = nuevo_max if nuevo_max > 0 else 1

    def _set_progress(self, actual):
        if self._ventana:
            porcentaje = int((actual / self._max_pasos) * 100)
            self._ventana.evaluate_js(f"actualizarProgreso({porcentaje})")

    def obtener_fondo(self, nombre_tema):
        if nombre_tema == "minimal" or not os.path.exists(FONDOS_DIR):
            return ""
        for archivo in os.listdir(FONDOS_DIR):
            nombre, ext = os.path.splitext(archivo)
            if nombre.lower() == nombre_tema.lower() and ext.lower() in [".jpg", ".jpeg", ".png", ".webp"]:
                return f"fondos/{archivo}"
        return ""

    def iniciar_juego(self, usuario, version, ram):
        threading.Thread(
            target=self._proceso_jugar, args=(usuario, version, ram), daemon=True
        ).start()

    def _proceso_jugar(self, usuario, version, ram):
        usuario = usuario.strip() or "Steve"
        try:
            os.makedirs(MINECRAFT_DIR, exist_ok=True)
            callback = {
                "setStatus": self._set_status,
                "setMax": self._set_max,
                "setProgress": self._set_progress,
            }

            self._set_status(f"Verificando {version}...")
            minecraft_launcher_lib.install.install_minecraft_version(
                version, MINECRAFT_DIR, callback=callback
            )

            opciones = {
                "username": usuario,
                "uuid": "",
                "token": "",
                "jvmArguments": [f"-Xmx{ram}G", "-Xms1G"],
            }

            self._set_status("Abriendo Minecraft...")
            comando = minecraft_launcher_lib.command.get_minecraft_command(
                version, MINECRAFT_DIR, opciones
            )
            subprocess.Popen(comando)
            self._set_status(f"¡{version} iniciado!")
        except Exception as e:
            self._set_status(f"Error: {str(e)}")


if __name__ == "__main__":
    api = Api()
    ruta_html = os.path.join(BASE_DIR, "ui", "index.html")
    ventana = webview.create_window(
        "FALauncher", ruta_html, js_api=api, width=960, height=600, resizable=False
    )
    api._ventana = ventana
    webview.start()
