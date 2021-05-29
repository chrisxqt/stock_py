# coding=utf-8
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tools.eval_measures import rmse
import seaborn as sns
import statsmodels.api as sm
import itertools
from statsmodels.tsa.arima_model import ARIMA, ARMA
import warnings
warnings.filterwarnings("ignore")

# https://www.datadriveninvestor.com/2020/07/07/introduction-to-time-series-forecasting-of-stock-prices-with-python/#

data = pd.read_csv('BTC-USD.csv')
data.head()

df = data[['Date', 'Close']]
df.Date = pd.to_datetime(df.Date)
df = df.set_index("Date")

df.plot(style="-")

# Define the p, d and q parameters to take any value between 0 and 3
p = d = q = range(0, 3)
pdq = list(itertools.product(p, d, q))

aic = []
parameters = []
for param in pdq:

    mod = sm.tsa.statespace.SARIMAX(df, order=param,
                                    enforce_stationarity=True, enforce_invertibility=True)

    results = mod.fit()
    # save results in lists
    aic.append(results.aic)
    parameters.append(param)
    # seasonal_param.append(param_seasonal)
    print('ARIMA{} - AIC:{}'.format(param, results.aic))

# find lowest aic
index_min = min(range(len(aic)), key=aic.__getitem__)

print(
    'The optimal model is: ARIMA{} -AIC{}'.format(parameters[index_min], aic[index_min]))

model = ARIMA(df, order=parameters[index_min])
model_fit = model.fit(disp=0) 
print(model_fit.summary())
model_fit.plot_predict(start=2, end=len(df)+12)
plt.show()
