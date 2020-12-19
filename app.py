import eventlet
eventlet.monkey_patch()

import flask_socketio

from flask_socketio import SocketIO, send, emit

from flask import Flask, \
    redirect, render_template, request, session

app = Flask(__name__)
app.secret_key = 'efewhfuyy2138423ijkr53249085-90rvg8e-3j42'
app.config['SECRET_KEY'] = 'efewhfuyy2138423ijkr53249085-90rvg8e-3j423242'
socketio = SocketIO(app, cors_allowed_origins='*')

@socketio.on('message')
def get_data(data):
    if "connected" in data:
        emit('bar', data, broadcast=True)
        print("[USER] "+data)
    else:
        send(data, broadcast=True)

users = []

@app.route("/", methods=['POST', 'GET'])
def index_page():
    try:
        aUser = session['username']
        return render_template("index.html", username=aUser, title="Chat")
    except:
        rUser = request.args.get('username')
        if rUser:
            if rUser not in users: 
                session['username'] = rUser
                users.append(rUser)
            return redirect("/")

        else:
            return render_template("index.html", username=None, title="Auth")

@app.route("/exit")
def exit_page():
    try:
        user = session['username']
        del session['username']
        users.remove(user)
    except:
        pass

    return redirect("/")

if __name__ == "__main__":
    print("[CONSOLE] Server run")
    socketio.run(app)



