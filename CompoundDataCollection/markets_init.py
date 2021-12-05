from graphqlclient import GraphQLClient
import pandas as pd
import json
import csv
import numpy as np
import os
import requests
import datetime
import glob
from collections import ChainMap








# ____________GLOBAL VARIABLES____________________
dir = input("Please enter the directory where you want to save the markets data: ")
os.chdir(dir)
time = input("Please enter the dates at which you want to extract the data, separating different dates with a space as follows: dd:mm:yyyy dd:mm:yyyy ")

datetimes = parse_string_to_dates(time)
print(datetimes)

# _________________FUNCTIONS______________________


def run_query(query): # A simple function to use requests.post to make the API call. Note the json= section.
    request = requests.post('https://api.thegraph.com/subgraphs/name/graphprotocol/compound-v2', json={'query': query})
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))

def convert_time_to_unix(datetime_obj):
    """ Takes a datetime object in as an argument and returns a query for account states with the first block after that
    """
    time = (datetime_obj.date() - datetime.date(1970,1,1)).total_seconds()
    query =  '''
    {mintEvents(first:1, where:{blockTime_gt: '''+str(int(time))+'''}, orderBy:blockTime,orderDirection:asc){
      blockNumber
    }}
    '''
    blockNumber = run_query(query)["data"]["mintEvents"][0]["blockNumber"]
    return(blockNumber)



def get_markets_at_time(date):
    blockNumber = convert_time_to_unix(date)
    return '''
    {
            markets(block:{number:'''+str(blockNumber)+'''}){
                underlyingName
                symbol
                cash
                collateralFactor
                exchangeRate
                supplyRate
                totalBorrows
                totalSupply
                blockTimestamp
                underlyingPriceUSD
                underlyingPrice
            }
        }
    '''











# ________________________MAIN CODE________________________________-



get_markets = lambda date: run_query(get_markets_at_time(date))

def parse_string_to_dates(string):
    dates_list =  list()
    datetimes = list()
    if string.find(" ") != -1:
        while string.find(" ") != -1:
            position = string.find(" ")
            dates_list.append(string[:position])
            string = string[position+1:]
    else:
        dates_list.append(string)
    for date in dates_list:
        datetimes.append(datetime.datetime.strptime(date, "%d:%m:%Y"))
    return datetimes



for time in datetimes:

    day = str(time.day).zfill(2)
    month = str(time.month).zfill(2)
    year = str(time.year)

    val_dict = get_markets(time)["data"]["markets"]

    list_of_dicts = []
    market_count = 0
    column_names = list(val_dict[0].keys())

    for market in val_dict:
            list_of_dicts.append({market_count: [market["underlyingName"],market["symbol"], market["cash"], market["collateralFactor"],
                                  market["exchangeRate"],market["supplyRate"], market["totalBorrows"],
                                  market["totalSupply"], market["blockTimestamp"], market["underlyingPriceUSD"],market["underlyingPrice"]]}) # if the query is expanded you must also expand this
            market_count += 1
            
    df = pd.DataFrame.from_dict(ChainMap(*list_of_dicts), orient='index',columns=[column_names])
    df = df.rename_axis(f"{day}/{month}/{year}", axis=1)
    df.to_csv(f"markets_"+str((int(day),int(month),int(year)))+".csv")

    print("done")
