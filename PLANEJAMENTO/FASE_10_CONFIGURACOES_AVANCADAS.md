# ⚙️ Fase 10: Página de Configurações Avançadas

**Objetivo:** Criar uma área de configurações centralizada onde o usuário possa personalizar a aparência e o comportamento da aplicação, com as preferências sendo salvas por usuário.

## Checklist de Etapas

### Fase 1: Estrutura Base e Navegação

-   [ ] **Etapa 1.1: Adicionar Botão de Configurações no Header**
    -   No template `base.html`, adicionar um novo botão com um ícone de engrenagem (`fas fa-cog`) na seção do usuário.
    -   Este botão deve levar para a nova rota `/configuracoes`.

-   [ ] **Etapa 1.2: Criar Modelo de Configuração no Banco de Dados**
    -   Em `app.py`, definir um novo modelo `Configuracao`.
    -   Campos: `id`, `user_id` (chave estrangeira para `User`), `theme` (String, ex: 'light', 'dark'), `items_per_page` (Integer).
    -   Estabelecer uma relação um-para-um entre `User` e `Configuracao`.

-   [ ] **Etapa 1.3: Criar Rota e Template Iniciais**
    -   Criar a rota `/configuracoes` em `app.py`, que requer login.
    -   A rota deve buscar as configurações do usuário atual ou criar uma configuração padrão se não existir.
    -   Criar o template `templates/configuracoes.html` com a estrutura básica da página.

### Fase 2: Implementação das Funcionalidades

-   [ ] **Etapa 2.1: Alternador de Tema (Claro/Escuro)**
    -   **Frontend:** Em `configuracoes.html`, adicionar um switch (interruptor) para o tema.
    -   **JavaScript:** Adicionar um script que, ao mudar o switch, aplica/remove uma classe (ex: `dark-mode`) no `<body>` da página para alterar o tema em tempo real.
    -   **Backend:** Salvar a preferência ('light' ou 'dark') no banco de dados via AJAX ou submissão de formulário.
    -   **Integração:** No `base.html`, aplicar a classe de tema ao `<body>` com base na configuração salva do usuário ao carregar a página.

-   [ ] **Etapa 2.2: Configurar Itens por Página**
    -   **Frontend:** Em `configuracoes.html`, adicionar um campo (`<select>` ou `<input type="number">`) para o usuário definir o número de itens por página.
    -   **Backend:** Salvar este valor no banco de dados.
    -   **Integração:** Modificar a rota `/api/restaurantes` para que o valor de `per_page` seja lido a partir das configurações do usuário logado, em vez de ser um valor fixo.

-   [ ] **Etapa 2.3: Configurar Tempo de Expiração do Login (Global)**
    -   **Frontend:** Adicionar um campo em `configuracoes.html` para definir o tempo de sessão em minutos.
    -   **Backend:** Esta será uma configuração global. A rota salvará o valor (talvez em um arquivo de configuração simples como JSON ou em uma tabela de configuração global, para não precisar reiniciar o app).
    -   **Integração:** Em `app.py`, ler esse valor e aplicá-lo à configuração `app.config['PERMANENT_SESSION_LIFETIME']`.

### Fase 3: Funcionalidades Avançadas (Opcional/Futuro)

-   [ ] **Etapa 3.1: Cores Personalizadas com Pré-visualização**
    -   **Frontend:** Adicionar "color pickers" para cores primárias/secundárias.
    -   **JavaScript:** Usar os valores dos color pickers para injetar/alterar variáveis CSS em tempo real, mostrando a pré-visualização.
    -   **Backend:** Salvar os códigos hexadecimais das cores no banco de dados.
    -   **Integração:** Carregar e aplicar as cores personalizadas via CSS/JS ao iniciar a aplicação.

-   [ ] **Etapa 3.2: Idioma do Sistema (i18n)**
    -   Requer uma biblioteca como `Flask-Babel`.
    -   Envolve marcar todos os textos para tradução e criar arquivos de idioma.
    -   É uma etapa de alta complexidade e será deixada para o futuro.

---

[Voltar ao Plano Principal](./ACOMPANHAMENTO_PROJETO.md) 