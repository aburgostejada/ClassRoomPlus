from google.appengine.ext import db

from crp.DB.classroom_model import ClassRoomModel


class StudentModel(db.Model):
    pin = db.IntegerProperty(required=True)
    name = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    status = db.StringProperty(required=True, choices={"active", "disabled", "pending"})
    class_room = db.ReferenceProperty(ClassRoomModel, collection_name='students')

    @classmethod
    def get_all_by(cls, attr, value):
        q = StudentModel.all()
        q.filter(attr+" =", value)
        q.filter("status =", "active")
        return q.fetch(1000)

    @classmethod
    def exits(cls, user_name):
        q = StudentModel.all()
        q.filter("pin =", user_name)

        total = q.count()
        if total > 0:
            return True
        return False

    # @classmethod
    # def get_by(cls, user_name):
    #     q = TeacherModel.all()
    #     q.filter("id =", user_name)
    #     return q.get()

    # @classmethod
    # def delete_by(cls, id):
    #     success = False
    #     q = TeacherModel.all()
    #     q.filter("id =", id)
    #     for obj in q.fetch(1000):
    #         success = obj.delete()
    #     return success

    # @classmethod
    # def get_by_username(cls, username):
    #     q = TeacherModel.all()
    #     q.filter("user_name =", username)
    #     return q.get()





