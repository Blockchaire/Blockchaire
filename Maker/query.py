import requests
import graphql
import pprint
import pandas as pd
import os
pp = pprint.PrettyPrinter(indent=2)

#_______________________________________________THE QUERY__________________________________

class query():

	"""
	Object to save the query text and the variables you want to pass to the query.

	variables:
		__init___
			query_text: the string of the query you want to send (string)
			query_variables: the variables that you want to pass to the query (dictionary)

		other:
			query_fields: the fields of the query, i.e. the actual data you're going to get in response (list)

	Methods:
		run_query(url):
			does a requests library request to the specified URL, using the text saved into self.query_text
	"""

	def __init__(self, query_text, query_variables = {}):
		# initiate the query text and the variables that are passed into the query https://stackoverflow.com/questions/62384215/best-way-to-construct-a-graphql-query-string-in-python

		if type(query_text) == str:
			self.query_text = query_text
			# first find the headers
			header_AST = graphql.parse(query_text).definitions[0].to_dict() # .parse returns an abstract syntax tree
			# print(header_AST)
			headers_arr = header_AST["selection_set"]["selections"] # the array containing dictionaries with headers in them
			self.fields = self.find_headers(headers_arr)
			
			# Second define the operation
			header_AST["name"] = "my_query" # give a name to the query/operation

			if query_variables: # if you passed variables to the query, then construct the operation variable_definitions field
				# following a structure:
				#{'kind': 'variable_definition', 'variable': {'kind': 'variable', 'name': {'kind': 'name', 'value': $Variable_name (STR)}}, 'type': {'kind': 'non_null_type', 'type': {'kind': 'named_type', 'name': {'kind': 'name', 'value': DATATYPE}}}, 'default_value': None, 'directives': []}
				# header_AST["variable_definitions"] = ['variable_definition', 'variable': {'kind': 'variable', 'name': {'kind': 'name', 'value': query_variables}}, 'type': {'kind': 'non_null_type', 'type': {'kind': 'named_type', 'name': {'kind': 'name', 'value': DATATYPE}}}, 'default_value': None, 'directives': []}]
			
				self.query_variables = query_variables

			# generate headers for the query by turning the graphql text into first a document node "https://graphql-core-3.readthedocs.io/en/latest/modules/language.html?highlight=parse#graphql.language.DocumentNode"
			# and then turning it into a dictionary		

		else:
			raise ValueError("query_text not string")
		if type(query_variables) == dict:
			self.query_type = "single"
		elif type(query_variables) == list:
			self.query_type = "multi"
		else:
			raise ValueError("query_type not dictionary or list of dictionaries")

	def find_headers(self, array, terminal_nodes=None):
		# method to take the self.query, which has been turned into a AST dictionary, and find all the terminal nodes, i.e. the datafields that we are querying
		# this is used to construct the headers for the file into which it will be saved
		terminal_nodes = [] if terminal_nodes is None else terminal_nodes
		for element in array:
			name = element["name"]
			if not element["selection_set"]:
				# print("haha", name)
				terminal_nodes.append(name["value"])
			else:
				# print("not found",element["selection_set"]["selections"],"\n")
				self.find_headers(element["selection_set"]["selections"], terminal_nodes)
		return terminal_nodes

	def run_query(self, url):
		# simple http request, returns a json object with the query response or raises an error
		request = requests.post(url, json={"query": self.query_text, "variables": self.query_variables})
		if request.status_code == 200:
			return request
		else:
			raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))

def save_df_to_dir(fields, data, previous_dir, directory_to_save_to, filename):
    """
        saves dataframe to specific directory
    """
    df = pd.DataFrame(data)
    df.columns = fields
    os.chdir(directory_to_save_to)
    print(directory_to_save_to, os.getcwd(), filename, len(df))
    df.to_csv(f'{filename}.csv') 
    os.chdir(previous_dir)
    data = []
    print("saved")

# ____________________________DEBUG______________________________________________________
"""
text = '''query a($blockNumber: Int!){
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
'''
variables = {"blockNumber": 1000000}


url = "https://api.thegraph.com/subgraphs/name/graphprotocol/compound-v2"
https://gateway.thegraph.com/api/[api-key]/subgraphs/id/EiRmckRKCFMN3hmych8LsefFvGei2ucF86Ka84HX1Jy6
#pp.pprint(c.to_dict())
r = requests.post(url, json={"query": text, "variables": variables})
print(r.text)

test_query = query(text,variables)
print(test_query.fields)
print(test_query.run_query(url))
print(test_query.fields)
#print(test_query.query_text)
#print(test_query.headers)
#print(test_query.run_query(url))
"""