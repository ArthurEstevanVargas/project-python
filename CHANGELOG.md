# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Semantic Versioning](https://semver.org/lang/pt-BR/).

## [0.1.0] - 2026-03-02

### Adicionado
- Git Review Agent: CLI para revisar diffs do Git usando OpenAI
- CV Extractor: Ferramenta de extração de dados de currículos
- Scripts de setup automatizado (Linux/Mac e Windows)
- Documentação completa:
  - README.md principal
  - QUICKSTART.md para início rápido
  - CONTRIBUTING.md para contribuidores
  - docs/ARCHITECTURE.md com arquitetura detalhada
  - docs/EXAMPLES.md com exemplos práticos
- Configuração de projeto com pyproject.toml
- Suporte para Python 3.10+
- Integração com OpenAI API (GPT-4.1)

### Funcionalidades

#### Git Review Agent
- Análise automática de diffs entre branches
- Identificação de riscos e bugs potenciais
- Sugestões de testes recomendados
- Histórico de reviews em Markdown
- Truncamento automático de diffs grandes (>50k chars)

#### CV Extractor
- Extração de dados de PDFs e imagens
- Estruturação em JSON padronizado
- Classificação automática de formações acadêmicas
- Identificação de tipos de links (GitHub, LinkedIn, etc)
- Aplicação de regras de negócio

### Estrutura
- Organização em pacotes separados
- CLI instalável via pip
- Ambiente virtual configurável
- Variáveis de ambiente para API keys

## [Unreleased]

### Planejado
- Suporte para múltiplos modelos de IA
- Interface web para CV Extractor
- Integração com GitHub Actions
- Testes automatizados
- Suporte para mais formatos de currículo
- Configuração customizável de prompts
- Cache de resultados
- Métricas de uso e custos

---

## Tipos de Mudanças

- `Adicionado` para novas funcionalidades
- `Modificado` para mudanças em funcionalidades existentes
- `Descontinuado` para funcionalidades que serão removidas
- `Removido` para funcionalidades removidas
- `Corrigido` para correções de bugs
- `Segurança` para vulnerabilidades corrigidas
