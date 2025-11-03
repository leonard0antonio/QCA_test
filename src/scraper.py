from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from src.constants import IBGE_URL, ESTADOS
from src.utils import salvar_em_excel
import time

def coletar_dados_estado(page, estado: str):
    """Coleta as informações de um estado específico no site do IBGE."""
    page.goto(IBGE_URL)
    page.wait_for_load_state("networkidle")
    time.sleep(1)

    try:
        # Localiza e digita o estado no campo de busca
        page.wait_for_selector('input[placeholder="O que você procura?"]', timeout=20000)
        search_box = page.locator('input[placeholder="O que você procura?"]')
        search_box.click()

        for letra in estado:
            search_box.type(letra, delay=120)

        # Aguarda resultados e clica no primeiro correspondente
        page.wait_for_selector(".busca__auto-completar__resultado__item__nome", timeout=10000)
        resultado = page.locator(f".busca__auto-completar__resultado__item__nome:has-text('{estado}')")
        resultado.first.click()

        page.wait_for_load_state("domcontentloaded")
        time.sleep(1)

    except PlaywrightTimeoutError:
        print(f"⚠️ Campo de busca não encontrado para {estado}")
        return {"Estado": estado, "Erro": "Campo de busca não encontrado"}

    # inicia o dicionário do estado
    secoes = ["População", "Educação", "Trabalho e Rendimento", "Economia", "Território"]
    dados_estado = {secao: "N/A" for secao in secoes}
    dados_estado["Estado"] = estado

    # --- População (já aberta) ---
    try:
        titulo_xpath = '//*[@id="dados"]/panorama-resumo/div/table/tr[2]/td[2]'
        valor_xpath = '//*[@id="dados"]/panorama-resumo/div/table/tr[2]/td[3]/valor-indicador/div/span[1]'
        titulo = page.locator(f'xpath={titulo_xpath}').inner_text().strip()
        valor = page.locator(f'xpath={valor_xpath}').inner_text().strip()
        dados_estado["População"] = {titulo: valor}
        print(f"População → {titulo}: {valor}")
    except Exception as e:
        dados_estado["População"] = "N/A"
        print(f"População → Erro ao coletar dados: {e}")
    time.sleep(1)

    # --- Educação ---
    try:
        elemento = page.get_by_role("cell", name="Educação", exact=False).first
        elemento.scroll_into_view_if_needed()
        time.sleep(0.3)
        elemento.click()
        page.wait_for_load_state("domcontentloaded")
        time.sleep(1)

        titulo_xpath = '//*[@id="dados"]/panorama-resumo/div/table/tr[11]/td[2]'
        valor_xpath = '//*[@id="dados"]/panorama-resumo/div/table/tr[11]/td[3]/valor-indicador/div/span[1]'
        titulo = page.locator(f'xpath={titulo_xpath}').inner_text().strip()
        valor = page.locator(f'xpath={valor_xpath}').inner_text().strip()
        dados_estado["Educação"] = {titulo: valor}
        print(f"Educação → {titulo}: {valor}")
    except Exception as e:
        dados_estado["Educação"] = "N/A"
        print(f"Educação → Erro ao coletar dados: {e}")
    time.sleep(1)

    # --- Trabalho e Rendimento ---
    try:
        elemento = page.get_by_role("cell", name="Trabalho e rendimento", exact=False).first
        elemento.scroll_into_view_if_needed()
        time.sleep(0.3)
        elemento.click()
        page.wait_for_load_state("domcontentloaded")
        time.sleep(1)

        titulo_xpath = '//*[@id="dados"]/panorama-resumo/div/table/tr[28]/td[2]'
        valor_xpath = '//*[@id="dados"]/panorama-resumo/div/table/tr[28]/td[3]'
        titulo = page.locator(f'xpath={titulo_xpath}').inner_text().strip()
        valor = page.locator(f'xpath={valor_xpath}').inner_text().strip()
        dados_estado["Trabalho e Rendimento"] = {titulo: valor}
        print(f"Trabalho e Rendimento → {titulo}: {valor}")
    except Exception as e:
        dados_estado["Trabalho e Rendimento"] = "N/A"
        print(f"Trabalho e Rendimento → Erro ao coletar dados: {e}")
    time.sleep(1)

    # --- Economia ---
    try:
        elemento = page.get_by_role("cell", name="Economia", exact=False).first
        elemento.scroll_into_view_if_needed()
        time.sleep(0.3)
        elemento.click()
        page.wait_for_load_state("domcontentloaded")
        time.sleep(1)

        titulo_xpath = '//*[@id="dados"]/panorama-resumo/div/table/tr[41]/td[2]'
        valor_xpath = '//*[@id="dados"]/panorama-resumo/div/table/tr[41]/td[3]'
        titulo = page.locator(f'xpath={titulo_xpath}').inner_text().strip()
        valor = page.locator(f'xpath={valor_xpath}').inner_text().strip()
        dados_estado["Economia"] = {titulo: valor}
        print(f"Economia → {titulo}: {valor}")
    except Exception as e:
        dados_estado["Economia"] = "N/A"
        print(f"Economia → Erro ao coletar dados: {e}")
    time.sleep(1)

    # --- Território ---
    try:
        elemento = page.get_by_role("cell", name="Território", exact=False).first
        elemento.scroll_into_view_if_needed()
        time.sleep(0.3)
        elemento.click()
        page.wait_for_load_state("domcontentloaded")
        time.sleep(1)

        titulo_xpath = '//*[@id="dados"]/panorama-resumo/div/table/tr[54]/td[2]'
        valor_xpath = '//*[@id="dados"]/panorama-resumo/div/table/tr[54]/td[3]'
        titulo = page.locator(f'xpath={titulo_xpath}').inner_text().strip()
        valor = page.locator(f'xpath={valor_xpath}').inner_text().strip()
        dados_estado["Território"] = {titulo: valor}
        print(f"Território → {titulo}: {valor}")
    except Exception as e:
        dados_estado["Território"] = "N/A"
        print(f"Território → Erro ao coletar dados: {e}")
    time.sleep(1)

    # retorna o dicionário completo (inclui "Estado")
    print(dados_estado)
    return dados_estado


def coletar_todos_os_estados():
    """Executa a coleta de todos os estados e salva o resultado em Excel."""
    resultados = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        for estado in ESTADOS:
            print(f"Coletando dados de {estado}...")
            try:
                dados = coletar_dados_estado(page, estado)
                resultados.append(dados)
            except Exception as e:
                print(f"⚠️ Erro ao coletar dados de {estado}: {e}")
                continue

        browser.close()

    salvar_em_excel(resultados)
    print("✅ Coleta concluída com sucesso!")
    return resultados
