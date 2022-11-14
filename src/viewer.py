# -- coding: utf-8 --
import PySimpleGUI as sg
import sys

from matplotlib.ticker import NullFormatter  # useful for `logit` scale
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
from datetime import datetime

sys.path.insert(0, 'src/include/')

from ychat_db  import ychatdb
from config import ychat_config as yconf
import pandas as pd




use_custom_titlebar = False

class AppSystem:

    def __init__(self) -> None:
        self.yc = yconf("C:\\Users\\LEGION\\work\\project\\nida\\youtube-chat-analytics\\src\\testing\\config.conf")
        self.dblist = self.yc.getconfig()


        pass

    def getDblist(self):
        return(self.dblist)

def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg

def draw_clear(window):
    fig, axs = plt.subplots(2, 1, figsize=(6, 6), constrained_layout=True)

    axs[0].set_title("NONE")

    draw_figure(window['-PLOT01-'].TKCanvas, fig)

#def draw_view(canvas, figure):

def delete_figure_agg(figure_agg):
    figure_agg.get_tk_widget().forget()
    try:
        draw_figure.canvas_packed.pop(figure_agg.get_tk_widget())
    except Exception as e:
        print(f'Error removing {figure_agg} from list', e)
    plt.close('all')

def MessageBox(topic,message):
    #sg.popup('Go button clicked', 'Input value:', self.values['-IN-'])
    sg.popup(topic, message)


def make_window(theme=None):
    global App
    NAME_SIZE = 5
    
    aa = App.getDblist()
    dblist=[]

    # Load Database list.
    cc=0
    for i in aa:
        if cc == 0:
            dblist=[i]
        else:
            dblist.append(i)

        cc+=1


    chlist =[]
    def name(name):
        dots = NAME_SIZE-len(name)-2
        return sg.Text(name, size=(len(name)+1,1), justification='l',pad=(0,0), font='Loma 10')

    font = ("Norasi", 11)
    layout_l = [[name('Channel'), sg.Combo(chlist, default_value=[], s=(15,40), enable_events=True, readonly=True,font=font,k='-CHCOMBO-')],
                [sg.Listbox([], no_scrollbar=True,  s=(40,30),k='-EP_LIST-')]]

    layout_c=[sg.Button('Apply'), 
                sg.Button('Clean')],
    layout_r = [[name('Channel')] ,[sg.Canvas(key='-PLOT01-')]]

    layout_main=[[sg.T('YouTube Chat Simple Analytics', font='Norasi 18', justification='c', expand_x=True)],
                [[name('Database:'), sg.Combo(dblist, default_value=dblist[0], s=(15,30), enable_events=False, readonly=True, k='-DBCOMBO-')]],
                [sg.Button('Connect'), sg.Button('Disconnect')],
                [sg.Col(layout_l),sg.Col(layout_c), sg.Col(layout_r)]]


    window = sg.Window('YouTube Chat Simple Analytics', layout_main, finalize=True, \
        right_click_menu=sg.MENU_RIGHT_CLICK_EDITME_VER_EXIT, keep_on_top=True, use_custom_titlebar=use_custom_titlebar)
    


    return window


def main():
    global App

 
    sg.theme('TanBlue')
    App = AppSystem()
    window = make_window()

    fig, axs = plt.subplots(1, 1, figsize=(8, 6), constrained_layout=True)
    axs.set_title("")
    figure_agg = draw_figure(window['-PLOT01-'].TKCanvas, fig)

    while True:
        at=[]
        event, values = window.read()

        if event == sg.WIN_CLOSED or event == 'Exit':
            break

        elif event == "Connect":
            dbl = App.getDblist()
            dbc = dbl[values['-DBCOMBO-']]
            print(dbc)
            

            try:
                dbconf={"host":dbc['host'],"database":dbc['database']}

            except Exception as e:
                MessageBox("Database fail,", "Please try again!!")
                continue
            else:
                pass

            print("Connect %s %s" %(values['-DBCOMBO-'], dbc['host']))
            client = ychatdb(dbconf)
            al=[]
            at = client.getChList()
            for  i in at:
                al.append(i['title_th'])

            window['-CHCOMBO-'].update(values=al, value='')

        elif event == "Disconnect":
            print("Disconnect")
        elif event == "Apply":
            ch = values['-CHCOMBO-']
            ep = values['-EP_LIST-']
            
            #client.getChCodeByTitleTh(ep)
            re = client.getChByTitleTh(ch,ep)
            #print(f"Apply  {re['vid']}")
            a=[]
            b=[]
            for i in re:
                t=i['datetime']
                a.append([datetime.strptime(t,'%Y-%m-%d %H:%M:%S'),1])
                b.append([datetime.strptime(t,'%Y-%m-%d %H:%M:%S'),i['aname']])
            
            df_user_count = pd.DataFrame({'timeplay': np.array([i for i,j in a]),
                          'user': np.array([j for i,j in a])})

            #df_user = pd.DataFrame({'timeplay': np.array([i for i,j in b]),
            #              'user': np.array([j for i,j in b])})
                          
            #df_user
            #df_sort_user = df_user.groupby('user',sort=False)['user'].count().sort_values(ascending=False).iloc[0:10] 

            #group_count = np.array([i for i in df_sort_user])
            #group_name = np.array([i for i in df_sort_user.keys()])

            delete_figure_agg(figure_agg)
            plt.rcParams['font.family'] = 'Tahoma'

            
            try:
                group_user_count = df_user_count.groupby(pd.Grouper(key='timeplay', axis=0, freq='1min')).sum()

            except Exception as e:
                print('Error Group By Dataframe', e)
                
                fig, axs = plt.subplots(1, 1, figsize=(8, 6), constrained_layout=True)
                axs.set_title("")
                figure_agg = draw_figure(window['-PLOT01-'].TKCanvas, fig)
                MessageBox("Data Error","Sorry, Program found some data error!!")
            else:
                fig, axs = plt.subplots(1, 1, figsize=(8, 6), constrained_layout=True)
                axs.plot(group_user_count)
                axs.set_xlabel('time (minute)')
                axs.set_ylabel('frequency (minute)')
                axs.set_title(ep)
                figure_agg =draw_figure(window['-PLOT01-'].TKCanvas, fig)
    

        elif event == "Clean":
            print("Clean Board")
        elif event == "-DBCOMBO-":
            print("-DBCOMBO-")

        elif event == "-CHCOMBO-":

            re = client.getChCodeByTitleTh(values['-CHCOMBO-'])
            eplist=[]
            for i in re:
                eplist.append(i['title_th'])

            window['-EP_LIST-'].update(values=eplist)


        
    print("Hello World!")

if __name__ == "__main__":
    main()