from requests import get
import pandas as pd
from balance import make_api_url, get_transactions

# df = pd.read_feather('./maker1.feather')
# print(df.shape)
# print(df.head())
address = "0x9f8F72aA9304c8B593d555F12eF6589cC3A579A2"
page = 1

'''
https://api.etherscan.io/api
   ?module=account
   &action=txlist
   &address=0xddbd2b932c763ba5b1b7ae3b362eac3e8d40121a
   &startblock=0
   &endblock=99999999
   &page=1
   &offset=10
   &sort=asc
   &apikey=YourApiKeyToken
'''

transactions_url = make_api_url("account", "txlist", address, startblock=0, endblock=99999999, page=page, offset=10000, sort="asc")
response = get(transactions_url)
data = response.json()["result"]

# internal_tx_url = make_api_url("account", "txlistinternal", address, startblock=0, endblock=99999999, page=1, offset=10000, sort="asc")
# response2 = get(internal_tx_url)
# data2 = response2.json()["result"]

# data.extend(data2)
# data.sort(key=lambda x: int(x["timeStamp"]))

print(data)