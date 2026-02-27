from openai import OpenAI

import os
import subprocess
from datetime import datetime
from pathlib import Path
import textwrap

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
    # Windows costuma usar cp1252 no terminal. Git pode retornar bytes fora disso.
    # Por isso forçamos UTF-8 e evitamos quebrar em caracteres inválidos.
    result = subprocess.run(
        ["git", *command],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )

    if result.returncode != 0:
        raise RuntimeError((result.stderr or "").strip())

    return (result.stdout or "").strip()


def __now_stamps() -> tuple[str, str]:
    # data para aparecer no conteúdo (ISO) + timestamp para nome de arquivo
    dt = datetime.now()
    return dt.strftime("%Y-%m-%d"), dt.strftime("%Y%m%d-%H%M%S")


def __process_name() -> str:
    # Nome do "processo" que executou (normalmente o arquivo .py)
    return Path(__file__).name


def __safe_slug(s: str) -> str:
    # Evita caracteres ruins no nome do arquivo
    out = []
    for ch in s:
        if ch.isalnum() or ch in ("-", "_", "."):
            out.append(ch)
        elif ch.isspace():
            out.append("_")
    return ("".join(out).strip("_") or "run")[:90]


def __strip_md_fences(text: str) -> str:
    # Se o modelo responder com ```md ... ```, remove as cercas para salvar limpo
    t = text.strip()
    if t.startswith("```"):
        t = t.split("\n", 1)[1] if "\n" in t else t[3:]
        if t.endswith("```"):
            t = t[:-3]
    return t.strip()


def __save_md_history(md_text: str, current_branch: str, target_branch: str) -> Path:
    out_dir = Path("history")
    out_dir.mkdir(parents=True, exist_ok=True)  # garante que exista em qualquer repo

    today_iso, ts = __now_stamps()
    proc = __process_name()

    # Nome do arquivo: timestamp + processo + branches
    slug = __safe_slug(f"{proc}-{current_branch}-vs-{target_branch}")
    filename = f"{ts}-{slug}.md"

    path = out_dir / filename
    path.write_text(md_text, encoding="utf-8")
    return path

def main():
    # # 1) Verifica se está dentro de um repositório git
    try:
        run_git(["rev-parse", "--is-inside-work-tree"])
    except Exception:
        print("Você não está dentro de um repositório Git.")
        return

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
    # AQUI a diferença: pedimos para o modelo retornar APENAS Markdown com estrutura fixa
    today_iso, _ts = __now_stamps()
    proc = __process_name()

    SYSTEM_PROMPT_MD = textwrap.dedent(f"""
        Você é um revisor técnico. Retorne APENAS Markdown puro (sem cercas ```), seguindo exatamente esta estrutura:

        # Histórico do Agente — Review de Diff
        - Data: {today_iso}
        - Processo: {proc}
        - Branch atual: {current_branch}
        - Branch alvo: {target_branch}
        - Merge-base: {merge_base}

        ## Riscos e possíveis bugs
        - <itens>

        ## Testes recomendados
        - <itens>

        Regras:
        - Seja objetivo.
        - Não invente nada fora do diff.
        - Se não houver informação suficiente, diga explicitamente.
    """)

    response = client.responses.create(
        model="gpt-4.1-mini-2025-04-14",
        input=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT_MD,
            },
            {
                "role": "user",
                "content": f"""
Diff:
{diff}
""",
            },
        ],
        temperature=0.3,
        max_output_tokens=2048,
    )

    # Conteúdo em Markdown (já pronto para salvar)
    md_text = __strip_md_fences(response.output_text)

    # Salva histórico em .md (com data e processo no conteúdo e no nome do arquivo)
    saved_path = __save_md_history(md_text, current_branch, target_branch)

    # Retorna no chat/terminal o Markdown e informa onde salvou
    # print(md_text)
    print(f"\n[Salvo em: {saved_path}]")

# Código que deve rodar apenas quando o arquivo for executado diretamente.
# Código que pode ser reutilizado quando o arquivo for importado como módulo.
# import meu_script
if __name__ == "__main__":
    main()