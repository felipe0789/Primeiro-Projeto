# RestaurantApp - Sistema de Gestão de Restaurantes

Este é um sistema de gestão de restaurantes desenvolvido em Flask. Ele permite o cadastro, visualização, edição e exclusão de restaurantes, além de contar com um dashboard completo, sistema de autenticação de usuários, configurações personalizáveis e funcionalidades de exportação de dados.

## ✨ Funcionalidades Principais

- **Dashboard Interativo:** KPIs (Key Performance Indicators) que mostram o total de restaurantes, status (ativos/inativos) e taxa de ativação.
- **Gestão de Restaurantes (CRUD):**
    - Adicionar novos restaurantes.
    - Visualizar, editar e excluir restaurantes existentes.
    - Alternar o status entre "Ativo" e "Inativo".
- **Busca e Filtragem:** Pesquisa dinâmica por nome ou endereço e filtros por status.
- **Paginação:** A lista de restaurantes é paginada para melhor performance e usabilidade.
- **Autenticação de Usuários:** Sistema de login/logout seguro.
- **Perfil de Usuário:** Página onde o usuário pode visualizar e atualizar suas informações.
- **Configurações do Sistema:**
    - Alterar o tema da aplicação (Light/Dark).
    - Definir o número de itens por página.
    - Mudar o idioma da interface (Português/Inglês).
    - Definir o tempo de expiração da sessão.
- **Exportação e Relatórios:**
    - Exportar a lista de restaurantes para um arquivo CSV.
    - Gerar relatórios em PDF com base em filtros personalizados.

## 🛠️ Tecnologias Utilizadas

- **Backend:**
    - [Python](https://www.python.org/)
    - [Flask](https://flask.palletsprojects.com/)
    - [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/) (para interação com o banco de dados)
    - [Flask-Login](https://flask-login.readthedocs.io/) (para gerenciamento de sessão e autenticação)
    - [Flask-Babel](https://python-babel.github.io/flask-babel/) (para internacionalização)
    - [pdfkit](https://pypi.org/project/pdfkit/) (para geração de PDFs)
- **Frontend:**
    - [Bootstrap 5](https://getbootstrap.com/)
    - [Font Awesome](https://fontawesome.com/)
    - JavaScript
- **Banco de Dados:**
    - [SQLite](https://www.sqlite.org/index.html) (banco de dados padrão para desenvolvimento)
- **Dependências Externas:**
    - [wkhtmltopdf](https://wkhtmltopdf.org/): Ferramenta de linha de comando para renderizar HTML em PDF.

## 🚀 Configuração e Instalação

Siga os passos abaixo para configurar e rodar o projeto em seu ambiente local.

### 1. Pré-requisitos

- Python 3.8 ou superior.
- `pip` (gerenciador de pacotes do Python).
- `git` (para clonar o repositório).
- **wkhtmltopdf:** É necessário ter o `wkhtmltopdf` instalado em seu sistema para que a geração de PDF funcione. Você pode baixá-lo em [wkhtmltopdf.org](https://wkhtmltopdf.org/downloads.html).

### 2. Clone o Repositório

```bash
git clone https://github.com/felipe0789/Primeiro-Projeto.git
cd Primeiro-Projeto
```

### 3. Crie e Ative o Ambiente Virtual

É uma boa prática usar um ambiente virtual para isolar as dependências do projeto.

- **No Linux/macOS:**
  ```bash
  python3 -m venv Ambiente_virtual
  source Ambiente_virtual/bin/activate
  ```

- **No Windows:**
  ```bash
  python -m venv Ambiente_virtual
  Ambiente_virtual\\Scripts\\activate
  ```

### 4. Instale as Dependências

Com o ambiente virtual ativado, instale todas as dependências listadas no arquivo `requirements.txt`.

```bash
pip install -r requirements.txt
```

## ▶️ Como Executar

Após a instalação, você pode iniciar a aplicação com o seguinte comando:

```bash
python3 app.py
```

A aplicação estará disponível em `http://127.0.0.1:5000` em seu navegador.

### Credenciais Padrão

Ao iniciar a aplicação pela primeira vez, um usuário administrador padrão é criado:
- **Usuário:** `admin`
- **Senha:** `admin`

## 📂 Estrutura do Projeto

```
Primeiro-projeto/
│
├── Ambiente_virtual/      # Ambiente virtual do Python
├── instance/              # Contém o banco de dados SQLite
├── static/                # Arquivos estáticos (CSS, JS, imagens)
│   └── style.css
├── templates/             # Arquivos HTML do Jinja2
│   ├── base.html
│   ├── index.html
│   └── ... (outros templates)
├── translations/          # Arquivos de tradução (i18n)
├── .gitignore
├── app.py                 # Arquivo principal da aplicação Flask
├── config.json            # Configurações globais (sessão, etc.)
├── requirements.txt       # Lista de dependências Python
├── restaurantes.db        # Banco de dados SQLite
└── README.md              # Este arquivo
``` 