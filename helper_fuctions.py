import nltk
from nltk import WordNetLemmatizer
from nltk.corpus import stopwords


def remove_contractions(tokens):
    contractions = ["'ll", "'s", "'d", "'m", "'re", "'ve", "'t", "'em", "n't", "'"]
    filtered_tokens = [token for token in tokens if token.lower() not in contractions]
    return filtered_tokens


def remove_short(tokens):
    filtered_tokens = [token for token in tokens if len(token) > 2]
    return filtered_tokens


def read_file(filename):
    with open(filename, 'r') as file:
        text = file.read()
    return text.lower()


def lemmatization(tokens):
    lemmatizer = WordNetLemmatizer()
    tokens_lemmatized = [lemmatizer.lemmatize(token) for token in tokens]
    return tokens_lemmatized


def remove_stopwords(tokens):
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [token for token in tokens if token.lower() not in stop_words]
    return filtered_tokens


def get_tokens(text):
    tokens = nltk.word_tokenize(text)
    tokens_without_stopwords = remove_stopwords(tokens)
    tokens_without_contractions = remove_contractions(tokens_without_stopwords)
    tokens_without_short = remove_short(tokens_without_contractions)
    tokens_lemmatized = lemmatization(tokens_without_short)
    return tokens_lemmatized
