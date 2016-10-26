from google.appengine.ext import db

from crp.DB.classroom_model import ClassRoomModel


class PollModel(db.Model):
    type = db.StringProperty(required=True, choices={"yes_no", "custom"})
    options = db.StringListProperty()
    time_allowed = db.IntegerProperty(required=True)
    question = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    status = db.StringProperty(required=True, choices={"active", "disabled", "pending"})
    class_room = db.ReferenceProperty(ClassRoomModel, collection_name='poll_list')

    @classmethod
    def get_all_by(cls, attr, value):
        q = PollModel.all()
        q.filter(attr+" =", value)
        return q.fetch(1000)


