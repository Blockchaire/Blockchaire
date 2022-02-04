import run_query as rn
import datetime
import os
import pandas as pd
import numpy as np
import graphql
import json
"""
Queries the compound subgraph for information about market for every 


"""

# __________________________________________Global Variables___________________________:
granularity_of_data = "d" # d - day

def data_inputs():
    start_date_entry = input('Enter a start date in YYYY-MM-DD format: ')
    year, month, day = map(int, start_date_entry.split('-'))
    start = datetime.datetime(year, month, day)
    end_date_entry = input('Enter an end date in YYYY-MM-DD format: ')
    year, month, day = map(int, end_date_entry.split('-'))
    end = datetime.datetime(2021,9,3)
    cwd = os.getcwd()
    return start,end

# ___________________________________________Functions_________________________________


def convert_time_to_unix(datetime_obj):
    """ Takes a datetime object in as an argument and returns a query for account states with the first block after that
    """
    global url
    time = (datetime_obj.date() - datetime.date(1970,1,1)).total_seconds()
    mintEvent_query = rn.query('''
    query a($blockNumber: Int!)
    {mintEvents(first:1, where:{blockTime_gt: $blockNumber}, orderBy:blockTime,orderDirection:asc){
      blockNumber
    }}
    ''',{"blockNumber":time}) 
    blockNumber = json.loads(mintEvent_query.run_query(url).text)["data"]["mintEvents"][0]["blockNumber"]
    return(blockNumber)




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

query = rn.query('''query a($blockNumber: Int!){
        markets(block:{number:$blockNumber}){
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
            reserveFactor
            borrowIndex
            exchangeRate
        }
    }
''')

url = "https://api.thegraph.com/subgraphs/name/graphprotocol/compound-v2"
def get_data():
    start,end = data_inputs()
    date_range = pd.date_range(start,end-datetime.timedelta(days=1),freq=granularity_of_data)
    markets_values = []
    market_count = 0
    for time in date_range:

        print(time)
        day = str(time.day).zfill(2)
        month = str(time.month).zfill(2)
        year = str(time.year)
        blockNumber = convert_time_to_unix(pd.to_datetime(time))
        query.query_variables = {"blockNumber":blockNumber}
        val_dict = json.loads(query.run_query(url).text)["data"]["markets"]
        column_names = query.fields
        #print(val_dict, "val dict")
        
        for market in val_dict:
                print(query.fields, "fields")
                markets_values.append([market[f"{field}"] for field in query.fields]) # if the query is expanded you must also expand this
                market_count += 1
        print(markets_values,"huh")
        if len(markets_values) > 0:
            rn.save_df_to_dir(query.fields,markets_values, os.getcwd(),f"{os.getcwd()}\\markets", f"markets{market_count}")
            markets_values = []
    print("gotten all, now combining")
    rn.combine_files(os.getcwd())
get_data()