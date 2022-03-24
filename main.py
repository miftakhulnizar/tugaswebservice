# 6D/19090081/miftakhulnizar
# 6D/19090128/annonpriantomo

from flask import Flask, jsonify, request
import os, random, string
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app_dir = os.path.dirname(os.path.abspath(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///{}".format(
    os.path.join(app_dir, "users.db"))
db = SQLAlchemy(app)


class User(db.Model):
    username = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
    password = db.Column(db.String(80), unique=False, nullable=False, primary_key=False)
    token = db.Column(db.String(225), unique=True, nullable=True, primary_key=False)


@app.route('/buat_db')
def create_db():
    db.create_all()
    return 'db berhasil'


@app.route('/nambah_user')
def add_user():
    print('Masukan username:')
    username = input()
    print('Masukan password:')
    password = input()

    data = User(username=username,password=password)
    db.session.add(data)

    db.session.commit()

    return 'Users berhasil'


# POST http://127.0.0.1:5000/api/v1/login
@app.route('/api/v1/login', methods=['POST'])
def authentication():

    username = request.values.get('username')
    password = request.values.get('password')

    
    account = User.query.filter_by(username=username, password=password).first()
    
    if account:
        token = ''.join(random.choices(
            string.ascii_uppercase + string.digits, k=10))

        User.query.filter_by(username=username, password=password).update({'token': token})
        db.session.commit()

        data = {'result': 'berhasil', 'msg': 'Login berhasil', 'token': token}
        return jsonify(data)
    else:
        data = {'result': 'gagal', 'msg': 'Login gagal'}
        return jsonify(data)


# POST http://127.0.0.1:5000/api/v2/users/info
@app.route('/api/v2/users/info', methods=['POST'])
def users_info():
    token = request.values.get('token')
    account = User.query.filter_by(token=token).first()
    if account:
        return account.username
    else:
        return 'token salah'

if __name__ == '__main__':
    app.run(debug=True, port=5000)