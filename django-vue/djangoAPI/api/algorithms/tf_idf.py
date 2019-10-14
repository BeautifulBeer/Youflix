# 카운트 기반의 단어 표현(Count Based Work Representation)
#
#       종류>
#           1. 국소 표현(Local Representation) : 해당 단어 그 자체만 보고, 특정값을 맵핑하여 단어를 표현하는 방법
#           2. 분산 표현(Distributed Representation) : 단어를 표현하고자 주변을 참고하여 단어를 표현하는 방법
#
#           EX)
#               puppy(강아지), cute(귀여운), lovely(사랑스러운)이라는 단어가 있을 때,
#               각 단어에 1번, 2번, 3번 등과 같은 숫자를 mapping한다면 이는 국소 표현 방법에 해당
#
#               분산 표현은 해당 단어를 표현하기 위해 주변 단어를 참고합니다. 
#               puppy(강아지)라는 단어 근처에는 주로 cute(귀여운), lovely(사랑스러운)이라는 단어가 자주 등장하므로, puppy라는 단어는 cute, lovely한 느낌이다로 단어를 정의합니다. 
#               이렇게 되면 이 두 방법의 차이는 국소 표현 방법은 단어의 의미, 뉘앙스를 표현할 수 없지만, 분산 표현 방법은 단어의 뉘앙스를 표현할 수 있게 됩니다.
#           
#           
# Bag of Words(BoW)
#
#       - 단어의 등장 순서를 고려하지 않는 빈도수 기반의 단어 표현 방법입니다.
#       
#       Bow를 만드는 과정
#           1. 우선, 각 단어에 교유한 인덱스를 부여합니다.
#           2. 각 인덱스의 위치에 단어 토큰의 등장 횟수를 기록한 벡터를 만듭니다.
#
from konlpy.tag import Okt
import re
okt=Okt()

token = re.sub("(\.)","","정부가 발표하는 물가상승률과 소비자가 느끼는 물가상승률은 다르다.")
# 정규 표현식을 통해 온점을 제거하는 정제 작업입니다.
token = okt.morphs(token)
# OKT 형태소 분석기를 통해 토큰화 작업을 수행한 뒤에, token에다가 넣습니다.

word2index={}
bow=[]

for voca in token:
        if voca not in word2index.keys():
            word2index[voca] = len(word2index)
            # token을 읽으면서, word2index에 없는 (not in) 단어는 새로 추가하고, 이미 있는 단어는 넘깁니다.   
             bow.insert(len(word2index)-1,1)
            # BoW 전체에 전부 기본값 1을 넣어줍니다. 단어의 개수는 최소 1개 이상이기 때문입니다.
        else:
            index = word2index.get(voca)
            # 재등장하는 단어의 인덱스를 받아옵니다.
            bow[index]=bow[index]+1
            # 재등장한 단어는 해당하는 인덱스의 위치에 1을 더해줍니다. (단어의 개수를 세는 것입니다.)
print(word2index)

#!/usr/bin/env python
# coding: utf-8

# TF-IDF(Term Frequency-Inverse Document Frequency)
# TF-IDF는 주로 문서의 유사도를 구하는 작업, 검색 시스템에서 검색 결과의 중요도를 정하는 작업, 문서 내에서 특정 단어의 중요도를 구하는 작업 등에 쓰일 수 있습니다.

# TF-IDF는 TF와 IDF를 곱한 값을 의미하는데 이를 식으로 표현해보겠습니다. 문서를 d, 단어를 t, 문서의 총 개수를 n이라고 표현할 때 TF, DF, IDF는 각각 다음과 같이 정의할 수 있습니다.

# (1) tf(d,t) : 특정 문서 d에서의 특정 단어 t의 등장 횟수.
# 생소한 글자때문에 어려워보일 수 있지만, 잘 생각해보면 TF는 이미 앞에서 구한 적이 있습니다. TF는 앞에서 배운 DTM의 예제에서 각 단어들이 가진 값들입니다. DTM이 각 문서에서의 각 단어의 등장 빈도를 나타내는 값이었기 때문입니다.

# (2) df(t) : 특정 단어 t가 등장한 문서의 수.
# 여기서 특정 단어가 각 문서, 또는 문서들에서 몇 번 등장했는지는 관심가지지 않으며 오직 특정 단어 t가 등장한 문서의 수에만 관심을 가집니다. 앞서 배운 DTM에서 바나나는 문서2와 문서3에서 등장했습니다. 이 경우, 바나나의 df는 2입니다. 문서3에서 바나나가 두 번 등장했지만, 그것은 중요한 게 아닙니다. 심지어 바나나란 단어가 문서2에서 100번 등장했고, 문서3에서 200번 등장했다고 하더라도 바나나의 df는 2가 됩니다.

# (3) idf(d, t) : df(t)에 반비례하는 수.
# idf(d,t)=log(n1+df(t))
# IDF라는 이름을 보고 DF의 역수가 아닐까 생각했다면, IDF는 DF의 역수를 취하고 싶은 것이 맞습니다. 
# 그런데 log와 분모에 1을 더해주는 식에 의아하실 수 있습니다. 
# log를 사용하지 않았을 때, IDF를 DF의 역수(n / df(t)라는 식)로 사용한다면 총 문서의 수 n이 커질 수록, IDF의 값은 기하급수적으로 커지게 됩니다. 그렇기 때문에 log를 사용합니다.

# TF-IDF는 모든 문서에서 자주 등장하는 단어는 중요도가 낮다고 판단하며, 특정 문서에서만 자주 등장하는 단어는 중요도가 높다고 판단합니다. 
# TF-IDF 값이 낮으면 중요도가 낮은 것이며, TF-IDF 값이 크면 중요도가 큰 것입니다. 
# 즉, the나 a와 같이 불용어의 경우에는 모든 문서에 자주 등장하기 마련이기 때문에, 
# 자연스럽게 불용어의 TF-IDF의 값은 다른 단어의 TF-IDF에 비해서 낮아지게 됩니다.

# from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer

corpus = [
    
    'you know I want your love',
    'I like you',
    'what should I do ',
]
# vector = CountVectorizer()
tfidfv = TfidfVectorizer().fit(corpus)
print(tfidfv.transform(corpus).toarray())
print(tfidfv.vocabulary_)
# print(vector.fit_transform(corpus).toarray())
# print(vector.vocabulary_)


# 코사인 유사도(Cosine Similarity)
from numpy import dot
from numpy.linalg import norm

import numpy as np

def cos_sim(A, B):
    return dot(A, B) / (norm(A) * norm(B))


doc1 = np.array([0, 1, 1, 1])
doc2 = np.array([1, 0, 1, 1])
doc3 = np.array([2, 0, 1, 2])

print(cos_sim(doc1, doc2)) #문서1과 문서2의 코사인 유사도
print(cos_sim(doc1, doc3)) #문서1과 문서3의 코사인 유사도
print(cos_sim(doc2, doc3)) #문서2과 문서3의 코사인 유사도


import pandas as pd


data = pd.read_csv('./meta_data/movies_metadata.csv', low_memory=False)
data.head(2)

data=data.head(20000)
data['overview'].isnull().sum()
data['overview'] = data['overview'].fillna('')

# TF-IDF 실행
from sklearn.feature_extraction.text import TfidfVectorizer
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(data['overview'])

print(tfidf_matrix.shapeape)


# overview 열에 대해서 tf-idf를 수행했습니다. 
# 20,000개의 영화를 표현하기위해 총 47,487개의 단어가 사용되었음을 보여주고 있습니다. 
# 이제 코사인 유사도를 사용하면 바로 문서의 유사도를 구할 수 있습니다.

from sklearn.metrics.pairwise import linear_kernel
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)


indices = pd.Series(data.index, index = data['title']).drop_duplicates()
print(indices.head())


idx = indices['Father of the Bride Part II']
print(idx)


def get_recommendations(title, cosine_sim=cosine_sim):
    
    idx = indices[title]
    
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]
    movie_indices = [i[0] for i in sim_scores]
    return data['title'].iloc[movie_indices]

get_recommendations('The Dark Knight Rises')

