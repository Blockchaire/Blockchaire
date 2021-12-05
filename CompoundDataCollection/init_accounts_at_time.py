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



"""

Get data about accounts at a specific time in the history of the blockchain


"""

# ___________GLOBAL VARIABLES__________________

dir = input("Please enter your accounts folder filepath: ")
os.chdir(dir)
time = input("Please enter the date at which you want to extract the data in the following format: dd:mm:yyyy; ")
day = int(time[:2])
month = int(time[3:5])
year = int(time[-4:])
date = datetime.date(year,month,day)

#______________FUNCITONS___________________




def run_query(query): # A simple function to use requests.post to make the API call. Note the json= section.
    request = requests.post('https://api.thegraph.com/subgraphs/name/graphprotocol/compound-v2', json={'query': query})
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))

def convert_time_to_unix(datetime_obj):
    """ Takes a datetime object in as an argument and returns a query for account states with the first block after that
    """
    time = (datetime_obj - datetime.date(1970,1,1)).total_seconds()
    query =  '''
    {mintEvents(first:1, where:{blockTime_gt: '''+str(int(time))+'''}, orderBy:blockTime,orderDirection:asc){
      blockNumber
    }}
    '''
    blockNumber = run_query(query)["data"]["mintEvents"][0]["blockNumber"]
    return(blockNumber)

def get_accounts_at_time_txt(last_id,date): # Returns the query text
    blockNumber = convert_time_to_unix(date)
    return '''{
    accounts(block:{number:'''+str(blockNumber)+'''},first: 1000, where: {id_gt:"'''+last_id+'''"}) {
        id
        countLiquidated
        countLiquidator
        hasBorrowed
        health
        totalBorrowValueInEth
        totalCollateralValueInEth
        tokens{
            symbol
            enteredMarket
            cTokenBalance
            totalUnderlyingSupplied
            totalUnderlyingRedeemed
            accountBorrowIndex
            totalUnderlyingBorrowed
            totalUnderlyingRepaid
            storedBorrowBalance
            supplyBalanceUnderlying
            lifetimeSupplyInterestAccrued
            borrowBalanceUnderlying
            lifetimeBorrowInterestAccrued
        }
        
    }
    }'''



# ___________________________MAIN CODE___________________________________

get_accounts_at_time = lambda last_id, date: run_query(get_accounts_at_time_txt(last_id,date)) # Lambda function to make everything simpler



list_of_dicts = []
entry_count = 0
last_id = ""
print("running")
# run until you get all users
while last_id < "0xffffa57756e1c19c1e0026487559982e721cffff":
    while True:
        try:
            val_dict = get_accounts_at_time(last_id,date)["data"]["accounts"]
            print("got accounts")
            user_count = 0
            for user in val_dict:
                user_count += 1
                template = [user["id"], user["countLiquidated"], user["countLiquidator"],user["hasBorrowed"],
                            user["health"], user["totalBorrowValueInEth"], user["totalCollateralValueInEth"]]
                for token in user["tokens"]:
                    token_template = [token["symbol"], token["enteredMarket"], token["cTokenBalance"], 
                                      token["totalUnderlyingSupplied"], token["totalUnderlyingRedeemed"],
                                      token["accountBorrowIndex"],token["totalUnderlyingBorrowed"],
                                      token["totalUnderlyingRepaid"], token["storedBorrowBalance"],
                                      token["supplyBalanceUnderlying"], token["lifetimeSupplyInterestAccrued"],
                                      token["borrowBalanceUnderlying"], token["lifetimeBorrowInterestAccrued"]]
                    list_of_dicts.append({entry_count: template+token_template})
                    entry_count += 1
            last_id = list_of_dicts[-1][entry_count-1][0]
            if len(list_of_dicts) > 20000 or user_count <= 2: # check if the 20000th element of the dictionary has been written to
                df = pd.DataFrame.from_dict(ChainMap(*list_of_dicts), orient='index',
                                        columns=["id","countLiquidated", "countLiquidator", "hasBorrowed",
                                                "health","totalBorrowValueInEth", "totalCollateralValueInEth",
                                                 "symbol", "enteredMarket", "cTokenBalance", "totalUnderlyingSupplied",
                                                "totalUnderlyingRedeemed", "accountBorrowIndex", "totalUnderlyingBorrowed",
                                                "totalUnderlyingRepaid","storedBorrowBalance","supplyBalanceUnderlying",
                                                    "lifetimeSupplyInterestAccrued","borrowBalanceUnderlying",
                                                     "lifetimeBorrowInterestAccrued"])
                #print(df)
                df.to_csv(f"accounts{entry_count}.csv")
                list_of_dicts = []
                print("Saved to file")
                #print(last_id)
            break
        except Exception as e:
            print(e, "huh")
            continue

# Process 
#df = df.set_index('id')
#df.to_csv("accounts.csv")  #save the user ID's and "has_borrowed" to a file
print("done extracting data")
print("Now compiling everything into one file")


def sorting_crit(file_name):
    return int(file_name[8:-4])

extension = 'csv'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
all_filenames.sort(key = sorting_crit, reverse = True)


#combine all files in the list
combined = pd.concat([pd.read_csv(f) for f in all_filenames ])
combined.rename(columns = {"Unnamed: 0" : f"{day}/{month}/{year}"}, inplace = True)
#export to csv
combined.to_csv( "all_accounts_"+str((day,month,year))+".csv", index=False, encoding='utf-8-sig')
print("done")

a = input("terminated")
