import requests
from argparse import ArgumentParser
import numpy as np
import pandas as pd



"""
Pulls the data from the API and cleans/engineers it
to a proper pandas DataFrame object.
"""
def api_caller():
    
    parser = ArgumentParser(description="Track forex for SEK-INR")
    parser.add_argument(
        "forex_key", help="Rapid API key"
    )
    
    args = vars(parser.parse_args())
    
    url = "https://alpha-vantage.p.rapidapi.com/query"
    forex_host = "alpha-vantage.p.rapidapi.com"
    forex_key = args["forex_key"]

    querystring = {"function":"FX_DAILY","from_symbol":"SEK",
                   "datatype":"json","outputsize":"compact","to_symbol":"INR"}

    headers = {
        'x-rapidapi-host': forex_host,
        'x-rapidapi-key': forex_key
        }

    response = requests.request("GET", url, headers=headers, params=querystring)
    
    # Put the json data from API into pandas DataFrame
    df = pd.DataFrame.from_dict(response.json()['Time Series FX (Daily)'], orient='index')
    # reversing the indexing to have past-present
    df = df[::-1]

    # change column names to the string after the " "
    # currently: '1. open' .. etc
    df = df.rename(columns=lambda x: x.split(" ")[1])
    # change value-columns from str to float64
    df = df.astype({column:np.float64 for column in df.columns},errors='raise')
    
    return df
