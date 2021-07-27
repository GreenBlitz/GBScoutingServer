from app import server
from flask import render_template
from flask import request

@server.route('/', methods=['GET', 'POST'])
def index():
    return 'GBHome' # render_template('home/home.html')