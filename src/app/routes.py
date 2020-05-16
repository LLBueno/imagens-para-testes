from app import app, db
from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required
from app.forms import LoginForm, RegistrationForm
from app.models import User


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Usuário ou Senha inválido')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('home'))
    return render_template('login.html', title='login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Parabéns, usuário cadastrado!')
        return redirect(url_for('login'))
    return render_template('registro.html', title='registro', form=form)


@app.route('/')
@app.route('/home')
@login_required
def home():
    return render_template('home.html', title='home')


@app.route('/imagem')
@login_required
def imagem():
    return render_template('imagem.html', title='imagem')


@app.route('/contato')
@login_required
def contato():
    return render_template('contato.html', title='contato')


@app.route('/sobre')
@login_required
def sobre():
    return render_template('sobre.html', title='sobre')
