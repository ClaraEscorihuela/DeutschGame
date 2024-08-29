from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.graphics import Color, Rectangle
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.uix.spinner import Spinner
from kivy.metrics import dp, sp
import random
import json
from kivy.uix.dropdown import DropDown
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout

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
        title_label = Label(
            text="Translation Game!",
            color=(0, 0, 0, 1),
            font_size=sp(24),
            size_hint=(1, 0.1),
            pos_hint={'center_x': 0.5}
        )
        self.main_layout.add_widget(title_label)

        # Button layout
        button_layout = BoxLayout(
            orientation="horizontal",
            spacing=dp(20),
            padding=[dp(10), dp(10), dp(10), dp(10)],
            size_hint=(1, 0.2)
        )

        # Button definitions
        buttons = [
            {"text": "Introduce New Word", "background_color": (0.87, 0.63, 0.87, 1)},
            {"text": "English to German", "background_color": (0.48, 0.78, 0.96, 1)},
            {"text": "German to English", "background_color": (0.5, 1, 0, 1)},
            {"text": "Exit", "background_color": (1, 0.84, 0, 1)},
        ]

        for btn_info in buttons:
            btn = Button(
                text=btn_info['text'],
                background_color=btn_info['background_color'],
                color=(1, 1, 1, 1),
                size_hint=(0.25, 1)
            )

            if btn_info['text'] == "Exit":
                btn.bind(on_press=App.get_running_app().stop)
            elif btn_info['text'] == "Introduce New Word":
                btn.bind(on_press=self.switch_to_topic_selection_screen)
            elif btn_info['text'] == "English to German":
                btn.bind(on_press=self.switch_to_topic_selection_for_ge_to_en)
            elif btn_info['text'] == "German to English":
                btn.bind(on_press=self.switch_to_topic_selection_for_ge_to_en)

            button_layout.add_widget(btn)

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

        # Main layout with white background
        self.layout = BoxLayout(orientation="vertical", size_hint=(1, 1), padding=dp(20), spacing=dp(20))
        with self.layout.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(size=self.layout.size, pos=self.layout.pos)
        self.layout.bind(size=self.update_rect, pos=self.update_rect)

        # Add a label at the top of the screen
        self.title_label = Label(
            text="Select a Topic",
            font_size=sp(24),
            color=(0, 0, 0, 1),
            size_hint=(1, 0.1)
        )
        self.layout.add_widget(self.title_label)

        # Dropdown for topic selection using DropDown widget
        self.dropdown = DropDown()
        for topic in self.topics.keys():
            btn = Button(
                text=topic,
                size_hint_y=None,
                height=dp(44),
                background_color=(0.87, 0.87, 0.87, 0.5),
                color=(0, 0, 0, 1),
                font_size=sp(20)
            )
            btn.bind(on_release=lambda btn: self.select_existing_topic(btn.text))
            self.dropdown.add_widget(btn)

        # Main button to trigger the dropdown
        self.main_button = Button(
            text='Choose a topic',
            size_hint=(1, 0.1),
            background_color=(0.87, 0.87, 0.87, 0.5),
            color=(0, 0, 0, 1),
            font_size=sp(20)
        )
        self.main_button.bind(on_release=self.dropdown.open)
        self.layout.add_widget(self.main_button)

        # Bottom layout for buttons
        button_layout = BoxLayout(
            orientation="horizontal",
            spacing=dp(20),
            size_hint=(1, 0.1)
        )

        # Add New Topic button
        btn_new_topic = Button(
            text="Add New Topic",
            background_color=(0.6, 0.4, 0.8, 1),
            color=(1, 1, 1, 1),
            size_hint=(0.5, 1),
            font_size=sp(18)
        )
        btn_new_topic.bind(on_press=self.add_new_topic)
        button_layout.add_widget(btn_new_topic)

        # Back to Main Menu button
        btn_back_to_main = Button(
            text="Back to Main Menu",
            background_color=(0.3, 0.3, 1, 1),  # Blue color
            color=(1, 1, 1, 1),
            size_hint=(0.5, 1),
            font_size=sp(18)
        )
        btn_back_to_main.bind(on_press=self.switch_to_main)
        button_layout.add_widget(btn_back_to_main)

        # Exit button
        btn_exit = Button(
            text="Exit",
            background_color=(1, 0.3, 0.3, 1),  # Light red color
            color=(1, 1, 1, 1),
            size_hint=(0.5, 1),
            font_size=sp(18)
        )
        btn_exit.bind(on_press=App.get_running_app().stop)
        button_layout.add_widget(btn_exit)

        # Add the button layout to the main layout
        self.layout.add_widget(button_layout)

        # Add the main layout to the screen
        self.add_widget(self.layout)

    def update_rect(self, *args):
        self.rect.pos = self.layout.pos
        self.rect.size = self.layout.size

    def select_existing_topic(self, text):
        # Handle the topic selection
        if text != 'Choose a topic':  # Make sure a valid topic is selected
            self.manager.get_screen('new_word_screen').set_topic(text)
            self.manager.current = 'new_word_screen'
            self.main_button.text = 'Choose a topic'  # Reset the main button text
        self.dropdown.dismiss()

    def add_new_topic(self, instance):
        # Implement the functionality for adding a new topic
        pass

    def switch_to_main(self, instance):
        self.manager.current = 'main_screen'

    def on_touch_down(self, touch):
        # Ensure touch events are passed to children
        super(TopicSelectionScreen, self).on_touch_down(touch)

        # Handle touch interactions if needed (e.g., for dropdowns)
        if self.collide_point(*touch.pos):
            # Additional logic for mobile interaction can be added here
            pass


class TopicSelectionForTranslationScreen(Screen):
    def __init__(self, topics, target_screen, **kwargs):
        super(TopicSelectionForTranslationScreen, self).__init__(**kwargs)
        self.topics = topics
        self.target_screen = target_screen

        # Main layout with white background
        self.layout = BoxLayout(orientation="vertical", size_hint=(1, 1))
        with self.layout.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(size=self.layout.size, pos=self.layout.pos)
        self.layout.bind(size=self.update_rect, pos=self.update_rect)

        # Title label
        title_label = Label(text="Select a Topic for Translation", color=(0, 0, 0, 1), font_size='24sp',
                            size_hint=(1, 0.1))
        self.layout.add_widget(title_label)

        # Create a ScrollView for the topic buttons
        scroll_view = ScrollView(size_hint=(1, 0.7))  # Take up most of the screen height
        self.button_container = GridLayout(cols=1, spacing=10, size_hint_y=None)  # Vertical stack of buttons
        self.button_container.bind(minimum_height=self.button_container.setter('height'))  # Enable dynamic height

        # Add existing topics
        self.add_existing_topics()

        scroll_view.add_widget(self.button_container)
        self.layout.add_widget(scroll_view)

        # Button layout for back button
        button_layout = BoxLayout(orientation="horizontal", spacing=20, padding=20, size_hint=(1, 0.2))

        # Back button
        btn_back = Button(text="Back to Main Menu", background_color=(1, 1, 1, 1), color=(0, 0, 0, 1),
                          size_hint=(0.5, 1))
        btn_back.bind(on_press=self.switch_to_main)
        button_layout.add_widget(btn_back)

        self.layout.add_widget(button_layout)
        self.add_widget(self.layout)

    def update_rect(self, *args):
        self.rect.pos = self.layout.pos
        self.rect.size = self.layout.size

    def add_existing_topics(self):
        for topic in self.topics.keys():
            btn_topic = Button(text=topic, background_color=(0.9, 0.9, 0.9, 1), color=(0, 0, 0, 1), size_hint_y=None,
                               height=50)  # Fixed height for each button
            btn_topic.bind(on_press=self.select_existing_topic)
            self.button_container.add_widget(btn_topic)

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

        # Main layout with white background
        self.layout = BoxLayout(orientation="vertical", size_hint=(1, 1), padding=dp(20), spacing=dp(20))
        with self.layout.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(size=self.layout.size, pos=self.layout.pos)
        self.layout.bind(size=self.update_rect, pos=self.update_rect)

        # Label for the title
        self.title_label = Label(
            text="New Word Screen",
            font_size=sp(24),
            color=(0, 0, 0, 1),
            size_hint=(1, 0.1)
        )
        self.layout.add_widget(self.title_label)

        # Horizontal layout for the top buttons and text inputs
        top_layout = BoxLayout(orientation="horizontal", size_hint=(1, 0.4), spacing=dp(10))

        # Vertical layout for the English word button and input
        english_layout = BoxLayout(orientation="vertical", size_hint=(0.5, 1), spacing=dp(10))

        # English Word Button
        btn_english = Button(
            text="Word in English",
            background_color=(0.6, 0.8, 1, 1),  # Light blue
            # color
            color=(0, 0, 0, 1),
            font_size=sp(18)
        )
        english_layout.add_widget(btn_english)

        # Input for English translation (under the button)
        self.translation_input = TextInput(
            hint_text="Enter English translation",
            multiline=False,
            background_color=(1, 1, 1, 1),
            foreground_color=(0, 0, 0, 1),
            font_size=sp(20)
        )
        english_layout.add_widget(self.translation_input)

        # Vertical layout for the German word button and input
        german_layout = BoxLayout(orientation="vertical", size_hint=(0.5, 1), spacing=dp(10))

        # German Word Button
        btn_german = Button(
            text="Word in German",
            background_color=(0.8, 0.6, 1, 1),  # Light purple color
            color=(0, 0, 0, 1),
            font_size=sp(18)
        )
        german_layout.add_widget(btn_german)

        # Input for German word (under the button)
        self.word_input = TextInput(
            hint_text="Enter German word",
            multiline=False,
            background_color=(1, 1, 1, 1),
            foreground_color=(0, 0, 0, 1),
            font_size=sp(20)
        )
        german_layout.add_widget(self.word_input)

        # Add the vertical layouts to the top horizontal layout
        top_layout.add_widget(english_layout)
        top_layout.add_widget(german_layout)

        # Add the top layout to the main layout
        self.layout.add_widget(top_layout)

        # Submit button
        self.submit_button = Button(
            text="Submit",
            background_color=(0.9, 0.9, 0.9, 1),
            size_hint=(1, 0.1),
            font_size=sp(20)
        )
        self.submit_button.bind(on_press=self.add_new_word)
        self.layout.add_widget(self.submit_button)

        # Result label
        self.result_label = Label(
            text="",
            color=(0, 0, 0, 1),
            size_hint=(1, 0.1),
            font_size=sp(16)
        )
        self.layout.add_widget(self.result_label)

        # Back button at the bottom
        btn_back = Button(
            text="Back to Main Menu",
            background_color=(1, 1, 1, 1),
            color=(0, 0, 0, 1),
            size_hint=(1, 0.1),
            font_size=sp(18)
        )
        btn_back.bind(on_press=self.switch_to_main)
        self.layout.add_widget(btn_back)

        # Add the main layout to the screen
        self.add_widget(self.layout)

    def update_rect(self, *args):
        self.rect.pos = self.layout.pos
        self.rect.size = self.layout.size

    def set_topic(self, topic):
        self.current_topic = topic
        self.title_label.text = f"New Word Screen - Topic: {topic}"

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

        self.layout = BoxLayout(orientation="vertical", padding=dp(20), spacing=dp(10))

        with self.layout.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(size=self.layout.size, pos=self.layout.pos)
        self.layout.bind(size=self.update_rect, pos=self.update_rect)

        # Label for the question
        self.question_label = Label(
            text="hola",
            color=(0, 0, 0, 1),
            font_size=sp(24),
            halign="center",
            size_hint=(1, 0.2)
        )
        self.layout.add_widget(self.question_label)

        # Text input for the answer
        self.answer_input = TextInput(
            multiline=False,
            background_color=(1, 1, 1, 1),
            foreground_color=(0, 0, 0, 1),
            font_size=sp(18),
            size_hint=(1, 0.2)
        )
        self.layout.add_widget(self.answer_input)

        # Submit button
        self.submit_button = Button(
            text="Submit",
            background_color=(0.9, 0.9, 0.9, 1),
            color=(0, 0, 0, 1),
            size_hint=(1, 0.2),
            font_size=sp(18)
        )
        self.submit_button.bind(on_press=self.check_answer)
        self.layout.add_widget(self.submit_button)

        # Label for the result
        self.result_label = Label(
            text="",
            color=(0, 0, 0, 1),
            font_size=sp(18),
            halign="center",
            size_hint=(1, 0.2)
        )
        self.layout.add_widget(self.result_label)

        # Back button to return to the main menu
        btn_back = Button(
            text="Back to Main Menu",
            background_color=(1, 1, 1, 1),
            color=(0, 0, 0, 1),
            size_hint=(1, 0.2),
            font_size=sp(18)
        )
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
        self.new_question()
        if self.current_topic:
            self.new_question()

    def new_question(self):
        if self.current_topic:
            translations = self.topics[self.current_topic]
            self.correct_key = random.choice(list(translations.keys()))
            self.current_value = translations[self.correct_key]

            # Test: Print to console for debugging
            print(f"Selected Word: {self.correct_key} - Translation: {self.current_value}")

            # Setting the word to be translated
            self.question_label.text = f"What is the English translation of '{self.correct_key}'?"
            self.answer_input.text = ""
            self.result_label.text = ""
        else:
            self.question_label.text = "No topic selected!"

    def check_answer(self, instance):
        user_input = self.answer_input.text.strip()

        if user_input.lower() == self.current_value.lower():
            self.result_label.text = "Correct!"
            self.schedule_new_question()
        else:
            self.result_label.text = "Incorrect, try again."

    def schedule_new_question(self):
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