from flask import render_template,request,redirect,url_for
from . import main
from flask_login import login_required,current_user


@main.route('/home')
def home():
    '''
    Home page
    '''
    if current_user is None:
        return redirect(url_for('auth.register'))


    message = 'Your time starts now'
    title = 'ThinkTank'
    return render_template('index.html', title = title, message = message)