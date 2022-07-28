import numpy as np
import pandas as pd

def fill_time_series_data(time_series_df, groupby_df_topic, key):

    for id, row in groupby_df_topic.iterrows():

        for sentiment in row['Max_SentimentCol']:

            if sentiment == 'Negative Sentiment':
                time_series_df.at[id, key][0] = row['Max_SentimentValue'][row['Max_SentimentCol'].index('Negative Sentiment')]

            if sentiment == 'Neutral Sentiment':
                time_series_df.at[id, key][1] = row['Max_SentimentValue'][row['Max_SentimentCol'].index('Neutral Sentiment')]

            if sentiment == 'Positive Sentiment':
                time_series_df.at[id, key][2] = row['Max_SentimentValue'][row['Max_SentimentCol'].index('Positive Sentiment')]

    return time_series_df



def preprocess_df_time_series(df_topic):
    tmp1 = df_topic.groupby(['Max_SentimentCol', 'YM'])[
        ['Max_SentimentValue', 'id']].agg(lambda x: list(x)).reset_index()

    tmp2 = tmp1.copy()
    tmp2['Max_SentimentValue'] = tmp1['Max_SentimentValue'].apply(lambda x: np.mean(x))

    tmp3 = tmp2.groupby(['YM'])[
        ['Max_SentimentCol', 'Max_SentimentValue', 'id']].agg(lambda x: list(x)).reset_index()

    return tmp3


def prepare_data_for_sklearn(train_feature_df, test_feature_df, inflation_data):

    if train_feature_df.ndim == 1:
        X_train = np.array([a for a in train_feature_df.to_numpy()])
    else:

        train_feature_df = train_feature_df.drop('ym', axis = 1, errors = 'ignore')
        num_columns = len(train_feature_df.columns)

        train_feature_df = train_feature_df.to_numpy()
        X_train = np.empty([len(train_feature_df), num_columns*3])
        counter = 0



        for column in train_feature_df.T[:,]:
            tmp = np.array([a for a in column])
            X_train[:, counter:counter+3] = tmp
            counter += 3

    if test_feature_df.ndim == 1:
        X_test = np.array([a for a in test_feature_df.to_numpy()])
    else:
        test_feature_df = test_feature_df.drop('ym', axis = 1, errors = 'ignore')
        num_columns = len(test_feature_df.columns)

        test_feature_df = test_feature_df.to_numpy()
        X_test = np.empty([len(test_feature_df), num_columns*3])
        counter = 0

        for column in test_feature_df.T[:,]:
            tmp = np.array([a for a in column])
            X_test[:, counter:counter+3] = tmp
            counter += 3

    y = inflation_data['T10YIEM'].to_numpy()

    return X_train, X_test, y

def prepare_data_for_plotting(X_train, X_test, inflation_data, model, split_index = 67):

    Y = inflation_data.set_index( pd.to_datetime(inflation_data['DATE']))
    Y = Y.drop(['DATE'], axis = 1)

    Y_pred_train = pd.Series(model.predict(X_train), index = pd.to_datetime(inflation_data.iloc[0:split_index]['DATE']))
    Y_pred_test = pd.Series(model.predict(X_test), index = pd.to_datetime(inflation_data.iloc[split_index:]['DATE']))

    return Y, Y_pred_train, Y_pred_test
