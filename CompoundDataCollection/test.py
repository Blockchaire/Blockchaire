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


def run_query(query): # A simple function to use requests.post to make the API call. Note the json= section.
    request = requests.post('https://api.thegraph.com/subgraphs/name/graphprotocol/compound-v2', json={'query': query})
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))

def mint():
    client = GraphQLClient('https://api.thegraph.com/subgraphs/name/uniswap/uniswap-v2')
    m=client.execute('''
{
  uniswapFactories(first: 5) {
    id
  }
}
    ''')
    return(m)

print(run_query(mint()))
