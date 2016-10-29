from google.appengine.ext import db

from crp.DB.poll_model import PollModel
from crp.DB.student_model import StudentModel


class StudentAnswersModel(db.Model):
    answer = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    student = db.ReferenceProperty(StudentModel, collection_name='answers')
    poll = db.ReferenceProperty(PollModel, collection_name='answers')






