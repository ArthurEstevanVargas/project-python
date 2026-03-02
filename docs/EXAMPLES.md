# Exemplos de Uso

## Git Review Agent

### Exemplo 1: Review Básico

```bash
# Você está na branch 'feature/user-auth'
git-review
```

**Saída esperada:**
```
[Salvo em: history/20260302-143022-cli.py-feature-user-auth-vs-main.md]
```

**Conteúdo do relatório gerado:**
```markdown
# Histórico do Agente — Review de Diff
- Data: 2026-03-02
- Processo: cli.py
- Branch atual: feature/user-auth
- Branch alvo: main
- Merge-base: abc123def

## Riscos e possíveis bugs
- Falta validação de senha forte no endpoint de registro
- Token JWT não tem expiração configurada
- Senha armazenada sem hash (CRÍTICO)

## Testes recomendados
- Testar registro com senhas fracas
- Verificar expiração de tokens
- Testar login com credenciais inválidas
- Validar proteção contra SQL injection
```

### Exemplo 2: Review em Branch de Bugfix

```bash
# Branch: bugfix/fix-null-pointer
git-review
```

**Relatório típico:**
```markdown
## Riscos e possíveis bugs
- Fix parece correto, mas falta tratamento de edge case quando lista está vazia
- Considerar adicionar logging para debug futuro

## Testes recomendados
- Testar com lista vazia
- Testar com lista contendo apenas null
- Adicionar teste unitário para o cenário corrigido
```

### Exemplo 3: Diff Muito Grande

```bash
# Branch com muitas mudanças
git-review
```

**Comportamento:**
- Diff é truncado em 50.000 caracteres
- Mensagem `[DIFF TRUNCADO]` é adicionada
- Review foca nas primeiras mudanças

## CV Extractor

### Exemplo 1: Extração de PDF

**Arquivo:** `profile.pdf`

```python
# Em cv_extractor/extractor.py
with open("profile.pdf", "rb") as f:
    file_bytes = f.read()

mime_type = "application/pdf"
```

**Executar:**
```bash
cv-extract
```

**Saída JSON:**
```json
{
  "sdtPessoaCompleto": {
    "Pessoa": {
      "PesNome": "João Silva",
      "PesDataNascimento": "1990-05-15",
      "PesGenero": "Masculino",
      "PesCpf": "123.456.789-00",
      "PesEmail": "joao.silva@email.com",
      "PesDddCelular": 11,
      "PesCelular": 987654321,
      "PesSobre": "Desenvolvedor Full Stack com 5 anos de experiência",
      "PesProfissao": "Desenvolvedor de Software",
      "PesPossuiAcessibilidade": "Não",
      "TipAdaAceId": 0
    },
    "Endereco": {
      "PesEndCep": "01234-567",
      "PesEndComplemento": "Apto 101",
      "PesEndNumero": "123"
    },
    "Formacoes": [
      {
        "TipForId": 4,
        "PesForStatus": "Concluído",
        "PesForCurso": "Ciência da Computação",
        "PesForInstituicao": "USP",
        "PesForDataConclusao": "2015-12-01"
      }
    ],
    "Experiencias": [
      {
        "PesExpProCargo": "Desenvolvedor Full Stack",
        "PesExpProEmpresa": "Tech Corp",
        "PesExpProDescricaoAtividades": "Desenvolvimento de aplicações web",
        "PesExpProDataInicio": "2020-01-01",
        "PesExpProDataFim": null,
        "PesExpProEmpregoAtual": true
      }
    ],
    "Links": [
      {
        "TipLinId": 1,
        "PesLinLink": "https://github.com/joaosilva"
      },
      {
        "TipLinId": 2,
        "PesLinLink": "https://linkedin.com/in/joaosilva"
      }
    ]
  }
}
```

### Exemplo 2: Extração de Imagem

**Arquivo:** `curriculo.jpg`

```python
# Em cv_extractor/extractor.py
with open("curriculo.jpg", "rb") as f:
    file_bytes = f.read()

mime_type = "image/jpeg"
```

**Executar:**
```bash
cv-extract
```

**Comportamento:**
- Funciona melhor com imagens de alta resolução
- Texto deve estar legível
- Evitar imagens escaneadas de baixa qualidade

### Exemplo 3: Classificação Automática

**Formações acadêmicas (TipForId):**
- Fundamental = 1
- Médio = 2
- Técnico = 3
- Superior = 4 ✓ (Ciência da Computação)
- Pós-graduação = 5
- Mestrado = 6
- Doutorado = 7
- Não identificável = 0

**Links (TipLinId):**
- GitHub = 1 ✓ (detectado por "github.com")
- LinkedIn = 2 ✓ (detectado por "linkedin.com")
- Portfólio = 3

## Casos de Uso Avançados

### Git Review: Integração com CI/CD

```yaml
# .github/workflows/review.yml
name: AI Code Review

on:
  pull_request:
    branches: [main]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Setup Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: pip install -e .
      - name: Run review
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        run: git-review
      - name: Upload report
        uses: actions/upload-artifact@v2
        with:
          name: review-report
          path: history/
```

### CV Extractor: Processamento em Lote

```python
# batch_extract.py
import os
from pathlib import Path
from cv_extractor.extractor import extract_cv

def process_batch(input_dir: str, output_dir: str):
    """Processa múltiplos currículos."""
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    for pdf_file in input_path.glob("*.pdf"):
        print(f"Processando {pdf_file.name}...")
        result = extract_cv(str(pdf_file))
        
        output_file = output_path / f"{pdf_file.stem}.json"
        output_file.write_text(result)
        print(f"✓ Salvo em {output_file}")

if __name__ == "__main__":
    process_batch("curriculos/", "resultados/")
```

## Troubleshooting

### Git Review: "Nenhuma diferença encontrada"

**Problema:** Branch está sincronizada com main

**Solução:**
```bash
# Verifique se há commits diferentes
git log main..HEAD

# Se não houver commits, faça suas mudanças primeiro
git add .
git commit -m "Minhas mudanças"
git-review
```

### CV Extractor: Campos vazios no JSON

**Problema:** Modelo não conseguiu extrair informações

**Possíveis causas:**
- Currículo em formato não padrão
- Imagem de baixa qualidade
- Texto ilegível

**Solução:**
- Use PDF de texto (não escaneado)
- Melhore a qualidade da imagem
- Ajuste o prompt em `extractor.py`

### Ambos: "API key not found"

**Problema:** Variável de ambiente não configurada

**Solução:**
```bash
# Verifique se o .env existe
cat .env

# Deve conter:
# OPENAI_API_KEY=sk-...

# Se não existir, crie:
cp .env.example .env
# Edite e adicione sua chave
```
