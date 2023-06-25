import pandas as pd
import spacy
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import warnings
warnings.filterwarnings('ignore')

nlp = spacy.load('en_core_web_lg')
data = pd.read_csv(r'top_1000_popular_movies_tmdb.csv', engine='python')

data = data.iloc[:, 1:]

movies = data[['id', 'title', 'genres', 'overview']]
movies['genres'] = movies['genres'].apply(lambda x: x.replace('[', '').replace(']', '').replace("'", ''))
movies['tags'] = movies['overview'] + movies['genres']
movies = movies.drop(columns=['overview', 'genres'])

titles = movies['title'].apply(lambda x: nlp(x)).to_numpy()

cv = CountVectorizer(max_features=10000,
                     stop_words='english')

vector = cv.fit_transform(movies['tags'].values.astype(str)).toarray()

sim = cosine_similarity(vector)


def select_title(user_inp):
    similar_names = [(title,title.similarity(user_inp)) for title in titles]
    similar_names.sort(reverse=True, key=lambda e:e[1])

    return similar_names[:5]


def similar_movies(mov_title):
    movie_index = movies[movies['title'] == mov_title].index
    list_of_sim = list(enumerate(sim[movie_index[0]]))
    list_of_sim.sort(reverse=True, key=lambda e:e[1])

    recommended_10 = [(movies.iloc[tpl[0]].title, *tpl) for tpl in list_of_sim[1:10]]
    return recommended_10

