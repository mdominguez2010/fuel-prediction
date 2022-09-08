# Iterate through BLS API (limits 20 years per request) at a time
# Start with 1976
# increment until current year (2022)
# 500 daily call limit
import matplotlib.pyplot as plt
from datetime import datetime
from dateutil import parser
import pandas as pd
import requests
import pickle
import keys

class GasPipeline:
    def __init__(self, year_start = 1976, api_key = keys.API_KEY, url = keys.URL, data_dict = {"period": [], "periodName": [], "value": [], "year": [], "date": []}):
        self.api_key = api_key
        self.url = url
        self.year_start = year_start
        self.data_dict = data_dict

    def get_raw_data(self):

        while self.year_start <= 2023:

            payload = {
                "seriesid": "APU000074714", # series Id
                "registrationkey": self.api_key,
                "startyear": "{}".format(self.year_start),
                "endyear": "{}".format(self.year_start + 1)
                }

            response = requests.post(url=self.url, data=payload)
            raw_data = response.json()
            raw_data = raw_data["Results"]["series"][0]["data"]

            for element in raw_data:
                for item in element:
                    if item != "latest" and item != "footnotes":
                        if item == "value":
                            self.data_dict[item].append(float(element[item]))
                        else:
                            self.data_dict[item].append(element[item])
                    else:
                        continue 

            self.year_start += 2

        return self.data_dict

    def create_date_column(self):
        for (i, j) in zip(self.data_dict["periodName"], self.data_dict["year"]):
            date_formatted = parser.parse(i + " " + "1" + " " + j)
            self.data_dict["date"].append(date_formatted)

    def save_pickle(self, data_dict_filename = "../data/raw/fuel_prices.p"):
        pickle.dump(self.data_dict, open(data_dict_filename, "wb"))

    def load_pickle(self, data_dict_filename = "../data/raw/fuel_prices.p"):
        return pickle.load(open(data_dict_filename, "rb"))

def train_val_split(series: list) -> list:
    """Divide the time series into training and validation set"""
    time_step = int(round(len(series) * 0.8, 0))
    series_train = series[:time_step]
    series_valid = series[time_step:]
    
    return series_train, series_valid

# Run pipeline to get raw data and save it
etl = GasPipeline()
data_dict = etl.get_raw_data()
etl.create_date_column()

# Organize data
df = pd.DataFrame(data=data_dict)
df.sort_values(by=["year", "period"], axis=0, ascending=True, inplace=True)
df = df[["date", "value"]]
df.reset_index(drop=True, inplace=True)
df["date"] = pd.to_datetime(df["date"], format = "%Y/%m/%d", unit = 'D')

# Split train and validate sets
series_train, series_valid = train_val_split(series = df)
print("series_train shape", series_train.shape)
print(series_train[:5])
print("series_valid shape", series_valid.shape)
print(series_valid[:5])
series_train.to_csv(path_or_buf="../data/processed/series_train.csv", index = False)
series_train.to_csv(path_or_buf="../data/processed/series_valid.csv", index = False)