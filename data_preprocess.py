import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


SENTIMENT_DATA_FILE = './data/sentiment_data.csv'
HIST_DATA_FILE = './data/hist_data.csv'
START_DATE = '2020-01-01'
END_DATE = '2022-11-01'

def preprocess_sentiment_data():
    df = pd.read_csv(SENTIMENT_DATA_FILE)
    df.rename(columns = {'date':'Date'}, inplace = True)
    df.Date = pd.to_datetime(df.Date)
    df.sort_values(by=['Date'], inplace = True)
    # print(df.info())
    return df

def preprocess_historical_data():
    df = pd.read_csv(HIST_DATA_FILE)
    df.Date = pd.to_datetime(df.Date)
    df = df[(df.Date >= pd.to_datetime(START_DATE)) & (df.Date <= pd.to_datetime(END_DATE))]
    # print(df.info())
    return df

def merge_data(df1= None, df2 =None):
    df = pd.merge(df1, df2, on=['Date'])
    df.set_index("Date", inplace = True)
    df = df[["count", "normalized", "Close", "Adjusted_close", "Volume"]]
    print(df)
    return df

def plot_normalized_to_close(df=None):
    tips = sns.load_dataset("tips")
    print(tips)
    # ax = sns.stripplot(data = tips)
    ax = sns.scatterplot(data=df, y = "normalized", x="Close")
    ax.set(xlabel ='price', ylabel ='normalized')
    plt.title('My first graph')
    plt.show()


if __name__ == "__main__":
    senti_df = preprocess_sentiment_data()
    hist_df  = preprocess_historical_data()
    merged_df = merge_data(senti_df, hist_df)
    merged_df.to_csv("./data/merged_data.csv", index =False)
    # normalized = merged_df.normalized.to_list()
    # close = merged_df.Close.to_list()
    # plot_normalized_to_close(merged_df)
