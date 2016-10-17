from flask.ext.login import UserMixin
import hashlib
# Basic Hash 256 ( No Secure enough for real app, desired (HMAC + SALT) )
user_database = {
    "aburgos": "f920cd4628136d5cef595ba8d629758b6d6e96463f64afe1407309d0be0cd361",
    "fandi": "4b2f3acea03a8e3858baa671a2ffcd4012f60e5ec248b1e0feb3b806e322d1cd" #  Welc0me1
 }

class User(UserMixin):
    def __init__(self, username, password):
        self.id = username
        self.password = password

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def get_username(self):
        return self.id

    def __repr__(self):
        return '<User %r>' % self.id

    @classmethod
    def get(cls, id):
        return query_user(id)


def query_user(username):
    return User(username, user_database[username])


def auth(username, password):
    if username in user_database:
        if user_database[username] == hashlib.sha256(password).hexdigest():
            return query_user(username)

    return None
