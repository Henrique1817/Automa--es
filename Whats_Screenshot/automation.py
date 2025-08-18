import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pywhatkit as kit

def run_automation( website_url, phone_number):
    # Configuração para o Chrome em segundo plano
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    #inicializando o servidor
    driver=webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )

    try:
        # Acessar o site
        driver.get(website_url)
        time.sleep(10)

        screenshot_path = os.path.join(os.getcwd(), "website_screenshot.png")
        driver.save_screenshot(screenshot_path)

        # Enviar para o WhatsApp
        time.sleep(10)
        kit.sendwhats_image(phone_number, screenshot_path, "Print do site solicitado", tab_close=True)

        # Remove o screenshot após o envio
        time.sleep(30)
        if os.path.exists(screenshot_path):
            os.remove(screenshot_path)

    finally:
        driver.quit()
