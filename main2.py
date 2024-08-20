from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.graphics import Color, Rectangle
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
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
        self.main_layout = BoxLayout(orientation="vertical", size_hint=(1, 1))
        with self.main_layout.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(size=self.main_layout.size, pos=self.main_layout.pos)
        self.main_layout.bind(size=self.update_rect, pos=self.update_rect)

        # Title label
        title_label = Label(text="Translation Game!", color=(0, 0, 0, 1), font_size='24sp', size_hint=(1, 0.1))
        self.main_layout.add_widget(title_label)

        # Button layout
        button_layout = BoxLayout(orientation="horizontal", spacing=20, padding=20, size_hint=(1, 0.2))

        # Introduce New Word button
        btn_new_word = Button(text="Introduce New Word", background_color='#DDA0DD', color=(1, 1, 1, 1), size_hint=(0.25, 1))
        btn_new_word.bind(on_press=self.switch_to_topic_selection_screen)
        button_layout.add_widget(btn_new_word)

        # Translate English to German button
        btn_translate_en_to_ge = Button(text="English to German", background_color='#7BC8F6', color=(1, 1, 1, 1), size_hint=(0.25, 1))
        btn_translate_en_to_ge.bind(on_press=self.switch_to_topic_selection_for_en_to_ge)
        button_layout.add_widget(btn_translate_en_to_ge)

        # Translate German to English button
        btn_translate_ge_to_en = Button(text="German to English", background_color='#7FFF00', color=(1, 1, 1, 1), size_hint=(0.25, 1))
        btn_translate_ge_to_en.bind(on_press=self.switch_to_topic_selection_for_ge_to_en)
        button_layout.add_widget(btn_translate_ge_to_en)

        # Exit button
        btn_exit = Button(text="Exit", background_color='#FFD700', color=(1, 1, 1, 1), size_hint=(0.25, 1))
        btn_exit.bind(on_press=App.get_running_app().stop)
        button_layout.add_widget(btn_exit)

        self.main_layout.add_widget(button_layout)
        self.add_widget(self.main_layout)

    def update_rect(self, *args):
        self.rect.pos = self.main_layout.pos
        self.rect.size = self.main_layout.size

    def switch_to_topic_selection_screen(self, instance):
        self.manager.current = 'topic_selection_screen'

    def switch_to_topic_selection_for_ge_to_en(self, instance):
        self.manager.current = 'topic_selection_for_ge_to_en_screen'

    def switch_to_topic_selection_for_en_to_ge(self, instance):
        self.manager.current = 'topic_selection_for_en_to_ge_screen'

class TopicSelectionScreen(Screen):
    def __init__(self, topics, save_callback, **kwargs):
        super(TopicSelectionScreen, self).__init__(**kwargs)
        self.topics = topics
        self.save_callback = save_callback

        self.layout = BoxLayout(orientation="vertical", size_hint=(1, 1))
        # Main layout with white background
        with self.layout.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(size=self.layout.size, pos=self.layout.pos)
        self.layout.bind(size=self.update_rect, pos=self.update_rect)

        # Add existing topics
        self.add_existing_topics()

        # Button layout
        button_layout = BoxLayout(orientation="horizontal", spacing=20, padding=20, size_hint=(1, 0.2))

        # Back button
        btn_back = Button(text="Back to Main Menu", background_color=(1, 1, 1, 1), color=(0, 0, 0, 1), size_hint=(0.5, 1))
        btn_back.bind(on_press=self.switch_to_main)
        button_layout.add_widget(btn_back)

        # Another button (e.g., for adding a new topic)
        btn_new_topic = Button(text="New Topic", background_color=(0.6, 0.4, 0.8, 1), color=(1, 1, 1, 1), size_hint=(0.5, 1))
        btn_new_topic.bind(on_press=self.add_new_topic)
        button_layout.add_widget(btn_new_topic)

        self.layout.add_widget(button_layout)
        self.add_widget(self.layout)

    def update_rect(self, *args):
        self.rect.pos = self.layout.pos
        self.rect.size = self.layout.size

    def add_existing_topics(self):
        background_color = ['#DDA0DD','#7BC8F6','#7FFF00','#FFD700']
        i = 0
        for topic in self.topics.keys():
            btn_topic = Button(text=topic, background_color=background_color[i], color=(0, 0, 0, 1), size_hint=(1, 0.1))
            btn_topic.bind(on_press=self.select_existing_topic)
            self.layout.add_widget(btn_topic)
            i = 0+1

    def select_existing_topic(self, instance):
        topic = instance.text
        self.manager.get_screen('new_word_screen').set_topic(topic)
        self.manager.current = 'new_word_screen'

    def switch_to_main(self, instance):
        self.manager.current = 'main_screen'

    def add_new_topic(self, instance):
        # Implement the functionality for adding a new topic
        pass

class TopicSelectionForTranslationScreen(Screen):
    def __init__(self, topics, target_screen, **kwargs):
        super(TopicSelectionForTranslationScreen, self).__init__(**kwargs)
        self.topics = topics
        self.target_screen = target_screen

        self.layout = BoxLayout(orientation="vertical", size_hint=(1, 1))
        # Main layout with white background
        with self.layout.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(size=self.layout.size, pos=self.layout.pos)
        self.layout.bind(size=self.update_rect, pos=self.update_rect)

        # Title label
        title_label = Label(text="Select a Topic for Translation", color=(0, 0, 0, 1), font_size='24sp', size_hint=(1, 0.1))
        self.layout.add_widget(title_label)

        # Add existing topics
        self.add_existing_topics()

        # Button layout
        button_layout = BoxLayout(orientation="horizontal", spacing=20, padding=20, size_hint=(1, 0.2))

        # Back button
        btn_back = Button(text="Back to Main Menu", background_color=(1, 1, 1, 1), color=(0, 0, 0, 1), size_hint=(0.5, 1))
        btn_back.bind(on_press=self.switch_to_main)
        button_layout.add_widget(btn_back)

        self.layout.add_widget(button_layout)
        self.add_widget(self.layout)

    def update_rect(self, *args):
        self.rect.pos = self.layout.pos
        self.rect.size = self.layout.size

    def add_existing_topics(self):
        for topic in self.topics.keys():
            btn_topic = Button(text=topic, background_color=(0.9, 0.9, 0.9, 1), color=(0, 0, 0, 1), size_hint=(1, 0.1))
            btn_topic.bind(on_press=self.select_existing_topic)
            self.layout.add_widget(btn_topic)

    def select_existing_topic(self, instance):
        topic = instance.text
        self.manager.get_screen(self.target_screen).set_topic(topic)
        self.manager.current = self.target_screen

    def switch_to_main(self, instance):
        self.manager.current = 'main_screen'



class NewWordScreen(Screen):
    def __init__(self, topics, save_callback, **kwargs):
        super(NewWordScreen, self).__init__(**kwargs)
        self.topics = topics
        self.save_callback = save_callback
        self.current_topic = None

        self.layout = BoxLayout(orientation="vertical")

        self.label = Label(text="New Word Screen", color=(0, 0, 0, 1))
        self.layout.add_widget(self.label)

        self.word_input = TextInput(hint_text="Enter German word", multiline=False, background_color=(1, 1, 1, 1), foreground_color=(0, 0, 0, 1))
        self.layout.add_widget(self.word_input)

        self.translation_input = TextInput(hint_text="Enter English translation", multiline=False, background_color=(1, 1, 1, 1), foreground_color=(0, 0, 0, 1))
        self.layout.add_widget(self.translation_input)

        self.submit_button = Button(text="Submit", background_color=(0.9, 0.9, 0.9, 1))
        self.submit_button.bind(on_press=self.add_new_word)
        self.layout.add_widget(self.submit_button)

        self.result_label = Label(text="", color=(0, 0, 0, 1))
        self.layout.add_widget(self.result_label)

        btn_back = Button(text="Back to Main Menu", background_color=(1, 1, 1, 1), color=(0, 0, 0, 1))
        btn_back.bind(on_press=self.switch_to_main)
        self.layout.add_widget(btn_back)

        self.add_widget(self.layout)

    def set_topic(self, topic):
        self.current_topic = topic
        self.label.text = f"New Word Screen - Topic: {topic}"

    def add_new_word(self, instance):
        german_word = self.word_input.text.strip()
        english_translation = self.translation_input.text.strip()

        if german_word and english_translation:
            self.topics[self.current_topic][german_word] = english_translation
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
        self.current_topic = None

        self.layout = BoxLayout(orientation="vertical")

        with self.layout.canvas.before:
            Color(1, 1, 1, 1)  # White background
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

    def set_topic(self, topic):
        self.current_topic = topic
        self.new_question()

    def on_enter(self, *args):
        if self.current_topic:
            self.new_question()

    def new_question(self):
        translations = self.topics[self.current_topic]
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
        self.new_question()

    def switch_to_main(self, instance):
        self.manager.current = 'main_screen'

class TranslateEnToGeScreen(Screen):
    def __init__(self, topics, **kwargs):
        super(TranslateEnToGeScreen, self).__init__(**kwargs)
        self.topics = topics
        self.current_topic = None

        self.layout = BoxLayout(orientation="vertical")

        with self.layout.canvas.before:
            Color(1, 1, 1, 1)  # White background
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

    def set_topic(self, topic):
        self.current_topic = topic
        self.new_question()

    def on_enter(self, *args):
        if self.current_topic:
            self.new_question()

    def new_question(self):
        translations = self.topics[self.current_topic]
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
        self.new_question()

    def switch_to_main(self, instance):
        self.manager.current = 'main_screen'

class TranslationApp(App):
    def build(self):
        self.filename = 'dictionary.json'
        self.topics = self.load_dictionary(self.filename)

        sm = ScreenManager()

        sm.add_widget(MainScreen(name='main_screen', topics=self.topics, save_callback=self.save_dictionary))
        sm.add_widget(TopicSelectionScreen(name='topic_selection_screen', topics=self.topics, save_callback=self.save_dictionary))
        sm.add_widget(NewWordScreen(name='new_word_screen', topics=self.topics, save_callback=self.save_dictionary))
        sm.add_widget(TranslateGeToEnScreen(name='translate_ge_to_en_screen', topics=self.topics))
        sm.add_widget(TranslateEnToGeScreen(name='translate_en_to_ge_screen', topics=self.topics))
        sm.add_widget(TopicSelectionForTranslationScreen(name='topic_selection_for_ge_to_en_screen', topics=self.topics, target_screen='translate_ge_to_en_screen'))
        sm.add_widget(TopicSelectionForTranslationScreen(name='topic_selection_for_en_to_ge_screen', topics=self.topics, target_screen='translate_en_to_ge_screen'))

        return sm

    def load_dictionary(self, filename):
        return load_dictionary(filename)

    def save_dictionary(self, topics):
        save_dictionary(topics, self.filename)

if __name__ == '__main__':
    TranslationApp().run()