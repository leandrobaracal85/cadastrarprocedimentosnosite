from playwright.sync_api import sync_playwright, TimeoutError
import time
import sys
import os

# Recebe o caminho da pasta como argumento
if len(sys.argv) < 2:
    print("Uso: python inquerito.py /caminho/da/pasta")
    sys.exit(1)

pasta_base = sys.argv[1]

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
        print(f"Enviando {caminho_completo}")
        try:
            input_file = pagina.locator('input[type="file"]')
            input_file.wait_for(state="visible", timeout=20000)
            input_file.set_input_files(caminho_completo)
            pagina.locator('xpath=/html/body/div[2]/div/div/div/div/form/button').click()
            time.sleep(2)
        except TimeoutError:
            print(f"Erro: Timeout ao tentar enviar o arquivo {nome}. Verifique o estado da página.")

    time.sleep(5)
    navegador.close()
