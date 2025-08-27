import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pywhatkit as kit

def run_automation( website_url, phone_number, mens):
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
        
        # FUNÇÃO PARA SCREENSHOT DA TELA INTEIRA
        def take_full_page_screenshot(driver, file_path):
            # Obtém a altura total da página
            
            total_height = driver.execute_script(
                "return document.body.scrollHeight,"
                "document.body.offsetHeight, "
                "document.documentElement.clientHeight, "
                "document.documentElement.scrollHeight, "
                "document.documentElement.offsetHeight)"
            )
            
            # Obtém a largura total
            total_width = driver.execute_script(
                "return document.body.scrollWidth"
                "document.body.offsetWidth, "
                "document.documentElement.clientWidth, "
                "document.documentElement.scrollWidth, "
                "document.documentElement.offsetWidth)"
            )

            # Configura a janela para o tamanho total
            print(total_height,total_width)
            driver.set_window_size(total_width, total_height)
            time.sleep(3)  # Espera o redimensionamento
            
            # Tira o screenshot
            driver.save_screenshot(file_path)
            print(f"Screenshot completo salvo! Dimensões: {total_width}x{total_height}px")

        screenshot_path = os.path.join(os.getcwd(), "website_screenshot.png")
        take_full_page_screenshot(driver, screenshot_path)

        # Enviar para o WhatsApp
        time.sleep(10)
        kit.sendwhats_image(phone_number, screenshot_path, mens, tab_close=True)

        # Remove o screenshot após o envio
        time.sleep(30)
        if os.path.exists(screenshot_path):
            os.remove(screenshot_path)

    finally:
        driver.quit()
