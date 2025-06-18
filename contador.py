import logging
import os

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

exec_counter_file = "/tmp/exec_counter.txt"

def obter_execucoes():
    if os.path.exists(exec_counter_file):
        with open(exec_counter_file, "r") as f:
            try:
                return int(f.read().strip())
            except:
                return 0
    return 0

def salvar_execucoes(contador):
    with open(exec_counter_file, "w") as f:
        f.write(str(contador))

def main():
    contador = obter_execucoes() + 1
    salvar_execucoes(contador)
    logging.info(f"🟢 Execução #{contador} realizada com sucesso.")

if __name__ == "__main__":
    main()

