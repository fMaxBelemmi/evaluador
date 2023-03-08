#from pathlib import Path
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from kivy.core.window import Window

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
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
from kivy.uix.image import Image
from kivy.logger import Logger
import requests
from numpy import asarray

class Screen1(Screen):
    def __init__(self, config_list, **kwargs):
        super(Screen1, self).__init__(**kwargs)
        self.config_list=config_list

        self.local_copy=[]
        self.local_head=[]
        
        self.layout = FloatLayout()
        self.layout.add_widget(Label(pos_hint={'center_x':0.5, 'center_y':0.9}, text='Field data annotator', color=[1,1,1,0.65]))

        self.main_grid=GridLayout(cols=1, rows=4, size_hint=(0.3,0.3), pos_hint={'center_x':0.5, 'center_y':0.5})
        self.layout.add_widget(self.main_grid)
        self.main_grid.add_widget(Button(text="Explore", on_release=self.change_page))
        self.main_grid.add_widget(Button(text="Sync", on_release=self.check_local))
        self.main_grid.add_widget(Button(text="Erase local data", on_release=self.wipe_warning))
        self.sync_stat=Label(text="Loading...")
        self.main_grid.add_widget(self.sync_stat)

        self.scope = ['https://spreadsheets.google.com/feeds']
        try:
            assert path.isfile(self.config_list[0]+"/app/client_secret.json")
            self.creds = ServiceAccountCredentials.from_json_keyfile_name(self.config_list[0]+'/app/client_secret.json', self.scope)
        except:
            self.creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', self.scope)

        self.warning = FloatLayout()
        self.warning.add_widget(Image(color=[0, 0, 0, 0.7]))
        self.warning_msg = Label(pos_hint={'center_x': 0.5, 'center_y': 0.6}, text='Name already exist. Overwrite?')
        self.warning.add_widget(self.warning_msg)
        self.warning_grid = GridLayout(cols=2, rows=1, pos_hint={'top': 0.8, 'center_x': 0.5}, size_hint=(0.6, 0.1))
        self.warning.add_widget(self.warning_grid)
        self.warning_yes = Button(text='Yes', on_release=self.clear_warning)
        self.warning_grid.add_widget(self.warning_yes)
        self.warning_no = Button(text='No', on_release=self.clear_warning)
        self.warning_grid.add_widget(self.warning_no)

        self.first_run()

    def load_spread(self):
        self.local_copy=[]
        self.local_head=[]
        self.spread_stat="loading"
        try:
            self.client = gspread.authorize(self.creds)
            # self.spreadsheet = self.client.open_by_url('https://docs.google.com/spreadsheets/d/19K0hJHnFIKh2VRMNEZ6sSf2-P9iDg8iZ8zZBYN06gp8/')
            self.spreadsheet = self.client.open_by_url('https://docs.google.com/spreadsheets/d/1P0gWdjtvZlVsWxTz4wyzYYIWj87pJj75CEuL8Wf2moY/')
            # print("################ open client correct")
            self.copy_gs_local()
            ws = self.spreadsheet.worksheet("prop")

            self.local_head = ws.row_values(1)
            cols=ws.row_values(2)
            types=ws.row_values(3)
            cats=ws.row_values(4)
            filt=ws.row_values(5)
            props=[','.join(self.local_head), ','.join(cols),','.join(types),','.join(cats), ','.join(filt)]
            filess = open("./local_data/prop.csv","w")
            filess.write("\n".join(props))

            self.spread_stat="ok"
            return
        except Exception as e:
            # Logger.info("########## {}".format(str(e)))
            self.spread_stat="bad"
            return

    def copy_gs_local(self):
        # response = requests.get('https://docs.google.com/spreadsheet/ccc?key=19K0hJHnFIKh2VRMNEZ6sSf2-P9iDg8iZ8zZBYN06gp8&output=csv')
        response = requests.get('https://docs.google.com/spreadsheet/ccc?key=1P0gWdjtvZlVsWxTz4wyzYYIWj87pJj75CEuL8Wf2moY&output=csv')
        # print("################ copy gs {}".format(response.status_code))
        # Logger.info("########## {}".format(response.status_code))
        assert response.status_code == 200, 'Wrong status code'
        filess = open("./local_data/online.csv", "wb")
        filess.write(response.content)
        filess.close()
        self.local_copy=[n.split(",") for n in response.content.decode("utf-8").split("\r\n")]

    def check_local(self, dt=None):
        # print("################ check_local {}".format(self.spread_stat))
        # Logger.info("########## check_local {}".format(self.spread_stat))
        if "local.csv" not in listdir("./local_data/"):
            if self.spread_stat == "ok":
                filess = open("./local_data/local.csv", "w")
                filess.write(",".join(self.local_head)+'\n')
                filess.close()
                self.sync_stat.text="Sync"
                return
            else:
                self.sync_stat.text="No data"
                return
        else:
            if self.spread_stat == "ok":
                self.sync_to_gs()
                self.sync_stat.text="Sync"
                return
            else:
                self.load_local()
                self.sync_stat.text="Not sync"
                return
        pass

    def load_ps(self):
        filess=open("./local_data/local.csv", 'r')
        txt=filess.read()
        filess.close()
        return [n.split(',') for n in txt.split('\n') if len(n) > 0]

    def load_prop(self):
        filess=open("./local_data/prop.csv", 'r')
        txt=filess.read()
        filess.close()
        return [n.split(',') for n in txt.split('\n')]

    def load_local(self):
        filess=open("./local_data/online.csv", 'r')
        txt=filess.read()
        self.local_copy=[n.split(',') for n in txt.split('\n') if len(n) > 0]
        filess.close()

    def sync_to_gs(self, dt=None):
        if self.spread_stat!="ok":
            self.sync_stat.text="Not sync"
            self.load_spread()
            return
        to_add = self.load_ps()[1:]
        if len(to_add)==0:
            self.sync_stat.text="Sync"
            return
        try:
            ws = self.spreadsheet.worksheet("prop")
            temp = ws.row_values(2)
            col_index=[]
            for n in range(len(temp)):
                if temp[n]=="x":
                    col_index.append(n)
            ws = self.spreadsheet.worksheet("main")
        except:
            self.spread_stat="bad"
            self.sync_stat.text="Not sync"
            return

        cell_list=[]


        for n in to_add: #replace only changed fields
            try:
                cell = ws.find(n[0])
            


                for v in col_index:
                    if len(n[v])==0:
                        continue
                    else:
                        ws.update_cell(cell.row, v+1, n[v])
            except:
                cell_list.append(n)
                continue # what if the id doesn't exist any more?
                    

        remove("./local_data/local.csv")
        filess = open("./local_data/local.csv", "w")
        filess.write('\n'.join([",".join(self.local_head),"\n".join([",".join(n) for n in cell_list])])+'\n')
        filess.close()
        self.copy_gs_local()

    def first_run(self):
        if "local_data" not in listdir("./"):
            mkdir("local_data")
        self.load_spread()
        self.check_local()
        if self.sync_stat.text=="Sync":
            self.add_widget(self.layout)
        elif self.sync_stat.text=="No data":
            self.warning_msg.text="Cannot sync"
            self.warning_yes.text="Retry"
            self.warning_no.text="Retry"
            self.add_widget(self.warning)
        else:
            self.warning_msg.text="Cannot sync"
            self.warning_yes.text="Retry"
            self.warning_no.text="Continue offline"
            self.add_widget(self.warning)

    def wipe_warning(self,dt=None):
        self.remove_widget(self.layout)
        self.warning_msg.text="Erase local data?"
        self.warning_yes.text="Erase"
        self.warning_no.text="Continue"
        self.add_widget(self.warning)

    def clear_warning(self, dt=None):
        if dt.text=='Retry':
            self.try_again()
        elif dt.text=="Continue offline" or dt.text=="Continue":
            self.remove_widget(self.warning)
            self.add_widget(self.layout)
        elif dt.text=="Erase":
            self.wipe_local()
            

    def wipe_local(self):
        self.clear_widgets()
        remove("./local_data/local.csv")
        remove("./local_data/online.csv")
        remove("./local_data/prop.csv")
        self.first_run()

    def try_again(self):
        self.remove_widget(self.warning)
        self.load_spread()
        self.check_local()

        if self.sync_stat.text=="Sync":
            self.add_widget(self.layout)
        elif self.sync_stat.text=="No data":
            self.warning_msg.text="Cannot sync"
            self.warning_yes.text="Retry"
            self.warning_no.text="Retry"
            self.add_widget(self.warning)
        else:
            self.warning_msg.text="Cannot sync"
            self.warning_yes.text="Retry"
            self.warning_no.text="Continue offline"
            self.add_widget(self.warning)

    def change_page(self,dt=None):
        if self.sync_stat.text=="Sync" or self.sync_stat.text=="Not sync":
            self.config_list[1]=self.local_copy
            self.config_list[2]=self.local_head
            self.config_list[3]=self.load_prop()
            self.sync_stat.text="Not sync"
            self.manager.current = 'Explore'