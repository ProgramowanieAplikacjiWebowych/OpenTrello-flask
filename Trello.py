from flask import Flask, Response, redirect, request, abort, render_template
from flask_login import LoginManager, login_required, login_user, logout_user, UserMixin
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

from Database.base import connectionSettings
from Form.LoginForm.LoginForm import LoginForm
from Form.RegisterForm.RegisterForm import RegisterForm
from UsersAccountManager.UsersAccountManager import UsersAccountManager

app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# config
app.config.update(
    DEBUG=True,
    SECRET_KEY='secret_xxx',
    SQLALCHEMY_TRACK_MODIFICATIONS=False
)

app.config['SQLALCHEMY_DATABASE_URI'] = connectionSettings
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class User(UserMixin, db.Model):
    __tablename__ = 'OT_USERS_T'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128))
    password = db.Column(db.String(128))
    email = db.Column(db.String(128))
    active = db.Column(db.Integer)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __init__(self, id):
        self.id = id
        self.name = "user" + str(id)
        self.password = self.name + "_secret"

    def __init__(self, username, email):
        self.username = username
        self.email = email
        self.active = 0


@app.route('/')
@login_required
def home():
    return render_template('index.html')


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    usersAccountManager = UsersAccountManager()

    if request.method == 'POST':
        if (form.validate_on_submit()):
            ##ser = usersAccountManager.getUserData(db, form.username.data, form.password.data)
            user = User.query.filter_by(email=form.username.data).first()

            if (user != None and user.check_password(form.password.data)):
                login_user(user)
                return redirect("/")
            else:
                return abort(401)
    else:
        return render_template('login.html', form=form)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if request.method == 'POST':
        if (form.validate()):
            # ser = usersAccountManager.getUserData(form.username.data, form.password.data)
            user = User.query.filter_by(email=form.email.data).first()

            if (user == None):
                user = User(username=form.username.data, email=form.email.data)
                user.set_password(form.password.data)
                db.session.add(user)
                db.session.commit()
                return redirect("/")
            else:
                return abort(401)
    else:
        return render_template('register.html', form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")


# handle login failed
@app.errorhandler(401)
def page_not_found(e):
    return Response('<p>Login failed</p>')


# callback to reload the user object
@login_manager.user_loader
def load_user(userid):
    return User(username="Example", email="exa")


if __name__ == "__main__":
    app.run()
