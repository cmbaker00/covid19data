import requests
import json
import numpy as np


class CovidData:
    def __init__(self, url, title):
        self.url = url
        self.title = title

    def download_and_save(self):
        raw_text = self.download_html()
        data_text = self.trim_to_data(raw_text)
        data_array = self.datastring_to_array(data_text)
        for i in range(len(data_array)):
            for j in range(len(data_array[i])):
                data_array[i][j] = data_array[i][j].replace(',','')
        self.save_data(data_array)

    def download_html(self):
        r = requests.get(self.url)
        return r.text

    @staticmethod
    def trim_to_data(text):
        start_index = text.find('window.infographicData=') + len('window.infographicData=')
        end_index = text.find(';</script>', start_index)
        return text[start_index: end_index]

    @staticmethod
    def datastring_to_array(input_string):
        full_data = json.loads(input_string)
        for element in full_data['elements']:
            try:
                return element['data'][0]
            except KeyError:
                pass
        raise Exception('Cannot find data')

    def save_data(self, data):
        np.savetxt("{}.csv".format(self.title), data, delimiter=",", fmt="%s")

if __name__ == '__main__':
    data_url_and_titles = [
        ['https://e.infogram.com/_/fGmCiqWT8M0AgX4fJOZd?src=embed',
                     "State and territory breakdowns of daily confirmed cases"],
        ['https://e.infogram.com/7ffaebfa-000b-459d-b592-af45f9f2d9b7?src=embed',
                     "Cumulative view of confirmed cases of COVID-19 in Australia"],
        ['https://e.infogram.com/_/3osqzRmYBiJsJafg79YC?src=embed',
                     "Total number of COVID-19 tests in each state or territory"],
        ['https://e.infogram.com/_/LSHmqF53MnDNvZBbtn8K?src=embed',
                     "Daily confirmed cases in NSW by transmission source"],
        ['https://infogram.com/1prln2g3rxxd9dtgjnyq961zm1am620p011',
                     "Daily confirmed cases in Victoria by transmission source"],
        ['https://infogram.com/1p1jkdzd091j53amld9pk9ww6es6d1m7nnx',
                     "SA Cumulative view of transmission sources over time"],
        ['https://infogram.com/1pqmex9m36qznjfqjjd73n6p7gi0zgn013d',
                     "WA Cumulative view of unknown local and other transmission sources over time"],
        ['https://infogram.com/1px0k50nvw91yltqmwp706nnjqinrperkv7',
                     "Daily confirmed cases in Tasmania by transmission source"],
        ['https://infogram.com/1pkzv101w932qyh97g06g660x6u3jz3qkwx',
                     "Daily confirmed cases in ACT by transmission source"],
        ['https://infogram.com/1p93l75n7ypl97b71lwp3j3rrrh377qw32m',
                     "Daily confirmed cases in NT by transmission source"]
    ]
    for url, title in data_url_and_titles:
        data = CovidData(url, title)
        data.download_and_save()
