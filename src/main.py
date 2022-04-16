from forex_utils import api_caller
from visualization import candlestickplot
from predictions import exchangerate_predictor

if __name__=="__main__":
    
    #Load data Obj
    df = api_caller()
    
    #Plot Candlesticks
    #candlestickplot(df)
    
    #Predict next days exchange rate.
    """ - Based on a trained Residual-LSTM model
        - Pass latest 30 days data
    """
    latest_30day, predictions = exchangerate_predictor(df.tail(30))
    
    candlestickplot(latest_30day,predictions)   
    