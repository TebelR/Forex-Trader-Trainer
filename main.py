import tkinter as tk
from json import loads
from tkinter import Menu
from interface.Terminal import Terminal
from interface.DataBridge import DataBridge

with open('V3/variables.json', 'r') as f:
    VARIABLES = loads(f.read())# for clarity, varaibles are defined in variables.json

MENU = VARIABLES['menu']
DATA_FILE = VARIABLES['data-file']
db = DataBridge(DATA_FILE)

# frame_container= None 
model_frame = None
analysis_frame= None
terminal_frame= None
settings_frame = None


def generateRootWindow():
    root = tk.Tk()
    #root = CoreApplication()
    root.geometry('{}x{}'.format(VARIABLES['width'], VARIABLES['height']))
    root.resizable(True, True)
    root.title('Trading Bot Interface {}'.format(VARIABLES['interface-version']))
    root.protocol('WM_DELETE_WINDOW', lambda: on_close(root))#lambda: root.destroy()
    return root


#This will create a menu on the side of the window
def generateMenu(root):
    menu = Menu(root)
    root.config(menu=menu)
    for key in MENU.keys():
        menu.add_cascade(label=MENU[key]['name'], menu=Menu(root, tearoff=0))




#This will create a layout for the applicaiton
def generateLayout(root):
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)
    root.grid_rowconfigure(0, weight=1)
    root.grid_rowconfigure(1, weight=1)

    # terminal_frame = tk.Frame(root, bg=VARIABLES['colors']['primary'])
    # terminal_frame.grid(row=0, column=0, sticky='nsew')
    # tk.Label(terminal_frame, text='Terminal', font=('Arial', 10)).pack(anchor='nw')

    model_frame = tk.Frame(root, bg=VARIABLES['colors']['primary'])
    model_frame.grid(row=0, column=1, sticky='nsew')
    tk.Label(model_frame, text='Model', font=('Arial', 10)).pack(anchor='nw')

    analysis_frame = tk.Frame(root, bg=VARIABLES['colors']['primary'])
    analysis_frame.grid(row=1, column=0, sticky='nsew')
    tk.Label(analysis_frame, text='Analysis', font=('Arial', 10)).pack( anchor='nw')

    settings_frame = tk.Frame(root, bg=VARIABLES['colors']['primary'])
    settings_frame.grid(row=1, column=1, sticky='nsew')
    tk.Label(settings_frame, text='Settings', font=('Arial', 10)).pack( anchor='nw')
    

def form_terminal_frame():
    global terminal_frame
    terminal_frame = Terminal(root, bg=VARIABLES['colors']['primary'], db = db)
    terminal_frame.grid(row=0, column=0, sticky='nsew')
    terminal_frame.restartSession()#try to find the last selected account

def form_model_frame():
    pass

def form_analysis_frame():
    pass

def form_settings_frame():
    pass

def on_close(root):
    global terminal_frame
    print("Closing the application...")
    if(terminal_frame is not None):
        terminal_frame.destroy()
    root.destroy()


if __name__ == '__main__':
    root = generateRootWindow() # start the root window
    generateMenu(root)
    generateLayout(root)
    form_terminal_frame()
    form_model_frame()
    form_analysis_frame()
    form_settings_frame()

    root.mainloop()