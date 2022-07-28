import pandas as pd

def add_topic_label(topic_matrix, df):

    df_topic_matrix = pd.DataFrame(topic_matrix)
    df_topic_matrix['Max'] = df_topic_matrix[df_topic_matrix.columns].idxmax(axis = 1)
    df['Max'] = df_topic_matrix['Max']

    return df

def filter_by_topic(df, topic_number: float):
    return df[df['Max'] == topic_number]