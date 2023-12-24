import kivymd
import kivy
# core and key imports
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivy.metrics import dp
from kivy.lang.builder import Builder
from kivy.core.window import Window
# UIX imports
from kivymd.uix.button import MDFillRoundFlatButton
from kivymd.uix.button import MDFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.pickers import MDTimePicker
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFillRoundFlatButton
from kivymd.uix.dialog import MDDialog
from datetime import datetime, time, timedelta

print(kivy.__version__)
print(kivymd.__version__)

# kivy version = 2.2.1
# kivymd version = 1.1.1
# cython = 3.0.5

class WindowManager(MDScreenManager):
    pass

class MainMenu(MDScreen):
    name = "menu"

class Cincinnati1(MDScreen):
    pass

class Cincinnati2(MDScreen):
    pass

class Cincinnati3(MDScreen):
    pass

class CincinnatiN(MDScreen):
    pass

class VitalesGlucotest_C1(MDScreen): # Tomar signos etc etc
    pass

class VitalesGlucotest_C2(MDScreen): # Tomar signos etc etc
    pass

class VitalesGlucotest_C3(MDScreen): # Tomar signos etc etc
    pass

class Time(MDScreen):
    def __init__(self, **kwargs):
        super(Time, self).__init__(**kwargs)
        self.selected_time = datetime.now()

    def on_time_picker_time(self, instance, value, time):
        selected_time_str = value.strftime('%H:%M')
        selected_time = datetime.strptime(selected_time_str, "%H:%M").time()
        current_time = datetime.now().time()
        time_difference = datetime.combine(datetime.today(), current_time) - datetime.combine(datetime.today(), selected_time)
        rounded_time_difference = timedelta(minutes=round(time_difference.total_seconds() / 60))
        self.root.get_screen('time').ids.selected_time_label.text = f"Hora seleccionada: {selected_time_str}"
        self.root.get_screen('time').ids.elapsed_time_label.text = f"Min. transcurridos: {rounded_time_difference.seconds // 60:02}"

        self.selected_time = datetime.combine(datetime.today(), time)

    def check_elapsed_time(self):
        current_time = datetime.now()

        if self.selected_time and self.root.current_screen.name == 'time':
            elapsed_time = current_time - self.selected_time
            elapsed_minutes = elapsed_time.total_seconds() / 60
        else:
            elapsed_minutes = 0

        elapsed_minutes_adjusted = elapsed_minutes % 1440

        if elapsed_minutes_adjusted < 0:
            elapsed_minutes_adjusted += 1440

        screen = self.root.get_screen('time')

        screen.ids.elapsed_time_label.text = f"Min. transcurridos: {elapsed_minutes_adjusted:.0f}"

        if self.selected_time is not None and elapsed_minutes_adjusted < 270 and self.root.current_screen.name == 'time':
            pantalla_objetivo = "ECV"
        else:
            pantalla_objetivo = "time_n"

        self.root.transition.direction = "left"
        self.root.current = pantalla_objetivo

class Time_N(MDScreen):
    pass

class HospitalECV(MDScreen):
    pass

class Tomografia(MDScreen):
    pass

class Hemorragia(MDScreen):
    pass

class CanTrombolisis(MDScreen):
    name = "c_t"

class CanTrombolisisN(MDScreen):
    pass

class Contraindicaciones(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Scrollview
        self.scrollview_contraindicaciones = MDScrollView(size_hint=(1, None), size = (Window.width, Window.height))

        # GridLayout
        layout_contraindicaciones = MDGridLayout(orientation = "lr-tb", spacing = "40dp", padding = "20dp", size_hint_x = 1, size_hint_y = None, cols = 2)
        layout_contraindicaciones.bind(minimum_height = layout_contraindicaciones.setter("height"))

        # Go Back Button:
        invisible_label1 = MDLabel(text = "")
        invisible_label1.size_hint_y = None
        invisible_label1.size_hint_x = 0.5
        invisible_label1.height = dp(50)

        back_button_layout = MDBoxLayout(orientation = "vertical")
        back_button = MDFillRoundFlatButton(text = "Anterior", font_name = "fonts/Lato-Bolditalic.ttf")
        back_button.haling = "left"
        back_button.size_hint_y = None
        back_button.size_hint_x = 0.8

        back_button.bind(on_release = self.back)

        back_button_layout.add_widget(back_button)
        layout_contraindicaciones.add_widget(back_button_layout)
        layout_contraindicaciones.add_widget(invisible_label1)

        #title
        title_label = MDLabel(text = "Contraindicaciones", halign="left")
        title_label.font_size = "25dp"
        title_label.size_hint_y = None
        title_label.size_hint_x = 1
        title_label.font_name = "fonts/Lato-Bolditalic.ttf"
        title_label.height = dp(50)

        # Invisible Label
        invisible_label2 = MDLabel(text = "")
        invisible_label2.size_hint_y = None
        invisible_label2.size_hint_x = 0.1
        invisible_label2.height = dp(50)

        # Title and Invisible Label to not mess the rest up
        layout_contraindicaciones.add_widget(title_label)
        layout_contraindicaciones.add_widget(invisible_label2)

        self.checkboxes = []

        contraindicaciones = ["Hemorragia intracraneal (HIC) previa", "Lesión vascular cerebral estructural conocida",
        "Neoplasia intracraneal maligna conocida ya sea primaria o metastásica", "Accidente cerebrovascular isquémico en un plazo de 3 meses",
        "Sospecha de disección aórtica", "Hemorragia activa o diátesis hemorrágica", "Traumatismo craneoencefálico cerrado importante o traumatismo facial en los últimos 3 meses",
        "Cirugía intracraneal o intramedular en un plazo de 3 meses", "Hipertensión no controlada grave", "En caso de estreptoquinasa, el tratamiento previo debe ser dentro de los 6 meses previos"]

        for i, contraindicacion in enumerate(contraindicaciones):
            size_checkbox = dp(32)
            size_labels = dp(12)
            checkbox = MDCheckbox(size_hint=(0.5, None), size=(size_checkbox, size_checkbox))
            invisible_labela = MDLabel(text = "", size_hint = (0.5, None), size = (size_labels, size_labels))
            label = MDLabel(text=contraindicacion, size_hint=(0.8, None), size=(size_labels, size_labels), font_size = "10dp", multiline = True)
            label.font_name = "fonts/Lato-Italic.ttf"
            invisible_labelb = MDLabel(text = "", size_hint = (0.5, None), size = (size_labels, size_labels))
            layout_contraindicaciones.add_widget(label)
            layout_contraindicaciones.add_widget(checkbox)
            layout_contraindicaciones.add_widget(invisible_labela)
            layout_contraindicaciones.add_widget(invisible_labelb)

            self.checkboxes.append(checkbox)

        # Button and invisible label
        invisible_label3 = MDLabel(text = "")
        invisible_label3.size_hint_y = None
        invisible_label3.size_hint_x = 0.5
        invisible_label3.height = dp(50)

        next_button = MDFillRoundFlatButton(text = "Continuar", font_name = "fonts/Lato-Bolditalic.ttf")
        next_button.haling = "right"
        next_button.size_hint_y = None
        next_button.size_hint_x = 0.5
        next_button.bind(on_release = self.forward)

        layout_contraindicaciones.add_widget(invisible_label3)
        layout_contraindicaciones.add_widget(next_button)

        #Se agrega Grid a Scroll
        self.scrollview_contraindicaciones.add_widget(layout_contraindicaciones)
        self.add_widget(self.scrollview_contraindicaciones)

    def back(self,*_):
        self.manager.transition.direction = "right"
        self.manager.current = "c_t"
    def forward(self,*_):
        if any(checkbox.active for checkbox in self.checkboxes):
            self.manager.transition.direction = "left"
            self.manager.current = "contra_n"
        else:
            self.manager.transition.direction = "left"
            self.manager.current = "t_y"

class ContraindicacionesN(MDScreen):
    name = "contra_n"

class TrombolisisY(MDScreen):
    name = "t_y"

class TrombolisisN(MDScreen):
    name = "t_n"

######
# NIHSS MESS

class NihssScore:
    """Singleton class for managing the NIHSS score."""

    _instance = None
    _nihss_score = {"1A": None,
                    "1B": None,
                    "1C": None,
                    "2": None,
                    "3": None,
                    "4": None,
                    "5A": None,
                    "5B": None,
                    "6A": None,
                    "6B": None,
                    "7": None,
                    "8": None,
                    "9": None,
                    "10": None,
                    "11": None}

    @classmethod
    def get_instance(cls):
        """Returns the singleton instance of the NihssScore class."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def update_score(self, screen_name, new_score):
        """Updates the NIHSS score.

        Args:
            new_score: The new NIHSS score.
        """
        self._nihss_score[screen_name] = new_score

class NIHSSCalc(MDScreen):
    name = "nihss"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Scrollview
        self.scrollview_nihss = MDScrollView(size_hint=(1, None), size = (Window.width, Window.height))

        # Main Box Layout

        self.main_layout = MDBoxLayout(orientation = "vertical", padding = "15dp", spacing = "10dp", size_hint_x = 1, size_hint_y = None)
        self.main_layout.bind(minimum_height = self.main_layout.setter("height"))

        # Go back button
        back_button = MDFillRoundFlatButton(text = "Anterior", font_name = "fonts/Lato-Bolditalic.ttf")
        back_button.haling = "left"
        back_button.size_hint_y = None
        back_button.size_hint_x = 0.5

        back_button.bind(on_release = self.back)

        self.main_layout.add_widget(back_button)

        # Title
        title_label = MDLabel()
        title_label.text = "Calculadora NIHSS"
        title_label.font_size = dp(20)
        title_label.size_hint = (1, None)
        title_label.font_name = "fonts/Lato-Bolditalic.ttf"

        self.main_layout.add_widget(title_label)

        # Buttons / Each Button to a different screen / Since there are 15 questions, 15 screens, one button for each screen

        def create_button(question, screen_name):
            question_button = MDFlatButton(text=question, size_hint = (1, 1))
            question_button.halign = "left"
            question_button.font_name = "fonts/Lato-Italic.ttf"
            question_button.theme_text_color = "Custom"
            # question_button.text_color = (0, 1, 0, 1)
            def on_release():
                self.manager.transition.direction = "left"
                setattr(self.manager, 'current', screen_name)

            question_button.on_release = on_release

            return question_button

        questions = ["1A. Nivel de Conciencia", "1B. Preguntas NDC", "1C. Órdenes NDC", "2. Mirada Conjugada", "3. Campos Visuales", "4. Parálisis Facial", "5A. Extremidades Superiores - Brazo derecho", "5B. Extremidades Superiores - Brazo izquierdo", "6A. Extremidades inferiores - Pierna derecha", "6B. Extremidades inferiores - Pierna izquierda", "7. Ataxia", "8. Sensibilidad", "9. Lenguaje", "10. Disartria", "11. Extinción y Falta de Atención"]
        screen_names = ["1A", "1B", "1C", "2", "3", "4", "5A", "5B", "6A", "6B", "7", "8", "9", "10", "11"]

        questions_and_screens = dict(zip(questions, screen_names))

        self.buttons = []
        for question, screen_name in questions_and_screens.items():
            self.button = create_button(question, screen_name)
            self.buttons.append(self.button)

        for button in self.buttons:
            self.main_layout.add_widget(button)
        # shows currents score

        self._score_text = MDLabel(text = f"Puntaje NIHSS: 0")
        self._score_text.font_size = dp(20)
        self._score_text.size_hint = (1, None)
        self._score_text.font_name = "fonts/Lato-Bolditalic.ttf"
        self.main_layout.add_widget(self._score_text)


        # goes next page
        next_button = MDFillRoundFlatButton(text = "Continuar", font_name = "fonts/Lato-Bolditalic.ttf")
        next_button.haling = "right"
        next_button.size_hint_y = None
        next_button.size_hint_x = 1
        next_button.bind(on_release = self.next_screen)
        self.main_layout.add_widget(next_button)

        self.scrollview_nihss.add_widget(self.main_layout)
        self.add_widget(self.scrollview_nihss)

    def next_screen(self,*_):
        score = NihssScore.get_instance()
        score = score._nihss_score.values()
        remaining_questions = None
        # checks if there are remaining questions
        remaining_questions = None
        for value in score:
            if value is None:
                remaining_questions = True
                break
            else:
                remaining_questions = False
        nihss_total = 0
        if remaining_questions is False:
            nihss_total = sum(score)
            if nihss_total >= 4 and nihss_total <= 25:
                self.manager.transition.direction = "left"
                self.manager.current = "trt"
            elif nihss_total < 4 or nihss_total > 25:
                self.manager.transition.direction = "left"
                self.manager.current = "t_n"
        else:
            dialog = MDDialog(title = "¡Cuidado!", text = "Faltan Preguntas")
            dialog.open()

    def back(self, *_):
        self.manager.transition.direction = "right"
        self.manager.current = 't_y'

    def update_button_color(self):
        scores = list(NihssScore.get_instance()._nihss_score.values())
        for button in self.buttons:
            if scores[self.buttons.index(button)] != None:
                button.text_color = (0, 0.8, 0, 1)
            else:
                button.text_color = (0, 0, 0, 1)

    def update_score_text(self):
        """Updates the score text label."""
        score = NihssScore.get_instance()
        score = score._nihss_score.values()
        sum_score = 0
        for value in score:
            if value is not None:
                sum_score += value
        self._score_text.text = f"Puntaje NIHSS: {sum_score}"

class OneA(MDScreen):
    name = "1A"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Main Layout
        self.main_layout = MDBoxLayout(orientation = "vertical", spacing = "10dp", padding = ("15dp"), size_hint_x = 1, size_hint_y = 1)

        # Titulo
        title_label = MDLabel()
        title_label.text = "1A. Nivel de conciencia: ¿Qué nivel de conciencia tiene el paciente?"
        title_label.font_size = dp(20)
        title_label.size_hint = (1, 0.3)
        title_label.font_name = "fonts/Lato-Bolditalic.ttf"

        self.main_layout.add_widget(title_label)

        # Layout options2
        self.options_layout = MDGridLayout(orientation = "lr-tb", spacing = "50dp", padding = ("15dp"), size_hint = (1, 1), cols = 2)
        options = ["Alerta/responde", "Respuesta a mínimos estímulos", "Respuesta solo al dolor", "Respuesta refleja/Coma"]

        self.checkboxes = []
        def create_checkbox(option, num):
            """Creates a checkbox and label for the given option."""
            size_checkbox = dp(32)
            size_labels = dp(12)
            checkbox = MDCheckbox(group = f"checkboxes{num}", size_hint=(0.5, None), size=(size_checkbox, size_checkbox), pos_hint={'center_x': 0.9})
            label = MDLabel(text=option, size_hint=(0.5, None), size=(size_labels, size_labels))
            label.font_name = "fonts/Lato-Italic.ttf"
            self.checkboxes.append(checkbox)
            return checkbox, label


        # Create a list of checkbox and label pairs
        checkbox_label_pairs = []
        for option in options:
            checkbox_label_pairs.append(create_checkbox(option, "1A"))

        # Add the checkbox and label pairs to the layout
        for checkbox, label in checkbox_label_pairs:
            self.options_layout.add_widget(label)
            self.options_layout.add_widget(checkbox)

        # Add the options layout to the main layout
        self.main_layout.add_widget(self.options_layout)

        self.next_button_click_count = 0
        next_button = MDFillRoundFlatButton(text = "Continuar", font_name = "fonts/Lato-Bolditalic.ttf")
        next_button.haling = "center"
        next_button.size_hint_y = 0.2
        next_button.size_hint_x = 1
        next_button.bind(on_release = (self.back))
        self.main_layout.add_widget(next_button)

        self.add_widget(self.main_layout)

    def back(self, *_):

        if self.next_button_click_count >=1:
            self.rewrite_marks()
        self.check_checkboxes()

        NIHSSCalc.update_score_text(self.manager.get_screen("nihss"))
        NIHSSCalc.update_button_color(self.manager.get_screen("nihss"))

        self.manager.transition.direction = "right"
        self.manager.current = 'nihss'
        self.next_button_click_count += 1
    def rewrite_marks(self):
        score = NihssScore.get_instance()
        score._nihss_score[self.name] = None

    def check_checkboxes(self):
        score = NihssScore.get_instance()
        for i, checkbox in enumerate(self.checkboxes):
            if checkbox.active:
                score.update_score(self.name,i)

class OneB(MDScreen):
    name = "1B"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Main Layout
        self.main_layout = MDBoxLayout(orientation = "vertical", spacing = "10dp", padding = ("15dp"), size_hint_x = 1, size_hint_y = 1)

        # Titulo
        title_label = MDLabel()
        title_label.text = "1B. Respuesta a preguntas: ¿Cómo responde el paciente si pregunta el mes actual y su propia edad?"
        title_label.font_size = dp(20)
        title_label.size_hint = (1, 0.3)
        title_label.font_name = "fonts/Lato-Bolditalic.ttf"

        self.main_layout.add_widget(title_label)

        # Layout options2
        self.options_layout = MDGridLayout(orientation = "lr-tb", spacing = "50dp", padding = ("15dp"), size_hint = (1, 1), cols = 2)
        options = ["Ambas correctas", "Una correcta", "Ninguna correcta"]

        self.checkboxes = []
        def create_checkbox(option, num):
            """Creates a checkbox and label for the given option."""
            size_checkbox = dp(32)
            size_labels = dp(12)
            checkbox = MDCheckbox(group = f"checkboxes{num}", size_hint=(0.5, None), size=(size_checkbox, size_checkbox), pos_hint={'center_x': 0.9})
            label = MDLabel(text=option, size_hint=(0.5, None), size=(size_labels, size_labels))
            label.font_name = "fonts/Lato-Italic.ttf"
            self.checkboxes.append(checkbox)
            return checkbox, label


        # Create a list of checkbox and label pairs
        checkbox_label_pairs = []
        for option in options:
            checkbox_label_pairs.append(create_checkbox(option, "1B"))

        # Add the checkbox and label pairs to the layout
        for checkbox, label in checkbox_label_pairs:
            self.options_layout.add_widget(label)
            self.options_layout.add_widget(checkbox)

        # Add the options layout to the main layout
        self.main_layout.add_widget(self.options_layout)

        self.next_button_click_count = 0
        next_button = MDFillRoundFlatButton(text = "Continuar", font_name = "fonts/Lato-Bolditalic.ttf")
        next_button.haling = "center"
        next_button.size_hint_y = 0.2
        next_button.size_hint_x = 1
        next_button.bind(on_release = (self.back))
        self.main_layout.add_widget(next_button)

        self.add_widget(self.main_layout)

    def back(self, *_):

        if self.next_button_click_count >=1:
            self.rewrite_marks()
        self.check_checkboxes()

        NIHSSCalc.update_score_text(self.manager.get_screen("nihss"))
        NIHSSCalc.update_button_color(self.manager.get_screen("nihss"))

        self.manager.transition.direction = "right"
        self.manager.current = 'nihss'
        self.next_button_click_count += 1
    def rewrite_marks(self):
        score = NihssScore.get_instance()
        score._nihss_score[self.name] = None

    def check_checkboxes(self):
        score = NihssScore.get_instance()
        for i, checkbox in enumerate(self.checkboxes):
            if checkbox.active:
                score.update_score(self.name,i)

class OneC(MDScreen):
    name = "1C"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Main Layout
        self.main_layout = MDBoxLayout(orientation = "vertical", spacing = "10dp", padding = ("15dp"), size_hint_x = 1, size_hint_y = 1)

        # Titulo
        title_label = MDLabel()
        title_label.text = "1C. Respuesta a órdenes: ¿Cómo responde el paciente a que le pida que abra y cierre los ojos, y luego que apriete y suelte la mano no parética?"
        title_label.font_size = dp(20)
        title_label.size_hint = (1, 0.3)
        title_label.font_name = "fonts/Lato-Bolditalic.ttf"

        self.main_layout.add_widget(title_label)

        # Layout options2
        self.options_layout = MDGridLayout(orientation = "lr-tb", spacing = "50dp", padding = ("15dp"), size_hint = (1, 1), cols = 2)
        options = ["Ambas órdenes correctas", "Una orden correcta", "Ninguna orden correcta"]
        self.checkboxes = []
        def create_checkbox(option, num):
            """Creates a checkbox and label for the given option."""
            size_checkbox = dp(32)
            size_labels = dp(12)
            checkbox = MDCheckbox(group = f"checkboxes{num}", size_hint=(0.5, None), size=(size_checkbox, size_checkbox), pos_hint={'center_x': 0.9})
            label = MDLabel(text=option, size_hint=(0.5, None), size=(size_labels, size_labels))
            label.font_name = "fonts/Lato-Italic.ttf"
            self.checkboxes.append(checkbox)
            return checkbox, label


        # Create a list of checkbox and label pairs
        checkbox_label_pairs = []
        for option in options:
            checkbox_label_pairs.append(create_checkbox(option, "1C"))

        # Add the checkbox and label pairs to the layout
        for checkbox, label in checkbox_label_pairs:
            self.options_layout.add_widget(label)
            self.options_layout.add_widget(checkbox)

        # Add the options layout to the main layout
        self.main_layout.add_widget(self.options_layout)

        self.next_button_click_count = 0
        next_button = MDFillRoundFlatButton(text = "Continuar", font_name = "fonts/Lato-Bolditalic.ttf")
        next_button.haling = "center"
        next_button.size_hint_y = 0.2
        next_button.size_hint_x = 1
        next_button.bind(on_release = (self.back))
        self.main_layout.add_widget(next_button)

        self.add_widget(self.main_layout)



    def back(self, *_):

        if self.next_button_click_count >=1:
            self.rewrite_marks()
        self.check_checkboxes()

        NIHSSCalc.update_score_text(self.manager.get_screen("nihss"))
        NIHSSCalc.update_button_color(self.manager.get_screen("nihss"))

        self.manager.transition.direction = "right"
        self.manager.current = 'nihss'
        self.next_button_click_count += 1
    def rewrite_marks(self):
        score = NihssScore.get_instance()
        score._nihss_score[self.name] = None

    def check_checkboxes(self):
        score = NihssScore.get_instance()
        for i, checkbox in enumerate(self.checkboxes):
            if checkbox.active:
                score.update_score(self.name,i)

class Two(MDScreen):
    name = "2"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Main Layout
        self.main_layout = MDBoxLayout(orientation = "vertical", spacing = "10dp", padding = ("15dp"), size_hint_x = 1, size_hint_y = 1)

        # Titulo
        title_label = MDLabel()
        title_label.text = "2. Mirada Conjugada: ¿Hay alguna parálisis en la mirada?"
        title_label.font_size = dp(20)
        title_label.size_hint = (1, 0.3)
        title_label.font_name = "fonts/Lato-Bolditalic.ttf"

        self.main_layout.add_widget(title_label)

        # Layout options2
        self.options_layout = MDGridLayout(orientation = "lr-tb", spacing = "50dp", padding = ("15dp"), size_hint = (1, 1), cols = 2)
        options = ["Normal", "Parálisis parcial de la mirada", "Desviación forzada-parálisis completa"]

        self.checkboxes = []
        def create_checkbox(option, num):
            """Creates a checkbox and label for the given option."""
            size_checkbox = dp(32)
            size_labels = dp(12)
            checkbox = MDCheckbox(group = f"checkboxes{num}", size_hint=(0.5, None), size=(size_checkbox, size_checkbox), pos_hint={'center_x': 0.9})
            label = MDLabel(text=option, size_hint=(0.5, None), size=(size_labels, size_labels))
            label.font_name = "fonts/Lato-Italic.ttf"
            self.checkboxes.append(checkbox)
            return checkbox, label


        # Create a list of checkbox and label pairs
        checkbox_label_pairs = []
        for option in options:
            checkbox_label_pairs.append(create_checkbox(option, "2"))

        # Add the checkbox and label pairs to the layout
        for checkbox, label in checkbox_label_pairs:
            self.options_layout.add_widget(label)
            self.options_layout.add_widget(checkbox)

        # Add the options layout to the main layout
        self.main_layout.add_widget(self.options_layout)

        self.next_button_click_count = 0
        next_button = MDFillRoundFlatButton(text = "Continuar", font_name = "fonts/Lato-Bolditalic.ttf")
        next_button.haling = "center"
        next_button.size_hint_y = 0.2
        next_button.size_hint_x = 1
        next_button.bind(on_release = (self.back))
        self.main_layout.add_widget(next_button)

        self.add_widget(self.main_layout)


    def back(self, *_):

        if self.next_button_click_count >=1:
            self.rewrite_marks()
        self.check_checkboxes()

        NIHSSCalc.update_score_text(self.manager.get_screen("nihss"))
        NIHSSCalc.update_button_color(self.manager.get_screen("nihss"))

        self.manager.transition.direction = "right"
        self.manager.current = 'nihss'
        self.next_button_click_count += 1
    def rewrite_marks(self):
        score = NihssScore.get_instance()
        score._nihss_score[self.name] = None

    def check_checkboxes(self):
        score = NihssScore.get_instance()
        for i, checkbox in enumerate(self.checkboxes):
            if checkbox.active:
                score.update_score(self.name,i)

class Three(MDScreen):
    name = "3"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Main Layout
        self.main_layout = MDBoxLayout(orientation = "vertical", spacing = "10dp", padding = ("15dp"), size_hint_x = 1, size_hint_y = 1)

        # Titulo
        title_label = MDLabel()
        title_label.text = "3. Campos visuales: ¿Hay alguna alteración en los campos visuales?"
        title_label.font_size = dp(20)
        title_label.size_hint = (1, 0.3)
        title_label.font_name = "fonts/Lato-Bolditalic.ttf"


        self.main_layout.add_widget(title_label)

        # Layout options2
        self.options_layout = MDGridLayout(orientation = "lr-tb", spacing = "50dp", padding = ("15dp"), size_hint = (1, 1), cols = 2)
        options = ["No alteración", "Hemianopsia parcial", "Hemianopsia completa", "Bilateral hemianopsia o Ceguera total"]
        self.checkboxes = []
        def create_checkbox(option, num):
            """Creates a checkbox and label for the given option."""
            size_checkbox = dp(32)
            size_labels = dp(12)
            checkbox = MDCheckbox(group = f"checkboxes{num}", size_hint=(0.5, None), size=(size_checkbox, size_checkbox), pos_hint={'center_x': 0.9})
            label = MDLabel(text=option, size_hint=(0.5, None), size=(size_labels, size_labels))
            label.font_name = "fonts/Lato-Italic.ttf"
            self.checkboxes.append(checkbox)
            return checkbox, label


        # Create a list of checkbox and label pairs
        checkbox_label_pairs = []
        for option in options:
            checkbox_label_pairs.append(create_checkbox(option, "3"))

        # Add the checkbox and label pairs to the layout
        for checkbox, label in checkbox_label_pairs:
            self.options_layout.add_widget(label)
            self.options_layout.add_widget(checkbox)

        # Add the options layout to the main layout
        self.main_layout.add_widget(self.options_layout)

        self.next_button_click_count = 0
        next_button = MDFillRoundFlatButton(text = "Continuar", font_name = "fonts/Lato-Bolditalic.ttf")
        next_button.haling = "center"
        next_button.size_hint_y = 0.2
        next_button.size_hint_x = 1
        next_button.bind(on_release = (self.back))
        self.main_layout.add_widget(next_button)

        self.add_widget(self.main_layout)



    def back(self, *_):

        if self.next_button_click_count >=1:
            self.rewrite_marks()
        self.check_checkboxes()

        NIHSSCalc.update_score_text(self.manager.get_screen("nihss"))
        NIHSSCalc.update_button_color(self.manager.get_screen("nihss"))

        self.manager.transition.direction = "right"
        self.manager.current = 'nihss'
        self.next_button_click_count += 1
    def rewrite_marks(self):
        score = NihssScore.get_instance()
        score._nihss_score[self.name] = None

    def check_checkboxes(self):
        score = NihssScore.get_instance()
        for i, checkbox in enumerate(self.checkboxes):
            if checkbox.active:
                score.update_score(self.name,i)

class Four(MDScreen):
    name = "4"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Main Layout
        self.main_layout = MDBoxLayout(orientation = "vertical", spacing = "10dp", padding = ("15dp"), size_hint_x = 1, size_hint_y = 1)

        # Titulo
        title_label = MDLabel()
        title_label.text = "4. Parálisis Facial: ¿Hay alguna parálisis facial?"
        title_label.font_size = dp(20)
        title_label.size_hint = (1, 0.3)
        title_label.font_name = "fonts/Lato-Bolditalic.ttf"

        self.main_layout.add_widget(title_label)

        # Layout options2
        self.options_layout = MDGridLayout(orientation = "lr-tb", spacing = "55dp", padding = ("15dp"), size_hint = (1, 1), cols = 2)
        options = ["Normal", "Debilidad // Paresia menor // aspecto normal y sonrisa asimétrica", "Parálisis//debilidad parcial", "Parálisis completa"]

        self.checkboxes = []
        def create_checkbox(option, num):
            """Creates a checkbox and label for the given option."""
            size_checkbox = dp(32)
            size_labels = dp(12)
            checkbox = MDCheckbox(group = f"checkboxes{num}", size_hint=(0.5, None), size=(size_checkbox, size_checkbox), pos_hint={'center_x': 0.9})
            label = MDLabel(text=option, size_hint=(0.5, None), size=(size_labels, size_labels))
            label.font_name = "fonts/Lato-Italic.ttf"
            self.checkboxes.append(checkbox)
            return checkbox, label


        # Create a list of checkbox and label pairs
        checkbox_label_pairs = []
        for option in options:
            checkbox_label_pairs.append(create_checkbox(option, "4"))

        # Add the checkbox and label pairs to the layout
        for checkbox, label in checkbox_label_pairs:
            self.options_layout.add_widget(label)
            self.options_layout.add_widget(checkbox)

        # Add the options layout to the main layout
        self.main_layout.add_widget(self.options_layout)

        self.next_button_click_count = 0
        next_button = MDFillRoundFlatButton(text = "Continuar", font_name = "fonts/Lato-Bolditalic.ttf")
        next_button.haling = "center"
        next_button.size_hint_y = 0.2
        next_button.size_hint_x = 1
        next_button.bind(on_release = (self.back))
        self.main_layout.add_widget(next_button)

        self.add_widget(self.main_layout)



    def back(self, *_):

        if self.next_button_click_count >=1:
            self.rewrite_marks()
        self.check_checkboxes()

        NIHSSCalc.update_score_text(self.manager.get_screen("nihss"))
        NIHSSCalc.update_button_color(self.manager.get_screen("nihss"))

        self.manager.transition.direction = "right"
        self.manager.current = 'nihss'
        self.next_button_click_count += 1
    def rewrite_marks(self):
        score = NihssScore.get_instance()
        score._nihss_score[self.name] = None

    def check_checkboxes(self):
        score = NihssScore.get_instance()
        for i, checkbox in enumerate(self.checkboxes):
            if checkbox.active:
                score.update_score(self.name,i)

class FiveA(MDScreen):
    name = "5A"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Main Layout
        self.main_layout = MDBoxLayout(orientation = "vertical", spacing = "10dp", padding = ("15dp"), size_hint_x = 1, size_hint_y =  1)


        # Titulo
        title_label = MDLabel()
        title_label.text = (
            "5A.¿Cómo está la función del brazo derecho al extender los brazos 90° si el paciente está en posición sentada o 45° si el paciente está en posición supina?"
        )
        title_label.font_size = dp(15)
        title_label.size_hint = (1, None)
        title_label.font_name = "fonts/Lato-Bolditalic.ttf"
        title_label.pos_hint = {'top': 0.5}

        self.main_layout.add_widget(title_label)

        # Layout options
        self.options_layout = MDGridLayout(orientation = "lr-tb", spacing = "55dp", padding = ("20dp"), size_hint = (1, 1), cols = 2)

        options = ["No claudica", "Claudica, no toca la cama", "Esfuerzo contra la gravedad pero no se sostiene", "Sin esfuerzo gravitatorio pero hay movimiento", "Ningún movimiento"]

        self.checkboxes = []
        def create_checkbox(option, num):
            """Creates a checkbox and label for the given option."""
            size_checkbox = dp(32)
            size_labels = dp(12)
            checkbox = MDCheckbox(group = f"checkboxes{num}", size_hint=(0.5, None), size=(size_checkbox, size_checkbox), pos_hint={'center_x': 0.9})
            label = MDLabel(text=option, size_hint=(0.5, None), size=(size_labels, size_labels))
            label.font_name = "fonts/Lato-Italic.ttf"
            self.checkboxes.append(checkbox)
            return checkbox, label


        # Create a list of checkbox and label pairs
        checkbox_label_pairs = []
        for option in options:
            checkbox_label_pairs.append(create_checkbox(option, "5A"))

        # Add the checkbox and label pairs to the layout
        for checkbox, label in checkbox_label_pairs:
            self.options_layout.add_widget(label)
            self.options_layout.add_widget(checkbox)

        # Add the options layout to the main layout
        self.main_layout.add_widget(self.options_layout)

        self.next_button_click_count = 0
        next_button = MDFillRoundFlatButton(text = "Continuar", font_name = "fonts/Lato-Bolditalic.ttf")
        next_button.haling = "center"
        next_button.size_hint_y = 0.2
        next_button.size_hint_x = 1
        next_button.bind(on_release = (self.back))
        self.main_layout.add_widget(next_button)

        self.add_widget(self.main_layout)



    def back(self, *_):

        if self.next_button_click_count >=1:
            self.rewrite_marks()
        self.check_checkboxes()

        NIHSSCalc.update_score_text(self.manager.get_screen("nihss"))
        NIHSSCalc.update_button_color(self.manager.get_screen("nihss"))

        self.manager.transition.direction = "right"
        self.manager.current = 'nihss'
        self.next_button_click_count += 1
    def rewrite_marks(self):
        score = NihssScore.get_instance()
        score._nihss_score[self.name] = None

    def check_checkboxes(self):
        score = NihssScore.get_instance()
        for i, checkbox in enumerate(self.checkboxes):
            if checkbox.active:
                score.update_score(self.name,i)

class FiveB(MDScreen):
    name = "5B"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Main Layout
        self.main_layout = MDBoxLayout(orientation = "vertical", spacing = "10dp", padding = ("15dp"), size_hint_x = 1, size_hint_y =  1)


        # Titulo
        title_label = MDLabel()
        title_label.text = (
            "5B. Extremidades superiores - Brazo izquierdo: ¿Cómo está la función del brazo izquierdo al extender los brazos 90° si el paciente está en posición sentada o 45° si el paciente está en posición supina?"
        )
        title_label.font_size = dp(15)
        title_label.size_hint = (1, None)
        title_label.font_name = "fonts/Lato-Bolditalic.ttf"
        title_label.pos_hint = {'top': 0.5}

        self.main_layout.add_widget(title_label)

        # Layout options
        self.options_layout = MDGridLayout(orientation = "lr-tb", spacing = "55dp", padding = ("20dp"), size_hint = (1, 1), cols = 2)

        options = ["No claudica", "Claudica, no toca la cama", "Esfuerzo contra la gravedad pero no se sostiene", "Sin esfuerzo gravitatorio pero hay movimiento", "Ningún movimiento"]

        self.checkboxes = []
        def create_checkbox(option, num):
            """Creates a checkbox and label for the given option."""
            size_checkbox = dp(32)
            size_labels = dp(12)
            checkbox = MDCheckbox(group = f"checkboxes{num}", size_hint=(0.5, None), size=(size_checkbox, size_checkbox), pos_hint={'center_x': 0.9})
            label = MDLabel(text=option, size_hint=(0.5, None), size=(size_labels, size_labels))
            label.font_name = "fonts/Lato-Italic.ttf"
            self.checkboxes.append(checkbox)
            return checkbox, label


        # Create a list of checkbox and label pairs
        checkbox_label_pairs = []
        for option in options:
            checkbox_label_pairs.append(create_checkbox(option, "5B"))

        # Add the checkbox and label pairs to the layout
        for checkbox, label in checkbox_label_pairs:
            self.options_layout.add_widget(label)
            self.options_layout.add_widget(checkbox)

        # Add the options layout to the main layout
        self.main_layout.add_widget(self.options_layout)

        self.next_button_click_count = 0
        next_button = MDFillRoundFlatButton(text = "Continuar", font_name = "fonts/Lato-Bolditalic.ttf")
        next_button.haling = "center"
        next_button.size_hint_y = 0.2
        next_button.size_hint_x = 1
        next_button.bind(on_release = (self.back))
        self.main_layout.add_widget(next_button)

        self.add_widget(self.main_layout)



    def back(self, *_):

        if self.next_button_click_count >=1:
            self.rewrite_marks()
        self.check_checkboxes()

        NIHSSCalc.update_score_text(self.manager.get_screen("nihss"))
        NIHSSCalc.update_button_color(self.manager.get_screen("nihss"))

        self.manager.transition.direction = "right"
        self.manager.current = 'nihss'
        self.next_button_click_count += 1
    def rewrite_marks(self):
        score = NihssScore.get_instance()
        score._nihss_score[self.name] = None

    def check_checkboxes(self):
        score = NihssScore.get_instance()
        for i, checkbox in enumerate(self.checkboxes):
            if checkbox.active:
                score.update_score(self.name,i)

class SixA(MDScreen):
    name = "6A"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Main Layout
        self.main_layout = MDBoxLayout(orientation = "vertical", spacing = "10dp", padding = ("15dp"), size_hint_x = 1, size_hint_y =  1)


        # Titulo
        title_label = MDLabel()
        title_label.text = (
            "6A. Extremidades inferiores - Pierna derecha: ¿Cómo está la función de la pierna derecha al sostener la pierna a 30° en posición supina?"
        )
        title_label.font_size = dp(15)
        title_label.size_hint = (1, None)
        title_label.font_name = "fonts/Lato-Bolditalic.ttf"
        title_label.pos_hint = {'top': 0.5}

        self.main_layout.add_widget(title_label)

        # Layout options
        self.options_layout = MDGridLayout(orientation = "lr-tb", spacing = "55dp", padding = ("20dp"), size_hint = (1, 1), cols = 2)

        options = ["No claudica", "Claudica, no toca la cama", "Esfuerzo contra la gravedad pero no se sostiene", "Sin esfuerzo gravitatorio pero hay movimiento", "Ningún movimiento"]

        self.checkboxes = []
        def create_checkbox(option, num):
            """Creates a checkbox and label for the given option."""
            size_checkbox = dp(32)
            size_labels = dp(12)
            checkbox = MDCheckbox(group = f"checkboxes{num}", size_hint=(0.5, None), size=(size_checkbox, size_checkbox), pos_hint={'center_x': 0.9})
            label = MDLabel(text=option, size_hint=(0.5, None), size=(size_labels, size_labels))
            label.font_name = "fonts/Lato-Italic.ttf"
            self.checkboxes.append(checkbox)
            return checkbox, label


        # Create a list of checkbox and label pairs
        checkbox_label_pairs = []
        for option in options:
            checkbox_label_pairs.append(create_checkbox(option, "6A"))

        # Add the checkbox and label pairs to the layout
        for checkbox, label in checkbox_label_pairs:
            self.options_layout.add_widget(label)
            self.options_layout.add_widget(checkbox)

        # Add the options layout to the main layout
        self.main_layout.add_widget(self.options_layout)

        self.next_button_click_count = 0
        next_button = MDFillRoundFlatButton(text = "Continuar", font_name = "fonts/Lato-Bolditalic.ttf")
        next_button.haling = "center"
        next_button.size_hint_y = 0.2
        next_button.size_hint_x = 1
        next_button.bind(on_release = (self.back))
        self.main_layout.add_widget(next_button)

        self.add_widget(self.main_layout)


    def back(self, *_):

        if self.next_button_click_count >=1:
            self.rewrite_marks()
        self.check_checkboxes()

        NIHSSCalc.update_score_text(self.manager.get_screen("nihss"))
        NIHSSCalc.update_button_color(self.manager.get_screen("nihss"))

        self.manager.transition.direction = "right"
        self.manager.current = 'nihss'
        self.next_button_click_count += 1
    def rewrite_marks(self):
        score = NihssScore.get_instance()
        score._nihss_score[self.name] = None

    def check_checkboxes(self):
        score = NihssScore.get_instance()
        for i, checkbox in enumerate(self.checkboxes):
            if checkbox.active:
                score.update_score(self.name,i)

class SixB(MDScreen):
    name = "6B"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Main Layout
        self.main_layout = MDBoxLayout(orientation = "vertical", spacing = "10dp", padding = ("15dp"), size_hint_x = 1, size_hint_y =  1)


        # Titulo
        title_label = MDLabel()
        title_label.text = (
            "6B. Extremidades inferiores - Pierna izquierda: ¿Cómo está la función de la pierna izquierda al sostener la pierna a 30° en posición supina?"
        )
        title_label.font_size = dp(15)
        title_label.size_hint = (1, None)
        title_label.font_name = "fonts/Lato-Bolditalic.ttf"
        title_label.pos_hint = {'top': 0.5}

        self.main_layout.add_widget(title_label)

        # Layout options
        self.options_layout = MDGridLayout(orientation = "lr-tb", spacing = "55dp", padding = ("20dp"), size_hint = (1, 1), cols = 2)

        options = ["No claudica", "Claudica, no toca la cama", "Esfuerzo contra la gravedad pero no se sostiene", "Sin esfuerzo gravitatorio pero hay movimiento", "Ningún movimiento"]

        self.checkboxes = []
        def create_checkbox(option, num):
            """Creates a checkbox and label for the given option."""
            size_checkbox = dp(32)
            size_labels = dp(12)
            checkbox = MDCheckbox(group = f"checkboxes{num}", size_hint=(0.5, None), size=(size_checkbox, size_checkbox), pos_hint={'center_x': 0.9})
            label = MDLabel(text=option, size_hint=(0.5, None), size=(size_labels, size_labels))
            label.font_name = "fonts/Lato-Italic.ttf"
            self.checkboxes.append(checkbox)
            return checkbox, label


        # Create a list of checkbox and label pairs
        checkbox_label_pairs = []
        for option in options:
            checkbox_label_pairs.append(create_checkbox(option, "6B"))

        # Add the checkbox and label pairs to the layout
        for checkbox, label in checkbox_label_pairs:
            self.options_layout.add_widget(label)
            self.options_layout.add_widget(checkbox)

        # Add the options layout to the main layout
        self.main_layout.add_widget(self.options_layout)

        self.next_button_click_count = 0
        next_button = MDFillRoundFlatButton(text = "Continuar", font_name = "fonts/Lato-Bolditalic.ttf")
        next_button.haling = "center"
        next_button.size_hint_y = 0.2
        next_button.size_hint_x = 1
        next_button.bind(on_release = (self.back))
        self.main_layout.add_widget(next_button)

        self.add_widget(self.main_layout)



    def back(self, *_):

        if self.next_button_click_count >=1:
            self.rewrite_marks()
        self.check_checkboxes()

        NIHSSCalc.update_score_text(self.manager.get_screen("nihss"))
        NIHSSCalc.update_button_color(self.manager.get_screen("nihss"))

        self.manager.transition.direction = "right"
        self.manager.current = 'nihss'
        self.next_button_click_count += 1
    def rewrite_marks(self):
        score = NihssScore.get_instance()
        score._nihss_score[self.name] = None

    def check_checkboxes(self):
        score = NihssScore.get_instance()
        for i, checkbox in enumerate(self.checkboxes):
            if checkbox.active:
                score.update_score(self.name,i)

class Seven(MDScreen):
    name = "7"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Main Layout
        self.main_layout = MDBoxLayout(orientation = "vertical", spacing = "10dp", padding = ("15dp"), size_hint_x = 1, size_hint_y = 1)

        # Titulo
        title_label = MDLabel()
        title_label.text = "7. Ataxia: ¿Hay alguna evidencia de ataxia en la prueba dedo-nariz-dedo y la prueba talón-espinilla?"
        title_label.font_size = dp(20)
        title_label.size_hint = (1, 0.3)
        title_label.font_name = "fonts/Lato-Bolditalic.ttf"

        self.main_layout.add_widget(title_label)

        # Layout options2
        self.options_layout = MDGridLayout(orientation = "lr-tb", spacing = "55dp", padding = ("15dp"), size_hint = (1, 1), cols = 2)
        options = ["No ataxia o afasia, hemiplegia", "Ataxia en miembro superior o inferior", "Ataxia en ambos miembros"]
        self.checkboxes = []
        def create_checkbox(option, num):
            """Creates a checkbox and label for the given option."""
            size_checkbox = dp(32)
            size_labels = dp(12)
            checkbox = MDCheckbox(group = f"checkboxes{num}", size_hint=(0.5, None), size=(size_checkbox, size_checkbox), pos_hint={'center_x': 0.9})
            label = MDLabel(text=option, size_hint=(0.5, None), size=(size_labels, size_labels))
            label.font_name = "fonts/Lato-Italic.ttf"
            self.checkboxes.append(checkbox)
            return checkbox, label


        # Create a list of checkbox and label pairs
        checkbox_label_pairs = []
        for option in options:
            checkbox_label_pairs.append(create_checkbox(option, "7"))

        # Add the checkbox and label pairs to the layout
        for checkbox, label in checkbox_label_pairs:
            self.options_layout.add_widget(label)
            self.options_layout.add_widget(checkbox)

        # Add the options layout to the main layout
        self.main_layout.add_widget(self.options_layout)

        self.next_button_click_count = 0
        next_button = MDFillRoundFlatButton(text = "Continuar", font_name = "fonts/Lato-Bolditalic.ttf")
        next_button.haling = "center"
        next_button.size_hint_y = 0.2
        next_button.size_hint_x = 1
        next_button.bind(on_release = (self.back))
        self.main_layout.add_widget(next_button)

        self.add_widget(self.main_layout)

    def back(self, *_):

        if self.next_button_click_count >=1:
            self.rewrite_marks()
        self.check_checkboxes()

        NIHSSCalc.update_score_text(self.manager.get_screen("nihss"))
        NIHSSCalc.update_button_color(self.manager.get_screen("nihss"))

        self.manager.transition.direction = "right"
        self.manager.current = 'nihss'
        self.next_button_click_count += 1
    def rewrite_marks(self):
        score = NihssScore.get_instance()
        score._nihss_score[self.name] = None

    def check_checkboxes(self):
        score = NihssScore.get_instance()
        for i, checkbox in enumerate(self.checkboxes):
            if checkbox.active:
                score.update_score(self.name,i)

class Eight(MDScreen):
    name = "8"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Main Layout
        self.main_layout = MDBoxLayout(orientation = "vertical", spacing = "10dp", padding = ("15dp"), size_hint_x = 1, size_hint_y = 1)

        # Titulo
        title_label = MDLabel()
        title_label.text = "8. Sensibilidad: ¿Hay pérdida de sensibilidad?"
        title_label.font_size = dp(20)
        title_label.size_hint = (1, 0.3)
        title_label.font_name = "fonts/Lato-Bolditalic.ttf"

        self.main_layout.add_widget(title_label)

        # Layout options2
        self.options_layout = MDGridLayout(orientation = "lr-tb", spacing = "55dp", padding = ("15dp"), size_hint = (1, 1), cols = 2)
        options = ["Normal", "Hipoestesia ligera o moderada", "Hipoestesia severa o bilateral o anestesia"]
        self.checkboxes = []
        def create_checkbox(option, num):
            """Creates a checkbox and label for the given option."""
            size_checkbox = dp(32)
            size_labels = dp(12)
            checkbox = MDCheckbox(group = f"checkboxes{num}", size_hint=(0.5, None), size=(size_checkbox, size_checkbox), pos_hint={'center_x': 0.9})
            label = MDLabel(text=option, size_hint=(0.5, None), size=(size_labels, size_labels))
            label.font_name = "fonts/Lato-Italic.ttf"
            self.checkboxes.append(checkbox)
            return checkbox, label


        # Create a list of checkbox and label pairs
        checkbox_label_pairs = []
        for option in options:
            checkbox_label_pairs.append(create_checkbox(option, "8"))

        # Add the checkbox and label pairs to the layout
        for checkbox, label in checkbox_label_pairs:
            self.options_layout.add_widget(label)
            self.options_layout.add_widget(checkbox)

        # Add the options layout to the main layout
        self.main_layout.add_widget(self.options_layout)

        self.next_button_click_count = 0
        next_button = MDFillRoundFlatButton(text = "Continuar", font_name = "fonts/Lato-Bolditalic.ttf")
        next_button.haling = "center"
        next_button.size_hint_y = 0.2
        next_button.size_hint_x = 1
        next_button.bind(on_release = (self.back))
        self.main_layout.add_widget(next_button)

        self.add_widget(self.main_layout)



    def back(self, *_):

        if self.next_button_click_count >=1:
            self.rewrite_marks()
        self.check_checkboxes()

        NIHSSCalc.update_score_text(self.manager.get_screen("nihss"))
        NIHSSCalc.update_button_color(self.manager.get_screen("nihss"))

        self.manager.transition.direction = "right"
        self.manager.current = 'nihss'
        self.next_button_click_count += 1
    def rewrite_marks(self):
        score = NihssScore.get_instance()
        score._nihss_score[self.name] = None

    def check_checkboxes(self):
        score = NihssScore.get_instance()
        for i, checkbox in enumerate(self.checkboxes):
            if checkbox.active:
                score.update_score(self.name,i)

class Nine(MDScreen):
    name = "9"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Main Layout
        self.main_layout = MDBoxLayout(orientation = "vertical", spacing = "10dp", padding = ("15dp"), size_hint_x = 1, size_hint_y = 1)

        # Titulo
        title_label = MDLabel()
        title_label.text = "9. Lenguaje: ¿Hay alguna dificultad en el lenguaje?"
        title_label.font_size = dp(20)
        title_label.size_hint = (1, 0.3)
        title_label.font_name = "fonts/Lato-Bolditalic.ttf"

        self.main_layout.add_widget(title_label)

        # Layout options2
        self.options_layout = MDGridLayout(orientation = "lr-tb", spacing = "55dp", padding = ("15dp"), size_hint = (1, 1), cols = 2)
        options = ["Normal", "Leve a moderada afasia", "Severa afasia", "Mutismo, afasia global, coma"]
        self.checkboxes = []
        def create_checkbox(option, num):
            """Creates a checkbox and label for the given option."""
            size_checkbox = dp(32)
            size_labels = dp(12)
            checkbox = MDCheckbox(group = f"checkboxes{num}", size_hint=(0.5, None), size=(size_checkbox, size_checkbox), pos_hint={'center_x': 0.9})
            label = MDLabel(text=option, size_hint=(0.5, None), size=(size_labels, size_labels))
            label.font_name = "fonts/Lato-Italic.ttf"
            self.checkboxes.append(checkbox)
            return checkbox, label


        # Create a list of checkbox and label pairs
        checkbox_label_pairs = []
        for option in options:
            checkbox_label_pairs.append(create_checkbox(option, "9"))

        # Add the checkbox and label pairs to the layout
        for checkbox, label in checkbox_label_pairs:
            self.options_layout.add_widget(label)
            self.options_layout.add_widget(checkbox)

        # Add the options layout to the main layout
        self.main_layout.add_widget(self.options_layout)

        self.next_button_click_count = 0
        next_button = MDFillRoundFlatButton(text = "Continuar", font_name = "fonts/Lato-Bolditalic.ttf")
        next_button.haling = "center"
        next_button.size_hint_y = 0.2
        next_button.size_hint_x = 1
        next_button.bind(on_release = (self.back))
        self.main_layout.add_widget(next_button)

        self.add_widget(self.main_layout)



    def back(self, *_):

        if self.next_button_click_count >=1:
            self.rewrite_marks()
        self.check_checkboxes()

        NIHSSCalc.update_score_text(self.manager.get_screen("nihss"))
        NIHSSCalc.update_button_color(self.manager.get_screen("nihss"))

        self.manager.transition.direction = "right"
        self.manager.current = 'nihss'
        self.next_button_click_count += 1
    def rewrite_marks(self):
        score = NihssScore.get_instance()
        score._nihss_score[self.name] = None

    def check_checkboxes(self):
        score = NihssScore.get_instance()
        for i, checkbox in enumerate(self.checkboxes):
            if checkbox.active:
                score.update_score(self.name,i)

class Ten(MDScreen):
    name = "10"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Main Layout
        self.main_layout = MDBoxLayout(orientation = "vertical", spacing = "10dp", padding = ("15dp"), size_hint_x = 1, size_hint_y = 1)

        # Titulo
        title_label = MDLabel()
        title_label.text = "10. Disartria: ¿Hay alguna dificultad en el habla?"
        title_label.font_size = dp(20)
        title_label.size_hint = (1, 0.3)
        title_label.font_name = "fonts/Lato-Bolditalic.ttf"

        self.main_layout.add_widget(title_label)

        # Layout options2
        self.options_layout = MDGridLayout(orientation = "lr-tb", spacing = "55dp", padding = ("15dp"), size_hint = (1, 1), cols = 2)
        options = ["Normal", "Leve a moderada-poco claro", "Severa, ininteligible, mutismo"]
        self.checkboxes = []
        def create_checkbox(option, num):
            """Creates a checkbox and label for the given option."""
            size_checkbox = dp(32)
            size_labels = dp(12)
            checkbox = MDCheckbox(group = f"checkboxes{num}", size_hint=(0.5, None), size=(size_checkbox, size_checkbox), pos_hint={'center_x': 0.9})
            label = MDLabel(text=option, size_hint=(0.5, None), size=(size_labels, size_labels))
            label.font_name = "fonts/Lato-Italic.ttf"
            self.checkboxes.append(checkbox)
            return checkbox, label


        # Create a list of checkbox and label pairs
        checkbox_label_pairs = []
        for option in options:
            checkbox_label_pairs.append(create_checkbox(option, "10"))

        # Add the checkbox and label pairs to the layout
        for checkbox, label in checkbox_label_pairs:
            self.options_layout.add_widget(label)
            self.options_layout.add_widget(checkbox)

        # Add the options layout to the main layout
        self.main_layout.add_widget(self.options_layout)

        self.next_button_click_count = 0
        next_button = MDFillRoundFlatButton(text = "Continuar", font_name = "fonts/Lato-Bolditalic.ttf")
        next_button.haling = "center"
        next_button.size_hint_y = 0.2
        next_button.size_hint_x = 1
        next_button.bind(on_release = (self.back))
        self.main_layout.add_widget(next_button)

        self.add_widget(self.main_layout)



    def back(self, *_):

        if self.next_button_click_count >=1:
            self.rewrite_marks()
        self.check_checkboxes()

        NIHSSCalc.update_score_text(self.manager.get_screen("nihss"))
        NIHSSCalc.update_button_color(self.manager.get_screen("nihss"))

        self.manager.transition.direction = "right"
        self.manager.current = 'nihss'
        self.next_button_click_count += 1
    def rewrite_marks(self):
        score = NihssScore.get_instance()
        score._nihss_score[self.name] = None

    def check_checkboxes(self):
        score = NihssScore.get_instance()
        for i, checkbox in enumerate(self.checkboxes):
            if checkbox.active:
                score.update_score(self.name,i)

class Eleven(MDScreen):
    name = "11"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Main Layout
        self.main_layout = MDBoxLayout(orientation = "vertical", spacing = "10dp", padding = ("15dp"), size_hint_x = 1, size_hint_y = 1)

        # Titulo
        title_label = MDLabel()
        title_label.text = "11. Extinción y falta de atención: ¿Hay negligencia visual o falta de atención?"
        title_label.font_size = dp(20)
        title_label.size_hint = (1, 0.3)
        title_label.font_name = "fonts/Lato-Bolditalic.ttf"

        self.main_layout.add_widget(title_label)

        # Layout options2
        self.options_layout = MDGridLayout(orientation = "lr-tb", spacing = "55dp", padding = ("15dp"), size_hint = (1, 1), cols = 2)
        options = ["Sin alteraciones", "Parcial, solo una modalidad afectada", "Completa, más de una modalidad"]

        self.checkboxes = []
        def create_checkbox(option, num):
            """Creates a checkbox and label for the given option."""
            size_checkbox = dp(32)
            size_labels = dp(12)
            checkbox = MDCheckbox(group = f"checkboxes{num}", size_hint=(0.5, None), size=(size_checkbox, size_checkbox), pos_hint={'center_x': 0.9})
            label = MDLabel(text=option, size_hint=(0.5, None), size=(size_labels, size_labels))
            label.font_name = "fonts/Lato-Italic.ttf"
            self.checkboxes.append(checkbox)
            return checkbox, label


        # Create a list of checkbox and label pairs
        checkbox_label_pairs = []
        for option in options:
            checkbox_label_pairs.append(create_checkbox(option, "11"))

        # Add the checkbox and label pairs to the layout
        for checkbox, label in checkbox_label_pairs:
            self.options_layout.add_widget(label)
            self.options_layout.add_widget(checkbox)

        # Add the options layout to the main layout
        self.main_layout.add_widget(self.options_layout)

        self.next_button_click_count = 0
        next_button = MDFillRoundFlatButton(text = "Continuar", font_name = "fonts/Lato-Bolditalic.ttf")
        next_button.haling = "center"
        next_button.size_hint_y = 0.2
        next_button.size_hint_x = 1
        next_button.bind(on_release = (self.back))
        self.main_layout.add_widget(next_button)

        self.add_widget(self.main_layout)

    def back(self, *_):

        if self.next_button_click_count >=1:
            self.rewrite_marks()
        self.check_checkboxes()

        NIHSSCalc.update_score_text(self.manager.get_screen("nihss"))
        NIHSSCalc.update_button_color(self.manager.get_screen("nihss"))

        self.manager.transition.direction = "right"
        self.manager.current = 'nihss'
        self.next_button_click_count += 1
    def rewrite_marks(self):
        score = NihssScore.get_instance()
        score._nihss_score[self.name] = None

    def check_checkboxes(self):
        score = NihssScore.get_instance()
        for i, checkbox in enumerate(self.checkboxes):
            if checkbox.active:
                score.update_score(self.name,i)

#######
class Tratamiento(MDScreen):
    name = "trt"

class Gracias(MDScreen):
    pass

class TimeScreen(MDBoxLayout):
    selected_time = ""

    def on_enter(self):
        self.ids.selected_time_label.text = "Hora: [Hora seleccionada]"

    def update_selected_time(self, selected_time):
        self.ids.selected_time_label.text = f"Hora: {selected_time}"

    def on_time(self, instance, time):
        self.ids.selected_time_label.text = f"Hora: {time}"
        self.ids.selected_time_label.update_widgets()

class PatricApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.previous_screen = ""
        self.selected_time = None

    def build(self):
        Window.clearcolor = (255, 255, 255, 255)
        self.root_widget = Builder.load_file("patric.kv")
        return self.root_widget

    def show_time_picker(self):
        time_dialog = MDTimePicker()
        time_dialog.bind(time=self.on_time_picker_time)
        time_dialog.open()

    def on_time_picker_time(self, instance, value):
        selected_time_str = value.strftime('%H:%M')
        selected_time = datetime.strptime(selected_time_str, "%H:%M").time()
        current_time = datetime.now().time()
        time_difference = datetime.combine(datetime.today(), current_time) - datetime.combine(datetime.today(), selected_time)
        rounded_time_difference = timedelta(minutes=round(time_difference.total_seconds() / 60))

        screen_time = self.root.get_screen('time')
        screen_time.ids.selected_time_label.text = f"Hora seleccionada: {selected_time_str}"
        screen_time.ids.elapsed_time_label.text = f"Min. transcurridos: {rounded_time_difference.seconds // 60:02}"

        self.selected_time = datetime.combine(datetime.today(), value)

    def check_elapsed_time(self):
        current_time = datetime.now()

        if self.selected_time and self.root.current_screen.name == 'time':
            elapsed_time = current_time - self.selected_time
            elapsed_minutes = elapsed_time.total_seconds() / 60
        else:
            elapsed_minutes = 0

        elapsed_minutes_adjusted = elapsed_minutes % 1440

        if elapsed_minutes_adjusted < 0:
            elapsed_minutes_adjusted += 1440

        screen = self.root.get_screen('time')

        screen.ids.elapsed_time_label.text = f"Min. transcurridos: {elapsed_minutes_adjusted:.0f}"

        if self.selected_time is not None and elapsed_minutes_adjusted < 270 and self.root.current_screen.name == 'time':
            pantalla_objetivo = "ECV"
        else:
            pantalla_objetivo = "time_n"

        self.root.transition.direction = "left"
        self.root.current = pantalla_objetivo

if __name__ == "__main__":
    PatricApp().run()