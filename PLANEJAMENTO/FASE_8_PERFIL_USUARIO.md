# 👤 Fase 8: Gerenciamento de Perfil de Usuário

**Objetivo:** Implementar uma área onde os usuários possam visualizar e editar suas próprias informações de perfil, incluindo dados cadastrais e alteração de senha, de forma segura e intuitiva.

## Checklist de Etapas

- [x] **Etapa 8.1: Expansão do Modelo de Usuário no Banco de Dados**
  - Adicionar os novos campos ao modelo `User` em `app.py`: `nome_completo`, `email`, `telefone`, `endereco`, `cpf_cnpj`. Estes campos devem permitir valores nulos para não afetar o usuário `admin` existente.

- [x] **Etapa 8.2: Criação da Rota e Página de Perfil (Modo de Visualização)**
  - Criar a rota `/perfil` que requer login.
  - Desenvolver o template `perfil.html` que exibe as informações do `current_user` em campos de formulário desabilitados (read-only).
  - Adicionar um botão "Editar" que habilitará os campos para edição.

- [x] **Etapa 8.3: Implementação da Edição de Dados Cadastrais**
  - Implementar a lógica JavaScript para habilitar/desabilitar a edição dos campos no formulário.
  - A rota `/perfil` deverá aceitar requisições `POST` para receber os dados do formulário, validar e salvar as alterações no banco de dados, retornando uma mensagem de sucesso.

- [x] **Etapa 8.4: Implementação da Funcionalidade de Alteração de Senha**
  - Adicionar um formulário separado ou um modal na página de perfil para a alteração de senha, contendo os campos: "Senha Atual", "Nova Senha" e "Confirmação da Nova Senha".
  - Criar uma nova rota, como `/alterar_senha`, que receberá os dados, verificará se a senha atual está correta, e então atualizará a senha do usuário de forma segura (usando hash).

- [x] **Etapa 8.5: Integração Final da Interface**
  - No template `base.html`, atualizar o link do botão "Meu Perfil" no menu dropdown para apontar para a nova rota `{{ url_for('perfil') }}`.

---

[Voltar ao Plano Principal](./ACOMPANHAMENTO_PROJETO.md) 