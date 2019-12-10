try:
    from android.permissions import request_permissions, Permission
    request_permissions([Permission.INTERNET])
except:
    pass

import kivy
kivy.require('1.1.3')
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window
from screen1 import Screen1
from screen2 import Screen2



class Evaluator(App):
    title = 'Evaluator'
    #icon = 'icon.png'
    
    def build(self):
        main_list=["",[],[],[]]
        self.Sm = ScreenManager()
        self.Sc1=Screen1(name="external", config_list=main_list)
        self.Sm.add_widget(self.Sc1)
        self.Sm.current="external"
        self.Sc2=Screen2(name="Explore", config_list=main_list)
        self.Sm.add_widget(self.Sc2)

        return self.Sm
    #def initialize_global_vars(self):
    #    root_folder = self.user_data_dir
    def on_pause(self):
        return True

if __name__ in ('__main__', '__android__'):
    Evaluator().run()
