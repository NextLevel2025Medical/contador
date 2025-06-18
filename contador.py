import logging
import webbrowser
import os

# Configura o log
logging.basicConfig(
    filename='log_execucao.txt',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Caminho do contador
contador_path = "contador.txt"

# Função para ler e atualizar o contador
def ler_contador():
    if not os.path.exists(contador_path):
        return 0
    with open(contador_path, "r") as f:
        return int(f.read().strip())

def salvar_contador(valor):
    with open(contador_path, "w") as f:
        f.write(str(valor))

# Execução principal
def main():
    contador = ler_contador()

    if contador >= 10:
        logging.info("Limite de 10 execuções atingido. Encerrando.")
        return

    webbrowser.open("https://ge.globo.com/")
    contador += 1
    salvar_contador(contador)
    logging.info(f"Abertura #{contador} realizada com sucesso.")

if __name__ == "__main__":
    main()
