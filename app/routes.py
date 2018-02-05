from app import app
from flask import render_template, flash, redirect, url_for
from app.forms import LoginForm

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Lmack'}
    categories = [
        {
            'name': 'Flask Resources',
            'sites': [{'description': 'Flask Blog Tutorial',
                    'link': 'https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iii-web-forms'}]
        }
    ]
    return render_template('index.html', title='Home', user=user, categories=categories)

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)
