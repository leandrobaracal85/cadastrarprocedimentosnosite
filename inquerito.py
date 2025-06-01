from playwright.sync_api import sync_playwright
import time
import sys
import os

# Caminho base no servidor (VPS Linux)
CAMINHO_BASE_VPS = "/root/inqueritos/Leandro Delegacia/Procedimentos/Inquéritos"

# Verifica se o número da pasta foi passado
if len(sys.argv) < 2:
    print("Uso: python inquerito.py <numero_da_pasta>")
    sys.exit(1)

numero_pasta = sys.argv[1]
pasta_base = os.path.join(CAMINHO_BASE_VPS, numero_pasta)

# Arquivos esperados
arquivos = ["capa.pdf", "extrato.pdf", "bo.pdf", "portaria.pdf"]

with sync_playwright() as p:
    navegador = p.chromium.launch(headless=True)
    pagina = navegador.new_page()
    pagina.goto("https://lebaracal.com/delegacia/visualizar.php")

    # Login
    pagina.fill('xpath=/html/body/div[1]/form/div[1]/input', 'leandrobaracal85@gmail.com')
    pagina.fill('xpath=//*[@id="senha"]', 'Polici@1402') 
    pagina.locator('xpath=/html/body/div[1]/form/div[2]/button').click()

    # Acessa página de inquéritos
    pagina.locator('xpath=//*[@id="navbarText"]/ul/li[6]/a').click()
    pagina.locator('xpath=/html/body/div[2]/div/div/div/div/form/button[1]').click()

    # Envia os arquivos PDF
    for nome in arquivos:
        caminho_completo = os.path.join(pasta_base, nome)
        if not os.path.exists(caminho_completo):
            print(f"Arquivo não encontrado: {caminho_completo}")
            continue
        print(f"Enviando {caminho_completo}")
        pagina.wait_for_selector('input[type="file"]', timeout=10000)
        pagina.set_input_files('input[type="file"]', caminho_completo)
        pagina.locator('xpath=/html/body/div[2]/div/div/div/div/form/button').click()
        time.sleep(1)

    time.sleep(5)
    navegador.close()
