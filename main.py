from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.video import Video
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDFillRoundFlatButton
from kivymd.uix.filemanager import MDFileManager

from track import *


Builder.load_string('''
<LoginScreen>:
    MDToolbar:
        title: "Drip Infusion Dashboard"
        left_action_items: [["👨‍⚕️", lambda x: None]]
    
    MDCard:
        orientation: 'vertical'
        size_hint: 0.7, None
        height: "300dp"
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        padding: '20dp'
        spacing: '10dp'

        MDLabel:
            text: 'Monitoring Drip Infusion'
            font_style: 'H4'
            halign: 'center'
            theme_text_color: 'Secondary'

        BoxLayout:
            orientation: 'vertical'
            MDLabel:
                text: 'Status:'
                halign: 'left'
                theme_text_color: 'Secondary'
            
            MDLabel:
                id: status_label
                text: 'Waiting for input'
                halign: 'left'

            MDLabel:
                text: 'Tetesan:'
                halign: 'left'
                theme_text_color: 'Secondary'
            
            MDLabel:
                id: tetesan_text
                text: '__'
                halign: 'left'
            
            MDLabel:
                text: 'Time:'
                halign: 'left'
                theme_text_color: 'Secondary'
            
            MDLabel:
                id: timer_text
                text: '__'
                halign: 'left'
            
            MDLabel:
                text: 'FPS:'
                halign: 'left'
                theme_text_color: 'Secondary'
            
            MDLabel:
                id: fps_text
                text: '__'
                halign: 'left'

        MDFillRoundFlatButton:
            text: 'Upload Video'
            theme_text_color: 'Custom'
            text_color: app.theme_cls.primary_color
            md_bg_color: app.theme_cls.accent_color
            pos_hint: {'center_x': 0.5}
            on_release: root.open_file_manager()

        MDFillRoundFlatButton:
            text: 'START'
            theme_text_color: 'Custom'
            text_color: app.theme_cls.primary_color
            md_bg_color: app.theme_cls.accent_color
            pos_hint: {'center_x': 0.5}
            on_release: root.start_tracking()

<MainScreen>:
    MDToolbar:
        title: "Drip Infusion Dashboard"
        left_action_items: [["👨‍⚕️", lambda x: root.show_login_screen()]]
    
    Video:
        id: video_player
        size_hint: 1, 1
        options: {'eos': 'loop'}
        allow_stretch: True

''')


class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.video_source = None

    def open_file_manager(self):
        file_manager = MDFileManager(exit=self.exit_file_manager, select=self.select_path)
        file_manager.show()

    def exit_file_manager(self, *args):
        self.manager_open = False

    def select_path(self, path):
        self.video_source = path
        self.exit_file_manager()

    def start_tracking(self):
        if self.video_source:
            # reset ID and count from 0
            reset()
            opt = parse_opt()
            opt.conf_thres = 0.5  # Set the default confidence value here
            opt.source = self.video_source

            self.ids.status_label.text = 'Running...'
            self.ids.video_player.state = 'play'
            with torch.no_grad():
                detect(opt, self.ids.tetesan_text, self.ids.timer_text, 0.50, self.ids.fps_text, [0])  # Set the default line position and custom_class here
            self.ids.status_label.text = 'Finished !'
            self.ids.video_player.state = 'stop'

    def on_stop(self):
        self.ids.video_player.unload()


class MainScreen(Screen):
    def show_login_screen(self):
        self.manager.current = "login_screen"
        self.manager.transition.direction = 'right'


class MainApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = 'Indigo'
        screen_manager = ScreenManager()
        screen_manager.add_widget(LoginScreen(name="login_screen"))
        screen_manager.add_widget(MainScreen(name="main_screen"))
        return screen_manager


if __name__ == '__main__':
    MainApp().run()
