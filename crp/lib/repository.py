import base64

from crp.DB.classroom_model import ClassRoomModel
import random

from crp.DB.poll_model import PollModel
from crp.DB.student_answers import StudentAnswersModel
from crp.DB.student_model import StudentModel


# TODO missing name validation

class Repository:
    def __init__(self, teacher):
        self.teacher = teacher

    @staticmethod
    def save_list_of_students(students, class_room):
        student_list = students.split(",")
        pin_list = random.sample(range(1000, 9999), len(student_list))

        for index, student_name in enumerate(student_list):
            name = student_name.strip()
            if str(name) is not "":
                StudentModel(name=name, pin=pin_list[index], class_room=class_room, status="active").put()

    @staticmethod
    def delete_all_of_students_for(class_room):
        for student_name in class_room.students:
            student_name.delete()

    @staticmethod
    def add_poll_to_classroom(key, time_allowed, question, answer_type, options):
        class_room = ClassRoomModel.get(key)

        poll = PollModel(class_room=class_room, type=answer_type, options=options,
                         time_allowed=time_allowed, question=question, status="active").put()
        return poll

    @staticmethod
    def disable_poll(key):
        poll = PollModel.get(key)
        poll.status = "close"
        poll.put()

    def create_new_classroom(self, name, students, comments):
        access_code = random.randint(10000, 99999) #TODO make sure is unique for active classes
        class_room_key = ClassRoomModel(name=name, access_code=access_code,
                                        comments=comments, status="active",
                                        teacher=self.teacher).put()

        self.save_list_of_students(students, ClassRoomModel.get(class_room_key))

        return class_room_key

    def update_classroom(self, key, name, students, comments):
        class_room = ClassRoomModel.get(key)
        class_room.name = name
        class_room.comments = comments
        self.delete_all_of_students_for(class_room)
        self.save_list_of_students(students, class_room)

        return class_room.put()

    def save_student_answer(self, student, poll, answer):
        if isinstance(answer, list):
            answer = ", ".join([base64.b64decode(x) for x in answer])
        elif poll.type == "single":
            answer = base64.b64decode(answer)

        StudentAnswersModel(student=student, poll=poll, answer=answer).put()