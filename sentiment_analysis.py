import sklearn as sk
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier

MERGED_FILE = './data/merged_data.csv'
TEST_SPLIT = 0.8

df = pd.read_csv(MERGED_FILE)
df.drop(["Close"], axis =1, inplace = True)
# print(df.describe())


df['Sentiment'] = np.where(df.normalized > 0.05, np.where(df.normalized > 0.11, "POSITIVE", "NEUTRAL"), "NEGATIVE")
# print(df['Sentiment'].value_counts())
# print(df)
new_df = pd.get_dummies(df, columns = ["Sentiment"])
# print(new_df)

new_df["Stock Trend"] = new_df["Adjusted_close"].diff()
# print(new_df)
new_df.dropna(inplace= True, axis =0)
print(new_df)
new_df["Stock Trend"] = np.where(new_df["Stock Trend"] > 0.0, 1, 0)
# print(new_df)


## split data into train and test
X_train = new_df[:int(TEST_SPLIT * len(new_df)) ]
X_test = new_df[int(TEST_SPLIT * len(new_df)): ]

Y_train = new_df["Stock Trend"][:int(TEST_SPLIT * len(new_df)) ]
Y_test = new_df["Stock Trend"][int(TEST_SPLIT * len(new_df)): ]
# print(Y_test)
##

scaler = StandardScaler()
scaler.fit(new_df)
print(scaler.mean_)
scaled_data = scaler.transform(new_df)
# print(scaled_data)


clf = RandomForestClassifier(max_depth=2, random_state=0)
clf.fit(X_train, Y_train)

score =clf.score(X_test, Y_test)
print(score)

