
class Localization:
    eng = "eng"
    spa = "sp"

    def __init__(self):
        pass

    @classmethod
    def get_text(cls, key, lan="eng"):
        english = {
            "dashboard": "Dashboard",
            "menu_one" : "Take Action!",
            "menu_two" : "Just Do it!",
            "login_sign_up": "Login / Sign-up",
            "copyright": "Copyright 2016 by Classroom Plus",
            "teacher_login": "Teacher's Login",
            "login": "Log In",
            "remember_me": "Remember Me",
            "you_are": "You are a",
            "student": "Student",
            "teacher": "Teacher",
            "student_landing": "Welcome",
            "create": "Create",
            "save": "Save",
            "enter_a_classroom": "Enter a Classroom",
            "create_classroom": "Create a Classroom",
        }

        spanish = {
            "dashboard": "Tablero",
            "menu_one" : "Toma Accion",
            "menu_two" : "Solo Hazlo",
            "login_sign_up": "Acceder / Crear Cuenta",
            "copyright": "Copyright 2016 Por Classroom Plus",
            "teacher_login": "Acceso de Profesores",
            "login": "Acceder",
            "remember_me": "Recordar Me",
            "you_are": "Usted es un",
            "student": "Estudiante",
            "teacher": "Professor",
            "student_landing": "Bienvenido",
            "create": "Crear",
            "save": "Salvar",
            "enter_a_classroom": "Entre a una clase",
            "create_classroom": "Crear una clase",
        }

        if lan == cls.eng and english.has_key(key):
            return english[key]
        elif lan == cls.spa and spanish.has_key(key):
            return spanish[key]

        return "Error"
