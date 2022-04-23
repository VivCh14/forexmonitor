from forex_utils import api_caller
from visualization import CandlestickChart
from predictions import exchangerate_predictor

if __name__=="__main__":
    
    #Load data Obj
    df = api_caller()
    
    #Candlesticks for observed data
    #obs = CandlestickChart(record=df)
    #obs.chart()
    
    """Predict next days exchange rate based on
    a trained Residual-LSTM model. Pass latest
    30 days data
    """
    latest_30day, predictions = exchangerate_predictor(df.tail(30))
    
    plot = CandlestickChart(record=latest_30day,predictions=predictions)
    plot.chart()
    