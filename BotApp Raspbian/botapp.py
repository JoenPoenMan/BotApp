import json, pyautogui
import os
from tkinter import *

import Duits.Antwoordvinder as duitsbot
import ReadTheory.ReadTheoryBot as readtheorybot


def read_files():
    with open('config.json') as file:
        content = json.loads(file.read())
    return content['creds'], content['settings']

def update_files(newsettings, newcreds):
    global Settings, creds
    Settings, creds = newsettings, newcreds
    with open('config.json', 'w') as file:
        file.write(json.dumps({"settings":newsettings, "creds":newcreds}))

def scroll():
    global apps, scrollbar, firstpos, oldpos, scrollbarpos, scrollbarenabled
    if scrollbarenabled == True:
        x, y = pyautogui.position()
        if firstpos == None:
            firstpos = y
            oldpos = canvas.coords(scrollbar)[1]
        if oldpos+(y-firstpos) < 0:
            canvas.move(scrollbar, 0, 0-canvas.coords(scrollbar)[1])
        elif (oldpos+(y-firstpos)+(canvas.coords(scrollbar)[3]-canvas.coords(scrollbar)[1])) > 500:
            canvas.move(scrollbar, 0, (500-(canvas.coords(scrollbar)[3]-canvas.coords(scrollbar)[1]))-canvas.coords(scrollbar)[1])
        else:
            canvas.move(scrollbar, 0, (oldpos+(y-firstpos))-canvas.coords(scrollbar)[1])
        
        scrollbarpos = int((canvas.coords(scrollbar)[1]/(500-canvas.coords(scrollbar)[3]+canvas.coords(scrollbar)[1]))*(len(apps)-3)*133)
        i = 0
        for app in apps:
            canvas.move(apps[app][0][0], 0, (i*133+2 - scrollbarpos) - canvas.coords(apps[app][0][0])[1])
            canvas.move(apps[app][0][1], 0, (i*133+40 - scrollbarpos) - canvas.coords(apps[app][0][1])[1])
            canvas.move(apps[app][0][2], 0, (i*133+80 - scrollbarpos) - canvas.coords(apps[app][0][2])[1])
            i += 1

def scrollbeg(*args):
    global scrolling
    scrolling = True

def scrollend(*args):
    global scrolling, firstpos, oldpos
    scrolling = False
    firstpos = None
    oldpos = None

def slide():
    global apps, slider, firstslidepos, oldslidepos, currpos, slideramount, currtriggers
    x, y = pyautogui.position()
    if firstslidepos == None:
        firstslidepos = x
        oldslidepos = canvas.coords(slider)[0]
    new_pos = int(round((oldslidepos+x-firstslidepos-246)/(450/(slideramount-1))))+1
    if new_pos < 1:
        new_pos = 1
    if new_pos > 12:
        new_pos = 12

    int(244+(450/(slideramount-1))*new_pos)
    canvas.move(slider, int(244+(450/(slideramount-1))*(new_pos-1)) - canvas.coords(slider)[0], 0)
    currtriggers['slider'] = new_pos

def slidebeg(event, clicked_app):
    global sliding
    sliding = clicked_app

def slideend(*args):
    global sliding, firstslidepos, oldslidepos
    sliding = False
    firstslidepos = None
    oldslidepos = None

def clickapp(event, clicked_app):
    create_app_layout(clicked_app)

def create_app_layout(clicked_app):
    global apps, currlayout, lastapp
    if not lastapp == clicked_app:
        for item in currlayout:
            canvas.delete(item)
        build_page(apps[clicked_app][3])
        lastapp = clicked_app

def round_rectangle(x1, y1, x2, y2, r=25, **kwargs):    
    points = (x1+r, y1, x1+r, y1, x2-r, y1, x2-r, y1, x2, y1, x2, y1+r, x2, y1+r, x2, y2-r, x2, y2-r, x2, y2, x2-r, y2, x2-r, y2, x1+r, y2, x1+r, y2, x1, y2, x1, y2-r, x1, y2-r, x1, y1+r, x1, y1+r, x1, y1)
    return canvas.create_polygon(points, **kwargs, smooth=True)

def dropdown(*args):
    global dropdowny, dropdownoptions, currdropdownoption, dropdownmenu
    dropdownmenu = []
    i = 0
    for option in dropdownoptions:
        dropdownmenu.append([])
        dropdownmenu[i].append(canvas.create_rectangle(500, dropdowny+(20*(i+1)), 600, dropdowny+(20*(i+2)), fill='#c0c5ce', outline='black'))
        canvas.tag_bind(dropdownmenu[i][-1], "<ButtonPress-1>", lambda event, app=i: click_dropdown(event, app))
        canvas.tag_bind(dropdownmenu[i][-1], "<Enter>", lambda event, app=i: hover_enter(event, app))
        canvas.tag_bind(dropdownmenu[i][-1], "<Leave>", lambda event, app=i: hover_leave(event, app))
        dropdownmenu[i].append(canvas.create_text(550, dropdowny+(20*(i+1))+10, fill='black', font='Times 8 bold', text=option))
        canvas.tag_bind(dropdownmenu[i][-1], "<ButtonPress-1>", lambda event, app=i: click_dropdown(event, app))
        canvas.tag_bind(dropdownmenu[i][-1], "<Enter>", lambda event, app=i: hover_enter(event, app))
        canvas.tag_bind(dropdownmenu[i][-1], "<Leave>", lambda event, app=i: hover_leave(event, app))
        i += 1

def hover_enter(event, i):
    global dropdownmenu
    canvas.itemconfig(dropdownmenu[i][0], fill='#a7adba')

def hover_leave(event, i):
    global dropdownmenu
    canvas.itemconfig(dropdownmenu[i][0], fill='#c0c5ce')

def click_dropdown(event, i):
    global dropdownmenu, currdropdownoption, dropdowntext
    for item in dropdownmenu:
        for x in item:
            canvas.delete(x)
    currdropdownoption = dropdownoptions[i]
    canvas.itemconfig(dropdowntext, text=currdropdownoption)

def build_page(template):
    global currlayout, Settings, currpos, slider, slideramount, currtriggers, dropdowny, dropdownoptions, currdropdownoption, dropdowntext
    currtriggers = {}
    y = 40
    if template[0] == 'Neue_Kontakte':
        if creds['itslearning'] == {}:
            currlayout.append(canvas.create_rectangle(275, 100, 675, 200, fill='#800000', outline='black', width='3'))
            currlayout.append(canvas.create_text(475, 130, fill='black', font='Times 18 bold', text='Geen ItsLearning account opgegeven'))
            currlayout.append(canvas.create_text(475, 180, fill='black', font='Times 15 bold', text='Voeg er een toe in bij \'accounts\''))
            return
    elif template[0] == 'slimleren':
        if creds['slim_leren'] == {}:
            currlayout.append(canvas.create_rectangle(275, 100, 675, 200, fill='#800000', outline='black', width='3'))
            currlayout.append(canvas.create_text(475, 130, fill='black', font='Times 18 bold', text='Geen Slim leren account opgegeven'))
            currlayout.append(canvas.create_text(475, 180, fill='black', font='Times 15 bold', text='Voeg er een toe in bij \'accounts\''))
            return
    for item in template[2:]:
        if item[0] == 'title':
            currlayout.append(canvas.create_text(475, y, fill='black', font='Times 20 bold', text=item[1]))
        elif item[0] == 'text':
            currlayout.append(canvas.create_text(475, y, fill='black', font='Times 15', text=item[1]))
        elif item[0] == 'slider':
            currlayout.append(canvas.create_text(475, y-10, fill='black', font='Times 15 bold', text=item[1] + ':'))
            currlayout.append(round_rectangle(245, y+5, 705, y+10, 5, fill='black', outline=''))
            slideramount = item[3]
            for i in range(item[3]):
                currlayout.append(canvas.create_rectangle(int(248+(450/(item[3]-1))*i), y+14, int(252+(450/(item[3]-1))*i), y+20, fill='black', outline=''))
                currlayout.append(canvas.create_text(int(250+(450/(item[3]-1))*i), y+27, fill='black', font='Times 10 bold', text=str(i+1)))
            currtriggers['slider'] = Settings["readtheorydefaultgrade"]
            currlayout.append(canvas.create_oval(int(244+(450/(item[3]-1))*(currtriggers['slider']-1)), y+2, int(255+(450/(item[3]-1))*(currtriggers['slider']-1)), y+13, fill='grey', outline=''))
            slider = currlayout[-1]
            canvas.tag_bind(currlayout[-1], "<ButtonPress-1>", lambda event, app=item[2]: slidebeg(event, app))
            canvas.tag_bind(currlayout[-1], "<ButtonRelease-1>", slideend)
        elif item[0] == 'invulvak':
            currlayout.append(canvas.create_text(475, y-10, fill='black', font='Times 15 bold', text=item[1] + ':'))
            entry = Entry(window)
            entry.insert(END, 5)
            currlayout.append(canvas.create_window(475, y+15, window=entry))
            currtriggers['input'] = entry
        elif item[0] == 'selectie':
            dropdowny = y
            if item[3] == 'accounts':
                if len(creds['read_theory']) == 0:
                    currlayout.append(canvas.create_rectangle(275, 100, 675, 200, fill='#800000', outline='black', width='3'))
                    currlayout.append(canvas.create_text(475, 130, fill='black', font='Times 18 bold', text='Geen read theory account opgegeven'))
                    currlayout.append(canvas.create_text(475, 180, fill='black', font='Times 15 bold', text='Voeg er een toe in bij \'accounts\''))
                    return
                dropdownoptions = []
                for account in creds['read_theory']:
                    dropdownoptions.append(account['usr'])
                try:
                    currdropdownoption = dropdownoptions[dropdownoptions.index(Settings["defaultreadtheoryaccount"])]
                except: 
                    currdropdownoption = dropdownoptions[0]
            else:
                dropdownoptions = item[3]
                currdropdownoption = dropdownoptions[0]
            
            currlayout.append(canvas.create_rectangle(500, y, 600, y+20, fill='white', outline='black'))
            canvas.tag_bind(currlayout[-1], "<ButtonPress-1>", dropdown)
            currlayout.append(canvas.create_polygon(589, y+8, 597, y+8, 593, y+13, fill='black', outline='black'))
            canvas.tag_bind(currlayout[-1], "<ButtonPress-1>", dropdown)
            currlayout.append(canvas.create_text(450, y+10, fill='black', font='Times 15 bold', text=item[1] + ':'))
            currlayout.append(canvas.create_text(550, y+10, fill='black', font='Times 9 bold', text=currdropdownoption))
            canvas.tag_bind(currlayout[-1], "<ButtonPress-1>", dropdown)
            dropdowntext = currlayout[-1]
        elif item[0] == 'startbutton':
            currlayout.append(canvas.create_rectangle(400, y-20, 550, y+20, fill='#c0c5ce', outline='black'))
            canvas.tag_bind(currlayout[-1], "<ButtonPress-1>", lambda event, app=template[0], max_y=y+80: start(event, app, max_y))
            currlayout.append(canvas.create_text(475, y, fill='black', font='Times 25 bold', text='START'))
            canvas.tag_bind(currlayout[-1], "<ButtonPress-1>", lambda event, app=template[0], max_y=y+80: start(event, app, max_y))
        elif item[0] == 'change_btn_account':
            currlayout.append(canvas.create_rectangle(300, y-20, 650, y+20, fill='#c0c5ce', outline='black'))
            canvas.tag_bind(currlayout[-1], "<ButtonPress-1>", change_creds)
            currlayout.append(canvas.create_text(475, y, fill='black', font='Times 25 bold', text='Verander accounts'))
            canvas.tag_bind(currlayout[-1], "<ButtonPress-1>", change_creds)
        elif item[0] == 'change_btn_setting':
            currlayout.append(canvas.create_rectangle(300, y-20, 650, y+20, fill='#c0c5ce', outline='black'))
            canvas.tag_bind(currlayout[-1], "<ButtonPress-1>", change_setts)
            currlayout.append(canvas.create_text(475, y, fill='black', font='Times 25 bold', text='Change settings'))
            canvas.tag_bind(currlayout[-1], "<ButtonPress-1>", change_setts)
        
        y += 80

def settingsfunc(*args):
    global currlayout, creds, Settings, lastapp
    lastapp = 'Settings'
    for item in currlayout:
            canvas.delete(item)
    build_page(['creds', None, ['title', 'Settings'], ['change_btn_setting']])

def accounts(*args):
    global currlayout, creds, Settings, lastapp
    lastapp = 'accounts'
    for item in currlayout:
            canvas.delete(item)
    build_page(['creds', None, ['title', 'Verander accounts'], ['change_btn_account']])

def change_setts(*args):
    global currlayout, creds, Settings
    os.system("/usr/share/raspi-ui-overrides/applications/mousepad.desktop sets.txt")
    with open("sets.txt", "r") as f:
        tmp = f.read().split('\n')
    new_sets = {}
    for line in tmp:
        try:
            Input = line.split(':')[1]
            done = False
            while done == False:
                if Input[0] == ' ':
                    Input = Input[1:]
                else:
                    done = True
            done = False
            while done == False:
                if Input[-1] == ' ':
                    Input = Input[:-1]
                else:
                    done = True
        except:
            pass
        if 'Default Account:' in line:
            new_sets["defaultreadtheoryaccount"] = Input
        elif 'Default Grade:' in line:
            new_sets["readtheorydefaultgrade"] = int(Input)
    update_files(new_sets, creds)

def change_creds(*args):
    global currlayout, creds, Settings
    os.system("/usr/share/raspi-ui-overrides/applications/mousepad.desktop input.txt")
    with open("input.txt", "r") as f:
        tmp = f.read().split('\n')
    new_creds = {'itslearning': {}, 'read_theory': [], 'slim_leren': {}}
    next = ''
    for line in tmp:
        if line == '':
            next = ''
        if not next == '':
            try:
                tmp2 = line.split(':')
                for i in range(2):
                    done = False
                    while done == False:
                        if tmp2[i][0] == ' ':
                            tmp2[i] = tmp2[i][1:]
                        else:
                            done = True
                    done = False
                    while done == False:
                        if tmp2[i][-1] == ' ':
                            tmp2[i] = tmp2[i][:-1]
                        else:
                            done = True
            except:
                next = ''
        if next == 'rt':
            new_creds['read_theory'].append({'usr':tmp2[0], 'pas':tmp2[1]})   
        elif next == 'its':
            new_creds['itslearning']['usr'] = tmp2[0]
            new_creds['itslearning']['pas'] = tmp2[1]
        elif next == 'sl':
            new_creds['slim_leren']['usr'] = tmp2[0]
            new_creds['slim_leren']['pas'] = tmp2[1]
        if 'Read Theory:' in line:
            next = 'rt'
        elif 'ItsLearning:' in line:
            next = 'its'
        elif 'Slimleren:' in line:
            next = 'sl'
    update_files(Settings, new_creds)

def start(event, app, max_y):
    global currtriggers, creds, currlayout
    args = currtriggers
    
    if app == 'read_theory':
        for account in creds["read_theory"]:
            if account['usr'] == args['dropdown']:
                pas = account['pas']
        try:
            readtheorybot.start(args['dropdown'], pas, int(args['slider']), int(args['input'].get()))
            currlayout.append(canvas.create_text(475, max_y, fill='green', font='Times 25 bold', text='Done!'))
        except Exception as E:
            print(E)
            currlayout.append(canvas.create_text(475, max_y, fill='red', font='Times 25 bold', text='ERROR: Probeer opnieuw'))
    elif app == 'Neue_Kontakte':
        try:
            duitsbot.start(creds["itslearning"]["usr"], creds["itslearning"]["pas"])
        except Exception as E:
            print(E)
        currlayout.append(canvas.create_text(475, max_y, fill='green', font='Times 25 bold', text='Done!'))
    else:
        print(app)

def update():
    global canvas, scrolling, sliding, currtriggers, currdropdownoption
    currtriggers['dropdown'] = currdropdownoption
    if scrolling == True:
        scroll()
    elif not sliding == False :
        slide()

    canvas.after(1, update)

window = Tk()
apps = {
    'Slimleren':[None, 'Wiskunde', 'Slimleren', ['slimleren', ['title','Slim leren bot'], ['text','Work in progress']]], 
    'Neue Kontakte':[None, 'Duits', 'Itslearning', ['Neue_Kontakte', ['title','Duits bot'], ['text','Navigeer naar de opdracht en druk op F2 om hem te maken.'], ['text',' Open vragen moet je handmatig maken.'], ['text','De Duits bot kan nog buggie zijn!'], ['startbutton']]], 
    'Read Theory':[None, 'Engels', 'Read Theory', ['read_theory', ['title', 'Read theory bot'], ['invulvak', 'Hoeveelheid texten'], ['slider', 'Niveau', 'readtheorydefaultgrade', 12], ['selectie', 'Account', 'defaultreadtheoryaccount', 'accounts'], ['startbutton']]]
    }
Main = ['main', None, ['title','Joempbot'], ['text','PeePeePooPoo'], ['text','OOOOOOHOOOO!']]
currlayout = []

lastapp = 'home'
dropdowntext = None
dropdownmenu = []
dropdownoptions = []
currdropdownoption = 0
dropdowny = 0
slideramount = 0
currpos = 0
firstpos = None
oldpos = None
scrollbarpos = 0
scrolling = False
sliding = False
slidepos = 0
slider = None
currslider = None
firstslidepos = None
oldslidepos = None
currtriggers = {}
window.title('Joempbot')
window.geometry("750x500+0+0")
window.resizable(0, 0)
canvas = Canvas(window, bg="#5c6776", height=500, width=750, highlightthickness=0)
creds, Settings = read_files()
build_page(Main)

#menu
itemselection = canvas.create_rectangle(0, 0, 200, 500, fill='#343d46', outline='')
scrollbarbg = canvas.create_rectangle(200, 0, 215, 500, fill='#202020', outline='')

if len(apps) > 3:
    scrollbarenabled = True
    scrollbarlen = 2**(-0.2*len(apps))
    if scrollbarlen < 0.1:
        scrollbarlen = 0.1
    scrollbar = canvas.create_rectangle(202, 2, 213, scrollbarlen*500, fill='#a7adba', outline='')
    canvas.tag_bind(scrollbar, "<ButtonPress-1>", scrollbeg)
    canvas.tag_bind(scrollbar, "<ButtonRelease-1>", scrollend)
else:
    scrollbarenabled = False
    scrollbar = canvas.create_rectangle(202, 2, 213, 498, fill='#a7adba', outline='')

for app in apps:
    apps[app][0] = []
    apps[app][0].append(canvas.create_rectangle(0, (list(apps.keys())).index(app)*133+2, 200, ((list(apps.keys())).index(app)+1)*133, fill='#5c6776', outline=''))
    apps[app][0].append(canvas.create_text(100, (list(apps.keys())).index(app)*133+40, fill='black', font='Times 20 bold', text=app))
    apps[app][0].append(canvas.create_text(100, (list(apps.keys())).index(app)*133+80, fill='black', font='Times 15 bold', text=apps[app][1]))
    canvas.tag_bind(apps[app][0][0], "<Button-1>", lambda event, app=app: clickapp(event, app))
    canvas.tag_bind(apps[app][0][1], "<Button-1>", lambda event, app=app: clickapp(event, app))
    canvas.tag_bind(apps[app][0][2], "<Button-1>", lambda event, app=app: clickapp(event, app))

deviderbar = canvas.create_rectangle(0, 400, 200, 500, fill='#1e2329', outline='')

settingsbtn = []
accountsbtn = []
settingsbtn.append(canvas.create_rectangle(0, 452, 200, 500, fill='#3f4852', outline=''))
accountsbtn.append(canvas.create_rectangle(0, 402, 200, 450, fill='#3f4852', outline=''))
settingsbtn.append(canvas.create_text(100, 476, fill='black', font='Times 15 bold', text='Settings'))
accountsbtn.append(canvas.create_text(100, 426, fill='black', font='Times 15 bold', text='Accounts'))
for i in range(2):
    canvas.tag_bind(settingsbtn[i], "<Button-1>", settingsfunc)
    canvas.tag_bind(accountsbtn[i], "<Button-1>", accounts)

update()
canvas.pack()
window.mainloop()