'''
In this module you will find all the functions needed to preprocess the data. You can either use it one by one in
your pipeline or use directly `preprocess_data()` which will apply all of them indiscriminately.
However be careful with the order of the filters!
'''

import re
import contractions
import random


def data_preprocessing(text):

    if text == None:
        return
    else:
        return remove_others(
            remove_metacharachters(
             remove_hashtag(
               substitute_backlash(
                remove_emojis(
                    remove_urls(
                          remove_punctuation(
                            substitute_amp(
                                remove_gt(
                                    contractions.fix(
                                        text.lower()
                                    ))))))))))


def test_preprocessing(dataframe, num_samples, func, seed = 121):
    random.seed(seed)
    indices = random.sample(list(range(0, len(dataframe))), num_samples, )
    row_list = dataframe.iloc[indices]['body'].tolist()

    for i, text in enumerate(row_list):
        print(indices[i])
        print('Input: \t', text, end='\n')
        print('Output: \t', func(text)  , end='\n')
        print('\t --- \t')



def remove_metacharachters(text):

    pattern = re.compile(r'[\n\t]\S+')

    return re.sub(pattern, ' ', text)


def substitute_backlash(text):

    pattern = re.compile(r'/')

    return re.sub(pattern, ' ', text)

def remove_others(text):

    rt = re.compile('(rt)+\s')

    return re.sub(rt, '', text)

def remove_emojis(text):
    emoj = re.compile("["
                      u"\U0001F600-\U0001F64F"  # emoticons
                      u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                      u"\U0001F680-\U0001F6FF"  # transport & map symbols
                      u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                      u"\U00002500-\U00002BEF"  # chinese char
                      u"\U00002702-\U000027B0"
                      u"\U00002702-\U000027B0"
                      u"\U000024C2-\U0001F251"
                      u"\U0001f926-\U0001f937"
                      u"\U00010000-\U0010ffff"
                      u"\u2640-\u2642"
                      u"\u2600-\u2B55"
                      u"\u200d"
                      u"\u23cf"
                      u"\u23e9"
                      u"\u231a"
                      u"\ufe0f"  # dingbats
                      u"\u3030"
                      "]+", re.UNICODE)
    return re.sub(emoj, '', text)

def remove_urls(text):
    urls = re.compile(r'http\S+')

    return re.sub(urls, '', text)

def remove_hashtag(text):
    hashtag = re.compile(r"#\S+")

    return re.sub(hashtag, '', text)

def remove_user(text):
    user = re.compile(r"@\S+")

    return re.sub(user, '', text)

def remove_punctuation(text):
    punct = re.compile(r"[^a-zA-Z0-9_\-\'\’/$%#\s]")

    return re.sub(punct, '', text)

def substitute_amp(text):
    pattern = re.compile('&amp')

    return re.sub(pattern, 'and', text)

def remove_gt(text):
    pattern = re.compile('&gt')

    return re.sub(pattern, '', text)