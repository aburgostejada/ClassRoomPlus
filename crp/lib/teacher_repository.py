from crp.DB.classroom_model import ClassRoomModel


class TeacherRepository:
    def __init__(self, teacher):
        self.teacher = teacher

    def create_new_classroom(self, name, passcode, comments):
        ClassRoomModel(name=name, passcode=passcode,
                       comments=comments, status="active",
                       teacher=self.teacher).put()

    def update_classroom(self, key, name, passcode, comments):
        class_room = ClassRoomModel.get(key)
        class_room.name = name
        class_room.passcode = passcode
        class_room.comments = comments
        return class_room.put()
