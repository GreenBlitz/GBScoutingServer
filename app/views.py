from app import server
from flask import render_template
from flask import request

@server.route('/', methods=['GET', 'POST'])
def index():
    return 'GBHome', 200 # render_template('home/home.html')