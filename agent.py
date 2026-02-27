from openai import OpenAI

import os
import subprocess

# IMPORT de configurações do .env
from dotenv import load_dotenv

# Função auxiliar para executar comandos git
# variavel command tem de ser list[str] e o retorno da def run_git tem de ser -> str
def run_git(command: list[str]) -> str:
    """
    Executa um comando git e retorna a saída.
    Se der erro, lança exceção com a mensagem.
    """
    # Quando você usa subprocess, 
    # seu Python está pedindo para o sistema operacional executar outro programa como se você tivesse digitado no terminal.
    result = subprocess.run(["git", *command],capture_output=True,text=True)

    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip())

    return result.stdout.strip()


def main():
    # # 1) Verifica se está dentro de um repositório git
    # try:
    #     run_git(["rev-parse", "--is-inside-work-tree"])
    # except Exception:
    #     print("Você não está dentro de um repositório Git.")
    #     return
    
    # 2) Descobre a branch atual
    current_branch = run_git(["branch", "--show-current"])

    # 3) Define branch alvo
    target_branch = "main"

    # 4) Calcula merge-base
    merge_base = run_git(["merge-base", "HEAD", target_branch])

    # 5) Gera diff
    diff = run_git(["diff", "--no-color", f"{merge_base}..HEAD"])

    if not diff:
        print(f"Nenhuma diferença entre {current_branch} e {target_branch}.")
        return

    # Limite simples para evitar gastar muitos tokens
    MAX_CHARS = 50000
    if len(diff) > MAX_CHARS:
        diff = diff[:MAX_CHARS] + "\n\n[DIFF TRUNCADO]"

    # 6) Inicializa cliente OpenAI
    # Carrega variável da open ia do .env
    load_dotenv()
    client = OpenAI()

    # 7) Envia para o modelo
    response = client.responses.create(
        model="gpt-4.1-mini-2025-04-14",
        input=[
            {
                "role": "system",
                "content": (
                    "Você é um revisor técnico. "
                    "Explique de forma objetiva: resumo das mudanças, "
                    "possíveis riscos, bugs, testes recomendados."
                )
            },
            {
                "role": "user",
                "content": f"""
Branch atual: {current_branch}
Comparando com: {target_branch}

Diff:
{diff}
"""
            }
        ],
        temperature=0.3,
        max_output_tokens=2048,
    )

    print(response.output_text)

# Código que deve rodar apenas quando o arquivo for executado diretamente.
# Código que pode ser reutilizado quando o arquivo for importado como módulo.
# import meu_script

if __name__ == "__main__":
    main()