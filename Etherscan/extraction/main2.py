from extraction import get_internal_transactions, get_last_normal_transactions, get_last_internal_transactions

API_KEY = "QH3NS55JXZ72B9VTZ6WBJ83BHVZVD84K4A"
ETH_VALUE = 10 ** 18
BASE_URL = "https://api.etherscan.io/api"

index = int(input("Index: "))

address = "0x6B175474E89094C44Da98b954EedeAC495271d0F" # dai contract

block_number, nb_tx = get_last_normal_transactions(address, index=index, startblock=13743000, endblock=13755000, format='csv')
print(f'Last block number: {block_number}; Number of transactions: {nb_tx}')