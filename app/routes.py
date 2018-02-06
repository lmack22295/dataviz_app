from app import app, db
from flask import render_template, flash, redirect, url_for, request
from app.forms import LoginForm, RegistrationForm, GroupForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Group
from werkzeug.urls import url_parse

@app.route('/', methods=['GET','POST'])
@app.route('/index', methods=['GET','POST'])
@login_required
def index():
    form = GroupForm()
    if form.validate_on_submit():
        group = Group(name=form.name.data)
        db.session.add(group)
        db.session.commit()
        flash('Your group is now live!')
        return redirect(url_for('index'))
    groups = Group.query.all()
    user = {'username': 'Lmack'}
    categories = [
        {
            'name': 'Flask Resources',
            'sites': [{'description': 'Flask Blog Tutorial',
                    'link': 'https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iii-web-forms'}]
        }
    ]
    return render_template('index.html', title='Home', groups=groups, form=form, categories=categories)

@app.route('/group/<group_id>')
def group(group_id):
    group = Group.query.get(group_id)
    siteList = group.sites
    sites = []
    for s in siteList:
        sites.append(s)
    return render_template('group.html', title=group.name, group=group, sites=sites)

@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)
