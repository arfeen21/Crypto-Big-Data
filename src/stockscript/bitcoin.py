'''
dit de script wat we gaan gebruiken om de bitcoin prijzen in een csv formaat te krijgen.
De Script van onze vormalige collega was helaas te ingewikkeld en het on veel makkelijker.
'''
import requests
import time
from datetime import datetime
import pandas as pd

startDate = "2020-10-01"

def get():
    '''
    Returns a dataframe containing the BTC/USD starting from November 1st 2020
    '''
    #API key from cryptocompare.com
    api_key = "46e75a89dd7430d9477f5a3825630243cfa6f976a75ee44a7b4077ea5f91124f"
    originalUrl = "https://min-api.cryptocompare.com/data/v2/histohour?fsym=BTC&tsym=USD&limit=2000"
    url = originalUrl

    #attach today's UNIX time and set a limit
    timestamp = time.time()
    url += "&toTs=" + str(int(timestamp))

    params = {"key": api_key}

    totalData = []  #this list will hold the aggregate of all the requests we will send (there is a limit of 2000 items per request)
    while True:
        #we make a GET request, adding the API key as a parameter
        response = requests.get(url, data = params).json()
        responseData = response["Data"]
        priceData = responseData["Data"]
        totalData += priceData

        #if we're before our set date, we stop collecting data
        earliestDate = datetime.utcfromtimestamp(priceData[0]["time"]).strftime("%Y-%m-%d")
        if(earliestDate < startDate):
            break

        #if we need to send a new request (due to the limit), we set the new timestamp as being the oldest record we just retrieved
        #this ensures we start collecting data where the current batch ends
        url = originalUrl
        url += "&toTs="+str(priceData[0]["time"])

    return clean(totalData)

def clean(data):
    data.reverse()  #the response is in ascending order (lowest date first), we flip it so we can skim the top off of it (from 01/11/2020 to today)
    cleanedData = []
    for btcEntry in data:
        dateOfEntry = datetime.fromtimestamp(btcEntry["time"]).date()

        #for every entry element that is after our set date, we add only the relevant columns to a list of dictionairies
        if(str(dateOfEntry) >= startDate):
            cleanedData.append({"Date": dateOfEntry, "Open": btcEntry["open"], "Close" : btcEntry['close'], "High" : btcEntry['high'] , "Low" : btcEntry['low']})
            #print("date: " + str(dateOfEntry))
        
    #convert the list of dicts to a dataframe
    df = pd.DataFrame(cleanedData, columns=["Date", "Open","Close", "High", "Low"])

    #convert the date entries to string values so we can compare them
    df = df.astype({"Date": 'string'})

    #we want it sorted by date
    df = df.sort_values(by="Date")

    #then reset the index to ensure it's still ascending
    df.reset_index(level=0, inplace=True)

    #we rename the column to be appropriate
    df.rename({"Open": "HourlyPrice"}, inplace=True, axis=1)

    #resetting the index adds the old index as a column, so we drop it
    return df.drop(['index'], axis=1)


df = get()
df = pd.DataFrame(df)

df.to_csv('btc.csv')
