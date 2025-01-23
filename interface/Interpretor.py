import json
import requests
import datetime
import DataBridge

URL = "https://api-fxpractice.oanda.com/"# practice account
VERSION = "v3" # current API version at OANDA
accounts = None
selected_account = None

with open('../token.json', 'r') as f:
    TOKEN = json.loads(f.read())

#Makes the innitial request to and fetches all accounts under the token
def getAccounts():
    global accounts
    headers = {"Authorization": "Bearer {}".format(TOKEN['key'])}
    try:
        r = requests.get(URL + VERSION + "/accounts", headers=headers)
        accounts = r.json()
        return accounts
    except:
        accounts = []
        raise Exception("Error fetching accounts")


#selects a new current account to work with
def selectAccount(index):
    global selected_account
    selected_account = accounts["accounts"][index]["id"]
    return selected_account



#sends out two requests to fetch candles, one for bid prices and another for ask prices
#gets 12 month candles for the past year
#90-92 day candles for the past 3 months
#730 hour candles for the past 1 month
#2520 15 minute candles for the past 1 week
#1440 minute candles for the past 1 day
#possible granularities:
#day - days
#mon - months
#hrs-hours
#min - minutes    
#15min - 15 minutes
#The maximum number of candles returned is 5000, so if the combination of time range and granularity is too large, additional requests will be sent
#until all data is fetched
#Note: granularity calculations are based on minutes (single minute)
def getPrices(pair, granularity, time_range, file_name):
    global selected_account
    if(selected_account != None):
        date_time_format = "%Y-%m-%dT%H:%M:%SZ"
        headers = {"Content-Type": "application/json",
                    "Authorization": "Bearer {}".format(TOKEN['key']),
                    "Accept-Datetime-Format": "RFC3339"}
        price = "BA"
        try:
            file = open(file_name, "a")
            file.write ('{"candles": [\n')

            point_count = 0
            data = None
            divisor = getDivisor(granularity)
            time_range = datetime.datetime.strptime(time_range, date_time_format)
            num_minutes = (datetime.datetime.now() - time_range).total_seconds() / 60
            num_candles = num_minutes / divisor
            num_candles = int(num_candles)
            print("Number of candles: {}".format(num_candles))
            if(num_candles > 5000):
                print("Number of candles is too large, splitting into multiple requests")
                #Now we need to find points in time at which the request needs to be split
                num_requests = num_candles / 5000
                num_requests = int(num_requests)
                print("Number of requests: {}".format(num_requests))
                for i in range(num_requests):
                    #calculate start and end times
                    start_time = time_range + datetime.timedelta(minutes = i * 5000 * divisor)
                    end_time = time_range + datetime.timedelta(minutes = (i + 1) * 5000 * divisor)
                    start_time = start_time.strftime(date_time_format)
                    end_time = end_time.strftime(date_time_format)
                    print("Start DateTime: {}".format(start_time))
                    print("End DateTime: {}".format(end_time))
                    #make request
                    r = requests.get(URL + VERSION + "/instruments/" + pair + "/candles?"
                                      + "price=" + price +
                                        "&granularity=" + granularity +
                                        "&from=" + start_time +
                                        "&to=" + end_time, headers=headers)
                    data = r.json()
                    if(r.text.find("error") != -1):
                        print("Got an error: {}".format(r.text))
                        data=None
                    
                    uploadData(data, file, point_count,num_candles)
            else:
                #Make a normal request if the number of candles is not too large
                #The body of the response should contain a JSON of all the candles
                r = requests.get(URL + VERSION + "/instruments/" + pair + "/candles?"
                                  + "price=" + price +
                                    "&granularity=" + granularity +
                                    "&from=" + time_range.strftime(date_time_format) +
                                    "&to=" + datetime.datetime.now().strftime(date_time_format), headers=headers)
                data = r.json()
                if(r.text.find("error") != -1):
                    print("Got an error: {}".format(r.text))
                    data=None
            
            uploadData(data, file, point_count,num_candles)
            

            #clean up and finish the JSON wrap
            file.seek(-3, 1)
            file.truncate()
            file.write('\n]}\n')
            file.close()    
        except:
            Exception("Error opening file")



#uploads data to a file 
def uploadData(data, file, point_count, num_candles):
    if(data is not None and data["candles"] is not None):
        print("Number of candles returned: {}".format(len(data["candles"])))

        point_count += len(data["candles"])
        #Append the new data to the file

        for candle in data["candles"]:
            file.write(json.dumps(candle) + ",\n")
        
    else:
        print("No data returned")


#converts granularity to an integer to calculate the number of candles that need to be fetched
def getDivisor(granularity):
    print(granularity)
    if(granularity == "M1"):
        return 1
    elif(granularity == "M5"):
        return 5
    elif(granularity == "M15"):
        return 15
    elif(granularity == "M30"):
        return 30
    elif(granularity == "H1"):
        return 60
    elif(granularity == "H4"):
        return 240
    elif(granularity == "D"):
        return 1440
    elif(granularity == "W"):
        return 10080
    elif(granularity == "M"):
        return 43200
    


