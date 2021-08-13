from flask import render_template,request,redirect,url_for

from . import main
from flask_login import login_required


@main.route('/')
def home():
    '''
    Home page
    '''

    message = 'Your time starts now'
    title = 'ThinkTank'
    return render_template('index.html', title = title, message = message)