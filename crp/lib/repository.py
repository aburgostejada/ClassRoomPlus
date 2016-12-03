import base64

from crp.DB.classroom_model import ClassRoomModel
import random
import datetime

from crp.DB.poll_model import PollModel
from crp.DB.quiz_model import QuizModel
from crp.DB.quiz_question_model import QuizQuestionModel
from crp.DB.student_poll_answer import StudentPollAnswerModel
from crp.DB.student_model import StudentModel


# TODO missing name validation
from crp.DB.student_quiz_question_answer import StudentQuizQuestionAnswerModel


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

    @staticmethod
    def disable_quiz(key):
        poll = QuizModel.get(key)
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

    @staticmethod
    def save_student_answer(student, poll, answer):
        if isinstance(answer, list):
            answer = ", ".join([base64.b64decode(x) for x in answer])
        elif poll.type == "single":
            answer = base64.b64decode(answer)

        StudentPollAnswerModel(student=student, poll=poll, answer=answer).put()

    @staticmethod
    def add_quiz_to_classroom(classroom_key, time_allowed, title):
        class_room = ClassRoomModel.get(classroom_key)

        return QuizModel(class_room=class_room, time_allowed=time_allowed, title=title, status="active").put()

    @staticmethod
    def update_quiz_to_classroom(quiz_key, time_allowed, title):
        quiz = QuizModel.get(quiz_key)
        quiz.time_allowed = time_allowed
        quiz.title = title
        return quiz.put()

    @staticmethod
    def update_quiz_question(question_key, question, answer_type, options):
        if str(question) is not "":
            quiz_question = QuizQuestionModel.get(question_key)
            quiz_question.question = question
            quiz_question.type = answer_type
            quiz_question.options = options
            return quiz_question.put()
        return False

    @staticmethod
    def add_question_to_quiz(quiz_key, question, answer_type, options):
        if str(question) is not "":
            quiz = QuizModel.get(quiz_key)
            quiz_question = QuizQuestionModel(quiz=quiz, question=question, type=answer_type,
                                              options=options, status="active")
            return quiz_question.put()
        return False

    @staticmethod
    def delete_quiz_question(key):
        quiz_question = QuizQuestionModel.get(key)
        quiz_question.status = "deleted"
        return quiz_question.put()

    def save_student_quiz_answer(self, student, question, answer):
        if isinstance(answer, list):
            answer = ", ".join([base64.b64decode(x) for x in answer])
        elif question.type == "single":
            answer = base64.b64decode(answer)

        StudentQuizQuestionAnswerModel(student=student, question=question, answer=answer).put()

    def confirmed(self):
        self.teacher.confirmed = True
        self.teacher.confirmed_on = datetime.datetime.now()
        return self.teacher.put()
