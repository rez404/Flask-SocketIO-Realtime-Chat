from flask import Flask,render_template,request,url_for,redirect
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/kande/Desktop/flask-chat-app/chat.db'
socketio=SocketIO(app)
db = SQLAlchemy(app)

@app.route('/')
def index():

    return render_template('index.html')

@app.route('/register')
def register():
    return render_template('register.html')


@app.route("/add" , methods=["POST"])
def add_user():
    username=request.form.get("username")
    password=request.form.get("password")
    add_user= User(username=username)
    add_user.set_password(password)
    db.session.add(add_user)
    db.session.commit()
    return redirect(url_for("index"))

@app.route('/chat' , methods=["POST","GET"])
def chat():
    user=request.form.get("username")
    password=request.form.get("password")
    real=User.query.filter_by(username=user).first()
    if real==None:
        return redirect(url_for("index"))
    elif user and real.check_password(password):
        return render_template("chat.html",user=user)
    else:
        return redirect(url_for("index"))


class User(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128),nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


if __name__ == '__main__':
    socketio.run(app,debug=True)