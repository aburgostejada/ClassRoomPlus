from google.appengine.ext import db
from crp.DB.teacher_model import TeacherModel


class ClassRoomModel(db.Model):
    name = db.TextProperty(required=True)
    passcode = db.TextProperty(required=True)
    comments = db.TextProperty()
    created = db.DateTimeProperty(auto_now_add=True)
    status = db.StringProperty(required=True, choices={"active", "disabled", "deleted"})
    teacher = db.ReferenceProperty(TeacherModel, collection_name='class_rooms')

    def students_list_string(self):
        return ', '.join([x.name for x in self.students])

    @classmethod
    def get_all_by(cls, attr, value):
        q = ClassRoomModel.all()
        q.filter(attr+" =", value)
        return q.fetch(1000)

    @classmethod
    def exits(cls, id):
        q = ClassRoomModel.all()
        q.filter("id =", id)

        total = q.count()
        if total > 0:
            return True
        return False

    @classmethod
    def delete_by(cls, id):
        success = False
        q = ClassRoomModel.all()
        q.filter("id =", id)
        for obj in q.fetch(1000):
            success = obj.delete()
        return success




