from crp.DB.classroom_model import ClassRoomModel
import random

from crp.DB.student_model import StudentModel


# TODO missing name validation

class TeacherRepository:
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

    def create_new_classroom(self, name, passcode, students, comments):
        class_room_key = ClassRoomModel(name=name, passcode=passcode,
                                        comments=comments, status="active",
                                        teacher=self.teacher).put()

        self.save_list_of_students(students, ClassRoomModel.get(class_room_key))

        return class_room_key

    def update_classroom(self, key, name, passcode, students, comments):
        class_room = ClassRoomModel.get(key)
        class_room.name = name
        class_room.passcode = passcode
        class_room.comments = comments
        self.delete_all_of_students_for(class_room)
        self.save_list_of_students(students, class_room)

        return class_room.put()

