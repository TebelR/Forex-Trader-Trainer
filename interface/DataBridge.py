#This file is meant to communicate with the database. It talks directly to the DataHandler class
from V3.data.DataHandler import DataHandler

class DataBridge:

    db = None

    def __init__(self, db_file):
        self.db = DataHandler(db_file)
        self.db.create_tables()

    def __del__(self):
        if self.db != None:
            self.db.__del__()


    #reconstructs a data point object and inserts it into DB
    def insertDataPoint(self, data_point, pair, granularity):
        dp = {}
        dp['timestamp'] = data_point[0]
        dp['volume'] = data_point["volume"]
        dp['pair'] = pair
        dp['granularity'] = granularity
        dp['bid_open'] = data_point["bid"]["o"]
        dp['bid_high'] = data_point["bid"]["h"]
        dp['bid_low'] = data_point["bid"]["l"]
        dp['bid_close'] = data_point["bid"]["c"]
        dp['ask_open'] = data_point["ask"]["o"]
        dp['ask_high'] = data_point["ask"]["h"]
        dp['ask_low'] = data_point["ask"]["l"]
        dp['ask_close'] = data_point["ask"]["c"]
        self.db.insertDataPoint(dp)



    #returns the last selected account
    def getLastAccount(self):
        try:
            return self.db.getLastSelectedAccount()
        except:
            return None
    

    #updates all accounts
    def updateAccounts(self, accounts):
        self.db.uploadAccounts(accounts)

    #selects an account
    def selectAccount(self, account_id):
        return self.db.selectAccount(account_id)
    
    #returns all accounts associated with a token
    def getAccounts(self):
        return self.db.getAccounts()
    

    #returns all data points for a pair
    def getDataPoints(self, pair):
        return self.db.getAllDataPointsFor(pair)
    

    #returns all bid prices for a pair
    def getBidPrices(self, pair):
        return self.db.getAllBidPricesFor(pair)
    

    #returns all ask prices for a pair
    def getAskPrices(self, pair):
        return self.db.getAllAskPricesFor(pair)
    

