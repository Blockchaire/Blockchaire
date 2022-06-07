from balance import get_transactions

API_KEY = "QH3NS55JXZ72B9VTZ6WBJ83BHVZVD84K4A"
ETH_VALUE = 10 ** 18
BASE_URL = "https://api.etherscan.io/api"

address = "0x9f8F72aA9304c8B593d555F12eF6589cC3A579A2"
get_transactions(address, page=1)