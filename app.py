import datetime
from flask import Flask, render_template, send_from_directory, request, Response
import database as db


DB_FILE = 'db.sqlite'


app = Flask(__name__)


@app.route('/')
def index():  # put application's code here
    return render_template("client/public/index.html")


@app.route('/<path:path>')
def resource(path):
    return send_from_directory("templates/client/public", path)


@app.route('/login', methods=['POST'])
def login():
    ctx = db.create_connection(DB_FILE)
    data = request.get_json()
    name, password = data['name'], data['password']
    user_id = db.auth_user(ctx, name, password)
    if user_id:
        response = Response("{userId: %d}" % user_id, 200, mimetype='application/json')
        response.set_cookie('auth', value=str(user_id), expires=datetime.date.today() + datetime.timedelta(days=10))
        return response
    return Response(status=403)


@app.route('/register', methods=['POST'])
def register():
    ctx = db.create_connection(DB_FILE)
    data = request.get_json()
    name, password = data['name'], data['password']
    user_id = db.register(ctx, name, password)
    if user_id:
        response = Response("{userId: %d}" % user_id, 200, mimetype='application/json')
        response.set_cookie('auth', value=str(user_id), expires=datetime.date.today() + datetime.timedelta(days=10))
        return response
    return Response(status=403)


@app.route('/notes', methods=['GET'])
def get_notes():
    ctx = db.create_connection(DB_FILE)
    user_id = request.cookies.get('auth')
    if user_id:
        notes = '['+",".join(map(lambda row: '{'+f'"id": {row[0]}, "note": "{row[1]}"'+'}',
                                 db.get_all_notes(ctx, user_id)))+']'
        response = Response(notes, 200, mimetype='application/json')
        return response
    return Response(status=403)


@app.route('/notes', methods=['POST'])
def post_note():
    ctx = db.create_connection(DB_FILE)
    user_id = request.cookies.get('auth')
    if user_id:
        note = db.post_note(ctx, user_id, request.get_json()['note'])
        response = Response('{'+f'id: {note[0]}, note: {note[1]}'+'}', 200, mimetype='application/json')
        return response
    return Response(status=403)


if __name__ == '__main__':
    app.run()
