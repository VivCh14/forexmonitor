# Exchange Rate Forecaster

## Description

- Daily foreign exchange data is pulled from a standard public REST API for the last 100 days.
- The data contains daily `open`, `high`, `low` and `close` rates for the SEK-INR combination.
- A machine learning model based on the LSTM neural network is used for training, validating
and testing all the data available from 2014. The model is saved once and then used to make predictions
given the latest 30 days data. The *grey* region shows the prediction for the next day.
- `Tensorflow` is the main driver for bulding the LSTM model.
- Checkout the `jupyter notebook` from model building/training.
- All the tasks here are automated using `GitHub Actions`. See the `./github/workflows/automation.yml` file.
- Below is a [Candlestick plot](https://en.wikipedia.org/wiki/Candlestick_chart) for the latest 30 days *recorded* and *predicted* values.
![alt forex monitor](fig/current.png "Candlestick plot showing daily recorded values as well ML predicted values")
