@echo off
REM Script de setup automatizado para Git Review Agent & CV Extractor (Windows)

echo 🚀 Iniciando setup do projeto...

REM Verifica se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python não encontrado. Por favor, instale Python 3.10 ou superior.
    exit /b 1
)

echo ✅ Python detectado

REM Cria ambiente virtual se não existir
if not exist ".venv" (
    echo 📦 Criando ambiente virtual...
    python -m venv .venv
) else (
    echo ✅ Ambiente virtual já existe
)

REM Ativa ambiente virtual
echo 🔧 Ativando ambiente virtual...
call .venv\Scripts\activate.bat

REM Atualiza pip
echo ⬆️  Atualizando pip...
python -m pip install --upgrade pip >nul 2>&1

REM Instala dependências
echo 📚 Instalando dependências...
pip install -e . >nul 2>&1

REM Cria arquivo .env se não existir
if not exist ".env" (
    echo 📝 Criando arquivo .env...
    copy .env.example .env >nul
    echo ⚠️  IMPORTANTE: Edite o arquivo .env e adicione sua OPENAI_API_KEY
) else (
    echo ✅ Arquivo .env já existe
)

REM Cria diretórios necessários
echo 📁 Criando diretórios...
if not exist "history" mkdir history
if not exist "docs" mkdir docs

echo.
echo ✨ Setup concluído com sucesso!
echo.
echo 📋 Próximos passos:
echo 1. Edite o arquivo .env e adicione sua OPENAI_API_KEY
echo 2. Ative o ambiente virtual: .venv\Scripts\activate
echo 3. Execute: git-review (para revisar diffs)
echo 4. Execute: cv-extract (para extrair dados de currículos)
echo.
echo 📖 Veja QUICKSTART.md para mais informações

pause
