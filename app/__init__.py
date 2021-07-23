from flask import Flask

server = Flask(__name__)


from app import views
from app import admin_views