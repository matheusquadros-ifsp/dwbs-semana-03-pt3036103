# Aplicação Flask com templates (Jinja2), Flask-Bootstrap, Flask-Moment e Flask-WTF.
# Atividade da semana 05 - PTBDSWS (Desenvolvimento Web Servidor) - Aula 050: Formulários.
from datetime import datetime

from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)

# Chave secreta: usada pelo Flask-WTF para proteger a sessão do usuário contra
# adulterações e para gerar o token de proteção contra ataques CSRF
# (Cross-Site Request Forgery). Em produção real, o ideal é ler esse valor de
# uma variável de ambiente, e não deixá-lo fixo no código.
app.config['SECRET_KEY'] = 'pt3036103-chave-secreta-dwbs-aula050'

bootstrap = Bootstrap(app)
moment = Moment(app)


# Formulário com um único campo de texto obrigatório (name) e um botão de
# submissão (submit). Cada formulário web é representado por uma classe que
# herda de FlaskForm.
class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')


# https://matheusquadros.pythonanywhere.com/
# Root. Exibe "Hello, Stranger!" até que o usuário informe o nome pelo
# formulário. Usa o padrão Post/Redirect/Get (PRG) para evitar reenvio
# duplicado do formulário ao atualizar a página, e dispara uma mensagem
# flash quando o nome enviado é diferente do último salvo na sessão.
@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        session['name'] = form.name.data
        return redirect(url_for('index'))
    return render_template(
        'index.html',
        form=form,
        name=session.get('name'),
    )


# https://matheusquadros.pythonanywhere.com/user/<name>/<prontuario>/<instituicao>
# Aba "Identificação". Recebe nome, prontuário e instituição como parâmetros na URL.
# Valores default usados no menu de navegação: Matheus Quadros, PT3036103, IFSP.
@app.route('/user/<name>/<prontuario>/<instituicao>')
def user(name, prontuario, instituicao):
    return render_template(
        'user.html',
        name=name,
        prontuario=prontuario,
        instituicao=instituicao,
    )


# https://matheusquadros.pythonanywhere.com/contextorequisicao/<name>
# Aba "Contexto da requisição". Exibe navegador, IP remoto e host da aplicação,
# obtidos a partir do contexto da requisição. Valor default: Matheus Quadros.
@app.route('/contextorequisicao/<name>')
def contexto_requisicao(name):
    user_agent = request.headers.get('User-Agent')
    remote_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    host = request.host_url
    return render_template(
        'context.html',
        name=name,
        user_agent=user_agent,
        remote_ip=remote_ip,
        host=host,
    )


if __name__ == '__main__':
    app.run(debug=True)
