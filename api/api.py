from alpha_vantage.timeseries import TimeSeries
from config.settings import ALPHA_VANTAGE_API_KEY



def fetch_data(symbol):
    ts = TimeSeries(key=ALPHA_VANTAGE_API_KEY, output_format='pandas')
    data, meta_data = ts.get_daily(symbol=symbol, outputsize='full')
    return data['4. close']
