import pandas as pd
import numpy as np
from scipy import sparse
from implicit.als import AlternatingLeastSquares

# 1. 데이터 받아오기. movie, rating, id 연결 위한 link
md = pd.read_csv('../../data/the-movies-dataset/movies_metadata.csv')
ratings = pd.read_csv('../../data/the-movies-dataset/ratings_small.csv')
link=pd.read_csv('../../data/the-movies-dataset/links.csv')
# print(md.head())
# print(ratings.head())
# print(link.head())
# movie data 필드별 null 개수
# print(md.isnull().sum())

# [[user별 높은 평점 매긴 영화 5개]]

# 2. movie와 rating movieId 기준으로 MERGING
# 2-1. movie 테이블의 id값과 맞추기 위해 rating, link merge
rating_id=ratings.merge(link,on='movieId')
# 2-2. 필요없는 필드 삭제 및 merge 위한 column 이름 동일하게 설정
rating_id = rating_id.drop(['movieId', 'imdbId'], axis=1).reset_index(drop=True)
rating_id.rename(columns=lambda x: x.replace('tmdbId', 'id'), inplace=True)
# 2-3. movie, rating id 기준으로 merge
movies_and_ratings = md.merge(rating_id, on='id')

# 3. 유저별 평점 평균
mean_rating = movies_and_ratings.groupby('userId')['rating'].mean()
movies_and_ratings['mean_rating'] = movies_and_ratings['userId'].apply(lambda x: mean_rating[x])

# 3-1. 평균 평점보다 높은 평점을 매긴 영화만 good_feedback으로 받아옴.
movies_and_ratings['good_rating'] = movies_and_ratings.apply(lambda x: x['rating'] if x['mean_rating'] <= x['rating'] else np.NaN, axis=1)

# pd.isnull( movies_and_ratings['good_rating'] ) == 0 : null이 아닌 것.
movies_and_ratings = movies_and_ratings[ pd.isnull( movies_and_ratings['good_rating'] ) == 0 ]
movies_and_ratings = movies_and_ratings.drop(['mean_rating', 'good_rating'], axis=1).reset_index(drop=True)

good_feedback = movies_and_ratings
good_feedback = movies_and_ratings.sort_values(['userId' ,'timestamp'], ascending=[True, False])

good_feedback_dict = {}
all_users = good_feedback['userId'].unique()

for user in all_users:
    top_movies = []
    for top in range(5):
        try:
            # user별 평균 평점보다 높게 평점 매긴 영화 중, 최근 영화 5개
            top_movies.append(good_feedback[good_feedback['userId']==user]['id'].values[top])
            good_feedback_dict[user] = top_movies
        except:
            continue

# print(good_feedback_dict)

# 4. 범주화
movies_and_ratings['userId'] = movies_and_ratings['userId'].astype("category").cat.codes
movies_and_ratings['id'] = movies_and_ratings['id'].astype("category").cat.codes

shape_0 = len(movies_and_ratings['id'].unique())
shape_1 = len(movies_and_ratings['userId'].unique())

users_act = movies_and_ratings.loc[:, ['userId','id']].reset_index(drop=True)
users_act['act'] = 1
print(users_act)

activity = list(users_act['act'])
cols = users_act['id'].astype(int)
rows = users_act['userId'].astype(int)

data_sparse = sparse.csr_matrix((activity, (rows, cols)), shape=(shape_1, shape_0))
print(data_sparse)

# ALS 방식
algo_0 = AlternatingLeastSquares(factors=50)
algo_0.fit(data_sparse)

userid = 2
user_items = data_sparse.T.tocsr()
print(user_items)
recommendations = algo_0.recommend(userid, user_items, N=15)
print(recommendations)

recommendations_list = []
for i in recommendations:
    recommendations_list.append(i[0])

print(recommendations_list)
print(md.iloc[recommendations_list]['genres'])

# [[ KNN 모델 훈련 ]]

