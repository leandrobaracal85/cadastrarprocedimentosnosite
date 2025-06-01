from playwright.sync_api import sync_playwright
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
        if not os.path.isfile(caminho_completo):
            print(f"Arquivo não encontrado: {caminho_completo}")
            continue
        print(f"Enviando {caminho_completo}")
        try:
            # Espera o input de arquivo estar visível
            pagina.wait_for_selector('input[type="file"]', state='visible', timeout=10000)
            pagina.set_input_files('input[type="file"]', caminho_completo)
            pagina.locator('xpath=/html/body/div[2]/div/div/div/div/form/button').click()
            time.sleep(1)
        except Exception as e:
            print(f"Erro ao enviar {nome}: {e}")

    time.sleep(5)
    navegador.close()
