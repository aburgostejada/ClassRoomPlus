from google.appengine.ext import db


class TeacherModel(db.Model):
    email = db.StringProperty(required=True)
    password = db.StringProperty(required=True)
    first_name = db.TextProperty()
    last_name = db.TextProperty()
    created = db.DateTimeProperty(auto_now_add=True)
    confirmed = db.BooleanProperty(default=False)
    confirmed_on = db.DateTimeProperty()
    status = db.StringProperty(required=True, choices={"active", "disabled", "pending"})

    @classmethod
    def get_all_by(cls, attr, value):
        q = TeacherModel.all()
        q.filter(attr+" =", value)
        q.filter("status =", "active")
        return q.fetch(1000)

    @classmethod
    def exits(cls, email):
        q = TeacherModel.all()
        q.filter("email =", email)

        total = q.count()
        if total > 0:
            return True
        return False

    @classmethod
    def delete_by(cls, id):
        success = False
        q = TeacherModel.all()
        q.filter("id =", id)
        for obj in q.fetch(1000):
            success = obj.delete()
        return success

    @classmethod
    def get_by_email(cls, email):
        q = TeacherModel.all()
        q.filter("email =", email)
        return q.get()

    @classmethod
    def get_valid_teacher(cls, email):
        q = TeacherModel.all()
        q.filter("email =", email)
        q.filter("status =", "active")
        q.filter("confirm =", True)
        total = q.count()
        if total == 1:
            return True
        return False



