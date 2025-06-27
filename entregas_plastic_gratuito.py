import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select

LOG_PATH = "Entregas Plastic .txt"

def escreve_log(msg):
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    linha = f"{timestamp} {msg}"
    print(linha)
    with open(LOG_PATH, "a", encoding="utf-8") as log:
        log.write(linha + "\n")

# 🔹 Mensagem inicial
escreve_log("🚚 Entrega Plastic sendo Realizada")

def extrair_e_ativar_aulas(driver, vitrine_id, nome_vitrine):
    escreve_log(f"\n🔎 Buscando aulas da vitrine {vitrine_id} – {nome_vitrine}")

    blocos = driver.find_elements(By.CSS_SELECTOR, f'div.acesso-item[data-vitrine_id="{vitrine_id}"]')
    if not blocos:
        escreve_log(f"⚠️ Nenhuma aula encontrada para a vitrine {vitrine_id}")
        return []

    for idx, bloco in enumerate(blocos):
        try:
            nome_elem = bloco.find_element(By.CSS_SELECTOR, "div.acesso-nome")
            nome_aula = nome_elem.text.strip()
            checkbox = bloco.find_element(By.CSS_SELECTOR, 'input[type="checkbox"]')
            slider = bloco.find_element(By.CSS_SELECTOR, "label.switch span.slider")

            if idx < 2:
                # Aula é uma das 2 mais recentes
                if checkbox.is_selected():
                    escreve_log(f"{idx+1}. {nome_aula} – ✅ Já está ativado.")
                else:
                    escreve_log(f"{idx+1}. {nome_aula} – ⚠️ Está desativado. Ativando...")
                    slider.click()
                    time.sleep(1)

                # Preencher duração (sempre que ativar ou garantir)
                select_duracao = bloco.find_element(By.CSS_SELECTOR, 'select[id*="acessoDuracaoTipo"]')
                Select(select_duracao).select_by_visible_text("Dias")
                escreve_log("📅 Tipo de duração setado como 'Dias'.")

                input_dias = bloco.find_element(By.CSS_SELECTOR, 'input[id*="acessoDuracao"]')
                input_dias.clear()
                input_dias.send_keys("15")
                escreve_log("🕒 Duração preenchida com 15 dias.")
                time.sleep(1)

            else:
                # Demais aulas – devem estar desativadas
                if checkbox.is_selected():
                    escreve_log(f"{idx+1}. {nome_aula} – ❌ Aula antiga ainda está ativa. Desativando...")
                    slider.click()
                    time.sleep(0.5)
                else:
                    escreve_log(f"{idx+1}. {nome_aula} – 🔕 Já está desativada.")

        except Exception as e:
            escreve_log(f"❌ Erro ao processar aula {idx+1} da vitrine {vitrine_id}: {e}")

# --- CONFIGURAÇÃO DO CHROME ---
chrome_options = Options()
chrome_options.add_argument("--headless=new")  # Executa sem mostrar o navegador
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
servico = Service()
driver = webdriver.Chrome(service=servico, options=chrome_options)

try:
    escreve_log("▶️ Acessando página de login")
    driver.get("https://members.nextlevelmedical.com.br/auth/login")
    time.sleep(2)

    # Login
    driver.find_element(By.ID, "AcessoEmail").send_keys("jpedroamorimsilva@gmail.com")
    escreve_log("✅ E-mail inserido")

    driver.find_element(By.ID, "AcessoSenha").send_keys("110303Jes")
    escreve_log("✅ Senha inserida")

    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    escreve_log("🔓 Clicado no botão 'Entrar'")
    time.sleep(5)

    # Ir para a vitrine de integração
    escreve_log("➡️ Acessando a tela de integração")
    driver.get("https://members.nextlevelmedical.com.br/office/vitrine/integracao/edit/168529")
    time.sleep(5)
    
    # Processar as vitrines
    extrair_e_ativar_aulas(driver, "72313", "The One Hour Learning League Plastic")
    extrair_e_ativar_aulas(driver, "96527", "The One Hour Learning League Recovery")
    extrair_e_ativar_aulas(driver, "75856", "The One Hour Learning League Business")

    # Clicar no botão "Salvar Alterações"
    try:
        salvar_btn = driver.find_element(By.CSS_SELECTOR, "button.btn.btn-lg.btn-form.btn-primary.float-button")
        salvar_btn.click()
        escreve_log("💾 Botão 'Salvar Alterações' clicado com sucesso.")
        time.sleep(3)
    except Exception as e:
        escreve_log(f"❌ Erro ao clicar no botão 'Salvar Alterações': {e}")

    input("\n🟡 Pressione ENTER para encerrar e fechar o navegador...")

except Exception as e:
    escreve_log(f"❌ Erro geral: {e}")

finally:
    driver.quit()
    escreve_log("🛑 Navegador fechado. Processo encerrado.")
