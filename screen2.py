from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.graphics import Color, Rectangle, Point, GraphicException
from random import random
from math import sqrt
from kivy.uix.screenmanager import Screen
from os import getcwd, listdir, mkdir, remove
from kivy.clock import Clock
from os import listdir, path
from datetime import datetime
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.checkbox import CheckBox
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
import requests
from numpy import asarray
from time import sleep


class TxtCat(TextInput):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.multiline=False
    def get_value(self):
        return self.text
    def insert_text(self, substring, from_undo=False):
        s = substring.replace(","," ")
        return super(TxtCat, self).insert_text(s, from_undo=from_undo)
    def load_value(self, text):
        self.text=text
    def clear_final(self):
        self.text=""

class NumCat(TextInput):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.multiline=False
        self.input_filter="float"
    def get_value(self):
        return self.text
    def load_value(self, number):
        self.text=number
    def clear_final(self):
        self.text=""

class YYYYInput(TextInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.multiline=False
        input_filter="int"
        hint_text="yyyy"
    def insert_text(self, substring, from_undo=False):
        if len(self.text)>3:
            substring=""
        try:
            int(substring)
        except:
            substring=""
        #substring = substring[:4 - len(self.text)]
        return super(YYYYInput, self).insert_text(substring, from_undo=from_undo)

class MMInput(TextInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.multiline=False
        input_filter="int"
        hint_text="mm"
    def insert_text(self, substring, from_undo=False):
        if len(self.text)>1:
            substring=""
        try:
            int(substring)
        except:
            substring=""
        #substring = substring[:4 - len(self.text)]
        return super(MMInput, self).insert_text(substring, from_undo=from_undo)

class DDInput(TextInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.multiline=False
        input_filter="int"
        hint_text="dd"
    def insert_text(self, substring, from_undo=False):
        if len(self.text)>1:
            substring=""
        try:
            int(substring)
        except:
            substring=""
        #substring = substring[:4 - len(self.text)]
        return super(DDInput, self).insert_text(substring, from_undo=from_undo)

class DatCat(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.rows=1
        self.cols=4
        self.stored=[YYYYInput(), MMInput(), DDInput()]
        self.add_widget(self.stored[0])
        self.add_widget(self.stored[1])
        self.add_widget(self.stored[2])
        self.add_widget(Button(text="now", on_release=self.fix_today))

    def happening(self, dt=None):
        print("wawawa")
    def fix_today(self,dt=None):
        temp=datetime.now()
        self.stored[0].text=temp.strftime("%Y")
        self.stored[1].text=temp.strftime("%m")
        self.stored[2].text=temp.strftime("%d")
    def get_value(self):
        for n in self.stored:
            if len(n.text)==0:
                self.stored[0].text=""
                self.stored[1].text=""
                self.stored[2].text=""
                return ""
                break
        while len(self.stored[0].text)<4:
            self.stored[0].text="0"+self.stored[0].text
        while len(self.stored[1].text)<2:
            self.stored[1].text="0"+self.stored[1].text
        while len(self.stored[2].text)<2:
            self.stored[2].text="0"+self.stored[2].text
        return "-".join([self.stored[0].text,self.stored[1].text,self.stored[2].text])
    def load_value(self,date):
        try:
            temp=date.split("-")
            assert len(temp)==3
            self.stored[0].text=temp[0]
            self.stored[1].text=temp[1]
            self.stored[2].text=temp[2]

        except:
            self.stored[0].text=""
            self.stored[1].text=""
            self.stored[2].text=""
    def clear_final(self):
        self.stored[0].text=""
        self.stored[1].text=""
        self.stored[2].text=""

class CatCat(GridLayout):
    def __init__(self, categories,**kwargs):
        super().__init__(**kwargs)
        self.rows=1
        self.categories=categories
        self.cols=len(categories)
        self.stored=[]

        self.final=""
        for n in categories:
            temp=GridLayout(rows=2, cols=1)
            check=CheckBox(group=".".join(categories))
            check.bind(on_release=self.happening)
            self.stored.append(check)
            temp.add_widget(Label(text=n))
            temp.add_widget(self.stored[-1])
            self.add_widget(temp)
    def happening(self, df=None):
        for n in range(len(self.stored)):
            if self.stored[n].active:
                self.final = self.categories[n]
    def get_value(self):
        return self.final

    def load_value(self, cat):
        try:
            assert len(cat)>0
            self.stored[self.categories.index(cat)].active=True
            #for n in range(len(self.stored)):
                #if self.stored[n].active:
                #    self.final = self.categories[n]
        except:
            self.final=""
    def clear_final(self):
        self.final=""
        for n in range(len(self.stored)):
            self.stored[n].active=False

class LogCat(CheckBox):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.final=""
    def on_state(self, widget, value):
        self.final=str(int(self.active))
    def get_value(self):
        return self.final
    def load_value(self, value):
        try:
            assert len(value)>0
            self.active=bool(int(value))
            #self.final=bool(int(value))
        except:
            self.final=""
    def clear_final(self):
        self.final=""
        self.active=False

class TxtFil(TextInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.loaded=False
        self.multiline=False
    def check_entry(self, entry):
        if not self.loaded:
            return True
        if len(self.text)<=0:
            return True
        try:
            if self.text==entry:
                return True
            else:
                return False
        except:
            return True
    def is_valid(self, filter=None):
        if filter==None:
            filter = self.text
        if len(filter)<=0:
            return False
        return True

    def load_filter(self,filter):
        if len(filter)>0 and self.is_valid(filter):
            self.text=filter
            self.loaded=True
        else:
            self.loaded=False
    def clean(self):
        self.text=""
        self.loaded=False
    def get_filter(self):
        
        if self.loaded:
            return self.text
        else:
            if self.is_valid():
                self.loaded=True
                return self.text
            else:
                return ""
    #def insert_text(self, substring, from_undo=False):
    #    return super(YYYYInput, self).insert_text(substring, from_undo=from_undo)

class LogFil(CheckBox):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.loaded=False

    def is_valid(self,filter=None):
        if filter == None:
            filter=str(int(self.active))
        try:
            assert int(filter)==0 or int(filter)==1
            return True
        except:
            return False

    def load_filter(self,filter):
        if len(filter)>0 and self.is_valid(filter):
            self.active=bool(int(filter))
            self.loaded=True
    def _on_state(self, instance, value):
        self.loaded=True
        return super()._on_state(instance, value)

    def check_entry(self, entry):
        #print("loaded", str(self.loaded))
        if not self.loaded:
            return True
        if len(entry)<=0:
            return False
        try:
            assert self.is_valid(entry)
            
            if str(int(self.active))==entry:
                return True
            else:
                return False
        except:
            return True
    def clean(self):
        self.active=False
        self.loaded=False
    def get_filter(self):
        #self.is_valid()
        if self.loaded:
            return str(int(self.active))
        else:
            return ""
class CatFil(GridLayout):
    def __init__(self,categories, **kwargs):
        super().__init__(**kwargs)
        self.categories=categories
        self.rows=1
        self.cols=len(categories)
        self.stored=[]
        self.loaded=False
        for n in categories:
            temp=GridLayout(rows=2, cols=1)
            check=CheckBox(group=".".join(categories))
            #check.bind(on_release=self.happening)
            self.stored.append(check)
            temp.add_widget(Label(text=n))
            temp.add_widget(self.stored[-1])
            self.add_widget(temp)

    def is_valid(self,filter=None):
        if filter==None:
            for n in range(len(self.categories)):
                if self.stored[n].active:
                    filter=self.categories[n]
        if filter==None:
            return False


        if len(filter)<=0:
            return False
        if filter in self.categories:
            return True
        else:
            return False

    def load_filter(self, filter):
        if len(filter)>0 and self.is_valid(filter):
            self.stored[self.categories.index(filter)].active=True

    def check_entry(self, entry):
        if not self.loaded:
            return True
        if True not in [n.active for n in self.stored]:
            return True
        if len(entry)<=0:
            return False
        try:
            assert self.is_valid(entry)
            for n in range(len(self.categories)):
                if self.stored[n].active:
                    temp=self.categories[n]
            if temp==entry:
                return True
            else:
                return False
        except:
            return True
    def clean(self):
        for n in range(len(self.categories)):
            self.stored[n].active=False
        self.loaded=False
    def get_filter(self):
        #self.is_valid()
        if self.loaded:
            for n in range(len(self.categories)):
                if self.stored[n].active:
                    return self.categories[n]
        else:
            if self.is_valid():
                self.loaded=True
                for n in range(len(self.categories)):
                    if self.stored[n].active:
                        return self.categories[n]
            else:
                return ""

class NumFil(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.rows=1
        self.cols=4
        self.stored=[]
        self.stored.append(TextInput(multiline=False, input_filter="int"))
        self.add_widget(Label(text="min"))
        self.add_widget(self.stored[-1])
        self.stored.append(TextInput(multiline=False, input_filter="int"))
        self.add_widget(Label(text="max"))
        self.add_widget(self.stored[-1])
        self.loaded=False

    def is_valid(self, filter=None):
        if filter == None:
            filter=";".join([self.stored[0].text,self.stored[1].text])
        if len(filter)<=1 or ";" not in filter:
            return False
        if filter.count(";")!=1:
            return False
        mmin,mmax=filter.split(";")
        try:
            mmin=int(mmin)
        except:
            if len(mmin)!=0:
                return False
        try:
            mmax=int(mmax)
        except:
            if len(mmax)!=0:
                return False
        if type(mmin)!=int and type(mmax)!=int:
            return False
        if type(mmin)==int and type(mmax)==int:
            if mmax<=mmin:
                return False
        return True
    def load_filter(self, filter):
        if len(filter)>0 and self.is_valid(filter):
            self.stored[0].text=filter.split(";")[0]
            self.stored[1].text=filter.split(";")[1]
            self.loaded=True
    def check_entry(self,entry):
        if not self.loaded:
            return True
        if len(self.stored[0].text)==0 and len(self.stored[1].text)==0:
            return True
        if len(entry)<=0:
            return False
        try:
            entry=int(entry)
            mmin=self.stored[0].text
            try:
                mmin=int(mmin)
            except:
                pass
            mmax=self.stored[1].text
            try:
                mmax=int(mmax)
            except:
                pass
            if type(mmin)==int and type(mmax)!=int:
                if entry>=mmin:
                    return True
                return False
            elif type(mmin)==int and type(mmax)==int:
                if mmin<=entry<mmax:
                    return True
                return False
            elif type(mmin)!=int and type(mmax)==int:
                if entry<mmax:
                    return True
                return False

        except:
            return True
    def clean(self):
        self.stored[0].text=""
        self.stored[1].text=""
        self.loaded=False
    def get_filter(self):
        #self.is_valid()
        if self.loaded:
            if len(self.stored[0].text)==0 and len(self.stored[1].text)==0:
                return ""
            return ";".join([self.stored[0].text,self.stored[1].text])
        else:
            if self.is_valid():
                self.loaded=True
                return ";".join([self.stored[0].text,self.stored[1].text])
            else:
                return ""

class Screen2(Screen):
    def __init__(self, config_list, **kwargs):
        super(Screen2, self).__init__(**kwargs)
        self.config_list=config_list
        try:
            self.config_list[3][4]
        except:
            self.config_list[3].append([])
        self.layout = FloatLayout()
        #self.layout.add_widget(Label(pos_hint={'center_x':0.5, 'center_y':0.9}, text='Berry Analyzer Camera - Desarrollado por Programa de Mejoramiento de Vides\nINIA La Platina, 2019', color=[1,1,1,0.65]))

        self.main_grid=GridLayout(cols=1, rows=5, size_hint=(1,0.7), pos_hint={'center_x':0.5, 'center_y':0.6})
        self.layout.add_widget(self.main_grid)

        self.buttons_grid=GridLayout(cols=4, rows=1, size_hint=(1,0.2), pos_hint={'center_x':0.5, 'center_y':0.1})
        
        self.layout.add_widget(self.buttons_grid)

        self.toggle=ToggleButton(text="Filters: OFF", on_release=self.toggle_filters)

        self.filter_buttons=GridLayout(rows=1, cols=4,size_hint=(1,0.2), pos_hint={'center_x':0.5, 'center_y':0.1})
        self.filter_buttons.add_widget(Button(text="Apply", on_release=self.apply_filter))
        self.filter_buttons.add_widget(self.toggle)
        self.filter_buttons.add_widget(Button(text="Clear", on_release=self.apply_filter))
        self.filter_buttons.add_widget(Button(text="Back", on_release=self.apply_filter))
        
        self.filter_toggle=False

        self.buttons_grid.add_widget(Button(text="Back", on_release=self.back))
        self.buttons_grid.add_widget(Button(text="Filter", on_release=self.show_filters))
        
        self.buttons_grid.add_widget(Button(text="<", on_release=self.list_explore))
        self.buttons_grid.add_widget(Button(text=">", on_release=self.list_explore))
        
        self.filter_to_change=[]
        self.filter_layout = FloatLayout()

        self.filter_grid=GridLayout(cols=1, rows=1, size_hint_y=None, spacing=5)
        self.filter_grid.bind(minimum_height=self.filter_grid.setter('height'))
        self.filter_scroll=ScrollView(do_scroll_x=False, size_hint=(1, None), size=(Window.width, Window.height))

        self.plant_to_change=[]
        self.plant_layout=FloatLayout()

        self.plant_grid=GridLayout(cols=1, rows=1, size_hint_y=None, spacing=5)
        self.plant_grid.bind(minimum_height=self.plant_grid.setter('height'))
        self.page_scroll = ScrollView(do_scroll_x=False, size_hint=(1, None), size=(Window.width, Window.height))
        

        self.add_widget(self.layout)

        self.on_enter=self.from_zero

    def load_ps(self):
        filess=open("./local_data/local.csv", 'r')
        txt=filess.read()
        filess.close()
        return [n.split(',') for n in txt.split('\n') if len(n) > 0]

    def from_zero(self, dt=None):
        #self.filtered=self.load_ps()

        self.list_index=0
        self.direction=1

        
        
        self.page_scroll.clear_widgets()
        self.plant_grid.clear_widgets()

        for n in list(range(len(self.plant_to_change)))[::-1]:
            del(self.plant_to_change[n])

        self.plant_grid.rows=1
        self.plant_to_change=[]
        for n in range(len(self.config_list[3][0])):

            try:
                self.config_list[3][1][n]
            except:
                self.plant_to_change.append(None)
                continue
            if self.config_list[3][1][n]=="x":
                if self.config_list[3][2][n]=="txt":
                    self.plant_to_change.append(TxtCat(size_hint_y=None, height=int(Window.height*0.2)))

                    self.plant_grid.rows=self.plant_grid.rows+2

                    self.plant_grid.add_widget(Label(text=self.config_list[3][0][n],size_hint_y=None, height=int(Window.height*0.2)))
                    self.plant_grid.add_widget(self.plant_to_change[-1])
                elif self.config_list[3][2][n]=="log":
                    self.plant_to_change.append(LogCat(size_hint_y=None, height=int(Window.height*0.2)))

                    self.plant_grid.rows=self.plant_grid.rows+2

                    self.plant_grid.add_widget(Label(text=self.config_list[3][0][n],size_hint_y=None, height=int(Window.height*0.2)))
                    self.plant_grid.add_widget(self.plant_to_change[-1])
                elif self.config_list[3][2][n]=="cat":
                    try:
                        assert len(self.config_list[3][3][n])!=0
                        self.config_list[3][3][n].split(";")
                    except:
                        self.plant_to_change.append(None)
                        continue

                    self.plant_grid.rows=self.plant_grid.rows+2

                    self.plant_to_change.append(CatCat(categories=self.config_list[3][3][n].split(";"),size_hint_y=None, height=int(Window.height*0.2)))
                    self.plant_grid.add_widget(Label(text=self.config_list[3][0][n],size_hint_y=None, height=int(Window.height*0.2)))
                    self.plant_grid.add_widget(self.plant_to_change[-1])
                    pass
                elif self.config_list[3][2][n]=="num":
                    self.plant_to_change.append(NumCat(size_hint_y=None, height=int(Window.height*0.2)))

                    self.plant_grid.rows=self.plant_grid.rows+2

                    self.plant_grid.add_widget(Label(text=self.config_list[3][0][n],size_hint_y=None, height=int(Window.height*0.2)))
                    self.plant_grid.add_widget(self.plant_to_change[-1])
                elif self.config_list[3][2][n]=="dat":
                    self.plant_to_change.append(DatCat(size_hint_y=None, height=int(Window.height*0.2)))

                    self.plant_grid.rows=self.plant_grid.rows+2

                    self.plant_grid.add_widget(Label(text=self.config_list[3][0][n],size_hint_y=None, height=int(Window.height*0.2)))
                    self.plant_grid.add_widget(self.plant_to_change[-1])
            else:
                self.plant_to_change.append(None)

        self.plant_grid.rows=self.plant_grid.rows+2

        self.plant_grid.add_widget(Label(text=" ", size_hint_y=None, height=int(Window.height*0.2)))
        self.plant_grid.add_widget(Label(text=" ", size_hint_y=None, height=int(Window.height*0.2)))
        

        self.page_scroll.add_widget(self.plant_grid)

        self.from_filter()

        self.load_list()

    def from_filter(self):
        self.toggle.state="normal"
        self.toggle_filters()
        self.filter_scroll.clear_widgets()
        self.filter_grid.clear_widgets()

        for n in list(range(len(self.filter_to_change)))[::-1]:
            del(self.filter_to_change[n])

        self.filter_grid.rows=1
        self.filter_to_change=[]

        for n in range(len(self.config_list[3][0])):
            try:
                assert len(self.config_list[3][2][n])==3
            except:
                self.filter_to_change.append(None)
                continue
            if self.config_list[3][2][n]=="txt":
                self.filter_to_change.append(TxtFil(size_hint_y=None, height=int(Window.height*0.2)))
                self.filter_grid.rows=self.filter_grid.rows+2
                self.filter_grid.add_widget(Label(text=self.config_list[3][0][n],size_hint_y=None, height=int(Window.height*0.2)))
                self.filter_grid.add_widget(self.filter_to_change[-1])
            elif self.config_list[3][2][n]=="log":
                self.filter_to_change.append(LogFil(size_hint_y=None, height=int(Window.height*0.2)))
                self.filter_grid.rows=self.filter_grid.rows+2
                self.filter_grid.add_widget(Label(text=self.config_list[3][0][n],size_hint_y=None, height=int(Window.height*0.2)))
                self.filter_grid.add_widget(self.filter_to_change[-1])
            elif self.config_list[3][2][n]=="num":
                self.filter_to_change.append(NumFil(size_hint_y=None, height=int(Window.height*0.2)))
                self.filter_grid.rows=self.filter_grid.rows+2
                self.filter_grid.add_widget(Label(text=self.config_list[3][0][n],size_hint_y=None, height=int(Window.height*0.2)))
                self.filter_grid.add_widget(self.filter_to_change[-1])
            elif self.config_list[3][2][n]=="cat":
                try:
                    assert len(self.config_list[3][3][n])!=0
                    self.config_list[3][3][n].split(";")
                except:
                    self.filter_to_change.append(None)
                    continue
                self.filter_to_change.append(CatFil(categories=self.config_list[3][3][n].split(";"),size_hint_y=None, height=int(Window.height*0.2)))
                self.filter_grid.rows=self.filter_grid.rows+2
                self.filter_grid.add_widget(Label(text=self.config_list[3][0][n],size_hint_y=None, height=int(Window.height*0.2)))
                self.filter_grid.add_widget(self.filter_to_change[-1])
            else:
                self.filter_to_change.append(None)

        self.filter_grid.rows=self.filter_grid.rows+2

        self.filter_grid.add_widget(Label(text=" ", size_hint_y=None, height=int(Window.height*0.2)))
        self.filter_grid.add_widget(Label(text=" ", size_hint_y=None, height=int(Window.height*0.2)))
        

        self.filter_scroll.add_widget(self.filter_grid)

    def list_explore(self, dt=None):
        if dt.text==">":
                self.direction=1
        elif dt.text=="<":
                self.direction=-1
        self.load_list()

    def check_filter(self,entry):
        if self.toggle.state =="normal":
            return True
        for n in range(len(entry)):
            #print(entry[n], end=" ")
            if self.filter_to_change[n] == None:
                #print("None")
                continue
            
            if not self.filter_to_change[n].check_entry(entry[n]):
                #print(False)
                return False
            #print(True)
        return True       

    def load_list(self):
        self.main_grid.clear_widgets()
        counter=0
        found=[]
        while counter<5:
            if 1<=self.list_index+self.direction<len(self.config_list[1]):
                self.list_index+=self.direction
                #sleep(0.2)
                if self.check_filter(entry=self.config_list[1][self.list_index]):
                    temp=[]
                    for s in range(len(self.config_list[3][1])):
                        if self.config_list[3][1][s]=="s":
                            temp.append(self.config_list[1][self.list_index][s])
                    temp=".".join(temp)
                    found.append("\n".join([temp,self.config_list[1][self.list_index][0]]))
                    #self.main_grid.add_widget(Button(text="\n".join([temp,self.config_list[1][self.list_index][0]]), on_release=self.open_plant, background_normal="", background_color=[0,0,0,0]))
                    counter+=1
                    #print("found")
            else:
                break
        if self.direction<0:
            found=found[::-1]
        for n in found:
            self.main_grid.add_widget(Button(text=n, on_release=self.open_plant, background_normal="", background_color=[0,0,0,1]))
            
    def show_filters(self, dt=None):
        while len(self.config_list[3][4])<len(self.config_list[3][0]):
            self.config_list[3][4].append("")
        for n in range(len(self.config_list[3][0])):
            if self.filter_to_change[n]==None:
                continue
            self.filter_to_change[n].load_filter(self.config_list[3][4][n])
        self.clear_widgets()
        self.add_widget(self.filter_scroll)

        
        self.add_widget(self.filter_buttons)
        
    def toggle_filters(self,dt=None):
        if self.toggle.state=="down":
            self.toggle.text="Filter: ON"
        else:
            self.toggle.text="Filter: OFF"

    def open_plant(self, dt=None):
        number=0
        
        for n in range(len(self.config_list[1])):
            if self.config_list[1][n][0]==dt.text.split("\n")[1]:
                number=n
                break
        counter=0
        self.current_plant=number

        for n in range(len(self.config_list[3][0])):
            if self.plant_to_change[n]==None:
                continue
            try:
                self.config_list[1][number][n]
            except:
                continue
            self.plant_to_change[n].clear_final()
            self.plant_to_change[n].load_value(self.config_list[1][number][n])

        self.clear_widgets()
        self.add_widget(self.page_scroll)

        grid=GridLayout(rows=1, cols=2,size_hint=(1,0.2), pos_hint={'center_x':0.5, 'center_y':0.1})
        grid.add_widget(Button(text="Save", on_release=self.save_data))
        grid.add_widget(Button(text="Back", on_release=self.save_data))
        self.add_widget(grid)

    def save_data(self, dt=None):
        if dt.text=="Save":
            self.filtered=[]

            for n in range(len(self.config_list[3][0])):
                if n == 0:
                    self.filtered.append(self.config_list[1][self.current_plant][n])
                    continue
                if self.plant_to_change[n]==None:

                    self.filtered.append("")
                else:
                    
                    #if self.config_list[1][self.current_plant][n]!=self.plant_to_change[n].get_value() and self.config_list[1][self.current_plant][n]!="":
                    if self.config_list[1][self.current_plant][n]!=self.plant_to_change[n].get_value():
                        self.config_list[1][self.current_plant][n]=self.plant_to_change[n].get_value()
                        self.filtered.append(self.plant_to_change[n].get_value())
                    else:
                        self.filtered.append("")

            self.save_local()
        self.clear_widgets()
        self.add_widget(self.layout)

        pass
    
    def save_local(self):
        #remove("./local_data/"+listdir("./local_data")[0])
        filess = open("./local_data/local.csv", "a")
        filess.write(",".join(self.filtered)+"\n")
        filess.close()
    
    def back(self, dt=None):
        self.manager.current = 'external'

    def apply_filter(self, dt=None):
        #print(self.config_list[3])
        if dt.text=="Apply":
            
            self.toggle.state="down"
            self.toggle_filters()
            while len(self.config_list[3][4])<len(self.config_list[3][0]):
                self.config_list[3][4].append("")
            for n in range(len(self.config_list[3][0])):
                if self.filter_to_change[n]==None:
                    continue
                self.config_list[3][4][n]=self.filter_to_change[n].get_filter()
            self.list_index=0
            self.direction=1
            self.load_list()
        elif dt.text=="Clear":
            self.toggle.state="normal"
            self.toggle_filters()
            while len(self.config_list[3][4])<len(self.config_list[3][0]):
                self.config_list[3][4].append("")
            for n in range(len(self.config_list[3][0])):
                if self.filter_to_change[n]==None:
                    continue
                self.config_list[3][4][n]=self.filter_to_change[n].clean()
                self.config_list[3][4][n]=self.filter_to_change[n].get_filter()
            self.list_index=0
            self.direction=1
            self.load_list()
        else:
            pass
        print("filters",self.config_list[3][4])
        self.clear_widgets()
        self.add_widget(self.layout)

