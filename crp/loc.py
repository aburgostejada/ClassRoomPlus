
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
            "login_sign_up": "Teacher Login",
            "copyright": "Copyright 2016 by Classroom Plus",
            "teacher_login": "Teacher's Login",
            "teacher_signup": "New Teacher Signup",
            "login": "Login",
            "signup": "Sign-up",
            "remember_me": "Remember Me",
            "you_are": "You are a",
            "student": "Student",
            "teacher": "Teacher",
            "student_landing": "Welcome",
            "create": "Create",
            "save": "Save",
            "edit": "Edit",
            "update": "Update",
            "enter_a_classroom": "Enter a Classroom",
            "create_classroom": "Create a Classroom",
            "view_classroom": "Details",
            "create_quiz": "Create a Quiz",
            "create_poll": "Create a Poll",
            "new_poll": "New Poll",
            "new_quiz": "New Quiz",
            "disable": "Disable",
            "close": "Close",
            "back": "Back",
            "add": "Add",
            "add_question": "Add Question",
            "time_allowed": "Time Allowed (mins):",
            "required": "Required",
            "quiz_title": "Quiz Title",
            "yes_no": "Yes / No",
            "free_text": "Open Text",
            "multiple": "Multiple Answers",
            "single": "Single Answer",

            "404": "URL Not Found...",
            "logout": "Logout",
            "username": "Username",
            "password": "Password",
            "active_polls": "Active Polls",
            "question": "Question",
            "answered": "Answered",
            "closed_polls": "Closed Polls",
            "active_quizzes": "Active Quizzes",
            "closed_quizzes": "Closed Quizzes",
            "completed": "Completed",
            "input_error": "Input Error",
            "class_access_code": "Class Access Code",
            "student_pin": "Student Pin",
            "enter": "Enter",
            "welcome": "Welcome",
            "yes": "Yes",
            "no": "No",
            "submit": "Submit",
            "time_left": "Time Left",
            "responses_here": "Responses Here",
            "thanks": "Thanks",
            "problem_occurred": "Problem Occurred",
            "poll_completed": "Poll Completed",
            "poll_already_taken": "Poll Already Taken",
            "class_name": "Class Name",
            "separated_by_comma": "Separated by Comma",
            "comments": "Comments",
            "go": "Go",
            "types_of_answer": "Types of Answer",
            "option": "Option",
            "options": "Options",

            "delete": "Delete",



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
            "edit": "Editar",
            "update": "Actualizar",
            "enter_a_classroom": "Entre a una clase",
            "create_classroom": "Crear una clase",
            "view_classroom": "Detalles de la Clase",
            "create_quiz": "Crear una prueba",
            "create_poll": "Crear una encuesta rapida",
            "new_poll": "Nueva encuesta",
            "new_quiz": "Nueva prueba",
            "quiz_title": "Titulo de la Prueba",
            "disable": "Deshabilitar",
             "close": "Cerrar",
            "back": "Volver",
            "add": "Agregar",
            "add_question": "Agregar Pregunta",
            "time_allowed": "Tiempo Permitido (minutos):",
            "required": "Requerido",
            "yes_no": "Si / No",
            "free_text": "Texto Abierto",
            "multiple": "Multiples Respuestas",
            "single": "Respuesta Unica",

            "404": "URL no encontrada...",
            "logout": "Cerrar sesion",
            "username": "nombre de usuario",
            "password": "contrasena",
            "active_polls": "Encuestas activas",
            "question": "Pregunta",
            "answered": "Respuesta",
            "closed_polls": "Encuestas cerradas",
            "active_quizzes": "Pruebas activas",
            "closed_quizzes": "Pruebas cerradas",
            "completed": "Completo",
            "input_error": "Error de entrada",
            "class_access_code": "Codigo de acceso a la clase",
            "student_pin": "Estudiante Pin",
            "enter": "Entrar",
            "welcome": "Bienvenido",
            "yes": "Si",
            "no": "No",
            "submit": "Enviar",
            "time_left": "Tiempo restante",
            "responses_here": "Respuestas aqui",
            "thanks": "Gracias",
            "problem_occurred": "Problema ocurrido",
            "poll_completed": "Encuesta completada",
            "poll_already_taken": "Encuesta ya tomada",
            "class_name": "Nombre de la clase",
            "separated_by_comma": "Separado por coma",
            "comments": "Comentarios",
            "go": "Ir",
            "types_of_answer": "Tipos de respuesta",
            "option": "Opcion",
            "options": "Opciones",
            "delete": "Borrar",


        }

        if lan == cls.eng and english.has_key(key):
            return english[key]
        elif lan == cls.spa and spanish.has_key(key):
            return spanish[key]

        return "Error"
