from requests import get
import pandas as pd
from balance import make_api_url, get_transactions

# df = pd.read_feather('./maker1.feather')
# print(df.shape)
# print(df.head())
address = "0x6B175474E89094C44Da98b954EedeAC495271d0F"
page = 1

transactions_url = make_api_url("account", "txlist", address, startblock=0, endblock=99999999, page=page, offset=10000, sort="asc")
response = get(transactions_url)
data = response.json()["result"]

# internal_tx_url = make_api_url("account", "txlistinternal", address, startblock=0, endblock=99999999, page=1, offset=10000, sort="asc")
# response2 = get(internal_tx_url)
# data2 = response2.json()["result"]

# data.extend(data2)
# data.sort(key=lambda x: int(x["timeStamp"]))

print(data[0])
