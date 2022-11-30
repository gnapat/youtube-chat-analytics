# -- coding: utf-8 --
import PySimpleGUI as sg
import sys

from matplotlib.ticker import NullFormatter  # useful for `logit` scale
#import matplotlib.pyplot as plt
from matplotlib import pyplot as plt, dates
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
from datetime import datetime, timedelta

sys.path.insert(0, 'src/include/')

from ychat_db  import ychatdb
from config import ychat_config as yconf
import pandas as pd


NUMOFPLOT = 1

use_custom_titlebar = False

class AppSystem:

    def __init__(self) -> None:
        #self.yc = yconf("C:\\Users\\LEGION\\work\\project\\nida\\youtube-chat-analytics\\src\\testing\\config.conf")
        self.yc = yconf("src\\config.conf")
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
    fig, axs = plt.subplots(NUMOFPLOT, 1, figsize=(6, 6), constrained_layout=True)

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

def MessageBoxError(topic,message):
    #sg.popup('Go button clicked', 'Input value:', self.values['-IN-'])
    #sg.popup(topic, message)
    sg.popup_error(topic,message,keep_on_top=True)

def MessageBoxInfo(topic,message):
    #sg.popup('Go button clicked', 'Input value:', self.values['-IN-'])
    #sg.popup(topic, message)
    sg.popup_ok(topic,message,keep_on_top=True)
def MessageBoxWarn(topic,message):
    #sg.popup('Go button clicked', 'Input value:', self.values['-IN-'])
    #sg.popup(topic, message)
    sg.popup_notify(topic,message,keep_on_top=True)


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


    layout_l = [[sg.T('YouTube Live Chat Viewer', font='Norasi 18', justification='c', expand_x=True)],
                [name('Database:'), sg.Combo(dblist, default_value=dblist[0], s=(25,30), enable_events=False, readonly=True, k='-DBCOMBO-')],
                [sg.Button('Connect'), sg.Button('Disconnect')],
                [name('Channel'), sg.Combo(chlist, default_value=[], s=(15,40), enable_events=True, readonly=True,font=font,k='-CHCOMBO-'),sg.Text(size=20,k='-CHCODE-')],
                [sg.T('Program', font='Norasi 12', justification='l', expand_x=True)],
                [sg.Listbox([], no_scrollbar=True,  s=(50,15),k='-EP_LIST-')],
                [sg.T('Program Manager', font='Norasi 12', justification='l', expand_x=True)],
                [sg.Button('Get Program'),sg.Button('Rename Program'),sg.Button('Delete Program')],
                [sg.Input(k='-Program-',s=50)], 
                [sg.T('Channel Manager', font='Norasi 12', justification='l', expand_x=True)],
                [sg.Button('Add New Channel'),sg.Button('Remove Channel')],
                [name('Channel Code'),sg.Input(k='-AddChCode-',s=20)],
                [name('Channel Name'),sg.Input(k='-AddChName-',s=35)],
                [sg.T('Clone Program', font='Norasi 12', justification='l', expand_x=True)],
                [name('Clone to:'),sg.Combo(dblist, default_value=dblist[0], s=(25,30), enable_events=False, readonly=True, k='-CLONEDBCOMBO-'),sg.Button('Submit Clone')] ]
    layout_c=[[sg.Button('Apply')], [sg.Button('Clean')]]

    #layout_r = [[sg.T('Display', font='Norasi 12', justification='c', expand_x=True)] ,[sg.Canvas(key='-PLOT01-')]]
    layout_r = [[sg.Canvas(key='-PLOT01-')]]
    
    layout_main=[[sg.Col(layout_l),sg.Col(layout_c), sg.Col(layout_r)]]
    
    window = sg.Window('YouTube Live Chat Viewer', layout_main, finalize=True, \
        right_click_menu=sg.MENU_RIGHT_CLICK_EDITME_VER_EXIT, keep_on_top=True, use_custom_titlebar=use_custom_titlebar)
    


    return window

def ToVirtualize(client,ch,ep):
    print(f"{ch}  {ep}")
    re = client.getChByTitleTh(ch,ep)
    a=[]; b=[]
    hh=0; mm=0
    cc = 0
    for i in re:
        t=i['datetime']

        if cc ==0:
            hh=int(t[11:13]); mm=int(t[14:16])

        a.append([datetime.strptime(t,'%Y-%m-%d %H:%M:%S'),1])
        b.append([datetime.strptime(t,'%Y-%m-%d %H:%M:%S'),i['aname']])

        cc += 1
            
    df_user_count = pd.DataFrame({'timeplay': np.array([i - timedelta(hours=hh,minutes=mm)  for i,j in a]),
                                'user': np.array([j for i,j in a])})
    plt.rcParams['font.family'] = 'Tahoma'
    try:
        group_user_count = df_user_count.groupby(pd.Grouper(key='timeplay', axis=0, freq='1min')).sum()
        mean_per_min = group_user_count['user'].mean()
        sum = group_user_count['user'].sum()

    except Exception as e:
        print('Error Group By Dataframe', e)
                
        fig, axs = plt.subplots(NUMOFPLOT, 1, figsize=(8, 6), constrained_layout=True)
        axs.set_title("")
        axs.grid()
        #figure_agg = draw_figure(window['-PLOT01-'].TKCanvas, fig)
        MessageBoxError("Data Error","Sorry, Program found some data error!!")
        return(fig)
    else:
        fig, axs = plt.subplots(NUMOFPLOT, 1, figsize=(8, 6), constrained_layout=True)
        axs.plot(group_user_count)
        axs.xaxis.set_major_formatter(dates.DateFormatter('%H:%M'))
        detail="avg = %0.2f message/minute, total = %d" %(mean_per_min,sum)
        axs.legend([detail], loc='upper center')
        axs.set_xlabel('time (Hour)')
        axs.set_ylabel('messages per minute')
        axs.xaxis.set_tick_params(rotation=10, labelsize=10)
        axs.set_title(ep)
        axs.grid()

        return(fig)
    #figure_agg =draw_figure(window['-PLOT01-'].TKCanvas, fig)

def UpdateValueOnDisplay(client,window):

    al=[]
    at = client.getChList()
    for  i in at:
        al.append(i['title_th'])

        window['-CHCOMBO-'].update(values=al, value='',set_to_index=0)

        re = client.getChCodeByTitleTh(al[0])
        eplist=[]
        for irec in re:
            eplist.append(irec['title_th'])
        
        #if eplist != []:
        window['-EP_LIST-'].update(values=eplist,set_to_index=0)
        window['-Program-'].update(value="")
        try:
            chcode="code: %s" %(client.getCodeByTitleTh(al[0]))
            window['-CHCODE-'].update(value=chcode)
        except Exception as e:
            pass
        



def main():
    global App

 
    sg.theme('TanBlue')
    App = AppSystem()
    window = make_window()

    fig, axs = plt.subplots(NUMOFPLOT, 1, figsize=(8, 6), constrained_layout=True)
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
            #print(dbc)
            

            try:
                dbconf={"host":dbc['host'],"database":dbc['database']}

            except Exception as e:
                MessageBoxError("Database fail,", "Please try again!!")
                continue
            else:
                pass

            print("Connect %s %s" %(values['-DBCOMBO-'], dbc['host']))
            client = ychatdb(dbconf)

            UpdateValueOnDisplay(client,window)

            ''''
            al=[]
            at = client.getChList()
            for  i in at:
                al.append(i['title_th'])

            window['-CHCOMBO-'].update(values=al, value='',set_to_index=0)

            re = client.getChCodeByTitleTh(al[0])
            eplist=[]
            for i in re:
                eplist.append(i['title_th'])

            window['-EP_LIST-'].update(values=eplist,set_to_index=0)
            '''

        elif event == "Disconnect":
            print("Disconnect")


        elif event == "Apply":
            ch = values['-CHCOMBO-']
            ep = values['-EP_LIST-']
            
            delete_figure_agg(figure_agg)
            fig = ToVirtualize(client,ch,ep)

            figure_agg = draw_figure(window['-PLOT01-'].TKCanvas, fig)


        elif event == "Clean":
            print("Clean Board")
        elif event == "-DBCOMBO-":
            print("-DBCOMBO-")

        elif event == "-CHCOMBO-":

            re = client.getChCodeByTitleTh(values['-CHCOMBO-'])
            eplist=[]
            for i in re:
                eplist.append(i['title_th'])

            window['-EP_LIST-'].update(values=eplist,set_to_index=0)
            try:
                #chcode="code: %s" %(i['code'])
                chcode="code: %s" %(client.getCodeByTitleTh(values['-CHCOMBO-']))
                print(chcode)
                window['-CHCODE-'].update(value=chcode)
            except Exception as e:
                pass
            

            #window['-Rename-'].update(value=values['-EP_LIST-'])
        elif event == "-EP_LIST-":
            print("-------------")
        elif event == "Rename Program":
            new_progm = values['-Program-']
            curr_progm = values['-EP_LIST-'][0]
            ch = values['-CHCOMBO-']

            if (len(new_progm)>0):
                client.renameProgram(ch,curr_progm,new_progm)
                UpdateValueOnDisplay(client,window)
            else:
                MessageBoxError("Rename","Please enter new program name.")
            
            #print(f"{values['-Program-']}")
        elif event == "Delete Program":
            curr_progm = values['-EP_LIST-'][0]
            ch = values['-CHCOMBO-']
            client.deleteProgram(ch,curr_progm)
            UpdateValueOnDisplay(client,window)
            strbuff = f"Delete {curr_progm}, done"
            MessageBoxInfo("Delete Program",strbuff)
            #print(curr_progm)

        elif event == "Get Program":
            window['-Program-'].update(value=values['-EP_LIST-'][0])
            
        elif event == "Add New Channel":
            #[name('Channel Code'),sg.Input(k='-AddChCode-',s=20)],
            #[name('Channel Name'),sg.Input(k='-AddChName-',s=35)] ]
            chcode = values['-AddChCode-']
            chname = values['-AddChName-']
            #print(f"- {chcode}={len(chcode)} {chname}={len(chname)} -")

            if (len(chcode)>0) and (len(chname)):
                print("OK-----------")
                
                ret = client.addNewChannel(chcode,chname)
                if ret <0:
                    MessageBoxError("New Channel","This code is exist!!")
                else:

                    MessageBoxInfo("New Channel","Add new channel Success.")
                    UpdateValueOnDisplay(client,window)


            else:
                MessageBoxError("New Channel","Please enter complete information.")
        
        elif event == "Remove Channel":

            chcode = values['-AddChCode-']


            if (len(chcode)>0):
                ret = client.removeChannel(chcode)
                if ret >0:
                    MessageBoxInfo("New Channel","Remove Success")
                    UpdateValueOnDisplay(client,window)
                else:

                    MessageBoxError("New Channel","Not found channel")


            else:
                MessageBoxError("New Channel","Please enter complete information.")

        elif event == "Submit Clone":
            ch = values['-CHCOMBO-']
            progm = values['-EP_LIST-']
            db_des = values['-CLONEDBCOMBO-']
            db_cur = values['-DBCOMBO-']
            
            if db_des == db_cur:
                MessageBoxInfo("Submit Clone","Can't clone to same database.")
            else:
                print("Go.")
                dbl = App.getDblist()
                dbc = dbl[values['-CLONEDBCOMBO-']]
                dbc_dest={"host":dbc['host'],"database":dbc['database']}
           
                client_dest = ychatdb(dbc_dest)
                retAllMsg = client.getChByTitleTh(ch,progm)
                
                
                chcode_curr = client.getCodeByCh(ch)
                client_dest.addNewChannel(chcode_curr,ch)
                client_dest.putMsg(chcode_curr,ch,progm,retAllMsg)

                MessageBoxInfo("Submit Clone","Success")
                #print(chcode_curr)
                #ret = client_dest.addNewChannel(chcode_curr,ch)
                #if ret >0:
                #    print("Add new")
                
        
    print("Hello World!")

if __name__ == "__main__":
    main()