from flask import render_template

from app import server


@server.route('/admin')
def admin():
    return 'GBAdmin' #render_template('admin/admin.html')
