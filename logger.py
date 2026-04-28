
# Logger del Sistema


import logging

# Crear logger
logger = logging.getLogger("SoftwareFJ")
logger.setLevel(logging.DEBUG)

# Formato de los mensajes
formato = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(message)s"
)

# Guardar en archivo
archivo = logging.FileHandler("sistema.log", encoding="utf-8")
archivo.setLevel(logging.DEBUG)
archivo.setFormatter(formato)

# Mostrar en consola (opcional)
consola = logging.StreamHandler()
consola.setLevel(logging.INFO)
consola.setFormatter(formato)

# Evitar duplicados
if not logger.handlers:
    logger.addHandler(archivo)
    logger.addHandler(consola)
