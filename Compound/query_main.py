import pprint

import run_query as rn
import get_markets_mass as gmm

granularity_of_data = "d" # day
pp = pprint.PrettyPrinter(indent=2)

query = rn.query('''query a($blockNumber: Int!){
        markets(block:{number:$blockNumber}){
            underlyingName
            symbol
            cash
            collateralFactor
            exchangeRate
            supplyRate
            totalBorrows
            totalSupply
            blockTimestamp
            underlyingPriceUSD
            underlyingPrice
            borrowRate
            reserveFactor
            borrowIndex
            exchangeRate
        }
    }
''')

url = "https://api.thegraph.com/subgraphs/name/graphprotocol/compound-v2"

gmm.get_data(query=query, granularity_of_data=granularity_of_data)