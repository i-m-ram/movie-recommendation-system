import pandas as pd
import numpy as np

import director
import convert_list
import cleaning_data
import joining

credit_df=pd.read_csv(r'E:\Projects\Movie recommendation System\DataSet\tmdb_5000_credits.csv')
movie_df=pd.read_csv(r'E:\Projects\Movie recommendation System\DataSet\tmdb_5000_movies.csv')

#movie_df.head()

#credit_df.head()

credit_df.columns=['id','title','cast','crew']

movie_df=movie_df.merge(credit_df,on='id')

#movie_df.head()

#movie_df.describe()

#movie_df.info()

from ast import literal_eval
features = ["cast", "crew", "keywords", "genres"]
for feature in features:
    movie_df[feature] = movie_df[feature].apply(literal_eval)
#movie_df[features].head(10)

#movie_df['cast'].head()


movie_df['Director']=movie_df['crew'].apply(director.get_director)

features = ["cast", "keywords", "genres"]
for feature in features:
    movie_df[feature] = movie_df[feature].apply(convert_list.get_list)

movie_df['title']=movie_df['original_title']

#movie_df[['title', 'cast', 'Director', 'keywords', 'genres']].head()

features = ['cast', 'keywords', 'Director', 'genres']
for feature in features:
    movie_df[feature] = movie_df[feature].apply(cleaning_data.clean_data)

#movie_df['cast'].head()


movie_df['soup']=movie_df.apply(joining.create_soup, axis=1)
#movie_df['soup'].head()


from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

count_vectorizer = CountVectorizer(stop_words='english')
count_matrix=count_vectorizer.fit_transform(movie_df['soup'])
#print(count_matrix.shape)
cosine_sim2 = cosine_similarity(count_matrix, count_matrix) 
#print(cosine_sim2.shape)

movie_df = movie_df.reset_index()
indices = pd.Series(movie_df.index, index=movie_df["title"]).drop_duplicates()
#print(indices.head())

def get_recommendations(title, cosine_sim):
    idx = indices[title]
    similarity_scores = list(enumerate(cosine_sim[idx]))
    similarity_scores= sorted(similarity_scores, key=lambda x: x[1], reverse=True)
    similarity_scores= similarity_scores[1:11]
    # (a, b) where a is id of movie, b is similarity_scores
    movie_indices = [ind[0] for ind in similarity_scores]
    movies = movie_df["title"].iloc[movie_indices]
    return movies

#print(get_recommendations("Iron Man 2", cosine_sim2))
Movie_name=str(input('Enter Movie Name'))
print(get_recommendations(Movie_name, cosine_sim2))
