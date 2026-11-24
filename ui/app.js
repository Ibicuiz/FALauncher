async function cambiarTema(tema) {
  document.documentElement.setAttribute('data-tema', tema);

  // Le pide a Python la ruta real de la imagen (sin importar si es .jpg o .png)
  if (window.pywebview && window.pywebview.api) {
    const rutaImagen = await pywebview.api.obtener_fondo(tema);
    if (rutaImagen) {
      document.body.style.backgroundImage = `url('${rutaImagen}')`;
    } else {
      document.body.style.backgroundImage = ''; // Usa el degradado CSS de respaldo
    }
  }
}

// Carga el fondo inicial apenas pywebview está listo
window.addEventListener('pywebviewready', () => {
  cambiarTema('aero');
});

function jugar() {
  const user = document.getElementById('usuario').value;
  const ver = document.getElementById('version').value;
  const ram = document.getElementById('ram').value;

  document.getElementById('btn-jugar').disabled = true;
  document.getElementById('barra-box').style.display = 'block';
  document.getElementById('barra').style.width = '0%';

  pywebview.api.iniciar_juego(user, ver, ram);
}

function actualizarEstado(texto) {
  document.getElementById('estado').innerText = texto;
  if (texto.includes('iniciado') || texto.includes('Error')) {
    document.getElementById('btn-jugar').disabled = false;
  }
}

function actualizarProgreso(porcentaje) {
  document.getElementById('barra').style.width = porcentaje + '%';
}
