# Guia Rápido de Uso

## Configuração Inicial (5 minutos)

### 1. Instale as dependências
```bash
pip install -e .
```

### 2. Configure a API Key
```bash
# Copie o arquivo de exemplo
cp .env.example .env

# Edite o .env e adicione sua chave
# OPENAI_API_KEY=sk-...
```

## Git Review Agent

### Uso Básico
```bash
# Certifique-se de estar em um repositório Git
cd seu-projeto

# Execute a revisão
git-review
```

### O que acontece?
1. Compara sua branch atual com `main`
2. Analisa as mudanças usando IA
3. Identifica riscos e bugs potenciais
4. Sugere testes
5. Salva relatório em `history/`

### Exemplo de Saída
```
[Salvo em: history/20260302-143022-cli.py-feature-auth-vs-main.md]
```

## CV Extractor

### Uso Básico
```bash
# Coloque seu currículo na raiz do projeto
# Exemplo: profile.pdf ou curriculo.jpg

# Execute a extração
cv-extract
```

### Personalizando
Edite `cv_extractor/extractor.py` para:
- Mudar o arquivo de entrada (linha ~180)
- Ajustar o tipo MIME (PDF ou imagem)
- Modificar campos extraídos

### Formato de Saída
JSON estruturado com:
- Dados pessoais
- Endereço
- Formações (com classificação automática)
- Experiências profissionais
- Links sociais (GitHub, LinkedIn, etc)

## Dicas

### Git Review Agent
- Use em branches de feature antes de fazer PR
- Revise o histórico em `history/` para acompanhar evolução
- Diffs muito grandes são truncados automaticamente

### CV Extractor
- Funciona melhor com PDFs de texto (não escaneados)
- Para imagens, use boa resolução
- O modelo classifica automaticamente tipos de formação e links

## Problemas Comuns

### "Você não está dentro de um repositório Git"
- Execute `git-review` dentro de um repositório Git válido

### "API key not found"
- Verifique se o arquivo `.env` existe e contém `OPENAI_API_KEY`

### "Module not found"
- Execute `pip install -e .` novamente
- Ative o ambiente virtual: `source .venv/bin/activate`

## Próximos Passos

- Leia o [README.md](README.md) completo
- Veja [CONTRIBUTING.md](CONTRIBUTING.md) para contribuir
- Explore os exemplos em `history/`
