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

    def get_quizzes(self, class_room):
        quizzes = []
        for quiz in class_room.quiz_list:
            if quiz.has_this_student_answered(self):
                quizzes.append(quiz)

        return quizzes

    def get_answers_for(self, quiz):
        answers = []
        for quiz_answer in self.quiz_answers:
            if quiz_answer.question.quiz.key() == quiz.key():
                answers.append(quiz_answer)

        return answers





