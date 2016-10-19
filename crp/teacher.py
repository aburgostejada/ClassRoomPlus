from flask.ext.login import UserMixin
import hashlib
# Basic Hash 256 ( No Secure enough for real app, desired (HMAC + SALT) )
from crp.DB.teacher_model import TeacherModel

class Teacher(UserMixin):
    def __init__(self, username, first_name, last_name):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.username)

    def get_username(self):
        return self.username

    def get_name(self):
        return self.first_name+" "+self.last_name

    def __repr__(self):
        return '<User %r>' % self.username

    @classmethod
    def get(cls, id):
        return query_user(id)


def query_user(username):
    teacher = TeacherModel.get_by_username(str(username))

    return Teacher(teacher.user_name, teacher.first_name, teacher.last_name)


def auth(username, password):
    if TeacherModel.auth(username, hashlib.sha256(password).hexdigest()):
        return query_user(username)
    return None
