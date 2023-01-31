from flask import render_template, request, redirect, session, flash, url_for
from jogoteca import app
from models import Usuarios
from helpers import FormularioUsuario
from flask_bcrypt import check_password_hash


@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    form = FormularioUsuario()
    # O if abaixo foi adicionado para que quando um usuário não logado acesse
    # a página de login ele seja direcionado para esta página, mas sem o envio
    # variável próxima
    if not proxima:
        return render_template('login.html', proxima=url_for('index'), form=form)
    return render_template('login.html', proxima=proxima, form=form)
    # return redirect(url_for('novo'))



@app.route('/autenticar', methods=['POST', ])
def autenticar():
    form = FormularioUsuario(request.form)
    usuario = Usuarios.query.filter_by(nickname=form.nickname.data).first()
    print(f'Aqui está o usuário: {usuario}')
    print(f'Aqui está o tipo do usuário: {type(usuario)}')
    senha = check_password_hash(usuario.senha, form.senha.data)
    if usuario and senha:
        session['usuario_logado'] = usuario.nickname
        flash(usuario.nome + ' logado com sucesso!')
        proxima_pagina = request.form['proxima']
        return redirect(proxima_pagina)
    else:
        flash('Usuário não logado')
        return redirect(url_for('login'))



@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Logout efetuado com sucesso!')
    return redirect(url_for('index'))

