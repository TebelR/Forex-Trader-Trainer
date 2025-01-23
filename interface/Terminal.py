from tkinter import Frame
from tkinter import scrolledtext
import tkinter as tk 
from V3.interface import Interpretor
from V3.interface.DataBridge import DataBridge

class Terminal(Frame):

    text_window = None
    command_line = None
    db = None
    def __init__(self, master, db, **kwargs):
        super().__init__(master, **kwargs)
        self.create_layout()
        self.db = db
        self.text_window = self.create_text_window()
        self.command_line = self.create_command_line()
        self.command_line.bind("<Return>", self.process_command)
    

    def destroy(self):
        if self.db != None:
            self.db.__del__()


    def create_text_window(self):
         text_window = scrolledtext.ScrolledText(self, bg="black", fg="white", insertbackground="white", wrap=tk.WORD, state=tk.DISABLED, font=("Consolas", 10))
         text_window.grid(row=0, column=0, sticky="nsew")
         return text_window
    

    def create_command_line(self):
        command_line = tk.Entry(self, bg="black", fg="white", insertbackground="white", font=("Consolas", 10))
        command_line.grid(row=1, column=0, sticky="nsew")
        return command_line
        


    #set up the grid layout
    def create_layout(self):
        self.grid_rowconfigure(0, weight=9)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)




    #switch on command types
    #list
    def execute_command(self, command):
        tokens = command.split(" ")

        if (tokens[0] == 'test'):#test command
            self.output_command('Test passed')

        elif (tokens[0] == "list"):#list all fetched accounts
            self.list_command(tokens)

        elif (tokens[0] == "select"):#select account
            self.select(tokens)

        elif (tokens[0] == "fetch"):#fetches accounts associated with the loaded token
            self.fetch(tokens)
        else:
            self.output_command('command not found')




    #preprocesses a command and resets the input line
    def process_command(self, event = None):
        command = self.command_line.get().strip()
        
        if (command):
            self.execute_command(command)
            self.command_line.delete(0, tk.END)

    


    #outputs text in the terminal
    def output_command(self, command):
        self.text_window.config(state=tk.NORMAL)
        self.text_window.insert(tk.END, command + '\n')
        self.text_window.config(state=tk.DISABLED)
        self.text_window.see(tk.END)




    #list
    #for now, this lists all currently fetched accounts
    def list_command(self, args):
        if(Interpretor.accounts != None):
            for account in Interpretor.accounts["accounts"]:
                self.output_command(account.__str__())
        else:
            self.output_command('no accounts have been fetched')




    #select
    #selects a certain element to focus on
    #the element can be one of the following:
    #account - index from the fetched accounts list
    def select(self, args):
        paramTwo = str(args[1])
        if (paramTwo == "account"):
            if(len(args)==3):
                index = int(args[2])
                id = Interpretor.selectAccount(index)
                self.db.selectAccount(id)
                self.output_command('account selected: ' + Interpretor.selected_account.__str__())

        # elif (paramTwo == "file"):
        #     file_name = args[2]
        #     result = Interpretor.selectFile(file_name)
        #     if result:
        #         self.output_command("file selected: {}".format(file_name))



    #fetch
    #talks to the borker API to fetch some kind of data, can be one of the following:
    #accounts - fetches all accounts associated with the loaded token
    #prices - fetches prices for a certain pair, need to specify addition arguments
    #   ex: fetch prices CAD_JPY M 2020-01-01T00:00:00Z CAD_JPY_4_Year_Months
    #       fetch prices "pair" "granularity" "timeRange" "fileName"
    #       fetch prices CAD_JPY D1 2022-01-01T00:00:00Z CAD_JPY_3_Year_Days
    #       fetch prices CAD_JPY H1 2022-01-01T00:00:00Z CAD_JPY_3_Year_Hours
    #   If file is not made yet, it will be created, otherwise new data will be appended to whatever is in the file
    #   One of the following granularities can be specified:
    #   M - moths
    #   W - weeks
    #   H12 - 12 hour preiods
    #   H1 - 1 hour preiods
    #   M15 - 15 minute preiods
    #   M1 - 1 minute preiods    
    def fetch(self, args):
        paramTwo = str(args[1])
        if (paramTwo == "accounts"):
            try:
                found_accounts = Interpretor.getAccounts()
                self.output_command('new accounts fetched')
                self.db.updateAccounts(found_accounts)
                self.output_command('stored accounts updated')
            except:
                self.output_command('error fetching accounts')
        elif (paramTwo == "prices"):
            try:
                pair = args[2]
                granuality = args[3]
                timeRange = args[4]
                fileName = args[5]
                Interpretor.getPrices(pair, granuality, timeRange, fileName)
                self.output_command('prices fetched')
            except:
                self.output_command('error fetching prices')




    #tries to retrieve the last selected account
    #prints whether an account was successfully recovered
    def restartSession(self):
        global selected_account
        selected_account = None
        try:
            found_account = self.db.getLastAccount()
            if found_account is not None:
                selected_account = found_account
                self.output_command("Selected account: {}".format(selected_account.__str__()))
        except Exception as e:
           print(e)
           self. output_command('No selected account found, need to fetch accounts first')