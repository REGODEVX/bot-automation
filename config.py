import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv() # Carga las variables desde el archivo .env

# Ruta absoluta
BASE_DIR = Path(__file__).resolve().parent

# Configuración URL
AMAZON_URL = "https://www.amazon.com"

# Configuración de logging
LOG_DIR = BASE_DIR / "logs"
LOG_FILE = LOG_DIR / "automation.log"

# Crea directorio de logs si no existe
LOG_DIR.mkdir(exist_ok=True)

# Configuración de la API .env
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", 8000))