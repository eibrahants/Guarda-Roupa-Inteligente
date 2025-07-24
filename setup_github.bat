@echo off
echo 🚀 CONFIGURANDO PROJETO PARA GITHUB...
echo.

REM Verificar se Git está instalado
git --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo ❌ Git não encontrado!
    echo.
    echo 📥 Por favor, instale o Git primeiro:
    echo    https://git-scm.com/download/windows
    echo.
    pause
    exit /b 1
)

echo ✅ Git encontrado!
echo.

REM Inicializar repositório
echo 📁 Inicializando repositório Git...
git init
if %ERRORLEVEL% neq 0 (
    echo ❌ Erro ao inicializar repositório
    pause
    exit /b 1
)

REM Adicionar remote
echo 🔗 Conectando ao GitHub...
git remote add origin https://github.com/eibrahants/Guarda-Roupa-Inteligente.git
if %ERRORLEVEL% neq 0 (
    echo ⚠️  Remote já existe ou erro na configuração
    git remote set-url origin https://github.com/eibrahants/Guarda-Roupa-Inteligente.git
)

REM Adicionar arquivos
echo 📦 Adicionando arquivos...
git add .
if %ERRORLEVEL% neq 0 (
    echo ❌ Erro ao adicionar arquivos
    pause
    exit /b 1
)

REM Fazer commit
echo 💾 Fazendo commit inicial...
git commit -m "🚀 Initial commit: Guarda Roupa Inteligente

✨ Funcionalidades implementadas:
- Sistema de sugestão IA baseado em clima
- Interface React minimalista e responsiva
- Backend Flask com SQLite
- Upload de imagens direto com preview
- Sistema de feedback com estrelas (1-5)
- Documentação completa e profissional

🛠️ Stack Tecnológica:
- Frontend: React 19 + Vite + CSS moderno
- Backend: Python + Flask + SQLite
- API: Open-Meteo para dados climáticos
- Upload: FormData + Werkzeug
- IA: Algoritmos personalizados de recomendação

📋 Recursos:
- Interface minimalista com foco UX
- Sugestão automática para Juiz de Fora
- Casaco recomendado para ≤25°C
- Sistema de aprendizado com feedback
- Upload com preview instantâneo
- Documentação técnica completa

🎯 Pronto para produção!"

if %ERRORLEVEL% neq 0 (
    echo ❌ Erro ao fazer commit
    pause
    exit /b 1
)

REM Configurar branch main
echo 🌟 Configurando branch main...
git branch -M main
if %ERRORLEVEL% neq 0 (
    echo ⚠️  Possível erro na configuração da branch
)

echo.
echo ✅ CONFIGURAÇÃO CONCLUÍDA!
echo.
echo 🚀 Para fazer push para o GitHub, execute:
echo    git push -u origin main
echo.
echo 🔐 Você precisará autenticar com GitHub
echo    (Personal Access Token recomendado)
echo.
echo 📖 Para mais detalhes, veja: CONFIGURACAO_GITHUB.md
echo.
pause
