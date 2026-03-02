# Git Review Agent & CV Extractor

Projeto Python com duas ferramentas principais:
- **Git Review Agent**: CLI para revisar diffs do Git usando IA
- **CV Extractor**: Extração automatizada de dados de currículos (PDF/imagem)

## 🚀 Início Rápido

Veja o [QUICKSTART.md](QUICKSTART.md) para começar em 5 minutos!

## Requisitos

- Python 3.10+
- Conta OpenAI com API key

## Instalação

### Opção 1: Setup Automatizado (Recomendado)

**Linux/Mac:**
```bash
chmod +x setup.sh
./setup.sh
```

**Windows:**
```cmd
setup.bat
```

### Opção 2: Setup Manual

1. Clone o repositório:
```bash
git clone <seu-repositorio>
cd <nome-do-projeto>
```

2. Crie e ative o ambiente virtual:
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate  # Windows
```

3. Instale as dependências:
```bash
pip install -e .
```

4. Configure a API key da OpenAI:
```bash
# Copie o arquivo de exemplo
cp .env.example .env  # Linux/Mac
# ou
copy .env.example .env  # Windows

# Edite o .env e adicione sua chave
# OPENAI_API_KEY=sua-chave-aqui
```

## Uso

### Git Review Agent

Ferramenta CLI que analisa diferenças entre branches e gera relatórios de revisão.

**Como usar:**
```bash
# Dentro de um repositório Git, execute:
git-review
```

O comando irá:
- Comparar a branch atual com `main`
- Gerar análise de riscos e bugs potenciais
- Sugerir testes recomendados
- Salvar o relatório em `history/`

**Exemplo de saída:**
```
[Salvo em: history/20260302-143022-cli.py-feature-branch-vs-main.md]
```

### CV Extractor

Script para extrair dados estruturados de currículos em PDF ou imagem.

**Como usar:**
```bash
# Opção 1: Usando o CLI instalado
cv-extract

# Opção 2: Executando diretamente
python cv_extractor/extractor.py
```

**Configuração:**
- Coloque o arquivo do currículo na raiz do projeto
- Edite `cv_extractor/extractor.py` para apontar para seu arquivo:
  - PDF: `with open("profile.pdf", "rb") as f:`
  - Imagem: `with open("imagem.jpg", "rb") as f:`
- Ajuste o `mime_type` conforme necessário

**Formato de saída:**
O script extrai e estrutura dados em JSON:
- Informações pessoais (nome, CPF, email, telefone)
- Endereço
- Formações acadêmicas
- Experiências profissionais
- Links (GitHub, LinkedIn, portfólio)

## Estrutura do Projeto

```
.
├── git_review_agent/       # Pacote Git Review Agent
│   ├── __init__.py
│   └── cli.py             # CLI principal
├── cv_extractor/          # Pacote CV Extractor
│   ├── __init__.py
│   └── extractor.py       # Script de extração
├── scripts/               # Scripts auxiliares
│   └── agent_git_diff.py  # Versão standalone do Git Review
├── history/               # Histórico de reviews gerados
├── prompt/                # Prompts auxiliares
├── architecture/          # Documentação de arquitetura
├── .env                   # Configurações (API keys) - não versionado
├── .env.example           # Exemplo de configuração
├── pyproject.toml         # Configuração do projeto
├── requirements.txt       # Dependências
├── README.md              # Este arquivo
└── CONTRIBUTING.md        # Guia de contribuição
```

## Dependências

- `openai` - Cliente oficial da OpenAI
- `python-dotenv` - Gerenciamento de variáveis de ambiente
- `pydantic` - Validação de dados

## Desenvolvimento

Para contribuir ou modificar o projeto:

1. Instale em modo desenvolvimento:
```bash
pip install -e .
```

2. Faça suas alterações

3. Teste localmente:
```bash
git-review      # Testa o CLI do Git Review
cv-extract      # Testa o CLI do CV Extractor
```

Veja [CONTRIBUTING.md](CONTRIBUTING.md) para mais detalhes sobre como contribuir.

## Licença

Veja o arquivo [LICENSE](LICENSE) para detalhes.

## Documentação Adicional

- [QUICKSTART.md](QUICKSTART.md) - Guia rápido de uso
- [CONTRIBUTING.md](CONTRIBUTING.md) - Como contribuir
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) - Arquitetura detalhada
- [docs/EXAMPLES.md](docs/EXAMPLES.md) - Exemplos práticos de uso

## Notas

- O Git Review Agent compara sempre com a branch `main` por padrão
- Diffs muito grandes (>50.000 caracteres) são truncados automaticamente
- Os relatórios são salvos com timestamp para histórico completo
- O CV Extractor usa regras específicas para classificação de formação e links
