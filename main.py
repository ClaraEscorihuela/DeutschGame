import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.graphics import Color, Rectangle
import random
import json

def load_dictionary(filename):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_dictionary(dictionary, filename):
    with open(filename, 'w') as file:
        json.dump(dictionary, file)


class MainScreen(Screen):
    def __init__(self, topics, save_callback, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.topics = topics
        self.save_callback = save_callback

        # Main layout with white background
        self.main_layout = BoxLayout(orientation="vertical")
        with self.main_layout.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(size=self.main_layout.size, pos=self.main_layout.pos)
        self.main_layout.bind(size=self.update_rect, pos=self.update_rect)

        # Welcome label
        welcome_label = Label(text="Welcome to the Translation Game!", color=(0, 0, 0, 1))
        self.main_layout.add_widget(welcome_label)

        # Add buttons for actions
        self.add_buttons()

        self.add_widget(self.main_layout)

    def update_rect(self, *args):
        self.rect.pos = self.main_layout.pos
        self.rect.size = self.main_layout.size

    def add_buttons(self):
        btn_new_word = Button(text="Introduce New Word", background_color=(1, 1, 1, 1), color=(0, 0, 0, 1))
        btn_new_word.bind(on_press=self.switch_to_new_word_screen)
        self.main_layout.add_widget(btn_new_word)

        btn_translate_ge_to_en = Button(text="Translate German to English", background_color=(1, 1, 1, 1), color=(0, 0, 0, 1))
        btn_translate_ge_to_en.bind(on_press=self.switch_to_translation_ge_to_en)
        self.main_layout.add_widget(btn_translate_ge_to_en)

        btn_translate_en_to_ge = Button(text="Translate English to German", background_color=(1, 1, 1, 1), color=(0, 0, 0, 1))
        btn_translate_en_to_ge.bind(on_press=self.switch_to_translation_en_to_ge)
        self.main_layout.add_widget(btn_translate_en_to_ge)

        btn_exit = Button(text="Exit", background_color=(1, 1, 1, 1), color=(0, 0, 0, 1))
        btn_exit.bind(on_press=App.get_running_app().stop)
        self.main_layout.add_widget(btn_exit)

    def switch_to_new_word_screen(self, instance):
        self.manager.current = 'new_word_screen'

    def switch_to_translation_ge_to_en(self, instance):
        self.manager.current = 'translate_ge_to_en_screen'

    def switch_to_translation_en_to_ge(self, instance):
        self.manager.current = 'translate_en_to_ge_screen'

class NewWordScreen(Screen):
    def __init__(self, topics, save_callback, **kwargs):
        super(NewWordScreen, self).__init__(**kwargs)
        self.topics = topics
        self.save_callback = save_callback

        self.layout = BoxLayout(orientation="vertical")

        self.label = Label(text="New Word Screen", color=(0, 0, 0, 1))
        self.layout.add_widget(self.label)

        self.word_input = TextInput(hint_text="Enter German word", multiline=False, background_color=(1, 1, 1, 1), foreground_color=(0, 0, 0, 1))
        self.layout.add_widget(self.word_input)

        self.translation_input = TextInput(hint_text="Enter English translation", multiline=False, background_color=(1, 1, 1, 1), foreground_color=(0, 0, 0, 1))
        self.layout.add_widget(self.translation_input)

        self.submit_button = Button(text="Submit", background_color=(0.9, 0.9, 0.9, 1), color=(0, 0, 0, 1))
        self.submit_button.bind(on_press=self.add_new_word)
        self.layout.add_widget(self.submit_button)

        self.result_label = Label(text="", color=(0, 0, 0, 1))
        self.layout.add_widget(self.result_label)

        btn_back = Button(text="Back to Main Menu", background_color=(1, 1, 1, 1), color=(0, 0, 0, 1))
        btn_back.bind(on_press=self.switch_to_main)
        self.layout.add_widget(btn_back)

        self.add_widget(self.layout)

    def add_new_word(self, instance):
        german_word = self.word_input.text.strip()
        english_translation = self.translation_input.text.strip()

        if german_word and english_translation:
            self.topics['pabloWords'][german_word] = english_translation
            self.save_callback(self.topics)
            self.result_label.text = "Word added successfully!"
            self.word_input.text = ""
            self.translation_input.text = ""
        else:
            self.result_label.text = "Please enter both the word and its translation."

    def switch_to_main(self, instance):
        self.manager.current = 'main_screen'


class TranslateGeToEnScreen(Screen):
    def __init__(self, topics, **kwargs):
        super(TranslateGeToEnScreen, self).__init__(**kwargs)
        self.topics = topics

        self.layout = BoxLayout(orientation="vertical")

        with self.layout.canvas.before:
            Color(1, 1, 1, 1)  # Fondo blanco
            self.rect = Rectangle(size=self.layout.size, pos=self.layout.pos)
        self.layout.bind(size=self.update_rect, pos=self.update_rect)

        self.question_label = Label(text="", color=(0, 0, 0, 1))
        self.layout.add_widget(self.question_label)

        self.answer_input = TextInput(multiline=False, background_color=(1, 1, 1, 1), foreground_color=(0, 0, 0, 1))
        self.layout.add_widget(self.answer_input)

        self.submit_button = Button(text="Submit", background_color=(0.9, 0.9, 0.9, 1), color=(0, 0, 0, 1))
        self.submit_button.bind(on_press=self.check_answer)
        self.layout.add_widget(self.submit_button)

        self.result_label = Label(text="", color=(0, 0, 0, 1))
        self.layout.add_widget(self.result_label)

        btn_back = Button(text="Back to Main Menu", background_color=(1, 1, 1, 1), color=(0, 0, 0, 1))
        btn_back.bind(on_press=self.switch_to_main)
        self.layout.add_widget(btn_back)

        self.add_widget(self.layout)

        self.current_value = ""
        self.correct_key = ""

    def update_rect(self, *args):
        self.rect.pos = self.layout.pos
        self.rect.size = self.layout.size

    def on_enter(self, *args):
        self.new_question()

    def new_question(self):
        self.result_label.text = "Correct!"
        topic = 'pabloWords'
        translations = self.topics[topic]
        self.correct_key = random.choice(list(translations.keys()))
        self.current_value = translations[self.correct_key]
        self.question_label.text = f"What is the English translation of '{self.correct_key}'?"
        self.answer_input.text = ""
        self.result_label.text = ""

    def check_answer(self, instance):
        user_input = self.answer_input.text.strip()

        if user_input.lower() == self.current_value.lower():
            self.result_label.text = "Correct!"
            self.schedule_new_question()
        else:
            self.result_label.text = "Incorrect, try again."

    def schedule_new_question(self):
        self.result_label.text = "Correct!"
        self.answer_input.text = ""
        self.result_label.text = "Correct!"
        self.new_question()

    def switch_to_main(self, instance):
        self.manager.current = 'main_screen'

class TranslateEnToGeScreen(Screen):
    def __init__(self, topics, **kwargs):
        super(TranslateEnToGeScreen, self).__init__(**kwargs)
        self.topics = topics

        self.layout = BoxLayout(orientation="vertical")

        with self.layout.canvas.before:
            Color(1, 1, 1, 1)  # Fondo blanco
            self.rect = Rectangle(size=self.layout.size, pos=self.layout.pos)
        self.layout.bind(size=self.update_rect, pos=self.update_rect)

        self.question_label = Label(text="", color=(0, 0, 0, 1))
        self.layout.add_widget(self.question_label)

        self.answer_input = TextInput(multiline=False, background_color=(1, 1, 1, 1), foreground_color=(0, 0, 0, 1))
        self.layout.add_widget(self.answer_input)

        self.submit_button = Button(text="Submit", background_color=(0.9, 0.9, 0.9, 1), color=(0, 0, 0, 1))
        self.submit_button.bind(on_press=self.check_answer)
        self.layout.add_widget(self.submit_button)

        self.result_label = Label(text="", color=(0, 0, 0, 1))
        self.layout.add_widget(self.result_label)

        btn_back = Button(text="Back to Main Menu", background_color=(1, 1, 1, 1), color=(0, 0, 0, 1))
        btn_back.bind(on_press=self.switch_to_main)
        self.layout.add_widget(btn_back)

        self.add_widget(self.layout)

        self.current_value = ""
        self.correct_key = ""

    def update_rect(self, *args):
        self.rect.pos = self.layout.pos
        self.rect.size = self.layout.size

    def on_enter(self, *args):
        self.new_question()

    def new_question(self):
        topic = 'pabloWords'
        translations = self.topics[topic]
        self.current_value = random.choice(list(translations.values()))
        self.correct_key = [key for key, value in translations.items() if value == self.current_value][0]
        self.question_label.text = f"What is the German translation of '{self.current_value}'?"
        self.answer_input.text = ""
        self.result_label.text = ""


    def check_answer(self, instance):
        user_input = self.answer_input.text.strip()

        if user_input.lower() == self.correct_key.lower():
            self.result_label.text = "Correct!"
            self.schedule_new_question()
        else:
            self.result_label.text = "Incorrect, try again."

    def schedule_new_question(self):
        self.result_label.text = "Correct!"
        self.answer_input.text = ""
        self.result_label.text = "Correct!"
        self.new_question()

    def switch_to_main(self, instance):
        self.manager.current = 'main_screen'


class TranslationApp(App):
    def build(self):
        self.filename = 'dictionary.json'
        self.topics = self.load_dictionary(self.filename)

        sm = ScreenManager()

        sm.add_widget(MainScreen(name='main_screen', topics=self.topics, save_callback=self.save_dictionary))
        sm.add_widget(NewWordScreen(name='new_word_screen', topics=self.topics, save_callback=self.save_dictionary))
        sm.add_widget(TranslateGeToEnScreen(name='translate_ge_to_en_screen', topics=self.topics))
        sm.add_widget(TranslateEnToGeScreen(name='translate_en_to_ge_screen', topics=self.topics))

        return sm

    def load_dictionary(self, filename):
        return load_dictionary(filename)

    def save_dictionary(self, topics):
        save_dictionary(topics, self.filename)

if __name__ == "__main__":
    TranslationApp().run()