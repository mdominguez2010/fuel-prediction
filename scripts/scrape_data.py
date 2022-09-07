# Iterate through BLS API (limits 20 years per request) at a time
# Start with 1976
# increment until current year (2022)
# 500 daily call limit
from datetime import datetime
from dateutil import parser
import requests
import pickle
import params

class GasPipeline:
    def __init__(self, year_start = 1976, api_key = params.api_key, url = params.url, data_dict = {"period": [], "periodName": [], "value": [], "year": [], "date": []}):
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

# Run pipeline
etl = GasPipeline()
data_dict = etl.get_raw_data()
etl.create_date_column()
etl.save_pickle()