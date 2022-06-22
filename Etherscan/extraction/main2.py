from extraction import get_internal_transactions, get_normal_transactions, get_last_transactions

API_KEY = "QH3NS55JXZ72B9VTZ6WBJ83BHVZVD84K4A"
ETH_VALUE = 10 ** 18
BASE_URL = "https://api.etherscan.io/api"

# index = int(input("Numéro de page : "))

address = "0x9f8f72aa9304c8b593d555F12ef6589cc3a579a2"

tx = get_last_transactions(address, startblock=15009446)
print(tx)