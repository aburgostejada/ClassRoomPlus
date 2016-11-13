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
        q.filter(attr + " =", value)
        return q.fetch(1000)

    @staticmethod
    def get_by(items, prop, value):
        items.filter(prop + " =", value)
        if items.count() == 0:
            return []

        result = items.fetch(1000)
        return result

    def has_this_student_answered(self, student):
        for question in self.questions_list:
            for answer in question.answers:
                if answer.student.key() == student.key():
                    return True
        return False

    def get_total_questions(self):
        questions = self.get_active_questions()
        if not questions:
            return 0

        return len(questions)

    def get_active_questions(self):
        return self.get_by(self.questions_list, "status", "active")

    def get_total_answered(self):
        total = 0
        for student in self.class_room.students:
            if self.has_this_student_answered(student):
                total += 1

        return total

    def completed(self):
        return self.get_total_answered() >= self.class_room.students.count()

    def is_close(self):
        return self.status == "close"
