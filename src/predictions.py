import numpy as np
import pandas as pd
import datetime
import tensorflow as tf

def exchangerate_predictor (latest_30day):
    
    assert len(latest_30day)==30, "Input length must be 30!!"
    
    # Normalization of the input data for prediction
    latest_30day_mean = latest_30day.mean()
    latest_30day_std = latest_30day.std()
    latest_30day = (latest_30day - latest_30day_mean) / latest_30day_std
    
    #Prepare the input in the same shape as the model was trained for
    inputs = tf.stack([np.array(latest_30day)])[:, slice(0,30), :] #latest 30 days to get prediction for 29+nextday
    
    predictormodel = tf.keras.models.load_model('../saved_model/residual_lstm_model')
    predictions = predictormodel.predict(inputs,verbose=0)
    
    # Reshape output to match the input for eaiser plotting
    predictions = predictions.transpose(2,0,1).reshape(-1,predictions.shape[1]).transpose()
    
    #de-Normalize to get real values
    predictions = pd.DataFrame(predictions,columns=['open','high','low','close']) * latest_30day_std + latest_30day_mean
    latest_30day = latest_30day * latest_30day_std + latest_30day_mean
    
    #Now plot the data and the prediction
    
    # add the date for nextday prediciton
    date_time = pd.to_datetime(latest_30day.index, format='%Y-%m-%d')
    date_time = date_time.append(date_time[-1:] + datetime.timedelta(days=1))
    predictions.index = date_time[1:]
    
    return latest_30day, predictions
    



