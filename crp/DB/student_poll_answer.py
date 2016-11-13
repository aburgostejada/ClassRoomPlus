from google.appengine.ext import db

from crp.DB.poll_model import PollModel
from crp.DB.student_model import StudentModel


class StudentPollAnswerModel(db.Model):
    answer = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    student = db.ReferenceProperty(StudentModel, collection_name='poll_answers')
    poll = db.ReferenceProperty(PollModel, collection_name='answers')

    def get_answer_text(self):
        return self.answer



