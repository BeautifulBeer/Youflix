import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from ast import literal_eval
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity
from nltk.stem.snowball import SnowballStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import wordnet
from surprise import Reader, Dataset, SVD
from sklearn.model_selection import cross_validate

import warnings; warnings.simplefilter('ignore')

md = pd.read_csv('input/movies_metadata.csv')
print(md.head())
print("================================================================================")
print(md.isnull().sum())
print("================================================================================")
print(md.describe())
print("================================================================================")

md['genres'] = md['genres'].fillna('[]').apply(literal_eval).apply(lambda x : [i['name'] for i in x] if isinstance(x, list) else [])

print(md['genres'])
print("================================================================================")

vote_count = md[md['vote_count'].notnull()]['vote_count'].astype('int')
vote_average = md[md['vote_average'].notnull()]['vote_average'].astype('int')
m = vote_count.quantile(0.95) #quanitle은 4분위 데이터를 말한건데 0.95는 95% 부터의 데이터를 의미한다.
C = vote_average.mean()

md['year'] = md['release_date'].apply(lambda x : str(x).split('-')[0] if x != np.nan else np.nan)

qualified = md[(md['vote_count'].notnull()) & (md['vote_average'].notnull()) & (md['vote_count'] >= m)][['title', 'year', 'vote_count', 'vote_average', 'popularity', 'genres']]
qualified['vote_count'] = qualified['vote_count'].astype(int)
qualified['vote_average'] = qualified['vote_average'].astype(int)

def weight_rate(x):
    v = x['vote_count']
    r = x['vote_average']
    return (v / (v + m)*r) + (m/(m+v)*C)

qualified['wr'] = qualified.apply(weight_rate, axis=1)
qualified = qualified.sort_values(by='wr', ascending=False)

print(qualified.head(10))
print("================================================================================")

s = md.apply(lambda x: pd.Series(x['genres']), axis=1).stack().reset_index(level=1, drop=True)
s.name = 'genres'
s_gen = md.drop('genres', axis=1).join(s)

def chart_bar(genre, percenTage=0.85):
    df = s_gen[s_gen['genres'] == genre]
    vote_count = df[df['vote_count'].notnull()]['vote_count'].astype(int)
    vote_average = df[df['vote_average'].notnull()]['vote_average'].astype(int)
    m = vote_count.quantile(percenTage)
    c = vote_average.mean()

    qualified = df[(df['vote_count'].notnull()) & (df['vote_count'] >= m) & (df['vote_average'].notnull())][['title', 'year', 'vote_count', 'vote_average', 'popularity']]
    qualified['vote_count'] = qualified['vote_count'].astype('int')
    qualified['vote_average'] = qualified['vote_average'].astype('int')
    qualified['wr'] = qualified.apply(lambda x: (x['vote_count'] / (x['vote_count'] + m)*x['vote_average']) + (m/(m+x['vote_count'])*c), axis=1)
    qualified = qualified.sort_values('wr', ascending=False)
    return qualified

print(chart_bar('Romance').head(3))
print("================================================================================")
print(chart_bar('Adventure').head(3))
print("================================================================================")

link_small = pd.read_csv('input/links_small.csv')
link_small = link_small[link_small['tmdbId'].notnull()]['tmdbId'].astype('int')
md = md.drop([19730, 29503, 35587])
md['id'] = md['id'].astype('int')
smd = md[md['id'].isin(link_small)]

smd['tagline'] = smd['tagline'].fillna('')
smd['description'] = smd['overview'] + smd['tagline']
smd['description'].fillna('')

tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 2), min_df=0, stop_words='english')

print(smd['description'].fillna(' '))
print("================================================================================")

tfidf_matrix = tf.fit_transform(smd['description'].values.astype('U'))

cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
cosine_sim[0]

print(cosine_sim[0])
print("================================================================================")

smd = smd.reset_index()
titles = smd['title']
indces = pd.Series(smd.index, index=titles)

def getrecommandations(title):
    index = indces[title]
    sim_scores = list(enumerate(cosine_sim[index]))
    sim_scores = sorted(sim_scores, key=lambda x:x[1], reverse=True)
    sim_scores = sim_scores[1:31]
    movie_indices = [i[0] for i in sim_scores]
    return titles.iloc[movie_indices]

print(list(enumerate(cosine_sim[0])))
print(getrecommandations('The Dark Knight'))
print("================================================================================")

credits = pd.read_csv('input/credits.csv')
keywords = pd.read_csv('input/keywords.csv')

keywords['id'] = keywords['id'].astype(int)
credits['id'] = credits['id'].astype(int)
md['id'] = md['id'].astype(int)

md = md.merge(credits, on='id')
md = md.merge(keywords, on='id')
smd = md[md['id'].isin(link_small)]

smd['cast'] = smd['cast'].apply(literal_eval) #cast데이터를 ''문자열안에 있는 document를
smd['crew'] = smd['crew'].apply(literal_eval) #진짜 document로 만든다.
smd['keywords'] = smd['keywords'].apply(literal_eval)
smd['cast_size'] = smd['cast'].apply(lambda x :len(x)) #배우 수를 적는다.
smd['crew_size'] = smd['crew'].apply(lambda x: len(x)) #스태프 수를 적는다.

def get_director(x):
    for i in x:
        if i['job'] == 'Director':
            return i['name']
    return np.nan

smd['director'] = smd['crew'].apply(get_director)
smd['cast'] = smd['cast'].apply(lambda x : [i['name'] for i in x] if isinstance(x, list) else [])
smd['cast'] = smd['cast'].apply(lambda x: x[:3] if len(x) >3 else x)

smd['keywords'] = smd['keywords'].apply(lambda x: [i['name'] for i in x] if isinstance(x, list) else [])
smd['cast'] = smd['cast'].apply(lambda x : [str.lower(i.replace(" ", "")) for i in x])
smd['director'] = smd['director'].astype(str).apply(lambda x: str.lower(x.replace(" ", "")))
smd['director'] = smd['director'].apply(lambda x: [x, x, x])

s = smd.apply(lambda x: pd.Series(x['keywords']), axis=1).stack().reset_index(level=1, drop=True)
s.name = 'keywords'
s = s.value_counts()

print(s)
print("================================================================================")

s = s[s>1]
stemmer = SnowballStemmer('english')
stemmer.stem('dogs')

def filter_keywords(x):
    words = []
    for i in x:
        if i in s:
            words.append(i)
    return words

smd['keywords'] = smd['keywords'].apply(filter_keywords)
smd['keywords'] = smd['keywords'].apply(lambda x :[stemmer.stem(i) for i in x])
smd['keywords'] = smd['keywords'].apply(lambda x: [str.lower(i.replace(" ", "")) for i in x])
smd['soup'] = smd['keywords']+smd['cast']+smd['director']+smd['genres']
smd['soup'] = smd['soup'].apply(lambda x: ' '.join(x))
count = CountVectorizer(analyzer='word', ngram_range=(1, 2), min_df=0, stop_words='english')
count_matrix = count.fit_transform(smd['soup'])
cosine_sim = cosine_similarity(count_matrix, count_matrix)

smd = smd.reset_index()
titles = smd['title']
indces = pd.Series(smd.index, index=smd['title'])

print(getrecommandations('The Dark Knight'))

def getrecommandations(title):
    index = indces[title]
    sim_scores = list(enumerate(cosine_sim[index]))
    sim_scores = sorted(sim_scores, key=lambda x:x[1], reverse=True)
    sim_scores = sim_scores[1:31]
    movie_indices = [i[0] for i in sim_scores]
    return titles.iloc[movie_indices]


# reader = Reader()
# ratings = pd.read_csv('input/ratings_small.csv')
#
# print("================================================================================")
# print("================================협업필터링======================================")
# print(ratings.head())
# print("================================================================================")
#
# data = Dataset.load_from_df(ratings[['userId', 'movieId', 'rating']], reader)
#
# # data.load_from_folds(5, reader)
# # svd = SVD()
# # evaluate(svd, data, measures=['RMSE', 'MAE'])
#
# grid_search = cross_validate(SVD, data, measures=['RMSE', 'MAE'])
# print(grid_search)