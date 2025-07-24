# 🚀 CONFIGURAÇÃO PARA GITHUB

## 📋 Pré-requisitos

### 1. Instalar Git
- Baixe em: https://git-scm.com/download/windows
- Instale com as configurações padrão

### 2. Configurar Git (primeira vez)
```bash
git config --global user.name "Seu Nome"
git config --global user.email "seu.email@exemplo.com"
```

## 🎯 Comandos para Publicar no GitHub

### 1. Navegar para o diretório do projeto
```bash
cd "C:\Users\pedro\OneDrive\Desktop\Projeto_Roupa"
```

### 2. Inicializar repositório Git
```bash
git init
```

### 3. Adicionar remote do GitHub
```bash
git remote add origin https://github.com/eibrahants/Guarda-Roupa-Inteligente.git
```

### 4. Adicionar todos os arquivos
```bash
git add .
```

### 5. Fazer commit inicial
```bash
git commit -m "🚀 Initial commit: Guarda Roupa Inteligente

✨ Funcionalidades implementadas:
- Sistema de sugestão IA baseado em clima
- Interface React minimalista
- Backend Flask com SQLite
- Upload de imagens direto
- Sistema de feedback com estrelas
- Documentação completa

🛠️ Stack: React + Flask + SQLite + Open-Meteo API"
```

### 6. Fazer push para GitHub
```bash
git branch -M main
git push -u origin main
```

## 📝 Comandos para Updates Futuros

### Adicionar mudanças
```bash
git add .
git commit -m "✨ Descrição das mudanças"
git push
```

## 🔐 Autenticação GitHub

Você precisará de:
- **GitHub Account** configurado
- **Personal Access Token** ou **SSH Keys**

### Personal Access Token:
1. GitHub → Settings → Developer settings → Personal access tokens
2. Generate new token (classic)
3. Selecionar scopes: `repo`, `workflow`
4. Usar token como senha quando o Git pedir

## 📁 Estrutura que será enviada:

```
Guarda-Roupa-Inteligente/
├── README.md                  # Documentação completa
├── LICENSE                   # Licença MIT
├── .gitignore               # Arquivos ignorados
├── DOCUMENTACAO_FINAL.md    # Resumo executivo
├── 
├── Backend/                 # API Flask
│   ├── app.py              # Servidor principal
│   ├── models.py           # Modelos de dados
│   ├── routes.py           # Endpoints API
│   ├── database.py         # Conexão SQLite
│   └── ia_sugestao_nova.py # Lógica IA
├── 
├── Frontend/               # Interface React
│   ├── src/
│   │   ├── components/
│   │   │   ├── Navigation.jsx
│   │   │   ├── SugestaoRoupa.jsx
│   │   │   └── RoupasList.jsx
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   ├── package.json
│   └── vite.config.js
├── 
├── Database/               # Dados
│   ├── roupas.db          # SQLite database
│   └── csv certo.csv      # Backup de dados
├── 
├── Imagens/               # Upload de imagens
└── BACKUP_*/              # Backups de desenvolvimento
```

## ⚠️ Arquivos Excluídos (.gitignore)

Os seguintes arquivos/pastas NÃO serão enviados:
- `node_modules/`
- `__pycache__/`
- `.env`
- `*.log`
- `.vite/`

## 🎉 Após o Push

Seu projeto estará disponível em:
**https://github.com/eibrahants/Guarda-Roupa-Inteligente**

### Para clonar em outro computador:
```bash
git clone https://github.com/eibrahants/Guarda-Roupa-Inteligente.git
cd Guarda-Roupa-Inteligente
```

### Setup do projeto clonado:
```bash
# Backend
cd Backend
pip install -r requirements.txt
python app.py

# Frontend (novo terminal)
cd Frontend
npm install
npm run dev
```

---

**🔥 DICA:** Execute os comandos acima em ordem após instalar o Git!
