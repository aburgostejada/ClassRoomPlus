"""`main` is the top level module for your Flask application."""

# Import the Flask Framework
import jinja2
from flask import Flask, request, flash, url_for, redirect, render_template, g, jsonify
from flask.ext.login import LoginManager, login_required, login_user, logout_user, current_user
from flask import Flask
from crp import teacher
from crp.DB.teacher_model import TeacherModel

app = Flask(__name__)
app.jinja_loader = jinja2.FileSystemLoader('crp/templates')
app.secret_key = "1u691O4d7?-9R(0G&o|L8iaR3740*O"
app.config['SESSION_TYPE'] = 'filesystem'
login_manager = LoginManager()
login_manager.init_app(app)
# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.
@login_manager.user_loader
def load_user(id):
    return teacher.query_user(id)


@app.before_request
def before_request():
    g.user = current_user


@app.route("/dashboard", methods=["GET"])
@login_required
def dashboard():
    return render_template('dashboard.html', name=current_user.get_name())


@app.route("/", methods=["GET"])
def index():
    return redirect(url_for('login'))

@app.route("/new_teacher_once", methods=["GET"])
def new_teacher_once():
    # TeacherModel(user_name="aburgos",
    #                        password="f920cd4628136d5cef595ba8d629758b6d6e96463f64afe1407309d0be0cd361",
    #                        first_name="Augusto",
    #                        last_name="Burgos",
    #                        status="active").put()

    # TeacherModel(user_name="fandi",
    #              password="4b2f3acea03a8e3858baa671a2ffcd4012f60e5ec248b1e0feb3b806e322d1cd",
    #              first_name="Fandi",
    #              last_name="Peng",
    #              status="active").put()
    return "true"


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET' and current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'GET':
        return render_template('login.html')

    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        remember_me = False
        if 'remember_me' in request.form:
            remember_me = True
        registered_user = teacher.auth(username=username, password=password)
        if registered_user is None:
            flash('Username or Password is invalid', 'error')
            return redirect(url_for('login'))
        login_user(registered_user, remember=remember_me)
        flash('Logged in successfully')
        return redirect(request.args.get('next') or url_for('dashboard'))
    return redirect(url_for("index"))


@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, Nothing at this URL.', 404


@app.errorhandler(500)
def application_error(e):
    """Return a custom 500 error."""
    return 'Sorry, unexpected error: {}'.format(e), 500
