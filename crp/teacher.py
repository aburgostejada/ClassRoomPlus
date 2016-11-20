from flask.ext.login import UserMixin
import hashlib
import re
from werkzeug.security import generate_password_hash, check_password_hash
from crp.DB.teacher_model import TeacherModel
from crp.lib.email import Email


class Teacher(UserMixin):
    def __init__(self, email, first_name, last_name):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name

    def is_authenticated(self):
        if self.email is None:
            return False

        return self.is_active()

    def is_confirmed(self):
        if self.email is None:
            return False

        teacher = self.get_model()
        return teacher.confirmed

    def is_active(self):
        if self.email is None:
            return False

        teacher = self.get_model()
        return teacher.status == "active"

    def is_anonymous(self):
        return False

    def get_id(self):
        if self.email is None:
            return False

        return unicode(self.email)

    def get_email(self):
        return self.email

    def get_name(self):
        return self.first_name + " " + self.last_name

    def get_model(self):
        return TeacherModel.get_by_email(str(self.email))

    def __repr__(self):
        return '<User %r>' % self.email

    @classmethod
    def get(cls, id):
        return query_user(id)


def get_password_hash(password):
    return generate_password_hash(password)


def check_password(pw_hash, password):
    return check_password_hash(pw_hash, password)


def query_user(email):
    teacher = TeacherModel.get_by_email(str(email))
    if teacher is None:
        return Teacher(None, None, None)
    return Teacher(teacher.email, teacher.first_name, teacher.last_name)


def auth(email, password):
    teacher = TeacherModel.get_valid_teacher(email)

    if teacher and check_password(teacher.password, password):
        return query_user(email)
    return None


def email_validator(email):
    p = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
    return p.match(email)


def sign_up(email, password, confirm, first_name, last_name):
    if not email_validator(email) or password != confirm or str(first_name) == "" or str(last_name) == "":
        return False

    teacher_key = TeacherModel(email=email, password=get_password_hash(password),
                               first_name=first_name, last_name=last_name, status="active").put()

    if teacher_key:
        Email().send_confirmation_message(email)

    return teacher_key
