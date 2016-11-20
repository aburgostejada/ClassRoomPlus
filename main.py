"""`main` is the top level module for your Flask application."""

# Import the Flask Framework
import calendar
import os

import flask
import jinja2
from flask import Flask, request, flash, url_for, redirect, render_template, g, jsonify
from flask.ext.login import LoginManager, login_required, login_user, logout_user, current_user
from flask import Flask
from crp import teacher
from crp import loc
import time
from crp.DB.classroom_model import ClassRoomModel
from crp.DB.poll_model import PollModel
from crp.DB.quiz_model import QuizModel
from crp.DB.student_model import StudentModel
from crp.DB.teacher_model import TeacherModel
from crp.lib.email import Email
from crp.lib.repository import Repository

localization = loc.Localization()
lan = localization.eng  # Allows to change the language
app = Flask(__name__)
app.jinja_loader = jinja2.FileSystemLoader('crp/templates')
app.secret_key =  os.environ['S_KEY']
app.config['SESSION_TYPE'] = 'filesystem'
login_manager = LoginManager()
login_manager.init_app(app)


# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.
@login_manager.user_loader
def load_user(username):
    return teacher.query_user(username)


@app.before_request
def before_request():
    g.user = current_user


@app.route("/dashboard", methods=["GET"])
def dashboard():
    if current_user.is_authenticated:
        class_rooms = current_user.get_model().class_rooms
        return render_template('dashboard.html', loc=localization, lan=lan, user=current_user, class_rooms=class_rooms)
    else:
        return redirect(url_for('login'))


@app.route("/", methods=["GET"])
def index():
    return redirect(url_for('identity'))


@app.route("/teacher_signup", methods=['GET', 'POST'])
def teacher_signup():
    if request.method == "POST":
            email = request.form['email']
            password = request.form['password']
            confirm = request.form['confirm']
            first_name = request.form['first_name']
            last_name = request.form['last_name']

            if teacher.sign_up(email=email, password=password, confirm=confirm, first_name=first_name, last_name=last_name):
                return redirect(url_for('login'))
            return render_template("teacher_signup.html", loc=localization, lan=lan, error=True)

    email = Email()
    email.send_confirmation_message("aburgostejada@gmail.com")
    return render_template("teacher_signup.html", loc=localization, lan=lan, error=False)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET' and current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'GET':
        return render_template('login.html', loc=localization, lan=lan)

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


@app.route("/identity")
def identity():
    if not current_user.is_authenticated:
        return render_template('identity.html', loc=localization, lan=lan, user=current_user)
    else:
        return redirect(url_for('dashboard'))


@app.route("/teacher_view_classroom", methods=['GET'])
@login_required
def teacher_view_classroom():
    key = request.args.get("key")
    class_room = False
    if key:
        class_room = ClassRoomModel.get(key)

    return render_template("teacher_view_classroom.html", loc=localization,
                           lan=lan, user=current_user, class_room=class_room,
                           page_title=localization.get_text("view_classroom", lan), active="classroom")


@app.route("/teacher_create_classroom", methods=['GET', 'POST'])
@login_required
def teacher_create_classroom():
    if request.method == "POST":
        teacher_repo = Repository(current_user.get_model())
        name = request.form['name']
        students = request.form['students']
        comments = request.form['comments']
        key = request.form['key']

        if key != "false":
            key = teacher_repo.update_classroom(
                key=key, name=name, students=students, comments=comments
            )
        else:
            key = teacher_repo.create_new_classroom(
                name=name, students=students, comments=comments
            )

        return redirect(url_for("teacher_view_classroom", key=key))
    else:
        key = request.args.get("key")
        class_room = False
        if key:
            class_room = ClassRoomModel.get(key)

        return render_template("teacher_create_classroom.html", loc=localization,
                               lan=lan, user=current_user, class_room=class_room,
                               page_title=localization.get_text("create_classroom", lan), active="page")


@app.route("/teacher_created_poll_success", methods=['GET'])
@login_required
def teacher_created_poll_success():
    key = request.args.get("key")
    poll = PollModel.get(key)

    return render_template("teacher_created_poll_success.html", loc=localization, lan=lan,
                           user=current_user, access_code=poll.class_room.access_code,
                           class_room=poll.class_room, page_title="Poll Created", active="page")


@app.route("/teacher_create_poll", methods=['GET', 'POST'])
@login_required
def teacher_create_poll():
    if request.method == "POST":
        repo = Repository(current_user.get_model())
        time_allowed = int(request.form['time_allowed'])
        question = request.form['question']
        answer_type = request.form['answer_type']
        options = request.form.getlist('option[]')
        key = request.form['key']

        poll_key = repo.add_poll_to_classroom(
            key=key, time_allowed=time_allowed, question=question, answer_type=answer_type, options=options
        )

        return redirect(url_for("teacher_created_poll_success", key=poll_key))
    else:
        key = request.args.get("key")
        class_room = ClassRoomModel.get(key)

        return render_template("teacher_create_poll.html", loc=localization, lan=lan,
                               user=current_user, class_room=class_room)


@app.route("/teacher_created_quiz_success", methods=['GET'])
@login_required
def teacher_created_quiz_success():
    key = request.args.get("key")
    quiz = QuizModel.get(key)

    return render_template("teacher_created_quiz_success.html", loc=localization, lan=lan,
                           user=current_user, access_code=quiz.class_room.access_code, class_room=quiz.class_room,
                           page_title="Quiz Created", active="page")


@app.route("/teacher_delete_quiz_question", methods=['POST'])
@login_required
def teacher_delete_quiz_question():
    repo = Repository(current_user.get_model())
    repo.delete_quiz_question(request.args.get("key"))
    return flask.jsonify(dict(result="success"))


def render_quiz(quiz, class_room):
    return render_template("teacher_create_quiz.html", loc=localization, lan=lan,
                           user=current_user, class_room=class_room, quiz=quiz,
                           page_title=localization.get_text("create_quiz", lan),
                           active="page")


@app.route("/teacher_create_quiz", methods=['GET', 'POST'])
@login_required
def teacher_create_quiz():
    if request.method == "POST":
        repo = Repository(current_user.get_model())
        time_allowed = int(request.form['time_allowed'])
        quiz_title = request.form['quiz_title']
        question = request.form['question']
        answer_type = request.form['answer_type']
        options = request.form.getlist('option[]')
        classroom_key = request.form['classroom_key']
        quiz_key = request.form['quiz_key']
        submit = request.form['submit']

        if not quiz_key or str(quiz_key) == "":
            quiz_key = repo.add_quiz_to_classroom(
                classroom_key=classroom_key, time_allowed=time_allowed, title=quiz_title
            )
        else:
            repo.update_quiz_to_classroom(
                quiz_key=quiz_key, time_allowed=time_allowed, title=quiz_title
            )

        if submit == "save":
            repo.add_question_to_quiz(
                quiz_key=quiz_key, question=question, answer_type=answer_type, options=options
            )
            return redirect(url_for("teacher_created_quiz_success", key=quiz_key))
        elif submit == "add":
            repo.add_question_to_quiz(
                quiz_key=quiz_key, question=question, answer_type=answer_type, options=options
            )
            return redirect(url_for("teacher_create_quiz", quiz_key=quiz_key, classroom_key=classroom_key, time=calendar.timegm(time.gmtime())))
    else:
        quiz = QuizModel.get(request.args.get("quiz_key")) if request.args.get("quiz_key") else False
        class_room = ClassRoomModel.get(request.args.get("classroom_key"))
        return render_quiz(quiz, class_room)





@app.route("/teacher_view_poll", methods=['GET', 'POST'])
@login_required
def teacher_view_poll():
    if request.method == "POST":
        key = request.form['key']
        poll = PollModel.get(key)
        repo = Repository(current_user.get_model())
        repo.disable_poll(
            key=key
        )
        return redirect(url_for("teacher_view_classroom", key=poll.class_room.key()))
    else:
        key = request.args.get("key")
        poll = PollModel.get(key)

        return render_template("teacher_view_poll.html", loc=localization, lan=lan,
                               user=current_user, poll=poll, class_room=poll.class_room,
                               page_title="Poll Details", active="page")


@app.route("/teacher_view_quiz", methods=['GET', 'POST'])
@login_required
def teacher_view_quiz():
    if request.method == "POST":
        key = request.form['key']
        quiz = QuizModel.get(key)
        repo = Repository(current_user.get_model())
        repo.disable_quiz(
            key=key
        )
        return redirect(url_for("teacher_view_classroom", key=quiz.class_room.key()))
    else:
        key = request.args.get("key")
        quiz = QuizModel.get(key)

        return render_template("teacher_view_quiz.html", loc=localization, lan=lan,
                               user=current_user, quiz=quiz, class_room=quiz.class_room,
                               page_title="Quiz Details", active="page")


@app.route("/teacher_view_student", methods=['GET'])
@login_required
def teacher_view_student():
        key = request.args.get("key")
        student = StudentModel.get(key)
        class_room = student.class_room

        return render_template("teacher_view_student.html", loc=localization,
                               lan=lan, user=current_user, student=student, class_room=class_room,
                               page_title="Student Details", active="page")


@app.route("/student_view_classroom", methods=['POST', 'GET'])
def student_view_classroom():
    if request.method == "POST":
        access_code = request.form['access_code']
        pin = request.form['pin']
        class_room = ClassRoomModel.get_by_access_code(access_code)

        if class_room and class_room.get_student(pin):
            student = class_room.get_student(pin)
            return render_template("student_view_classroom.html", loc=localization,
                                   lan=lan, user=current_user, class_room=class_room,
                                   page_title=localization.get_text("view_classroom", lan),
                                   active="classroom", student=student)
        else:
            return render_template("student_landing.html", loc=localization,
                                   lan=lan, user=current_user, error=True)
        # else:
        #     return redirect(url_for("student_take_poll", poll_key=poll.key(), student_key=student.key()))
    else:
        return redirect(url_for("student_landing"))


@app.route("/student_landing", methods=['GET'])
def student_landing():
    return render_template("student_landing.html", loc=localization, lan=lan, user=current_user)


@app.route("/student_take_quiz", methods=['GET', 'POST'])
def student_take_quiz():
    if request.method == "POST":
        quiz_key = request.form['quiz_key']
        student_key = request.form['student_key']
        quiz = QuizModel.get(quiz_key)
        student = StudentModel.get(student_key)
        student_answered = False

        if not quiz.has_this_student_answered(student):
            repo = Repository(None)
            for question in quiz.get_active_questions():
                question_id = str(question.key().id_or_name())
                if question.type == "yes_no" or question.type == "free_text" or question.type == "single":
                    repo.save_student_quiz_answer(student, question, request.form['answer-'+question_id])
                elif question.type == "multiple":
                    repo.save_student_quiz_answer(student, question, request.form.getlist('answer-'+question_id+'[]'))
        else:
            student_answered = True

        return render_template("student_take_quiz_success.html", loc=localization, lan=lan,
                               user=current_user, student_answered=student_answered)
    else:
        quiz_key = request.args.get("quiz_key")
        student_key = request.args.get("student_key")
        quiz = QuizModel.get(quiz_key)
        student = StudentModel.get(student_key)
        classroom = quiz.class_room

        return render_template("student_take_quiz.html", loc=localization, lan=lan,
                               user=current_user, class_room=classroom, quiz=quiz,
                               student=student)


@app.route("/student_take_poll", methods=['GET', 'POST'])
def student_take_poll():
    if request.method == "POST":
        poll_key = request.form['poll_key']
        student_key = request.form['student_key']
        poll = PollModel.get(poll_key)
        student = StudentModel.get(student_key)
        student_answered = False

        if not poll.has_this_student_answered(student):
            repo = Repository(None)
            if poll.type == "yes_no" or poll.type == "free_text" or poll.type == "single":
                repo.save_student_answer(student, poll, request.form['answer'])
            elif poll.type == "multiple":
                repo.save_student_answer(student, poll, request.form.getlist('answer[]'))
        else:
            student_answered = True

        return render_template("student_take_poll_success.html", loc=localization, lan=lan,
                               user=current_user, student_answered=student_answered)
    else:
        poll_key = request.args.get("poll_key")
        student_key = request.args.get("student_key")
        poll = PollModel.get(poll_key)
        student = StudentModel.get(student_key)
        classroom = poll.class_room

        return render_template("student_take_poll.html", loc=localization, lan=lan,
                               user=current_user, class_room=classroom, poll=poll,
                               student=student)
