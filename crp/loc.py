
class Localization:
    eng = "en"
    spa = "sp"

    def __init__(self):
        pass

    @classmethod
    def get_text(cls, key, lan="en"):
        english = {
            "dashboard": "Dashboard",
            "menu_one" : "Take Action!",
            "menu_two" : "Just Do it!"
        }

        spanish = {
            "dashboard": "Tablero",
            "menu_one" : "Toma Accion",
            "menu_two" : "Solo Hazlo"
        }

        if lan == cls.eng:
            return english[key]
        elif lan == cls.spa:
            return spanish[key]

        return "Error"
