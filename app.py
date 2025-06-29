from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, make_response, Response
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import func
import io
import csv
import pdfkit
from datetime import datetime
import os

# Cria a instância da aplicação Flask
app = Flask(__name__)

# Configurações
# Caminho absoluto para o banco de dados na raiz do projeto
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "restaurantes.db")}'
app.config['SECRET_KEY'] = 'sua_chave_secreta_aqui'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['WKHTMLTOPDF_PATH'] = os.path.join(basedir, 'wkhtmltopdf')

# Inicializa o banco de dados
db = SQLAlchemy(app)

# Configuração do Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = "Por favor, faça o login para acessar esta página."
login_manager.login_message_category = "info"

# Modelos
class Restaurante(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False, unique=True)
    endereco = db.Column(db.String(200), nullable=False)
    tipo_cozinha = db.Column(db.String(50), nullable=False)
    ativo = db.Column(db.Boolean, default=True)
    avaliacoes = db.relationship('Avaliacao', backref='restaurante', lazy=True, cascade="all, delete-orphan")

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    
    # Novos campos para o perfil do usuário
    nome_completo = db.Column(db.String(200), nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=True)
    telefone = db.Column(db.String(20), nullable=True)
    endereco = db.Column(db.String(250), nullable=True)
    cpf_cnpj = db.Column(db.String(20), unique=True, nullable=True)
    
    avaliacoes = db.relationship('Avaliacao', backref='user', lazy=True)

class Avaliacao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nota = db.Column(db.Integer, nullable=False)
    comentario = db.Column(db.Text, nullable=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    restaurante_id = db.Column(db.Integer, db.ForeignKey('restaurante.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    """Carrega o usuário para o Flask-Login"""
    return User.query.get(int(user_id))

@app.before_request
def create_tables():
    db.create_all()
    if not User.query.filter_by(username='admin').first():
        hashed_password = generate_password_hash('admin')
        admin_user = User(username='admin', password=hashed_password)
        db.session.add(admin_user)
        db.session.commit()
        print("Usuário 'admin' padrão criado com sucesso!")

# Rotas
@app.route('/')
@login_required
def index():
    filtro = request.args.get('filtro')
    
    if filtro == 'ativo':
        restaurantes = Restaurante.query.filter_by(ativo=True).all()
    elif filtro == 'inativo':
        restaurantes = Restaurante.query.filter_by(ativo=False).all()
    else:
        restaurantes = Restaurante.query.all()
    
    # Estatísticas
    total_restaurantes = Restaurante.query.count()
    restaurantes_ativos = Restaurante.query.filter_by(ativo=True).count()
    restaurantes_inativos = Restaurante.query.filter_by(ativo=False).count()
    
    # Contar tipos de cozinha únicos
    tipos_cozinha_count = db.session.query(func.count(func.distinct(Restaurante.tipo_cozinha))).scalar()
    
    return render_template('index.html', 
                         restaurantes=restaurantes,
                         total_restaurantes=total_restaurantes,
                         restaurantes_ativos=restaurantes_ativos,
                         restaurantes_inativos=restaurantes_inativos,
                         tipos_cozinha_count=tipos_cozinha_count,
                         filtro_ativo=filtro)

# Rota para adicionar um novo restaurante
@app.route('/adicionar_restaurante', methods=['GET', 'POST'])
@login_required
def adicionar_restaurante():
    if request.method == 'POST':
        # Pega os dados do formulário
        nome = request.form['nome']
        endereco = request.form['endereco']
        tipo_cozinha = request.form['tipo_cozinha']
        
        # Cria um novo objeto Restaurante (o status 'ativo' é True por padrão)
        novo_restaurante = Restaurante(
            nome=nome, 
            endereco=endereco, 
            tipo_cozinha=tipo_cozinha
        )
        
        # Adiciona e salva no banco de dados
        db.session.add(novo_restaurante)
        db.session.commit()
        
        # Envia uma mensagem de sucesso
        flash(f'Restaurante "{novo_restaurante.nome}" adicionado com sucesso!', 'success')
        
        # Redireciona para a página inicial
        return redirect(url_for('index'))
    
    # Se for GET, apenas mostra o formulário
    return render_template('adicionar_restaurante.html')

# Rota para editar um restaurante
@app.route('/editar_restaurante/<int:restaurante_id>', methods=['POST'])
@login_required
def editar_restaurante(restaurante_id):
    restaurante = Restaurante.query.get_or_404(restaurante_id)
    
    # Pega os dados do formulário de edição
    nome = request.form['nome']
    endereco = request.form['endereco']
    tipo_cozinha = request.form['tipo_cozinha']
    
    # Atualiza os campos do restaurante
    if nome:
        restaurante.nome = nome
    if endereco:
        restaurante.endereco = endereco
    if tipo_cozinha:
        restaurante.tipo_cozinha = tipo_cozinha
        
    db.session.commit()
    
    flash(f'Restaurante "{restaurante.nome}" editado com sucesso!', 'success')
    return redirect(url_for('index'))

# Rota para alternar o status de um restaurante (ativo/inativo)
@app.route('/alternar_status/<int:restaurante_id>', methods=['POST'])
@login_required
def alternar_status(restaurante_id):
    try:
        restaurante = Restaurante.query.get_or_404(restaurante_id)
        restaurante.ativo = not restaurante.ativo
        db.session.commit()
        
        return jsonify({
            'success': True,
            'novo_status': restaurante.ativo,
            'message': f'Status do restaurante alterado para {"Ativo" if restaurante.ativo else "Inativo"}'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Erro ao alterar status do restaurante'
        }), 500

# Rota para excluir um restaurante
@app.route('/excluir_restaurante/<int:restaurante_id>', methods=['POST'])
@login_required
def excluir_restaurante(restaurante_id):
    try:
        restaurante = Restaurante.query.get_or_404(restaurante_id)
        nome_restaurante = restaurante.nome
        
        db.session.delete(restaurante)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'Restaurante "{nome_restaurante}" excluído com sucesso!'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Erro ao excluir restaurante'
        }), 500

# Rota para API para buscar e filtrar restaurantes
@app.route('/api/restaurantes')
@login_required
def api_restaurantes():
    termo_busca = request.args.get('busca', '').strip()
    filtro_status = request.args.get('filtro', 'todos')
    page = request.args.get('page', 1, type=int)
    per_page = 10 # Define quantos restaurantes por página

    query = Restaurante.query

    # Aplicar filtro de busca, se houver
    if termo_busca:
        query = query.filter(
            db.or_(
                Restaurante.nome.ilike(f'%{termo_busca}%'),
                Restaurante.endereco.ilike(f'%{termo_busca}%'),
                Restaurante.tipo_cozinha.ilike(f'%{termo_busca}%')
            )
        )

    # Aplicar filtro de status
    if filtro_status == 'ativo':
        query = query.filter_by(ativo=True)
    elif filtro_status == 'inativo':
        query = query.filter_by(ativo=False)

    paginacao = query.order_by(Restaurante.nome).paginate(page=page, per_page=per_page, error_out=False)
    restaurantes_paginados = paginacao.items

    # Converter para formato JSON
    resultados = [{
        'id': r.id,
        'nome': r.nome,
        'endereco': r.endereco,
        'tipo_cozinha': r.tipo_cozinha,
        'ativo': r.ativo
    } for r in restaurantes_paginados]

    return jsonify({
        'restaurantes': resultados,
        'total_restaurantes': paginacao.total,
        'total_paginas': paginacao.pages,
        'pagina_atual': paginacao.page,
        'tem_pagina_anterior': paginacao.has_prev,
        'tem_proxima_pagina': paginacao.has_next
    })

# Rota para obter estatísticas
@app.route('/estatisticas')
@login_required
def estatisticas():
    """Endpoint para obter estatísticas atualizadas"""
    total_restaurantes = Restaurante.query.count()
    restaurantes_ativos = Restaurante.query.filter_by(ativo=True).count()
    restaurantes_inativos = Restaurante.query.filter_by(ativo=False).count()
    tipos_cozinha_count = db.session.query(func.count(func.distinct(Restaurante.tipo_cozinha))).scalar()
    
    # Calcular taxa de ativação
    taxa_ativacao = (restaurantes_ativos / total_restaurantes * 100) if total_restaurantes > 0 else 0
    
    # Estatísticas por tipo de cozinha
    tipos_stats = db.session.query(
        Restaurante.tipo_cozinha,
        func.count(Restaurante.id).label('total'),
        func.sum(func.cast(Restaurante.ativo, db.Integer)).label('ativos')
    ).group_by(Restaurante.tipo_cozinha).all()
    
    tipos_cozinha_detalhes = []
    for tipo, total, ativos in tipos_stats:
        tipos_cozinha_detalhes.append({
            'tipo': tipo,
            'total': total,
            'ativos': ativos or 0,
            'inativos': total - (ativos or 0)
        })
    
    return jsonify({
        'total_restaurantes': total_restaurantes,
        'restaurantes_ativos': restaurantes_ativos,
        'restaurantes_inativos': restaurantes_inativos,
        'tipos_cozinha_count': tipos_cozinha_count,
        'taxa_ativacao': round(taxa_ativacao, 1),
        'tipos_cozinha_detalhes': tipos_cozinha_detalhes
    })

@app.route('/exportar_csv')
@login_required
def exportar_csv():
    """Exporta os dados filtrados para um arquivo CSV."""
    termo_busca = request.args.get('busca', '').strip()
    filtro_status = request.args.get('filtro', 'todos')

    query = Restaurante.query

    if termo_busca:
        query = query.filter(
            db.or_(
                Restaurante.nome.ilike(f'%{termo_busca}%'),
                Restaurante.endereco.ilike(f'%{termo_busca}%'),
                Restaurante.tipo_cozinha.ilike(f'%{termo_busca}%')
            )
        )

    if filtro_status == 'ativo':
        query = query.filter_by(ativo=True)
    elif filtro_status == 'inativo':
        query = query.filter_by(ativo=False)

    restaurantes_filtrados = query.order_by(Restaurante.nome).all()

    # Criação do CSV em memória
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Escreve o cabeçalho
    writer.writerow(['ID', 'Nome', 'Endereço', 'Tipo de Cozinha', 'Status'])
    
    # Escreve os dados
    for r in restaurantes_filtrados:
        status = 'Ativo' if r.ativo else 'Inativo'
        writer.writerow([r.id, r.nome, r.endereco, r.tipo_cozinha, status])
    
    output.seek(0)
    
    # Prepara a resposta para download
    response = make_response(output.getvalue())
    response.headers["Content-Disposition"] = "attachment; filename=restaurantes.csv"
    response.headers["Content-type"] = "text/csv"
    
    return response

# --- Rotas de Autenticação ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Login realizado com sucesso!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Usuário ou senha incorretos.', 'danger')
            
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout realizado com sucesso.', 'info')
    return redirect(url_for('login'))

# --- Rotas de Relatório ---
@app.route('/relatorio')
@login_required
def relatorio():
    """Exibe a página de configuração do relatório."""
    # Futuramente, podemos carregar opções de filtro do banco de dados aqui
    tipos_cozinha = db.session.query(Restaurante.tipo_cozinha).distinct().order_by(Restaurante.tipo_cozinha).all()
    # Extrai o valor de cada tupla
    tipos_cozinha = [tipo[0] for tipo in tipos_cozinha]
    
    return render_template('relatorio.html', tipos_cozinha=tipos_cozinha)

@app.route('/previa_relatorio', methods=['POST'])
@login_required
def previa_relatorio():
    """Recebe os filtros, busca os dados e exibe a pré-visualização."""
    filtros = request.form
    status = filtros.get('status')
    tipos_cozinha_selecionados = filtros.getlist('tipos_cozinha')
    
    query = Restaurante.query

    # Aplicar filtro de status
    if status == 'ativo':
        query = query.filter_by(ativo=True)
    elif status == 'inativo':
        query = query.filter_by(ativo=False)

    # Aplicar filtro de tipos de cozinha
    if tipos_cozinha_selecionados:
        query = query.filter(Restaurante.tipo_cozinha.in_(tipos_cozinha_selecionados))

    # Obter os resultados
    restaurantes = query.order_by(Restaurante.nome).all()
    
    # Passar os filtros para o template para poder reenviá-los
    configuracao_relatorio = {
        'status': status,
        'tipos_cozinha': ','.join(tipos_cozinha_selecionados)
    }

    return render_template('previa_relatorio.html', 
                           restaurantes=restaurantes, 
                           configuracao_relatorio=configuracao_relatorio,
                           total_encontrado=len(restaurantes))

@app.route('/relatorio_pdf', methods=['POST'])
@login_required
def relatorio_pdf():
    """Gera o relatório em PDF com base nos filtros da pré-visualização."""
    # Recebe os filtros do formulário oculto
    filtros = request.form
    status = filtros.get('status')
    tipos_cozinha_str = filtros.get('tipos_cozinha', '')
    
    query = Restaurante.query

    # Aplicar filtro de status
    if status == 'ativo':
        query = query.filter_by(ativo=True)
    elif status == 'inativo':
        query = query.filter_by(ativo=False)

    # Aplicar filtro de tipos de cozinha
    if tipos_cozinha_str:
        tipos_cozinha_selecionados = tipos_cozinha_str.split(',')
        query = query.filter(Restaurante.tipo_cozinha.in_(tipos_cozinha_selecionados))
    
    restaurantes = query.order_by(Restaurante.nome).all()
    
    rendered_template = render_template('relatorio_pdf.html', 
                                        restaurantes=restaurantes, 
                                        data_geracao=datetime.now())
    
    path_wkhtmltopdf = app.config.get('WKHTMLTOPDF_PATH')
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    
    try:
        pdf = pdfkit.from_string(rendered_template, False, configuration=config)
        response = make_response(pdf)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'inline; filename=relatorio_restaurantes.pdf'
        return response
    except Exception as e:
        print(f"Erro ao gerar PDF: {e}")
        return "Erro ao gerar PDF. Verifique os logs do servidor.", 500

# Rota para o perfil do usuário
@app.route('/perfil', methods=['GET', 'POST'])
@login_required
def perfil():
    if request.method == 'POST':
        current_user.email = request.form.get('email')
        current_user.nome_completo = request.form.get('nome_completo')
        current_user.telefone = request.form.get('telefone')
        current_user.endereco = request.form.get('endereco')
        current_user.cpf_cnpj = request.form.get('cpf_cnpj')
        
        try:
            db.session.commit()
            flash('Perfil atualizado com sucesso!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao atualizar o perfil: {e}', 'danger')
        
        return redirect(url_for('perfil'))
    
    return render_template('perfil.html')

@app.route('/alterar_senha', methods=['POST'])
@login_required
def alterar_senha():
    dados = request.get_json()
    senha_atual = dados.get('senha_atual')
    nova_senha = dados.get('nova_senha')
    confirmar_senha = dados.get('confirmar_senha')

    if not all([senha_atual, nova_senha, confirmar_senha]):
        return jsonify({'sucesso': False, 'mensagem': 'Todos os campos são obrigatórios.'}), 400

    if not check_password_hash(current_user.password, senha_atual):
        return jsonify({'sucesso': False, 'mensagem': 'A senha atual está incorreta.'}), 403
    
    if nova_senha != confirmar_senha:
        return jsonify({'sucesso': False, 'mensagem': 'A nova senha e a confirmação não correspondem.'}), 400

    current_user.password = generate_password_hash(nova_senha)
    
    try:
        db.session.commit()
        return jsonify({'sucesso': True, 'mensagem': 'Senha alterada com sucesso!'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'sucesso': False, 'mensagem': f'Erro ao alterar a senha: {e}'}), 500

# Permite executar a aplicação diretamente com 'python app.py'
if __name__ == '__main__':
    app.run(debug=True)
