import quantstats as qs
import yfinance as yf
import pandas as pd
import numpy as np
import seaborn as sns
from datetime import datetime
from datetime import date
from IPython.display import display


def create_dataframe(list_securities, start_date = pd.to_datetime('2007-01-03'), end_date = date.today()):
    df = pd.DataFrame()
    for security in list_securities:
        SEC = yf.Ticker(security)
        if start_date:
            hist = SEC.history(start = start_date, end = end_date)
        else:    
            hist = SEC.history(period="max")
        df[security] = hist['Close'] #I just consider the close price, is that correct?
        #df.dropna() #if this line the data are only from 2010 otyherwise some columns arrive until 2006
    return df


def return_df(df):
    return df.div(df.shift(1))-1


def df_inverse_volatility(df_perc, window):

    #compute the  1/ volatility (standard_deviation) over a range of window days
    return df_perc.rolling(window).apply(lambda x: 1/(x.std()))


def df_wheighted(inv_volat_df):

    #create a new df with the same columns
    df = pd.DataFrame(columns = inv_volat_df.columns)

    #itarate over row (always avoid it, if possible)
    for index, row in inv_volat_df.iterrows():

        #append the new value at each row
        df.loc[index] = row.div(sum(list(row)))
    return df


def df_earnings(df_weight_portf, data_perc):

    #compte the earning dataframe (df_weight*df_returns - entries by entries)
    df = df_weight_portf*data_perc
    df['Tot'] = df.sum(axis= 1)
    return df


def df_earnings_equal_weight(df_percentage):

    #compute a dataframe with all equal weight for benchmarking
    df = df_percentage.mul(0.25)
    df['Tot'] = df.sum(axis= 1)
    return df


if __name__ == '__main__':
    #set parameters
    list_securities = ['SSO','UBT', 'UST', 'UGL']
    window = 30 #days

    #main
    data = create_dataframe(list_securities)
    data_perc = return_df(data)
    inv_volat_data = df_inverse_volatility(data_perc, window)
    data_wheighted = df_wheighted(inv_volat_data)
    data_earnings = df_earnings(data_wheighted, data_perc)
    data_earn_eq_weight = df_earnings_equal_weight(data_perc)
    data_earnings.dropna(inplace = True)
    data_earn_eq_weight.dropna(inplace = True)
    print(data_earn_eq_weight)
    qs.reports.html(data_earnings['Tot'], benchmark = data_earn_eq_weight['Tot'] ,
                    output = 'no_none',  title='All weather performance',
                    download_filename='all_weather_performance.html')
