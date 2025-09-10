import automation
import requests

def test_conexao_internet():
    """Testa se há conexão com a internet"""
    try:
        response = requests.get("https://www.google.com", timeout=10)
        print(f"✅ Conexão com internet: Status {response.status_code}")
        return True
    except:
        print("❌ Sem conexão com a internet")
        return False

def test_chrome_driver():
    """Testa se o Chrome Driver funciona"""
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.chrome.service import Service
        from webdriver_manager.chrome import ChromeDriverManager
        
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )
        
        driver.get("about:blank")
        print("✅ Chrome Driver funciona")
        driver.quit()
        return True
    except Exception as e:
        print(f"❌ Erro no Chrome Driver: {e}")
        return False

def test_site_acessivel(url):
    """Testa se um site específico é acessível"""
    try:
        response = requests.get(url, timeout=15)
        print(f"✅ Site {url} acessível: Status {response.status_code}")
        return True
    except Exception as e:
        print(f"❌ Site {url} inacessível: {e}")
        return False

def test_diagnostic_completo():
    print("🧪 TESTE DE DIAGNÓSTICO COMPLETO")
    print("=" * 50)
    
    # Teste 1: Conexão com internet
    internet_ok = test_conexao_internet()
    
    # Teste 2: Chrome Driver
    chrome_ok = test_chrome_driver()
    
    # Teste 3: Sites de teste
    sites_test = [
        "https://www.google.com",
        "https://www.github.com", 
        "https://httpbin.org/status/200"
    ]
    
    for site in sites_test:
        test_site_acessivel(site)
    
    print("=" * 50)
    
    if internet_ok and chrome_ok:
        print("🚀 Testando automação completa...")
        try:
            # Usa um número de teste
            automation.run_automation(
                "https://www.google.com", 
                "+5511964455296",  # Número de teste
                "Teste diagnóstico"
            )
            print("✅ Automação executada com sucesso!")
        except Exception as e:
            print(f"❌ Erro na automação: {e}")
    else:
        print("⚠️ Corrija os problemas acima antes de testar a automação")

if __name__ == "__main__":
    test_diagnostic_completo() 
    