from requests import get
import pandas as pd
from balance import make_api_url, get_transactions

# df = pd.read_feather('./maker1.feather')
# print(df.shape)
# print(df.head())
address = "0x68b3465833fb72a70ecdf485e0e4c7bd8665fc45"

transactions_url = make_api_url("account", "txlist", address, startblock=15013391, endblock=99999999, page=1, offset=10000, sort="asc")
response = get(transactions_url)
data = response.json()["result"]

# internal_tx_url = make_api_url("account", "txlistinternal", address, startblock=0, endblock=99999999, page=1, offset=10000, sort="asc")
# response2 = get(internal_tx_url)
# data2 = response2.json()["result"]

# data.extend(data2)
# data.sort(key=lambda x: int(x["timeStamp"]))

print(data)
