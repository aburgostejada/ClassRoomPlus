from google.appengine.ext import db


class ClassModel(db.Model):
    id = db.IntegerProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)

    @classmethod
    def get_all_by(cls, attr, value):
        q = ClassModel.all()
        q.filter(attr+" =", value)
        return q.fetch(1000)

    @classmethod
    def exits(cls, id):
        q = ClassModel.all()
        q.filter("id =", id)

        total = q.count()
        if total > 0:
            return True
        return False


    @classmethod
    def delete_by(cls, id):
        success = False
        q = ClassModel.all()
        q.filter("id =", id)
        for obj in q.fetch(1000):
            success = obj.delete()
        return success




