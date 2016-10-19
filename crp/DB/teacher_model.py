from google.appengine.ext import db


class TeacherModel(db.Model):
    user_name = db.StringProperty(required=True)
    password = db.StringProperty(required=True)
    first_name = db.TextProperty()
    last_name = db.TextProperty()
    created = db.DateTimeProperty(auto_now_add=True)
    status = db.StringProperty(required=True, choices={"active", "disabled", "pending"})

    @classmethod
    def get_all_by(cls, attr, value):
        q = TeacherModel.all()
        q.filter(attr+" =", value)
        q.filter("status =", "active")
        return q.fetch(1000)

    @classmethod
    def exits(cls, user_name):
        q = TeacherModel.all()
        q.filter("user_name =", user_name)

        total = q.count()
        if total > 0:
            return True
        return False

    # @classmethod
    # def get_by(cls, user_name):
    #     q = TeacherModel.all()
    #     q.filter("id =", user_name)
    #     return q.get()

    @classmethod
    def delete_by(cls, id):
        success = False
        q = TeacherModel.all()
        q.filter("id =", id)
        for obj in q.fetch(1000):
            success = obj.delete()
        return success

    @classmethod
    def get_by_username(cls, username):
        q = TeacherModel.all()
        q.filter("user_name =", username)
        return q.get()

    @classmethod
    def auth(cls, username, password):
        q = TeacherModel.all()
        q.filter("user_name =", username)
        q.filter("password =", password)
        total = q.count()
        if total == 1:
            return True
        return False



