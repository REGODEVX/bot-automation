import logging
from playwright.sync_api import sync_playwright
from config import AMAZON_URL, LOG_FILE
from time import sleep

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

    def search_product(self):
        try:
            logger.info("Buscando producto..")
            
            # Paso 1: Abrir el menú "Todo"
            self.page.goto(AMAZON_URL)
            self.page.wait_for_selector('#nav-hamburger-menu', timeout=5000)
            self.page.click("#nav-hamburger-menu")
            logger.info("Menú 'Todo' abierto")

            # Paso 2: Seleccionar "Electrónicos"
            self.page.wait_for_selector('a.hmenu-item:has-text("Electrónicos")', timeout=5000)
            self.page.click('a.hmenu-item:has-text("Electrónicos")')
            logger.info("selección Electrónicos seleccionada")

            # Paso 3: Seleccionar "Televisión y Video"
            self.page.wait_for_selector('#hmenu-content', state='visible', timeout=5000)
            tv_link_selector = 'ul[data-menu-id="6"] a:has-text("Televisión y video")'
            self.page.wait_for_selector(tv_link_selector, state='visible', timeout=5000)
            tv_link = self.page.locator(tv_link_selector).last
            tv_link.hover()
            tv_link.click(timeout=15000)

            logger.info("Sección 'Televisión y Video' seleccionada")
            return True
            
        except Exception as e:
            logger.error(f"Error al buscar el producto: {e}")
            return False

    def select_product(self):
        try:
            logger.info("Seleccionando primer producto de la lista")

            first_product = self.page.query_selector("div[data-component-type='s-search-result'] a.a-link-normal") #Encuentra el primer enlace del primer producto

            if first_product:
                product_url = f"{AMAZON_URL}{first_product.get_attribute('href')}"
                self.page.goto(product_url) #Navega al prodcuto

                logger.info("Página de producto cargada")
                return True

            logger.error("No se encontraron productos")
            return False

        except Exception as e:
            logger.error(f"Error al seleccinar el producto: {e}")
            return False

    def add_to_cart(self):
        try:
            logger.info("Añadiendo producto al carrito")

            # Añadir producto al carrito
            self.page.wait_for_selector('input[name="submit.add-to-cart"]', timeout=5000)
            self.page.click('input[name="submit.add-to-cart"]')

            logger.info("Producto añadido al carrito")
            return True

        except Exception as e:
            logger.error(f"Error al añadir el producto al carrito: {e}")
            return False

    def proceed_to_checkout(self):
        try:
            logger.info("Procediendo al checkout")

            # Ir al carrito
            self.page.goto(f"{AMAZON_URL}/gp/cart/view.html")

            # Procesar la compra
            self.page.wait_for_selector('input[name="proceedToRetailCheckout"]', timeout=5000)
            self.page.click('input[name="proceedToRetailCheckout"]')

            sleep(3)
            logger.info("Compra correcta...")
            return True

        except Exception as e:
            logger.error(f"Error al procesar checkout: {e}")
            return False

    def simulate_purchase(self, email: str, password: str):
        try:
            if not self.login(email, password):
                return False
            
            if not self.search_product():
                return False
            
            if not self.select_product():
                return False
            
            if not self.add_to_cart():
                return False
            
            return self.proceed_to_checkout()

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

        

        
