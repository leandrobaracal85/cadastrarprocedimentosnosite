# inquerito.py
from playwright.sync_api import sync_playwright
import time
import sys
import os

if len(sys.argv) < 2:
    print("Uso: python inquerito.py <numero_da_pasta>")
    sys.exit(1)

pasta_base = f"/root/inqueritos/Inquéritos/{sys.argv[1]}"
arquivos = ["capa.pdf", "extrato.pdf", "bo.pdf", "portaria.pdf"]

with sync_playwright() as p:
    navegador = p.chromium.launch(headless=True)
    pagina = navegador.new_page()
    pagina.goto("https://lebaracal.com/delegacia/visualizar.php")
    pagina.fill('xpath=/html/body/div[1]/form/div[1]/input', 'leandrobaracal85@gmail.com')
    pagina.fill('xpath=//*[@id="senha"]', 'Polici@1402') 
    pagina.locator('xpath=/html/body/div[1]/form/div[2]/button').click()
    pagina.locator('xpath=//*[@id="navbarText"]/ul/li[6]/a').click()
    pagina.locator('xpath=/html/body/div[2]/div/div/div/div/form/button[1]').click()

    for nome in arquivos:
        caminho_completo = os.path.join(pasta_base, nome)
        print(f"Enviando {caminho_completo}")
        if not os.path.isfile(caminho_completo):
            print(f"Arquivo não encontrado: {caminho_completo}")
            continue
        pagina.wait_for_selector('input[type="file"]', timeout=10000)
        pagina.set_input_files('input[type="file"]', caminho_completo)
        pagina.locator('xpath=/html/body/div[2]/div/div/div/div/form/button').click()
        time.sleep(1)

    time.sleep(5)
    navegador.close()
