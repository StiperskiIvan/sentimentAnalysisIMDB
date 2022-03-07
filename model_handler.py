from keras.models import load_model
from keras.preprocessing.sequence import pad_sequences
from nltk.corpus import stopwords
import re
from keras.preprocessing.text import Tokenizer
import nltk
import pandas as pd


nltk.download('stopwords')
data = pd.read_csv('IMDB Dataset.csv')
english_stops = set(stopwords.words('english'))
padding_length = 2494


def load_dataset():
    df = pd.read_csv('IMDB Dataset.csv')
    dataset = df['review']

    # PRE-PROCESS REVIEW
    dataset = dataset.replace({'<.*?>': ''}, regex=True)  # remove html tag
    dataset = dataset.replace({'[^A-Za-z]': ' '}, regex=True)  # remove non alphabet
    dataset = dataset.apply(lambda review: [w for w in review.split() if w not in english_stops])  # remove stop words
    dataset = dataset.apply(lambda review: [w.lower() for w in review])  # lower case

    return dataset


def model_loader(model_path):
    model = load_model(model_path)
    return model


x_data = load_dataset()


def predict_result(input_review, model):

    token = Tokenizer(lower=False)
    token.fit_on_texts(x_data)
    regex = re.compile(r'[^a-zA-Z\s]')
    review = input_review
    review = regex.sub('', review)

    words = review.split(' ')
    filtered = [w for w in words if w not in english_stops]
    filtered = ' '.join(filtered)
    filtered = [filtered.lower()]

    tokenize_words = token.texts_to_sequences(filtered)
    if len(filtered) < padding_length:
        tokenize_words = pad_sequences(tokenize_words, maxlen=len(filtered), padding='post', truncating='post')
    else:
        tokenize_words = pad_sequences(tokenize_words, maxlen=padding_length, padding='post', truncating='post')
    try:
        prediction = model.predict(tokenize_words)

        if prediction >= 0.4:
            result = 'Positive'
        else:
            result = 'Negative'
        return result

    except:
        result = []
        return result
