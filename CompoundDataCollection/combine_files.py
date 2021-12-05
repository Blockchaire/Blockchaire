
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


dir = input("Enter directory where to combine files from")
os.chdir(dir)


extension = 'csv'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
#all_filenames.sort(key = sorting_crit, reverse = True)


#combine all files in the list
combined = pd.concat([pd.read_csv(f) for f in all_filenames ])
#export to csv
combined.to_csv( "all_markets.csv", index=False, encoding='utf-8-sig')
print("done")
