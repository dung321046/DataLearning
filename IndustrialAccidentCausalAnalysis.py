import holoviews as hv
import numpy as np
import pandas as pd
from holoviews import opts
from nltk import tokenize, stem

hv.extension('bokeh')
import nltk
nltk.download('wordnet')
nltk.download('punkt')
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from wordcloud import STOPWORDS
import shap

shap.initjs()

df = pd.read_csv(
    "./input/IndustrialSafety/IHMStefanini_industrial_safety_and_health_database_with_accidents_description.csv")

df.drop("Unnamed: 0", axis=1, inplace=True)
df.rename(
    columns={'Data': 'Date', 'Countries': 'Country', 'Genre': 'Gender', 'Employee or Third Party': 'Employee type'},
    inplace=True)
df.head(3)

df['Date'] = pd.to_datetime(df['Date'])
df['Year'] = df['Date'].apply(lambda x: x.year)
df['Month'] = df['Date'].apply(lambda x: x.month)
df['Day'] = df['Date'].apply(lambda x: x.day)
df['Weekday'] = df['Date'].apply(lambda x: x.day_name())
df['WeekofYear'] = df['Date'].apply(lambda x: x.weekofyear)
df.head(3)


def month2seasons(x):
    if x in [9, 10, 11]:
        season = 'Spring'
    elif x in [12, 1, 2]:
        season = 'Summer'
    elif x in [3, 4, 5]:
        season = 'Autumn'
    elif x in [6, 7, 8]:
        season = 'Winter'
    return season


df['Season'] = df['Month'].apply(month2seasons)
df.head(3)
STOPWORDS.update(["cm", "kg", "mr", "wa", "nv", "ore", "da", "pm", "am", "cx"])
print(STOPWORDS)


def nlp_preprocesser(row):
    sentence = row.Description
    # convert all characters to lowercase
    lowered = sentence.lower()
    tok = tokenize.word_tokenize(lowered)

    # lemmatizing & stemming
    lemmatizer = stem.WordNetLemmatizer()
    lem = [lemmatizer.lemmatize(i) for i in tok if i not in STOPWORDS]
    stemmer = stem.PorterStemmer()
    stems = [stemmer.stem(i) for i in lem if i not in STOPWORDS]

    # remove non-alphabetical characters like '(', '.' or '!'
    alphas = [i for i in stems if i.isalpha() and (i not in STOPWORDS)]
    return " ".join(alphas)


df['Description_processed'] = df.apply(nlp_preprocesser, axis=1)
df.head(3)


def sentiment2score(text):
    analyzer = SentimentIntensityAnalyzer()
    sent_score = analyzer.polarity_scores(text)["compound"]
    return float(sent_score)


df['Description_sentiment_score'] = df['Description'].apply(lambda x: sentiment2score(x))
df.head(3)

cr_risk_cnt = np.round(df['Critical Risk'].value_counts(normalize=True) * 100)
hv.Bars(cr_risk_cnt[::-1]).opts(title="Critical Risk Count", color="green", xlabel="Critical Risks",
                                ylabel="Percentage", xformatter='%d%%') \
    .opts(opts.Bars(width=600, height=600, tools=['hover'], show_grid=True, invert_axes=True))
