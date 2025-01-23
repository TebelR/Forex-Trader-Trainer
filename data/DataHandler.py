import sqlite3

class DataHandler:
    cursor = None
    db_file = None
    conn = None

    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        # self.cursor = self.conn.cursor
        self.db_file = db_file

    def __del__(self):
        if(self.conn != None):
            self.conn.close()

    
    def create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS DataPoints (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            timestamp TEXT NOT NULL,
                            pair TEXT NOT NULL,
                            granularity TEXT NOT NULL,
                            bid_open REAL NOT NULL,
                            bid_high REAL NOT NULL,
                            bid_low REAL NOT NULL,
                            bid_close REAL NOT NULL,
                            ask_open REAL NOT NULL,
                            ask_high REAL NOT NULL,
                            ask_low REAL NOT NULL,
                            ask_close REAL NOT NULL,
                            volume REAL NOT NULL
                            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Accounts (
                            account_id TEXT(20) PRIMARY KEY ,
                            tags TEXT,
                            balance REAL NOT NULL DEFAULT 0.0,
                            last_selected INTEGER NOT NULL DEFAULT 0
                            )
        """)
        self.conn.commit()



    #returns the id of the acocunt that was selected in the last session of the app
    def getLastSelectedAccount(self):
        try:
            self.cursor.execute("SELECT account_id FROM Accounts WHERE last_selected = 1")
            return self.cursor.fetchone()[0]
        except:
            raise Exception("Error fetching last selected account - nothing found")
    


    #returns a list of all accounts
    def getAccounts(self):
        self.cursor.execute("SELECT * FROM Accounts")
        return self.cursor.fetchall()
    


    #selects a new account, returns its id
    def selectAccount(self, account_id):
        self.cursor.execute("UPDATE Accounts SET last_selected = 0 WHERE last_selected = 1")
        self.cursor.execute("UPDATE Accounts SET last_selected = 1 WHERE account_id = ?", (account_id,))
        self.conn.commit()

        #DEBUG
        accounts = self.getAccounts()
        for account in accounts:
            print(account)
        self.cursor.execute("SELECT account_id FROM Accounts WHERE last_selected = 1")
        return self.cursor.fetchone()[0]
    

    #takes in a list of newly fetched accounts and creates/updates them accordingly
    def uploadAccounts(self, accounts):
        for account in accounts['accounts']:
            try:
                self.cursor.execute("INSERT INTO Accounts (account_id, balance) VALUES (?, ?)", ((account['id']),0)) #account['balance'] inserted later
            except Exception as e:
                try:
                    self.cursor.execute("INSERT INTO Accounts (account_id) VALUES (?)", ((account['id'])))#insert account without balance
                except Exception as e:
                    print(e)
                    self.cursor.execute("UPDATE Accounts SET balance = ? WHERE account_id = ?", (0 ,account['id']))#or update account if it exists already
        self.conn.commit()

    

    #inserts a new data point with 12 arguments
    def insertDataPoint(self, data_point):
        try:
            if(len(data_point) == 12):
                self.cursor.execute("INSERT INTO DataPoints (timestamp, pair, granularity, bid_open, bid_high, bid_low, bid_close, ask_open, ask_high, ask_low, ask_close, volume) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                                     data_point["timestamp"], data_point["pair"], data_point["granularity"], data_point["bid"]["o"], data_point["bid"]["h"], data_point["bid"]["l"], data_point["bid"]["c"], data_point["ask"]["o"], data_point["ask"]["h"], data_point["ask"]["l"], data_point["ask"]["c"], data_point["volume"])
                self.conn.commit()
            else:
                raise Exception ("Error inserting data point, incorrect number of arguments")
        except:
            raise Exception ("Error inserting data point, the point already exists")
        


    def getAllDataPointsFor(self, pair):
        try:
            self.cursor.execute("SELECT * FROM DataPoints WHERE pair = ?", (pair,))
            return self.cursor.fetchall()
        except:
            return []
    
    def getAllBidPricesFor(self, pair):
        try:
            self.cursor.execute("SELECT pair, granularity, bid_close, bid_open, bid_high, bid_low, timestamp FROM DataPoints WHERE pair = ?", (pair,))
            return self.cursor.fetchall()
        except:
            return []
        
        
    def getAllAskPricesFor(self, pair):
        try:
            self.cursor.execute("SELECT pair, granularity, ask_close, ask_open, ask_high, ask_low, timestamp FROM DataPoints WHERE pair = ?", (pair,))
            return self.cursor.fetchall()
        except:
            return []
        


    #This might have issues because timestamp is just text, filtering for time range might need to happen outside the DB engine
    def getAllDataPointsGranBetween(self, pair, granularity, start, end):
        try:
            self.cursor.execute("SELECT * FROM DataPoints WHERE pair = ? AND granularity = ? AND timestamp BETWEEN ? AND ?", (pair, granularity, start, end))
            return self.cursor.fetchall()
        except:
            return []
        

    
    
    
    
