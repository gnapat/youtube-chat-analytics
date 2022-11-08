# -- coding: utf-8 --
import PySimpleGUI as sg



use_custom_titlebar = False

def make_window(theme=None):

    NAME_SIZE = 5
    dblist=["local","Mongodb"]
    chlist =["เรื่องเล่าเช้านี้","สถานีข่าว"]
    def name(name):
        dots = NAME_SIZE-len(name)-2
        return sg.Text(name, size=(len(name)+1,1), justification='l',pad=(0,0), font='Loma 10')

    font = ("Norasi", 11)
    layout_l = [[name('Channel'), sg.Combo(chlist, default_value=chlist[0], s=(15,50), enable_events=False, readonly=True,font=font)],
                [sg.Text('EP_INFO')],[sg.Multiline(size=(35, 50))]]


    layout_r = [[name('Text Right'), sg.Text('Text')]]

    layout_main=[[sg.T('Youtube Chat Analye', font='Norasi 18', justification='c', expand_x=True)],
                [[name('Database:'), sg.Combo(dblist, default_value=dblist[0], s=(15,30), enable_events=False, readonly=True)]],
                [sg.Button('Connect'), sg.Button('Disconnect')],
                [sg.Col(layout_l), sg.Col(layout_r)]]


    window = sg.Window('YouTube Chat Simple Analytic', layout_main, finalize=True, \
        right_click_menu=sg.MENU_RIGHT_CLICK_EDITME_VER_EXIT, keep_on_top=True, use_custom_titlebar=use_custom_titlebar)
    


    return window


def main():

    sg.theme('TanBlue')
    window = make_window()

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED or event == 'Exit':
            break

        elif event == "Connect":
            print("Connect")
        elif event == "Disconnect":
            print("Disconnect")

        
    print("Hello World!")

if __name__ == "__main__":
    main()