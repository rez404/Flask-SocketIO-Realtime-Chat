from flask import Flask,render_template,request,url_for,redirect
from flask_socketio import SocketIO
app = Flask(__name__)
socketio=SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat')
def chat():
    username=request.args.get("username")
    password=request.args.get("password")
    if username and password:
        return render_template("chat.html",username=username,password=password)
    else:
        return redirect(url_for("home"))

if __name__ == '__main__':
  socketio.run(app,debug=True)


class Message():
    pass