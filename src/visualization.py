import matplotlib.pyplot as plt
import pylab
from matplotlib import dates
import datetime
from numpy import sqrt
import matplotlib.patches as mpatches
import pandas as pd


class CandlestickChart():

    """Plot Candlestick chart for the
    given data. Should have OHLC columns."""

    def __init__(self, record=None,predictions=None):
        
        assert record is not None,"Provide atleast one data-set!"

        self.record = record
        self.predictions = predictions

        # up,down prices and dates
        self.up = []
        self.down = []
        self.up_dates = []
        self.down_dates = []
        

    def __del__(self):
        
        class_name = self.__class__.__name__
        print(f"{class_name} destroyed")


    def candlestickData(self, data):
    
        """define up and down prices"""
        
        # close>=open : rate gone up
        self.up = data[data.close>=data.open]
        # close<open : rate gone down
        self.down = data[data.close<data.open]

        #Need date recognized by matplotlib    
        self.up_dates = pd.to_datetime(self.up.index, format='%Y-%m-%d')
        self.down_dates = pd.to_datetime(self.down.index, format='%Y-%m-%d')
    

    def chart(self):

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
        
        # Setup figure
        fig, ax = plt.subplots(1,1)

        #define width of candlestick elements
        width = 0.4
        width2 = 0.05
        
        # colors for the up, down
        col1 = 'green'
        col2 = 'red'
        
        # opacity
        alpha = 1.

        # Get the candlestick data
        self.candlestickData(self.record)

        #plot up prices
        ax.bar(self.up_dates,self.up.close-self.up.open,width,bottom=self.up.open,color=col1,alpha=alpha)
        ax.bar(self.up_dates,self.up.high-self.up.close,width2,bottom=self.up.close,color=col1,alpha=alpha)
        ax.bar(self.up_dates,self.up.low-self.up.open,width2,bottom=self.up.open,color=col1,alpha=alpha)


        #plot down prices
        ax.bar(self.down_dates,self.down.close-self.down.open,width,bottom=self.down.open,color=col2,alpha=alpha)
        ax.bar(self.down_dates,self.down.high-self.down.open,width2,bottom=self.down.open,color=col2,alpha=alpha)
        ax.bar(self.down_dates,self.down.low-self.down.close,width2,bottom=self.down.close,color=col2,alpha=alpha)
        
        record_patch1 = mpatches.Patch(color=col1, label='$Recorded: \\uparrow$')
        record_patch2 = mpatches.Patch(color=col2, label='$\\downarrow$')

        record_handle = [record_patch1,record_patch2]
    
        pred_handle = []
        if self.predictions is not None:
            
            col1 = 'blue'
            col2 = 'gold'
            
            alpha = 0.5
            
            # Get the candlestick data
            self.candlestickData(self.predictions)

            #plot up prices
            ax.bar(self.up_dates,self.up.close-self.up.open,width,bottom=self.up.open,color=col1,alpha=alpha)
            ax.bar(self.up_dates,self.up.high-self.up.close,width2,bottom=self.up.close,color=col1,alpha=alpha)
            ax.bar(self.up_dates,self.up.low-self.up.open,width2,bottom=self.up.open,color=col1,alpha=alpha)


            #plot down prices
            ax.bar(self.down_dates,self.down.close-self.down.open,width,bottom=self.down.open,color=col2,alpha=alpha)
            ax.bar(self.down_dates,self.down.high-self.down.open,width2,bottom=self.down.open,color=col2,alpha=alpha)
            ax.bar(self.down_dates,self.down.low-self.down.close,width2,bottom=self.down.close,color=col2,alpha=alpha)

            date_time = self.predictions.index

            # highlight the nexrday of prediction
            ax.axvspan(date_time[-2:][:-1], date_time[-1:]+datetime.timedelta(days=1), facecolor='0.75', alpha=0.5)

            pred_patch1 = mpatches.Patch(color=col1, label='$Predicted \\uparrow$')
            pred_patch2 = mpatches.Patch(color=col2, label='$\\downarrow$')
            pred_handle = [pred_patch1,pred_patch2]


        formatter = dates.DateFormatter('%Y-%m-%d')

        ax.xaxis.set_major_formatter(formatter)
        ax.tick_params(labelrotation=45)
        
        ax.set_ylabel("Exchange Rate (INR/SEK)")
        ax.set_xlabel("Dates")     

        plt.legend(handles=record_handle+pred_handle)

        fig.savefig("../fig/current.png", bbox_inches='tight', dpi=600)
