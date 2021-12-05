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

Get data about accounts

"""

def run_query(query): # A simple function to use requests.post to make the API call. Note the json= section.
    request = requests.post('https://api.thegraph.com/subgraphs/name/graphprotocol/compound-v2', json={'query': query})
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))


def get_accounts_txt(last_id):
    # Returns the query to collect account data with the correct last_id inserted in the last place
    
    return '''{
    accounts(first: 1000, where: {id_gt:"'''+last_id+'''"}) {
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

def get_blockNumber():
	query = '''
	{
	mintEvents(first:1, orderBy:blockNumber, orderDirection:desc){
  		blockNumber
	}}
	'''
	response = run_query(query)["data"]["mintEvents"]
	return response[0]["blockNumber"]


# ________________ MAIN RUNNING______________________________________
blockNumber = get_blockNumber()

get_accounts = lambda last_id: run_query(get_accounts_txt(last_id))
# Implement a lambda function to shorten the amount of typing I have to do


list_of_dicts = []
entry_count = 0
last_id = ""
# run once with empty query id

dir = input("Please enter the full filepath to your accounts file")

os.chdir(dir)


# run until you get all users
while last_id < "0xffffa57756e1c19c1e0026487559982e721cffff":
    while True:
        try:
            val_dict = get_accounts(last_id)["data"]["accounts"]
            for user in val_dict:
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
            if len(list_of_dicts) > 20000: # check if the 20000th element of the dictionary has been written to
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
print("done executing query")
print("now compiling all the data into one large file")


def sorting_crit(file_name):
    return int(file_name[8:-4])


extension = 'csv'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
all_filenames.sort(key = sorting_crit, reverse = True)
print("These are the files that will be compiled", all_filenames)


#combine all files in the list
combined = pd.concat([pd.read_csv(f) for f in all_filenames ])
combined.rename(columns = {"Unnamed: 0" : f"{blockNumber}"}, inplace = True)

#export to csv
combined.to_csv( "all_accounts"+str(blockNumber)+".csv", index=False, encoding='utf-8-sig')
print("done")
