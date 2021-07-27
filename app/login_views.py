from flask import request
from app import server

@server.route('/register_user', methods=['GET', 'POST'])
def register_user():
    params = request.args
    name = params.get('uname')
    role = params.get('role')

    users_txt = ''
    with open('DB/users.txt', 'r') as f:
        users_txt = f.read()

    uid = 0
    if users_txt != '':
        pass

    with open('DB/users.txt', 'a') as f:
        pass

    return 'Register' #render_template('admin/admin.html')
