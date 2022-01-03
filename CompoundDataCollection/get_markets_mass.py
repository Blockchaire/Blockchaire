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
from tqdm import tqdm
"""
Queries the compound subgraph for information about market for every 


"""

# __________________________________________Global Variables___________________________:
granularity_of_data = "d" # d - day

def data_inputs():
    start_date_entry = input('Enter a start date in YYYY-MM-DD format')
    year, month, day = map(int, start_date_entry.split('-'))
    global start 
    start = datetime.datetime(year, month, day)
    end_date_entry = input('Enter a start date in YYYY-MM-DD format')
    year, month, day = map(int, end_date_entry.split('-'))
    global end
    end = datetime.datetime(2021,9,3)
    cwd = os.getcwd()
    print(cwd)
    dir = input("Please enter the directory where you want to save the markets data: ")
    os.chdir(dir)

# ___________________________________________Functions_________________________________

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
            borrowRate
        }
    }
'''


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


# ______________________________Running code____________________________:

def get_graph_data():
    data_inputs()
    get_markets = lambda date: run_query(get_markets_at_time(date))
    date_range = pd.date_range(start,end-datetime.timedelta(days=1),freq=granularity_of_data)
    for time in tqdm(date_range):

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
                                    market["totalSupply"], market["blockTimestamp"], market["underlyingPriceUSD"],market["underlyingPrice"], market["borrowRate"]]}) # if the query is expanded you must also expand this
                market_count += 1
                
        df = pd.DataFrame.from_dict(ChainMap(*list_of_dicts), orient='index',columns=[column_names])
        #df = df.rename_axis(f"{day}/{month}/{year}", axis=1)
        df.to_csv(f"markets_"+str((int(day),int(month),int(year)))+".csv")

        #print("done")

    print("gotten all, now combining")
    extension = 'csv'
    all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
    #all_filenames.sort(key = sorting_crit, reverse = True)
    #combine all files in the list
    combined = pd.concat([pd.read_csv(f) for f in all_filenames ])
    #export to csv
    combined.to_csv( "all_markets.csv", index=False, encoding='utf-8-sig')

get_graph_data()