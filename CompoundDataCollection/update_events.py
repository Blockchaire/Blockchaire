from graphqlclient import GraphQLClient
import pandas as pd
import json
import csv
import numpy as np
from collections import ChainMap
import os
import requests
import datetime
from collections import ChainMap






"""

    Script to update the events database

"""







def run_query(query): # A simple function to use requests.post to make the API call. Note the json= section.
    request = requests.post('https://api.thegraph.com/subgraphs/name/graphprotocol/compound-v2', json={'query': query})
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))

def update_events_text(block_number): 
    return '''
    {
        mintEvents(where:{blockNumber_gt:'''+str(block_number)+'''}){
            to
            amount
            cTokenSymbol
            underlyingAmount
            blockTime
            blockNumber
        }
        borrowEvents(where:{blockNumber_gt: "'''+str(block_number)+'''"}){
            borrower
            amount
            underlyingSymbol
            accountBorrows
            blockTime
            blockNumber
        }
        repayEvents(where: {blockNumber_gt: "'''+str(block_number)+'''"}){
            borrower
            amount
            accountBorrows
            underlyingSymbol
            blockTime
            blockNumber
        }
        redeemEvents(where: {blockNumber_gt: "'''+str(block_number)+'''"}){
            from
            amount
            cTokenSymbol
            underlyingAmount
            blockTime
            blockNumber
        }
        liquidationEvents(where: {blockNumber_gt: "'''+str(block_number)+'''"}){
            from
            amount
            cTokenSymbol
            underlyingSymbol
            underlyingRepayAmount
            blockTime
            blockNumber
            to
        }
        transferEvents(where:{blockNumber_gt:"'''+str(block_number)+'''"}){
            from
            to
            amount
            cTokenSymbol
            blockTime
            blockNumber
        }
    }
    '''

update_events = lambda block_number: run_query(update_events_text(block_number))

dir = input("Enter your events folder filepath")

os.chdir(dir)




def get_blockNumber():
    query = '''
    {
    mintEvents(first:1, orderBy:blockNumber, orderDirection:desc){
        blockNumber
    }}
    '''
    response = run_query(query)["data"]["mintEvents"]
    return response[0]["blockTime"]
blockNumber = get_blockNumber()

list_of_dicts = []
entry_count = 0
block_number = ""


#Find when the events were last updated by looking for the largest BlockNumber
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
def find_largest_blocknumber(files_list):
    max = 0
    for file in files_list:
        if file.find("allEvents") != -1:
            blockNumber = file[9:-4]
            if int(blockNumber) > max:
                max = int(blockNumber)
    return max

block_number = find_largest_blocknumber(all_filenames)

# run once with empty query id

while True:
    try:
        val_dict = get_events(block_number)["data"]["accounts"]
        for events in val_dict:
            if events["transferEvents"]:
                for transferEvent in events["transferEvents"]
                    list_of_dicts.append({event_count: [transferEvent["from"], "unknown","T",transferEvent["cTokenSymbol"],
                                                    transferEvent["amount"],transferEvent["to"],
                                                    transferEvent["blockTime"], transferEvent["blockNumber"], None, None]})
                event_count += 1
            if events["borrowEvents"]: # only executes if there are borrow events
                for borrowEvent in events["borrowEvents"]:
                    list_of_dicts.append({event_count:[borrowEvent["borrower"], "unknown","B", borrowEvent["underlyingSymbol"],
                                                       borrowEvent["amount"],borrowEvent["accountBorrows"],
                                                       borrowEvent["blockTime"], borrowEvent["blockNumber"], None, None]})
                    event_count += 1
            if events["repayEvents"]: # only executes if there are repay events
                for repayEvent in events["repayEvents"]:
                    list_of_dicts.append({event_count:[repayEvent["borrower"], "unknown","Rep", repayEvent["underlyingSymbol"],
                                                       repayEvent["amount"], repayEvent["accountBorrows"],
                                                       repayEvent["blockTime"],repayEvent["blockNumber"],None, None]})
                    event_count += 1
            if events["redeemEvents"]:
                for redeemEvent in events["redeemEvents"]:
                    list_of_dicts.append({event_count: [redeemEvent["from"], "unknown", "Red", redeemEvent["cTokenSymbol"],
                                                       redeemEvent["amount"], redeemEvent["underlyingAmount"],
                                                       redeemEvent["blockTime"], redeemEvent["blockNumber"], None, None]})
                    event_count += 1
            if events["liquidationEvents"]:
                for liquidationEvent in events["liquidationEvents"]:
                    list_of_dicts.append({event_count: [liquidationEvent["from"], "unknown", "L", liquidationEvent["cTokenSymbol"],
                                                        liquidationEvent["amount"], liquidationEvent["underlyingRepayAmount"],
                                                        liquidationEvent["blockTime"], liquidationEvent["blockNumber"],
                                                        liquidationEvent["to"], liquidationEvent["underlyingSymbol"]]})
                    event_count += 1
            if events["mintEvents"]:
                for mintEvent in events["mintEvents"]:
                    list_of_dicts.append({event_count:[mintEvent["to"], "unknown","M",mintEvent["cTokenSymbol"],
                                                      mintEvent["underlyingAmount"],mintEvent["blockTime"],mintEvent["blockNumber"],
                                                      None,None]})
            if len(list_of_dicts) > 20000:
                df = pd.DataFrame.from_dict(ChainMap(*list_of_dicts), orient='index',
                                            columns=["id","hasBorrowed", "Type", "Coin",
                                                    "amount","underlyingAmount/accountBorrows/to", "blockTime",
                                                     "blockNumber", "Liquidator", "assetRepaid"])
                df.to_csv(f"events{event_count}.csv")
                list_of_dicts = []
                print("Saved to file")
            break
        except Exception as e:
            print("oh oh", e)
            continue
print("done")
# FIND THE OLD EVENTS CSV FILE

extension = 'csv'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
all_filenames.sort(key = sorting_crit, reverse = True)


#combine all files in the list
combined = pd.concat([pd.read_csv(f) for f in all_filenames ])
#export to csv
combined.to_csv( "allEvents_as_of"+blockNumber+".csv", index=False, encoding='utf-8-sig')
print("done")
