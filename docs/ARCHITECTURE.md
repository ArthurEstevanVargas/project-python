# Arquitetura do Projeto

## Visão Geral

Este projeto contém duas ferramentas independentes que compartilham a mesma infraestrutura base (OpenAI API).

```
┌─────────────────────────────────────────────────────────┐
│                    Projeto Principal                    │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────────────────┐  ┌──────────────────────┐     │
│  │  Git Review Agent    │  │    CV Extractor      │     │
│  │                      │  │                      │     │
│  │  - Analisa diffs     │  │  - Extrai dados      │     │
│  │  - Gera relatórios   │  │  - Estrutura JSON    │     │
│  │  - Salva histórico   │  │  - Classifica info   │     │
│  └──────────┬───────────┘  └──────────┬───────────┘     │
│             │                          │                │
│             └──────────┬───────────────┘                │
│                        │                                │
│                ┌───────▼────────┐                       │
│                │  OpenAI API    │                       │
│                │  (GPT-4.1)     │                       │
│                └────────────────┘                       │
└─────────────────────────────────────────────────────────┘
```

## Componentes

### 1. Git Review Agent (`git_review_agent/`)

**Responsabilidade**: Análise automatizada de mudanças no código

**Fluxo de execução**:
1. Detecta repositório Git
2. Identifica branch atual
3. Calcula merge-base com `main`
4. Gera diff
5. Envia para OpenAI com prompt estruturado
6. Salva relatório em Markdown

**Arquivos**:
- `cli.py`: Ponto de entrada CLI
- `__init__.py`: Inicialização do pacote

**Comando**: `git-review`

### 2. CV Extractor (`cv_extractor/`)

**Responsabilidade**: Extração estruturada de dados de currículos

**Fluxo de execução**:
1. Carrega arquivo (PDF ou imagem)
2. Converte para base64
3. Envia para OpenAI com prompt de extração
4. Aplica regras de classificação
5. Retorna JSON estruturado

**Arquivos**:
- `extractor.py`: Lógica de extração
- `__init__.py`: Inicialização do pacote

**Comando**: `cv-extract`

### 3. Scripts Auxiliares (`scripts/`)

**Conteúdo**:
- `agent_git_diff.py`: Versão standalone do Git Review Agent

**Uso**: Para execução direta sem instalação do pacote

## Dependências

### Principais
- `openai`: Cliente oficial da OpenAI API
- `python-dotenv`: Gerenciamento de variáveis de ambiente
- `pydantic`: Validação e serialização de dados

### Sistema
- Python 3.10+
- Git (para Git Review Agent)

## Configuração

### Variáveis de Ambiente (`.env`)
```
OPENAI_API_KEY=sk-...
```

### Modelos Utilizados
- `gpt-4.1-mini-2025-04-14`: Modelo padrão para ambas as ferramentas

## Fluxo de Dados

### Git Review Agent
```
Git Repo → Diff → OpenAI → Markdown → history/
```

### CV Extractor
```
PDF/Image → Base64 → OpenAI → JSON → stdout
```

## Estrutura de Diretórios

```
.
├── git_review_agent/       # Pacote Git Review
│   ├── __init__.py
│   └── cli.py
├── cv_extractor/           # Pacote CV Extractor
│   ├── __init__.py
│   └── extractor.py
├── scripts/                # Scripts auxiliares
├── history/                # Histórico de reviews
├── docs/                   # Documentação
├── architecture/           # Diagramas e specs
└── prompt/                 # Prompts auxiliares
```

## Extensibilidade

### Adicionar Novo Extrator
1. Criar novo pacote em raiz
2. Implementar lógica de extração
3. Adicionar entry point em `pyproject.toml`
4. Documentar em README

### Modificar Prompts
- Git Review: Editar `SYSTEM_PROMPT_MD` em `cli.py`
- CV Extractor: Editar `EXTRACTION_PROMPT` e `RULES_PROMPT` em `extractor.py`

## Considerações de Segurança

- API keys nunca devem ser commitadas (`.env` no `.gitignore`)
- Diffs grandes são truncados para evitar custos excessivos
- Arquivos de currículo não são versionados por padrão

## Performance

### Git Review Agent
- Limite de diff: 50.000 caracteres
- Timeout: Padrão do subprocess
- Custo: ~$0.01-0.05 por review (depende do tamanho)

### CV Extractor
- Suporta PDFs até 10MB
- Imagens: Recomendado < 5MB
- Custo: ~$0.02-0.10 por extração
