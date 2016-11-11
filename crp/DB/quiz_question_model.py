
import base64

from google.appengine.ext import db
from crp.DB.quiz_model import QuizModel


class QuizQuestionModel(db.Model):
    type = db.StringProperty(required=True, choices={"yes_no", "free_text", "multiple", "single"})
    options = db.StringListProperty()
    question = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    status = db.StringProperty(required=True, choices={"active", "close", "pending", "deleted"})
    quiz = db.ReferenceProperty(QuizModel, collection_name='questions_list')

    @classmethod
    def get_all_by(cls, attr, value):
        q = QuizQuestionModel.all()
        q.filter(attr+" =", value)
        return q.fetch(1000)

    def get_total_options(self):
        if not self.options:
            return 0

        return len(self.options)

    def get_total_answered(self):
        return self.answers.count()

    def completed(self):
        return self.get_total_answered() >= self.class_room.students.count()

    def get_options_description(self):
        if self.type == "yes_no" or self.type == "free_text":
            return "N/A"

        return ", ".join(self.options)

    def get_encoded_options(self):
        return [(x, base64.b64encode(x)) for x in self.options]


