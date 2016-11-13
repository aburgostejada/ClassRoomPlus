import base64

from google.appengine.ext import db

from crp.DB.classroom_model import ClassRoomModel


class PollModel(db.Model):
    type = db.StringProperty(required=True, choices={"yes_no", "free_text", "multiple", "single"})
    options = db.StringListProperty()
    time_allowed = db.IntegerProperty(required=True)
    question = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    status = db.StringProperty(required=True, choices={"active", "close", "pending"})
    class_room = db.ReferenceProperty(ClassRoomModel, collection_name='poll_list')

    @classmethod
    def get_all_by(cls, attr, value):
        q = PollModel.all()
        q.filter(attr+" =", value)
        return q.fetch(1000)

    def is_close(self):
        return self.status == "close"

    def get_total_answered(self):
        total = 0
        for student in self.class_room.students:
            if self.has_this_student_answered(student):
                total += 1

        return total

    def completed(self):
        return self.get_total_answered() >= self.class_room.students.count()

    def get_encoded_options(self):
        return [(x, base64.b64encode(x)) for x in self.options]

    def has_this_student_answered(self, student):
        for answer in self.answers:
            if answer.student.key() == student.key():
                return True

        return False
