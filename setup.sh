#!/bin/bash
# Script de setup automatizado para Git Review Agent & CV Extractor

set -e

echo "🚀 Iniciando setup do projeto..."

# Verifica se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 não encontrado. Por favor, instale Python 3.10 ou superior."
    exit 1
fi

# Verifica versão do Python
PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
REQUIRED_VERSION="3.10"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo "❌ Python $REQUIRED_VERSION ou superior é necessário. Versão atual: $PYTHON_VERSION"
    exit 1
fi

echo "✅ Python $PYTHON_VERSION detectado"

# Cria ambiente virtual se não existir
if [ ! -d ".venv" ]; then
    echo "📦 Criando ambiente virtual..."
    python3 -m venv .venv
else
    echo "✅ Ambiente virtual já existe"
fi

# Ativa ambiente virtual
echo "🔧 Ativando ambiente virtual..."
source .venv/bin/activate

# Atualiza pip
echo "⬆️  Atualizando pip..."
pip install --upgrade pip > /dev/null 2>&1

# Instala dependências
echo "📚 Instalando dependências..."
pip install -e . > /dev/null 2>&1

# Cria arquivo .env se não existir
if [ ! -f ".env" ]; then
    echo "📝 Criando arquivo .env..."
    cp .env.example .env
    echo "⚠️  IMPORTANTE: Edite o arquivo .env e adicione sua OPENAI_API_KEY"
else
    echo "✅ Arquivo .env já existe"
fi

# Cria diretórios necessários
echo "📁 Criando diretórios..."
mkdir -p history
mkdir -p docs

echo ""
echo "✨ Setup concluído com sucesso!"
echo ""
echo "📋 Próximos passos:"
echo "1. Edite o arquivo .env e adicione sua OPENAI_API_KEY"
echo "2. Ative o ambiente virtual: source .venv/bin/activate"
echo "3. Execute: git-review (para revisar diffs)"
echo "4. Execute: cv-extract (para extrair dados de currículos)"
echo ""
echo "📖 Veja QUICKSTART.md para mais informações"
