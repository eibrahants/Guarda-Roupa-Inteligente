<<<<<<< HEAD
# 👕 Guarda Roupa Inteligente

Um sistema inteligente de sugestão de roupas baseado em IA que analisa o clima em tempo real e recomenda os melhores outfits para cada ocasião.

![Status](https://img.shields.io/badge/Status-Ativo-brightgreen)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![React](https://img.shields.io/badge/React-19.1.0-blue)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green)

## 📋 Índice

- [Sobre o Projeto](#sobre-o-projeto)
- [Funcionalidades](#funcionalidades)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Instalação](#instalação)
- [Como Usar](#como-usar)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [API Endpoints](#api-endpoints)
- [Contribuição](#contribuição)
- [Licença](#licença)

## 🎯 Sobre o Projeto

O **Guarda Roupa Inteligente** é uma aplicação web que utiliza inteligência artificial para gerar sugestões personalizadas de roupas baseadas nas condições climáticas atuais. O sistema considera fatores como temperatura, umidade, vento e condições meteorológicas para recomendar combinações perfeitas de roupas.

### ✨ Diferenciais

- **IA Inteligente**: Sistema de aprendizado que melhora as sugestões com base no feedback do usuário
- **Clima em Tempo Real**: Integração com APIs meteorológicas para dados precisos
- **Interface Moderna**: Design responsivo e minimalista
- **Sistema de Feedback**: Avaliação por estrelas (1-5) para melhorar recomendações
- **Upload de Imagens**: Adicione suas próprias roupas com fotos
- **Gestão Completa**: CRUD completo do guarda-roupa

## 🚀 Funcionalidades

### 🤖 Sugestão IA
- ✅ Análise automática do clima para Juiz de Fora (padrão)
- ✅ Sugestões completas: casaco, superior, inferior e calçado
- ✅ Sistema de pontuação de confiança
- ✅ Botão "Novo Outfit" para gerar alternativas
- ✅ Feedback com sistema de estrelas (1-5)
- ✅ Recomendações textuais inteligentes

### 👕 Guarda-roupa
- ✅ Visualização de todas as roupas cadastradas
- ✅ Upload direto de imagens via interface
- ✅ Preview de imagens antes do upload
- ✅ Edição completa de roupas (popup moderno)
- ✅ Exclusão com confirmação
- ✅ Menu de opções com três pontos
- ✅ Validação de tipos de arquivo

### 🎨 Interface
- ✅ Design responsivo para mobile e desktop
- ✅ Header com navegação intuitiva
- ✅ Cards modernos com bordas arredondadas
- ✅ Estados de loading elegantes
- ✅ Animações suaves
- ✅ Cores minimalistas

## 🛠️ Tecnologias Utilizadas

### Frontend
- **React** 19.1.0 - Biblioteca JavaScript para interfaces
- **Vite** - Build tool moderna e rápida
- **CSS3** - Estilização customizada
- **Axios** 1.10.0 - Cliente HTTP
- **Lucide React** 0.525.0 - Ícones modernos

### Backend
- **Python** 3.8+
- **Flask** 3.0.0 - Framework web
- **Flask-CORS** 4.0.0 - Cross-Origin Resource Sharing
- **SQLite** - Banco de dados local
- **Open-Meteo API** - Dados meteorológicos

### Banco de Dados
- **SQLite** - Armazenamento de roupas e feedback
- **Tabelas**: `roupas`, `feedback_usuario`

## 📦 Instalação

### Pré-requisitos
- Python 3.8 ou superior
- Node.js 16 ou superior
- npm ou yarn

### 1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/guarda-roupa-inteligente.git
cd guarda-roupa-inteligente
```

### 2. Configuração do Backend
```bash
cd Backend
pip install -r requirements.txt
```

### 3. Configuração do Frontend
```bash
cd Frontend
npm install
```

### 4. Configuração do Banco de Dados
```bash
cd Backend
python models.py  # Cria as tabelas automaticamente
```

## 🚀 Como Usar

### 1. Iniciar o Backend
```bash
cd Backend
python app.py
```
O servidor Flask estará disponível em `http://localhost:5000`

### 2. Iniciar o Frontend
```bash
cd Frontend
npm run dev
```
A aplicação estará disponível em `http://localhost:5173`

### 3. Usar a Aplicação

#### Sugestão IA:
1. Acesse a aba "Sugestão IA"
2. Digite uma cidade ou use "Juiz de Fora" (padrão)
3. Clique em "🔍 Buscar" ou pressione Enter
4. Visualize a sugestão completa com clima e outfit
5. Use "🔄 Novo Outfit" para gerar alternativas
6. Avalie com estrelas (1-5) para melhorar a IA

#### Guarda-roupa:
1. Acesse a aba "Guarda-roupa"
2. Clique em "➕ Adicionar Roupa"
3. Preencha os dados e faça upload da imagem
4. Use "Editar" para modificar roupas existentes
5. Use o menu "⋮" para opções avançadas

## 📁 Estrutura do Projeto

```
Guarda_Roupa_Inteligente/
├── Backend/                    # Servidor Flask
│   ├── app.py                 # Aplicação principal
│   ├── routes.py              # Rotas da API
│   ├── models.py              # Modelos do banco
│   ├── ia_sugestao_nova.py    # Sistema de IA
│   ├── style_ai_avancado.py   # IA avançada
│   ├── clima_service.py       # Serviço de clima
│   ├── feedback_learning.py   # Sistema de aprendizado
│   ├── database.py            # Conexão com DB
│   ├── requirements.txt       # Dependências Python
│   └── utils/                 # Utilitários
│       ├── popular_banco.py   # Popular banco com dados
│       └── corrigir_imagens.py # Correção de imagens
├── Frontend/                   # Interface React
│   ├── public/                # Arquivos públicos
│   ├── src/                   # Código fonte
│   │   ├── components/        # Componentes React
│   │   │   ├── Navigation.jsx # Navegação
│   │   │   ├── SugestaoRoupa.jsx # Página de sugestões
│   │   │   └── RoupasList.jsx # Página do guarda-roupa
│   │   ├── services/          # Serviços
│   │   │   └── api.js         # Cliente HTTP
│   │   ├── assets/            # Recursos estáticos
│   │   ├── App.jsx            # Componente principal
│   │   ├── main.jsx           # Entry point
│   │   └── index.css          # Estilos globais
│   ├── package.json           # Dependências Node
│   └── vite.config.js         # Configuração Vite
├── Database/                   # Banco de dados
│   ├── roupas.db              # SQLite database
│   └── csv certo.csv          # Dados iniciais
├── Imagens/                    # Imagens das roupas
└── README.md                   # Este arquivo
```

## 🔌 API Endpoints

### Sugestões
- `POST /api/sugestao` - Gerar sugestão de roupa
  ```json
  {
    "cidade": "Juiz de Fora"
  }
  ```

### Roupas
- `GET /api/roupas` - Listar todas as roupas
- `POST /api/roupas` - Adicionar nova roupa
- `PUT /api/roupas/{id}` - Atualizar roupa
- `DELETE /api/roupas/{id}` - Deletar roupa

### Upload
- `POST /api/upload` - Upload de imagem
- `GET /api/image/{id}` - Servir imagem

### Feedback
- `POST /api/feedback` - Registrar feedback
  ```json
  {
    "cidade": "Juiz de Fora",
    "temperatura": 20,
    "score": 5,
    "tipo_feedback": "positivo"
  }
  ```

### Clima
- `GET /api/clima/{cidade}` - Obter clima atual

## 🤖 Sistema de IA

### Algoritmo de Sugestão
O sistema utiliza múltiplos fatores para gerar sugestões:

1. **Análise Climática** (35% do peso)
   - Temperatura atual
   - Umidade e vento
   - Condições meteorológicas

2. **Harmonização de Cores** (25% do peso)
   - Compatibilidade entre cores
   - Regras de estilo

3. **Coerência de Estilo** (20% do peso)
   - Formal vs casual vs esportivo
   - Consistência do conjunto

4. **Histórico de Uso** (15% do peso)
   - Feedback anterior do usuário
   - Combinações bem avaliadas

5. **Preferências Pessoais** (5% do peso)
   - Cores favoritas
   - Tipos preferidos

### Lógica de Casaco
- **≤ 15°C**: Casaco obrigatório
- **16-25°C**: Casaco recomendado
- **> 25°C**: Sem necessidade de casaco

## 📊 Funcionalidades Avançadas

### Sistema de Aprendizado
- Feedback com estrelas (1-5)
- Análise de padrões de uso
- Melhoria contínua das sugestões
- Preferências personalizadas

### Upload Inteligente
- Validação de tipos de arquivo
- Preview antes do upload
- Redimensionamento automático
- Limpeza de arquivos antigos

### Interface Responsiva
- Mobile-first design
- Breakpoints otimizados
- Touch-friendly interactions
- Carregamento otimizado

## 🐛 Solução de Problemas

### Backend não inicia
```bash
# Verificar dependências
pip install -r requirements.txt

# Verificar porta 5000
netstat -ano | findstr :5000
```

### Frontend com tela branca
```bash
# Limpar cache
rm -rf node_modules
npm install

# Verificar porta 5173
npm run dev
```

### Banco de dados corrompido
```bash
cd Backend
python models.py  # Recriar tabelas
python utils/popular_banco.py  # Popular com dados iniciais
```

## 🔄 Atualizações Recentes

### v2.0.0 (24/07/2025)
- ✅ Botão "Novo Outfit" para gerar alternativas
- ✅ Ordenação correta: casaco → superior → inferior → calçado
- ✅ Sistema de feedback com estrelas (1-5)
- ✅ Lógica de casaco melhorada (≤25°C)
- ✅ Interface sem emojis nos menus
- ✅ Nome atualizado para "Guarda Roupa Inteligente"

### v1.5.0 (23/07/2025)
- ✅ Upload direto de imagens
- ✅ Sistema de edição com popup
- ✅ Menu de opções avançado
- ✅ Validação de arquivos
- ✅ Preview de imagens

## 📈 Roadmap

### Próximas Funcionalidades
- [ ] Histórico de outfits
- [ ] Favoritos e coleções
- [ ] Compartilhamento social
- [ ] Modo escuro
- [ ] Notificações push
- [ ] App mobile nativo
- [ ] Integração com e-commerce
- [ ] IA de reconhecimento de roupas
- [ ] Previsão do tempo 7 dias
- [ ] Sugestões por ocasião

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

### Padrões de Código
- **Frontend**: ESLint + Prettier
- **Backend**: PEP8 + Black
- **Commits**: Conventional Commits

## 📝 Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 👥 Autores

- **Desenvolvedor Principal** - [Seu Nome](https://github.com/seu-usuario)

## 📞 Suporte

- 📧 Email: suporte@guardaroupainteligente.com
- 🐛 Issues: [GitHub Issues](https://github.com/seu-usuario/guarda-roupa-inteligente/issues)
- 📖 Documentação: [Wiki](https://github.com/seu-usuario/guarda-roupa-inteligente/wiki)

## ⭐ Agradecimentos

- [Open-Meteo](https://open-meteo.com/) - API meteorológica gratuita
- [React](https://reactjs.org/) - Biblioteca JavaScript
- [Flask](https://flask.palletsprojects.com/) - Framework Python
- [Vite](https://vitejs.dev/) - Build tool moderna

---

<div align="center">

**Desenvolvido com ❤️ para deixar seu guarda-roupa mais inteligente!**

[⬆ Voltar ao topo](#-guarda-roupa-inteligente)

</div>
=======
# Guarda-Roupa-Inteligente
Projeto pessoal
>>>>>>> bef930019a0a9b6f5aa3abd4aa3c2c5a5f6ceaea
