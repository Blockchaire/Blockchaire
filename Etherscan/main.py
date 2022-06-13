from balance import get_transactions

API_KEY = "QH3NS55JXZ72B9VTZ6WBJ83BHVZVD84K4A"
ETH_VALUE = 10 ** 18
BASE_URL = "https://api.etherscan.io/api"

index = int(input("Numéro de page : "))

address = "0x6B175474E89094C44Da98b954EedeAC495271d0F"
get_transactions(address, index=index)