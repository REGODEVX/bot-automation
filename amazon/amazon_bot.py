import logging
from playwright.sync_api import sync_playwright
from config import AMAZON_URL, LOG_FILE

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format= "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler() # IMPRESIÓN EN CONSOLA
    ]
)

logger = logging.getLogger(__name__)

class AmazonAutomation:
    # Constructor de la clase
    def __init__(self, mode: str = "headless"):
        self.mode = mode.lower() == "headed"
        self.playwright = sync_playwright().start() # Inicia Playwright
        self.browser = self.playwright.chromium.launch(
            headless=not self.mode,
            slow_mo=1000,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            ]
        )
        self.context = self.browser.new_context(
            viewport={"width": 1280, "height": 1024},
            locale="en-US",
            geolocation={"latitude": 40.71, "longitude": -74.01},
            permissions=["geolocation"]
        ) # Contexto de navegador
        self.page = self.context.new_page() # Nueva pestaña
        logger.info("Navegador iniciado en modo %s", "headed" if self.mode else "headless")
    
    def login(self, email: str, password: str):
        try:
            logger.info("Iniciando sesión en Amazon")

            self.page.goto(f"{AMAZON_URL}/gp/css/account/address/view.html?ref_=nav_AccountFlyout_addressbook")

            # LOGUEO EN FORMULARIO
            self.page.wait_for_selector('input[name="email"]', timeout=5000)
            self.page.fill('input[name="email"]', email)
            
            self.page.click("#continue")

            self.page.wait_for_selector('input[name="password"]', timeout=5000)
            self.page.fill('input[name="password"]', password)
            self.page.click("#signInSubmit")

            logger.info("Sesión iniciada correctamente")
            return True

        except Exception as e:
            logger.error(f"Error al iniciar sesión: {e}")
            return False
        
    def simulate_purchase(self, email: str, password: str):
        try:
            if not self.login(email, password):
                return False
            
            return True

        except Exception as e:
            logger.error(f"Error durante la automatización: {str(e)}")
            return False

        finally:
            self.close()

    def close(self):
        self.context.close()
        self.browser.close()
        self.playwright.stop()
        logger.info("Navegador cerrado")

        

        
