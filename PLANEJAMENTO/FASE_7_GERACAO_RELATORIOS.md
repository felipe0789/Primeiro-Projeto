# 📄 Fase 7: Geração de Relatórios em PDF

**Objetivo:** Implementar um módulo completo para que o usuário possa configurar, pré-visualizar e gerar relatórios em PDF sobre os restaurantes cadastrados.

## Checklist de Etapas

- [x] **Etapa 7.1: Instalação de Dependências**
  - Instalar a biblioteca `pdfkit` para a conversão de HTML para PDF.
  - Verificar a necessidade da dependência de sistema `wkhtmltopdf`.

- [x] **Etapa 7.2: Rota e Página de Configuração**
  - Criar a rota `/relatorio` no `app.py`.
  - Desenvolver o template `relatorio.html` com um formulário para o usuário definir os parâmetros do relatório (datas, status, tipo de cozinha).
  - Atualizar o botão "Gerar Relatório" no `index.html` para apontar para a nova rota.

- [x] **Etapa 7.3: Lógica de Pré-visualização**
  - Criar a rota `/previa_relatorio` que recebe os dados do formulário.
  - Implementar a lógica de consulta no banco de dados com base nos filtros.
  - Desenvolver o template `previa_relatorio.html` para exibir os dados filtrados em uma tabela, servindo como uma prévia do PDF.

- [x] **Etapa 7.4: Geração do Arquivo PDF**
  - Criar a rota `/gerar_pdf` que também recebe os filtros.
  - Desenvolver um template minimalista (`relatorio_pdf.html`) otimizado para a renderização em PDF.
  - Usar a biblioteca `pdfkit` para converter o HTML renderizado em um arquivo PDF e retorná-lo como download.

- [x] **Etapa 7.5: Modais e Experiência do Usuário**
  - Adicionar um modal de confirmação na página `previa_relatorio.html` antes de acionar a geração final do PDF.
  - Garantir que todo o fluxo seja intuitivo e mantenha a identidade visual do sistema.

---

[Voltar ao Plano Principal](./ACOMPANHAMENTO_PROJETO.md) 