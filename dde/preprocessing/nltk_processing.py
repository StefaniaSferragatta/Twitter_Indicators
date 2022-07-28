from nltk.stem import WordNetLemmatizer
from nltk import pos_tag
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet
from nltk.corpus import stopwords


def lemmatize(text):
    wnl = WordNetLemmatizer()

    sentence_with_pos = pos_tag(word_tokenize(text))

    lemmatized_text = []
    for word_pos in sentence_with_pos:
        lemmatized_text.append(wnl.lemmatize(word_pos[0], pos=get_wordnet_pos(word_pos[1])))

    return lemmatized_text



def get_wordnet_pos(treebank_tag):

    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return 'n'


def remove_stopwords(tokenized_text):

    stop_words = set(stopwords.words('english')).add('\n')

    return [word for word in tokenized_text if not word in stop_words]