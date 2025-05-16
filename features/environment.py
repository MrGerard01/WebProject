import os
import django
from selenium import webdriver
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager

def before_all(context):
    print("✅ Configurando entorno Django + Splinter")

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MyProject.settings')
    django.setup()

    # Configuración correcta del navegador
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")  # Opcional, para ejecutar sin interfaz gráfica

    # Inicializar el navegador en Splinter con Selenium WebDriver
    context.browser = Browser('chrome')

    context.get_url = lambda path: f"http://localhost:8000{path}"

    # Puedes importar aquí tus modelos y meterlos en el context
    from web.models import Videojuego
    context.Videojuego = Videojuego

def after_all(context):
    if hasattr(context, 'browser'):
        context.browser.quit()
