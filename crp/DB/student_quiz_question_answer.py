from google.appengine.ext import db

from crp.DB.quiz_question_model import QuizQuestionModel
from crp.DB.student_model import StudentModel


class StudentQuizQuestionAnswerModel(db.Model):
    answer = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    student = db.ReferenceProperty(StudentModel, collection_name='quiz_answers')
    question = db.ReferenceProperty(QuizQuestionModel, collection_name='answers')

    def get_answer_text(self):
        return self.answer




