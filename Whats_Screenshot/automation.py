import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import mss
import mss.tools
import pywhatkit as kit
import logging
from datetime import datetime

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def run_automation(website_url, phone_number, mens):
    logger.info(f"Iniciando automação para: {website_url}")
    
    # Configuração otimizada para Chrome headless
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")  # Nova sintaxe para headless
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--remote-debugging-port=9222")
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)

    driver = None
    try:
        # Inicializando o driver
        logger.info("Inicializando driver Chrome...")
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )
        
        # Executar script para evitar detecção
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        logger.info(f"Acessando site: {website_url}")
        
        # Primeiro teste de conexão
        driver.get("about:blank")
        time.sleep(2)
        
        # Agora acessa o site real
        driver.get(website_url)
        
        # Espera com timeout mais inteligente
        try:
            WebDriverWait(driver, 15).until(
                lambda d: d.execute_script('return document.readyState') == 'complete'
            )
            logger.info("Página carregada completamente")
        except:
            logger.warning("Timeout no carregamento, continuando mesmo assim...")
        
        time.sleep(3)  # Espera adicional
        
        # Verifica se a página carregou corretamente
        page_title = driver.title
        page_url = driver.current_url
        logger.info(f"Título da página: {page_title}")
        logger.info(f"URL atual: {page_url}")
        
        # Tenta várias estratégias para obter dimensões
        try:
            total_height = driver.execute_script("""
                return Math.max(
                    document.body.scrollHeight,
                    document.body.offsetHeight,
                    document.documentElement.clientHeight,
                    document.documentElement.scrollHeight,
                    document.documentElement.offsetHeight
                );
            """)
            
            total_width = driver.execute_script("""
                return Math.max(
                    document.body.scrollWidth,
                    document.body.offsetWidth, 
                    document.documentElement.clientWidth,
                    document.documentElement.scrollWidth,
                    document.documentElement.offsetWidth
                );
            """)
            
            logger.info(f"Dimensões calculadas: {total_width}x{total_height}")
            
            # Limita tamanho máximo para evitar problemas
            total_width = min(total_width, 3840)
            total_height = min(total_height, 2160)
            
            driver.set_window_size(total_width, total_height)
            time.sleep(2)
            
        except Exception as e:
            logger.warning(f"Erro ao obter dimensões, usando padrão: {e}")
            total_width, total_height = 1920, 1080
            driver.set_window_size(total_width, total_height)
        
        # Captura de tela com MSS
        screenshot_path = os.path.join(os.getcwd(), "website_screenshot.png")
        logger.info(f"Capturando screenshot: {screenshot_path}")
        
        try:
            with mss.mss() as sct:
                # Tenta capturar a tela inteira
                monitor = sct.monitors[1]  # Monitor principal
                sct_img = sct.grab(monitor)
                
                # Salva a imagem
                mss.tools.to_png(sct_img.rgb, sct_img.size, output=screenshot_path)
                logger.info("✅ Screenshot capturado com sucesso!")
                
        except Exception as e:
            logger.error(f"❌ Erro ao capturar screenshot: {e}")
            # Fallback: usa método do Selenium
            try:
                driver.save_screenshot(screenshot_path)
                logger.info("✅ Screenshot de fallback capturado!")
            except Exception as fallback_error:
                logger.error(f"❌ Erro no fallback também: {fallback_error}")
                raise

        # Verifica se o arquivo foi criado
        if os.path.exists(screenshot_path):
            file_size = os.path.getsize(screenshot_path)
            logger.info(f"✅ Arquivo criado. Tamanho: {file_size} bytes")
            
            # Tenta enviar para WhatsApp
            try:
                logger.info("Tentando enviar para WhatsApp...")
                timestamp = datetime.now().strftime("%H:%M:%S")
                kit.sendwhats_image(phone_number, screenshot_path, f"{mens} - {timestamp}", tab_close=True, wait_time=20)
                logger.info("✅ Mensagem enviada com sucesso!")
                
            except Exception as whatsapp_error:
                logger.error(f"❌ Erro ao enviar para WhatsApp: {whatsapp_error}")
                # Continua mesmo com erro no WhatsApp
                
        else:
            logger.error("❌ Arquivo de screenshot não foi criado!")
            raise Exception("Screenshot não foi criado")

    except Exception as e:
        logger.error(f"❌ Erro durante a automação: {e}")
        raise e
        
    finally:
        if driver:
            try:
                driver.quit()
                logger.info("Driver fechado")
            except:
                pass
        
        # Remove o screenshot após algum tempo
        time.sleep(10)
        try:
            if os.path.exists(screenshot_path):
                os.remove(screenshot_path)
                logger.info("Screenshot removido")
        except:
            pass