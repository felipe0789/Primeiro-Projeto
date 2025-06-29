# FASE 9: Implementação da Paginação na Tabela de Restaurantes

## Objetivo

Implementar a funcionalidade de paginação na tabela de restaurantes da página principal para melhorar a performance e a usabilidade da aplicação, especialmente quando a lista de restaurantes for muito grande.

## Fases do Desenvolvimento

### Fase 1: Atualização do Backend (API)

-   [x] **Modificar a rota `/api/restaurantes`**:
    -   A rota deve aceitar um parâmetro de query, `page`, para especificar qual página de resultados deve ser retornada.
    -   Utilizar a função `paginate()` do SQLAlchemy para buscar um subconjunto de restaurantes do banco de dados (ex: 10 por página).
    -   A rota deve continuar a funcionar com os parâmetros de `filtro` e `busca` existentes, em conjunto com a paginação.

-   [x] **Ajustar a resposta da API**:
    -   A API deve retornar um objeto JSON contendo não apenas a lista de restaurantes (`items`), mas também metadados sobre a paginação.
    -   Campos necessários na resposta:
        -   `restaurantes`: A lista de itens da página atual.
        -   `total_paginas`: O número total de páginas.
        -   `pagina_atual`: O número da página atual.
        -   `tem_pagina_anterior`: Booleano indicando se existe uma página anterior.
        -   `tem_proxima_pagina`: Booleano indicando se existe uma página seguinte.
        -   `total_restaurantes`: O número total de restaurantes que correspondem à consulta.

### Fase 2: Atualização do Frontend (Interface)

-   [x] **Adicionar Controles de Paginação no HTML (`index.html`)**:
    -   Adicionar uma nova `div` abaixo da tabela para conter os elementos de navegação da paginação.
    -   Essa `div` será populada dinamicamente pelo JavaScript.

-   [x] **Adaptar o JavaScript para a API Paginada**:
    -   Manter uma variável de estado `currentPage` para rastrear a página atual.
    -   Na função `carregarRestaurantes()`, incluir o parâmetro `page` na URL da requisição à API.
    -   Atualizar a lógica que processa a resposta para extrair a lista de restaurantes do novo objeto JSON.

-   [x] **Criar a Função `renderizarPaginacao()`**:
    -   Esta função será chamada após cada busca bem-sucedida de dados.
    -   Ela receberá os metadados da paginação da API.
    -   Será responsável por gerar os botões ("Anterior", números de página, "Próximo") e inseri-los no container de paginação no HTML.
    -   Os botões "Anterior" e "Próximo" devem ser desabilitados condicionalmente (se estiver na primeira ou na última página).

-   [x] **Implementar Interatividade**:
    -   Adicionar `event listeners` aos botões de paginação.
    -   Um clique em um botão de página deve atualizar a variável `currentPage` e chamar `carregarRestaurantes()` novamente para buscar e exibir os dados da nova página.
    -   A busca e os filtros devem resetar a paginação para a primeira página.

### Fase 3: Testes e Refinamentos

-   [x] **Testar a funcionalidade**:
    -   Verificar se a navegação entre páginas funciona corretamente.
    -   Testar se a paginação coexiste com a funcionalidade de busca e os filtros (Ativo/Inativo/Todos).
    -   Verificar o comportamento em casos extremos (nenhum restaurante, apenas uma página de resultados).

-   [x] **Refinamento de Estilo (CSS)**:
    -   Garantir que os controles de paginação estejam visualmente alinhados com o design do restante da aplicação.
    -   Adicionar feedback visual para a página ativa. 