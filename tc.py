from playwright.sync_api import sync_playwright
import time
import os

# Formulário para colar o caminho
pasta_base = input("Cole o caminho da pasta onde estão os arquivos PDF: ").strip()

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

    # Navegar até upload
    pagina.locator('xpath=//*[@id="navbarText"]/ul/li[6]/a').click()
    pagina.locator('xpath=/html/body/div[2]/div/div/div/div/form/button[3]').click()

    # Upload de arquivos
    for nome_arquivo in arquivos:
        caminho_completo = os.path.join(pasta_base, nome_arquivo)
        pagina.set_input_files('input[type="file"]', caminho_completo)
        pagina.locator('xpath=/html/body/div[2]/div/div/div/div/form/button').click()
        time.sleep(1)  # Pequena pausa para evitar erros em sequência rápida

    print("Todos os arquivos foram enviados com sucesso.")
    time.sleep(5)
    navegador.close()
