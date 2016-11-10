from google.appengine.ext import db

from crp.DB.classroom_model import ClassRoomModel

class QuizModel(db.Model):
    time_allowed = db.IntegerProperty(required=True)
    title = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    status = db.StringProperty(required=True, choices={"active", "close", "pending"})
    class_room = db.ReferenceProperty(ClassRoomModel, collection_name='quiz_list')

    @classmethod
    def get_all_by(cls, attr, value):
        q = QuizModel.all()
        q.filter(attr+" =", value)
        return q.fetch(1000)

    def get_total_answered(self):
        return 0

    def completed(self):
        return False

    def is_close(self):
        return self.status == "close"
