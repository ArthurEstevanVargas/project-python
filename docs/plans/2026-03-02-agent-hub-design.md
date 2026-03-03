# Agent Hub - Design Document

**Data**: 2026-03-02  
**Versão**: 1.0  
**Status**: Design Aprovado

## 📋 Sumário Executivo

Este documento descreve o design de um Hub de Agentes baseado no padrão Supervisor usando LangGraph. O objetivo é criar uma infraestrutura extensível que permita orquestrar múltiplos agentes especializados através de um orquestrador central inteligente.

## 🎯 Objetivos

### Objetivo Principal
Criar um framework de orquestração de agentes que permita:
- Adicionar novos agentes facilmente
- Rotear requisições automaticamente para agentes apropriados
- Manter contexto entre execuções
- Escalar horizontalmente conforme necessário

### Objetivos Secundários
- Migrar agentes existentes (Git Review, CV Extractor) para nova estrutura
- Preparar base para agentes futuros (monitor de logs, email summarizer, etc.)
- Aprender conceitos de orquestração (LangGraph, state machines)
- Criar ferramenta de trabalho útil no dia a dia

## 🏗️ Arquitetura

### Visão Geral

```
┌─────────────────────────────────────────────────────────┐
│                      Agent Hub                          │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────────────────────────────────────────────┐   │
│  │              CLI Interface                       │   │
│  │  agent-hub run "sua requisição"                  │   │
│  └────────────────────┬─────────────────────────────┘   │
│                       │                                 │
│  ┌────────────────────▼─────────────────────────────┐   │
│  │           Supervisor (LangGraph)                 │   │
│  │  - Analisa requisição                            │   │
│  │  - Decide qual worker chamar                     │   │
│  │  - Coordena execução                             │   │
│  │  - Agrega resultados                             │   │
│  └────────┬──────────────────────────┬──────────────┘   │
│           │                          │                  │
│  ┌────────▼────────┐       ┌────────▼────────┐          │
│  │  Git Review     │       │  CV Extractor   │          │
│  │  Worker         │       │  Worker         │          │
│  └─────────────────┘       └─────────────────┘          │
│           │                          │                  │
│  ┌────────▼──────────────────────────▼──────────────┐   │
│  │         Shared Tools & Memory                    │   │
│  │  - Git operations                                │   │
│  │  - File operations                               │   │
│  │  - API calls                                     │   │
│  └──────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

### Padrão Arquitetural: Supervisor Pattern

**Supervisor**: Agente central que:
- Recebe requisições em linguagem natural
- Analisa intenção usando LLM
- Roteia para worker(s) apropriado(s)
- Coordena execução (sequencial ou paralela)
- Agrega e formata resultados

**Workers**: Agentes especializados que:
- Implementam interface padronizada
- Executam tarefas específicas
- Retornam resultados estruturados
- Podem usar ferramentas compartilhadas

**Shared Components**: Recursos comuns:
- Tools: funções reutilizáveis
- Memory: contexto compartilhado
- Config: configurações centralizadas

## 📁 Estrutura de Arquivos

```
agent_hub/
├── __init__.py
├── cli.py                          # Entry point CLI
│
├── core/
│   ├── __init__.py
│   ├── supervisor.py               # Supervisor agent (LangGraph)
│   ├── state.py                    # State definitions
│   ├── worker_registry.py          # Registro de workers
│   └── config.py                   # Configurações centralizadas
│
├── workers/
│   ├── __init__.py
│   ├── base.py                     # Classe base Worker
│   ├── git_review_worker.py        # Worker para git review
│   ├── cv_extractor_worker.py      # Worker para CV extraction
│   └── [futuros workers]
│
├── shared/
│   ├── __init__.py
│   ├── tools.py                    # Ferramentas compartilhadas
│   ├── memory.py                   # Sistema de memória
│   └── prompts.py                  # Prompts reutilizáveis
│
├── storage/
│   ├── history/                    # Histórico de execuções
│   ├── cache/                      # Cache de resultados
│   └── logs/                       # Logs do sistema
│
└── tests/
    ├── test_supervisor.py
    ├── test_workers.py
    └── test_integration.py

# Arquivos de configuração na raiz
pyproject.toml                      # Dependências e metadata
.env                                # API keys e configs
.env.example
README.md
```

## 🔄 Fluxo de Execução

### Fluxo Principal

```
1. Usuário → CLI
   Input: "revisar meu código"
   
2. CLI → Supervisor
   Contexto: {request, cwd, git_status, etc}
   
3. Supervisor → Análise
   LLM classifica intenção
   Consulta worker registry
   Decide: git_review_worker
   
4. Supervisor → Worker
   Executa git_review_worker.execute(input)
   
5. Worker → Ferramentas
   Usa shared tools (git diff, etc)
   Processa com LLM
   
6. Worker → Supervisor
   Retorna resultado estruturado
   
7. Supervisor → CLI
   Formata resultado final
   
8. CLI → Usuário
   Exibe resultado
   Salva histórico
```

### State Management (LangGraph)

**Estado Global**:
```python
{
  "request": "string",           # Requisição original
  "context": {},                 # Contexto (cwd, git, etc)
  "selected_worker": "string",   # Worker selecionado
  "worker_input": {},            # Input para worker
  "worker_output": {},           # Output do worker
  "final_result": {},            # Resultado final
  "history": []                  # Histórico de transições
}
```

**Transições**:
1. `start` → `analyze_request`
2. `analyze_request` → `select_worker`
3. `select_worker` → `execute_worker`
4. `execute_worker` → `format_result`
5. `format_result` → `end`

## 🧩 Componentes Detalhados

### 1. CLI Interface (`cli.py`)

**Responsabilidades**:
- Parsear argumentos de linha de comando
- Coletar contexto inicial (cwd, git status, etc)
- Invocar supervisor
- Exibir resultados formatados
- Salvar histórico

**Comandos**:
```bash
# Execução básica
agent-hub run "revisar meu código"

# Especificar worker
agent-hub run "revisar código" --worker git_review

# Modo verbose
agent-hub run "extrair CV" --verbose

# Ver histórico
agent-hub history

# Listar workers disponíveis
agent-hub list-workers
```

### 2. Supervisor (`core/supervisor.py`)

**Responsabilidades**:
- Implementar grafo LangGraph
- Analisar requisições
- Selecionar workers
- Coordenar execução
- Agregar resultados

**Componentes**:
- **Router**: Decide qual worker usar
- **Executor**: Executa worker selecionado
- **Aggregator**: Combina resultados (se múltiplos workers)
- **Formatter**: Formata resultado final

**Roteamento**:

Fase 1 (MVP): Baseado em regras
```python
# Supervisor usa prompt com descrições dos workers
# LLM decide baseado em similaridade semântica
prompt = f"""
Workers disponíveis:
- git_review: Analisa diffs do Git
- cv_extractor: Extrai dados de currículos

Requisição: {user_request}
Qual worker usar?
"""
```

Fase 2: Com histórico
```python
# Consulta histórico de decisões anteriores
# Prioriza workers que funcionaram bem em casos similares
history = load_history()
similar_cases = find_similar(user_request, history)
if similar_cases:
    suggested_worker = similar_cases[0].worker
```

Fase 3: Com feedback
```python
# Usuário avalia resultado (👍/👎)
# Supervisor ajusta confiança em workers
feedback = get_user_feedback()
update_worker_confidence(worker, feedback)
```

### 3. Worker Registry (`core/worker_registry.py`)

**Responsabilidades**:
- Auto-discovery de workers
- Manter metadados de workers
- Validar workers
- Fornecer lista de workers disponíveis

**Metadados de Worker**:
```python
{
  "name": "git_review",
  "description": "Analisa diffs do Git e gera relatórios",
  "capabilities": ["git", "code_review"],
  "input_schema": {...},
  "output_schema": {...}
}
```

**Auto-discovery**:
```python
# Escaneia workers/ e registra automaticamente
# Workers devem herdar de BaseWorker
for file in workers_dir:
    if is_worker(file):
        worker = load_worker(file)
        registry.register(worker)
```

### 4. Base Worker (`workers/base.py`)

**Interface Padrão**:
```python
class BaseWorker:
    name: str
    description: str
    capabilities: List[str]
    
    def execute(self, input: dict) -> dict:
        """
        Executa a tarefa do worker.
        
        Args:
            input: Dados de entrada estruturados
            
        Returns:
            {
                "status": "success" | "failure" | "partial",
                "result": {...},
                "metadata": {
                    "execution_time": float,
                    "tokens_used": int,
                    "confidence": float
                }
            }
        """
        raise NotImplementedError
    
    def validate_input(self, input: dict) -> bool:
        """Valida input antes de executar"""
        pass
    
    def get_metadata(self) -> dict:
        """Retorna metadados do worker"""
        return {
            "name": self.name,
            "description": self.description,
            "capabilities": self.capabilities
        }
```

### 5. Shared Tools (`shared/tools.py`)

**Ferramentas Comuns**:
- `run_git(command)`: Executa comandos git
- `read_file(path)`: Lê arquivos
- `write_file(path, content)`: Escreve arquivos
- `call_api(url, method, data)`: Chamadas HTTP
- `encode_base64(data)`: Encoding
- `parse_json(text)`: Parsing

**Características**:
- Reutilizáveis por todos os workers
- Com tratamento de erros
- Logging automático
- Cache opcional

### 6. Memory System (`shared/memory.py`)

**Tipos de Memória**:

**Short-term**: Contexto da sessão atual
```python
{
  "current_request": "...",
  "previous_results": [...],
  "user_preferences": {...}
}
```

**Long-term**: Histórico persistente
```python
{
  "request": "...",
  "worker_used": "...",
  "result": {...},
  "feedback": "positive" | "negative",
  "timestamp": "..."
}
```

**Cache**: Resultados reutilizáveis
```python
# Cache de resultados caros
# Ex: diff do git não muda se commit não mudou
cache_key = hash(git_commit + request)
if cache_key in cache:
    return cache[cache_key]
```

## 🔧 Implementação

### Dependências Principais

```toml
[project.dependencies]
langgraph = "^0.2.0"          # Orquestração
langchain = "^0.3.0"          # Utilities
langchain-openai = "^0.2.0"   # OpenAI integration
openai = "^1.0.0"             # Cliente OpenAI
pydantic = "^2.0.0"           # Validação
python-dotenv = "^1.0.0"      # Config
rich = "^13.0.0"              # CLI bonito (opcional)
```

### Configuração (`.env`)

```bash
# OpenAI
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4.1-mini-2025-04-14

# Supervisor
SUPERVISOR_TEMPERATURE=0.3
SUPERVISOR_MAX_TOKENS=2048

# Workers
WORKER_TIMEOUT=60
WORKER_MAX_RETRIES=3

# Storage
HISTORY_DIR=storage/history
CACHE_DIR=storage/cache
LOG_DIR=storage/logs
```

### Exemplo de Worker

```python
# workers/git_review_worker.py
from workers.base import BaseWorker
from shared.tools import run_git
from openai import OpenAI

class GitReviewWorker(BaseWorker):
    name = "git_review"
    description = "Analisa diffs do Git e gera relatórios de revisão"
    capabilities = ["git", "code_review"]
    
    def execute(self, input: dict) -> dict:
        # 1. Validar input
        if not self.validate_input(input):
            return {"status": "failure", "error": "Invalid input"}
        
        # 2. Coletar dados
        current_branch = run_git(["branch", "--show-current"])
        target_branch = input.get("target_branch", "main")
        merge_base = run_git(["merge-base", "HEAD", target_branch])
        diff = run_git(["diff", f"{merge_base}..HEAD"])
        
        # 3. Processar com LLM
        client = OpenAI()
        response = client.responses.create(
            model="gpt-4.1-mini-2025-04-14",
            input=[
                {"role": "system", "content": "Você é um revisor técnico..."},
                {"role": "user", "content": f"Diff:\n{diff}"}
            ]
        )
        
        # 4. Retornar resultado
        return {
            "status": "success",
            "result": {
                "review": response.output_text,
                "branch": current_branch,
                "target": target_branch
            },
            "metadata": {
                "execution_time": 2.5,
                "tokens_used": 1500
            }
        }
```

### Exemplo de Supervisor

```python
# core/supervisor.py
from langgraph.graph import StateGraph, END
from core.state import AgentState
from core.worker_registry import WorkerRegistry

def create_supervisor_graph():
    # 1. Definir grafo
    workflow = StateGraph(AgentState)
    
    # 2. Adicionar nós
    workflow.add_node("analyze_request", analyze_request_node)
    workflow.add_node("select_worker", select_worker_node)
    workflow.add_node("execute_worker", execute_worker_node)
    workflow.add_node("format_result", format_result_node)
    
    # 3. Definir transições
    workflow.set_entry_point("analyze_request")
    workflow.add_edge("analyze_request", "select_worker")
    workflow.add_edge("select_worker", "execute_worker")
    workflow.add_edge("execute_worker", "format_result")
    workflow.add_edge("format_result", END)
    
    return workflow.compile()

def select_worker_node(state: AgentState) -> AgentState:
    """Seleciona worker apropriado"""
    registry = WorkerRegistry()
    workers = registry.list_workers()
    
    # Usar LLM para decidir
    prompt = f"""
    Workers disponíveis:
    {format_workers(workers)}
    
    Requisição: {state["request"]}
    
    Qual worker usar? Responda apenas o nome.
    """
    
    # ... lógica de seleção ...
    
    state["selected_worker"] = selected_worker
    return state
```

## 📊 Observability

### Logging

**Níveis**:
- DEBUG: Detalhes de execução
- INFO: Eventos importantes
- WARNING: Situações anormais
- ERROR: Erros que impedem execução

**Formato**:
```json
{
  "timestamp": "2026-03-02T10:30:00Z",
  "level": "INFO",
  "component": "supervisor",
  "message": "Worker selected: git_review",
  "context": {
    "request": "revisar código",
    "worker": "git_review"
  }
}
```

### Métricas

**Por Worker**:
- Tempo médio de execução
- Taxa de sucesso
- Tokens usados
- Frequência de uso

**Por Supervisor**:
- Acurácia de roteamento
- Tempo total de requisição
- Cache hit rate

### Histórico

**Estrutura**:
```json
{
  "id": "uuid",
  "timestamp": "2026-03-02T10:30:00Z",
  "request": "revisar meu código",
  "context": {...},
  "worker_used": "git_review",
  "result": {...},
  "metadata": {
    "execution_time": 2.5,
    "tokens_used": 1500
  },
  "feedback": null
}
```

## 🚀 Roadmap de Implementação

### Fase 1: MVP (Semana 1-2)
- [ ] Estrutura básica de arquivos
- [ ] CLI simples
- [ ] Supervisor com roteamento por regras
- [ ] Worker registry básico
- [ ] Migrar git_review como worker
- [ ] Testes básicos

### Fase 2: Funcionalidades Core (Semana 3-4)
- [ ] Migrar cv_extractor como worker
- [ ] Shared tools
- [ ] Memory system (short-term)
- [ ] Logging estruturado
- [ ] Tratamento de erros robusto

### Fase 3: Melhorias (Semana 5-6)
- [ ] Histórico persistente
- [ ] Cache de resultados
- [ ] Roteamento com histórico
- [ ] Métricas e observability
- [ ] Documentação completa

### Fase 4: Novos Agentes (Semana 7+)
- [ ] Email summarizer worker
- [ ] Log monitor worker
- [ ] Auto git-review worker (hook)
- [ ] Outros conforme necessidade

## 📚 Guia de Estudo

### Conceitos Fundamentais

#### 1. LangGraph (Essencial)
**O que é**: Framework para criar aplicações com LLMs usando grafos de estados.

**Conceitos-chave**:
- **State**: Dados que fluem pelo grafo
- **Nodes**: Funções que processam o estado
- **Edges**: Transições entre nós
- **Conditional Edges**: Transições baseadas em condições

**Recursos**:
- Documentação oficial: https://langchain-ai.github.io/langgraph/
- Tutorial: "LangGraph Quickstart"
- Exemplo: "Multi-Agent Supervisor"

**Tempo estimado**: 4-6 horas

#### 2. State Machines (Importante)
**O que é**: Padrão de design onde sistema tem estados definidos e transições entre eles.

**Conceitos-chave**:
- Estados finitos
- Transições determinísticas
- Estado inicial e final
- Ações em transições

**Recursos**:
- Artigo: "Finite State Machines Explained"
- Vídeo: "State Machines in Python"

**Tempo estimado**: 2-3 horas

#### 3. Supervisor Pattern (Importante)
**O que é**: Padrão onde um agente central coordena múltiplos agentes workers.

**Conceitos-chave**:
- Supervisor: coordenador central
- Workers: executores especializados
- Task routing: roteamento de tarefas
- Result aggregation: agregação de resultados

**Recursos**:
- LangGraph docs: "Multi-Agent Supervisor"
- Artigo: "Agent Orchestration Patterns"

**Tempo estimado**: 2-3 horas

#### 4. LangChain Basics (Útil)
**O que é**: Framework para desenvolvimento com LLMs.

**Conceitos-chave**:
- Chains: sequências de operações
- Prompts: templates de prompts
- Memory: contexto entre chamadas
- Tools: funções que LLMs podem chamar

**Recursos**:
- Documentação: https://python.langchain.com/
- Tutorial: "LangChain Quickstart"

**Tempo estimado**: 3-4 horas

### Conceitos Avançados (Opcional)

#### 5. Multi-Agent Systems
**O que é**: Sistemas com múltiplos agentes que colaboram.

**Conceitos-chave**:
- Agent communication
- Task decomposition
- Coordination strategies
- Emergent behavior

**Recursos**:
- Paper: "Multi-Agent Systems: A Survey"
- Framework: CrewAI, AutoGen

**Tempo estimado**: 4-6 horas

#### 6. Prompt Engineering
**O que é**: Arte de criar prompts efetivos para LLMs.

**Conceitos-chave**:
- Few-shot learning
- Chain of thought
- System vs user prompts
- Temperature e sampling

**Recursos**:
- OpenAI Prompt Engineering Guide
- Anthropic Prompt Engineering

**Tempo estimado**: 2-3 horas

#### 7. Observability & Monitoring
**O que é**: Práticas para entender comportamento de sistemas.

**Conceitos-chave**:
- Structured logging
- Metrics collection
- Tracing
- Debugging distributed systems

**Recursos**:
- LangSmith (LangChain observability)
- OpenTelemetry basics

**Tempo estimado**: 2-3 horas

### Plano de Estudo Sugerido

**Semana 1: Fundamentos**
- Dia 1-2: LangGraph basics
- Dia 3: State machines
- Dia 4: Supervisor pattern
- Dia 5: LangChain basics

**Semana 2: Prática**
- Dia 1-2: Implementar MVP do supervisor
- Dia 3: Criar primeiro worker
- Dia 4: Integrar LangGraph
- Dia 5: Testes e refinamento

**Semana 3+: Expansão**
- Adicionar novos workers
- Implementar features avançadas
- Estudar conceitos conforme necessidade

### Recursos Práticos

**Repositórios de Exemplo**:
- LangGraph examples: https://github.com/langchain-ai/langgraph/tree/main/examples
- Multi-agent systems: https://github.com/langchain-ai/langchain/tree/master/cookbook

**Comunidades**:
- LangChain Discord
- Reddit: r/LangChain
- GitHub Discussions

**Ferramentas**:
- LangSmith: Debugging e observability
- LangServe: Deploy de chains
- LangGraph Studio: Visualização de grafos

## 🎓 Próximos Passos

### Para Começar a Implementação

1. **Setup Inicial**:
   ```bash
   # Criar estrutura de diretórios
   mkdir -p agent_hub/{core,workers,shared,storage/{history,cache,logs},tests}
   
   # Instalar dependências
   pip install langgraph langchain langchain-openai openai pydantic python-dotenv rich
   ```

2. **Estudar LangGraph**:
   - Ler documentação oficial
   - Fazer tutorial quickstart
   - Estudar exemplo "Multi-Agent Supervisor"

3. **Implementar MVP**:
   - Criar estrutura básica
   - Implementar supervisor simples
   - Migrar git_review como worker
   - Testar end-to-end

4. **Iterar**:
   - Adicionar features incrementalmente
   - Testar cada componente
   - Refinar baseado em uso real

### Dúvidas Comuns

**Q: Preciso saber LangGraph antes de começar?**
A: Não, mas ajuda. Você pode começar com estrutura básica e adicionar LangGraph depois.

**Q: Posso usar outro framework de orquestração?**
A: Sim, mas LangGraph é recomendado por ser mantido pela LangChain e ter boa documentação.

**Q: Como adiciono um novo worker?**
A: Crie arquivo em `workers/`, herde de `BaseWorker`, implemente `execute()`. Auto-registrado.

**Q: Workers podem chamar outros workers?**
A: Sim, mas recomendado passar pelo supervisor para manter controle e observability.

**Q: Como testo o supervisor?**
A: Testes unitários para cada nó, testes de integração para fluxo completo.

## 📝 Conclusão

Este design fornece uma base sólida para construir um hub de agentes extensível e escalável. O padrão Supervisor com LangGraph permite:

- **Extensibilidade**: Adicionar novos workers facilmente
- **Manutenibilidade**: Componentes isolados e testáveis
- **Escalabilidade**: Workers independentes podem rodar em paralelo
- **Observability**: Logging e métricas em todos os níveis
- **Aprendizado**: Estrutura clara para entender orquestração de agentes

O roadmap de implementação é incremental, permitindo validar cada fase antes de avançar. O guia de estudo fornece os conceitos necessários para implementar com confiança.

---

**Próximo passo**: Estudar LangGraph e começar implementação do MVP.
