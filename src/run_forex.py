import requests
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pylab
from matplotlib import dates
import datetime

from argparse import ArgumentParser


def api_caller():
    
    parser = ArgumentParser(description="Track forex for SEK-INR")
    parser.add_argument(
        "forex_key", help="Rapid API key"
    )
    
    args = vars(parser.parse_args())
    
    url = "https://alpha-vantage.p.rapidapi.com/query"
    forex_host = "alpha-vantage.p.rapidapi.com"
    forex_key = args["forex_key"]

    querystring = {"function":"FX_DAILY","from_symbol":"SEK","datatype":"json","outputsize":"compact","to_symbol":"INR"}

    headers = {
        'x-rapidapi-host': forex_host,
        'x-rapidapi-key': forex_key
        }

    return requests.request("GET", url, headers=headers, params=querystring)


if __name__=="__main__":
    
    #Get data from api
    response = api_caller()
    
    # Put the json data from API into pandas DataFrame
    df = pd.DataFrame.from_dict(response.json()['Time Series FX (Daily)'], orient='index')
    # reversing the indexing to have past-present
    df = df[::-1]

    # change column names to the string after the " "
    # currently: '1. open' .. etc
    df = df.rename(columns=lambda x: x.split(" ")[1])
    # change value-columns from str to float64
    df = df.astype({column:np.float64 for column in df.columns},errors='raise')
    
    
    fig_width_pt = 1200.0  # Get this from LaTeX using \showthe\columnwidth
    inches_per_pt = 1.0/72.27               # Convert pt to inch
    golden_mean = (np.sqrt(5)-1.0)/2.0         # Aesthetic ratio
    fig_width = fig_width_pt*inches_per_pt  # width in inches
    fig_height = fig_width*golden_mean      # height in inches
    fig_size =  [fig_width,fig_height]
    params = {'backend': 'pdf',
          'axes.labelsize': 13,
          'legend.fontsize': 13,
          'xtick.labelsize': 13,
          'ytick.labelsize': 13,
          'text.usetex': False, #Error here in nb!
          'figure.figsize': fig_size}
    pylab.rcParams.update(params)

    fig, ax = plt.subplots(1,1)

    #define width of candlestick elements
    width = .4
    width2 = .05


    """define up and down prices"""
    # DataFrame containing close>=open : rate gone up
    up = df[df.close>=df.open]
    # DataFrame containing close<open : rate gone down
    down = df[df.close<df.open]


    #Need date recognized by matplotlib
    up_dates = list(map(datetime.datetime.strptime, up.index, len(up.index)*['%Y-%m-%d']))
    down_dates = list(map(datetime.datetime.strptime, down.index, len(down.index)*['%Y-%m-%d']))

    #define colors to use
    col1 = 'green'
    col2 = 'red'

    #plot up prices
    ax.bar(up_dates,up.close-up.open,width,bottom=up.open,color=col1)
    ax.bar(up_dates,up.high-up.close,width2,bottom=up.close,color=col1)
    ax.bar(up_dates,up.low-up.open,width2,bottom=up.open,color=col1)


    #plot down prices
    ax.bar(down_dates,down.close-down.open,width,bottom=down.open,color=col2)
    ax.bar(down_dates,down.high-down.open,width2,bottom=down.open,color=col2)
    ax.bar(down_dates,down.low-down.close,width2,bottom=down.close,color=col2)

    formatter = dates.DateFormatter('%Y-%m-%d')

    ax.xaxis.set_major_formatter(formatter)
    ax.tick_params(labelrotation=45)

    fig.savefig("../fig/current.png", bbox_inches='tight', dpi=600)