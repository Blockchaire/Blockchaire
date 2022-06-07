from requests import get
from matplotlib import pyplot as plt
from datetime import datetime
import pandas as pd

API_KEY = "QH3NS55JXZ72B9VTZ6WBJ83BHVZVD84K4A"
ETH_VALUE = 10 ** 18
BASE_URL = "https://api.etherscan.io/api"

def make_api_url(module, action, address, **kwargs):
    url = BASE_URL + f'?module={module}&action={action}&address={address}&apikey={API_KEY}'

    for key, value in kwargs.items():
        url += f'&{key}={value}'

    return url

def get_account_balance(address):
    get_balance_url = make_api_url("account", "balance", address, tag="latest")
    response = get(get_balance_url)
    data = response.json()
    value = int(data["result"]) / ETH_VALUE
    return value

def get_transactions_graph(address):
    """Normal transactions + internal transactions"""
    transactions_url = make_api_url("account", "txlist", address, startblock=0, endblock=99999999, page=1, offset=10000, sort="asc")
    response = get(transactions_url)
    data = response.json()["result"]

    internal_tx_url = make_api_url("account", "txlistinternal", address, startblock=0, endblock=99999999, page=1, offset=10000, sort="asc")
    response2 = get(internal_tx_url)
    data2 = response2.json()["result"]

    data.extend(data2)
    data.sort(key=lambda x: int(x["timeStamp"]))

    current_balance = 0
    balances = []
    times = []
    
    for tx in data:
        to = tx["to"]
        from_addr = tx["from"]
        value = int(tx["value"]) / ETH_VALUE
        if "gasPrice" in tx:
            gas = (int(tx["gasUsed"]) * int(tx["gasPrice"])) / ETH_VALUE
        else:
            gas = int(tx["gasUsed"]) / ETH_VALUE
        time = datetime.fromtimestamp(int(tx["timeStamp"]))
        money_in = to.lower() == address.lower()

        if money_in:
            current_balance += value
        else:
            current_balance -= (value + gas)
        
        balances.append(current_balance)
        times.append(time)

    plt.plot(times, balances)
    plt.show()

def get_transactions(address, page):
    print('Making API calls.')
    transactions_url = make_api_url("account", "txlist", address, startblock=0, endblock=99999999, page=page, offset=10000, sort="asc")
    response = get(transactions_url)
    data = response.json()["result"]

    internal_tx_url = make_api_url("account", "txlistinternal", address, startblock=0, endblock=99999999, page=1, offset=10000, sort="asc")
    response2 = get(internal_tx_url)
    data2 = response2.json()["result"]

    print('API calls finished.')
    print('Gathering data')

    data.extend(data2)
    data.sort(key=lambda x: int(x["timeStamp"]))

    lst = []

    for tx in data:
        lst_tx = []
        lst_tx.append(tx["to"])
        lst_tx.append(tx["from"])
        lst_tx.append(int(tx["value"]) / ETH_VALUE)
        if "gasPrice" in tx:
            gas = (int(tx["gasUsed"]) * int(tx["gasPrice"])) / ETH_VALUE
        else:
            gas = int(tx["gasUsed"]) / ETH_VALUE
        lst_tx.append(gas)
        time = datetime.fromtimestamp(int(tx["timeStamp"]))
        lst_tx.append(time)
        lst_tx.append(tx["nonce"])
        lst.append(lst_tx)
        
    print('Data gathered.')
    print('Saving to feather format.')

    columns = ['to', 'from', 'value', 'gas', 'time', 'nonce']
    df = pd.DataFrame(lst, columns=columns)
    df.to_feather('maker' + str(page) + '.feather')
    print(f'Download finished. Last transaction time: {time}')