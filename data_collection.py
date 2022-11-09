import yaml
import requests
import pandas as pd
import json
## read config

def get_ticker_list():
    with open("config.yaml", 'r') as fp:
        yaml_content = yaml.safe_load(fp)

    return yaml_content['ticker']

def get_ticker_string():
    ticker_list = get_ticker_list()
    ticker_string = ''
    for i in ticker_list:
        ticker_string += i+','
    ticker_string = ticker_string.rstrip(',')
    return ticker_string

def send_request(url = '', method = 'GET'):
    api_response = None
    if method == "GET":
        api_response = requests.get(url)
    elif method == "POST":
        api_response = requests.post(url)
    
    return api_response


def get_store_twitter_data():
    api_url = 'https://eodhistoricaldata.com/api/tweets-sentiments?s=<PLACEHOLDER>&from=2020-01-01&to=2022-11-01&api_token=demo'

    ticker_string = get_ticker_string()
    api_url = api_url.replace('<PLACEHOLDER>', ticker_string)
    print(api_url)

    api_response = send_request(api_url)

    with open("./data/api_response.json", 'w+') as fp:
        fp.write(api_response.text)

    with open("./data/api_response.json", 'r') as fp:
        json_file = json.load(fp)
        df = pd.DataFrame(json_file)
        # print(df)
        date_list = []
        count = []
        normalize = []
        for i, row in df.iterrows():
            date_list.append(row[0]['date'])
            count.append(row[0]['count'])
            normalize.append(row[0]['normalized'])
        
        df = pd.DataFrame({'date': date_list, 'count': count, 'normalized': normalize})
        print(df)
        df.to_csv("./data/sentiment_data.csv", index = False)

def get_store_historical_data():
    api_url = 'https://eodhistoricaldata.com/api/eod/<PLACEHOLDER>.US?api_token=demo'

    ticker_string = get_ticker_string()
    api_url = api_url.replace('<PLACEHOLDER>', ticker_string)
    print(api_url)

    api_response = send_request(api_url)

    with open("./data/hist_data.csv", 'w+') as fp:
        fp.write(api_response.text)


if __name__ == "__main__":
    get_store_twitter_data()
    get_store_historical_data()
