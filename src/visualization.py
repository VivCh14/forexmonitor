import matplotlib.pyplot as plt
import pylab
from matplotlib import dates
import datetime
from numpy import sqrt
import matplotlib.patches as mpatches

from forex_utils import candlestickdata


def candlestickplot(data=None,predictions=None):
    
    # Get the candlestick data
    up, down, up_dates, down_dates = candlestickdata(data)
    
    if predictions is not None:
        # Get the canlestick data
        pred_up, pred_down, \
        pred_up_dates, pred_down_dates = candlestickdata(predictions)
        date_time = predictions.index

    ########## Aesthetics #############
    
    fig_width_pt = 1200.0
    inches_per_pt = 1.0/72.27               # Convert pt to inch
    golden_mean = (sqrt(5)-1.0)/2.0      # Aesthetic ratio
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
    
    ###################################

    fig, ax = plt.subplots(1,1)

    #define width of candlestick elements
    width = .4
    width2 = .05

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

    
    #predicitons plot
    if predictions is not None:
        
        #define colors to use
        col1 = 'blue'
        col2 = 'gold'

        #plot up prices
        ax.bar(pred_up_dates,pred_up.close-pred_up.open,width,bottom=pred_up.open,color=col1,alpha=0.75)
        ax.bar(pred_up_dates,pred_up.high-pred_up.close,width2,bottom=pred_up.close,color=col1,alpha=0.75)
        ax.bar(pred_up_dates,pred_up.low-pred_up.open,width2,bottom=pred_up.open,color=col1,alpha=0.75)


        #plot down prices
        ax.bar(pred_down_dates,pred_down.close-pred_down.open,width,bottom=pred_down.open,color=col2,alpha=0.75)
        ax.bar(pred_down_dates,pred_down.high-pred_down.open,width2,bottom=pred_down.open,color=col2,alpha=0.75)
        ax.bar(pred_down_dates,pred_down.low-pred_down.close,width2,bottom=pred_down.close,color=col2,alpha=0.75)

        ax.axvspan(date_time[-2:][:-1], date_time[-1:]+datetime.timedelta(days=1), facecolor='0.75', alpha=0.5)
        
        
    formatter = dates.DateFormatter('%Y-%m-%d')

    ax.xaxis.set_major_formatter(formatter)
    ax.tick_params(labelrotation=45)
    
    ax.set_ylabel("Exchange Rate (INR/SEK)")
    ax.set_xlabel("Dates(YYYY-MM-DD)")
    
    actual_patch1 = mpatches.Patch(color='green', label='$Recorded: \\uparrow$')
    actual_patch2 = mpatches.Patch(color='red', label='$\\downarrow$')

    pred_patch1 = mpatches.Patch(color='blue', label='$Predicted \\uparrow$')
    pred_patch2 = mpatches.Patch(color='gold', label='$\\downarrow$')
    plt.legend(handles=[actual_patch1,actual_patch2,pred_patch1,pred_patch2])

    fig.savefig("../fig/current.png", bbox_inches='tight', dpi=600)