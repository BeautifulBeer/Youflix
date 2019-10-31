from rest_framework import status
from rest_framework.decorators import api_view

from django.http import JsonResponse

from api.models import Movie, User, Profile, Rating, UserCluster,Profile

from sklearn.cluster import KMeans
from collections import Counter

import pandas as pd
import numpy as np

import json
import os
import sys

BASE_DIR = os.path.dirname(
            os.path.dirname(
                    os.path.dirname(
                            os.path.abspath(__file__)
                    )
            )
        )

url = os.path.join(BASE_DIR, 'data', 'mapper')
latent_user = np.load(os.path.join(url, 'latent_user.npy'))
user_mapper = open(os.path.join(url, 'userMapper.json')).read()
# mapper / KEY:userid, value: index
user_mapper = json.loads(user_mapper)


@api_view(['GET'])
def C_Cluster(request):
    # 주기적으로 할 예정
    # user Cluster
    # kmeans 클러스터링
    kmeans = KMeans(n_clusters=7).fit(latent_user)

    df = pd.DataFrame(latent_user)
    df['cluster'] = kmeans.labels_
    print(df)

    for userid, index in user_mapper.items():
        print(userid)
        try:
            profile = Profile.objects.get(id=userid)
            cluster = df.loc[index]['cluster']
            profile.kmeans_cluster = cluster
            profile.save()
            UserCluster(user_id=userid, kmeans_cluster=cluster).save()
        except Profile.DoesNotExist:
            cluster = df.loc[index]['cluster']
            UserCluster(user_id=userid, kmeans_cluster=cluster).save()

    return JsonResponse({'status': status.HTTP_200_OK})


# 벡터사이 유클리드 거리 구하는 함수
def dist_raw(v1, v2):
    # 정규화
    v1_normalized = v1/np.linalg.norm(v1)
    v2_normalized = v2/np.linalg.norm(v2)
    delta = v1_normalized - v2_normalized
    return np.linalg.norm(delta)


def U_Cluster(request):
    profiles = Profile.objects.all()
    df = pd.DataFrame(list(profiles.values()))
    # admin 제거 및 불필요한 열 삭제
    new_df = df[df.occupation != 'admin'].drop(['id', 'username'], axis=1)
    # 군집별 centroid값 구하기 위한 범주형 변수 수치화
    new_df.loc[df['gender'] == 'M', 'gender'] = 1
    new_df.loc[df['gender'] == 'F', 'gender'] = 2
    new_df.loc[df['gender'] == 'other', 'gender'] = 3
    occupation_map = {
        0: "other", 1: "academic/educator", 2: "artist", 3: "clerical/admin", 4: "college/grad student",
        5: "customer service", 6: "doctor/health care", 7: "executive/managerial", 8: "farmer", 9: "homemaker",
        10: "K-12 student", 11: "lawyer", 12: "programmer", 13: "retired", 14: "sales/marketing",
        15: "scientist", 16:  "self-employed", 17: "technician/engineer", 18: "tradesman/craftsman",
        19: "unemployed", 20: "writer"
    }
    for k, v in occupation_map.items():
        new_df.loc[df['occupation'] == v, 'occupation'] = k
    # 군집별 centroid
    mean_df = new_df.drop('user_id', axis=1).groupby(['kmeans_cluster']).mean()
    cluter_mean_vec = mean_df.to_numpy()
    # C_Cluster되지 않은 유저 대상
    target_users = new_df.loc[new_df.isnull()['kmeans_cluster'], ['gender', 'age', 'occupation']]

    new_cluster_list = []
    for i, new_user in enumerate(target_users.to_numpy()):
        min_dist = sys.maxsize
        min_cluster_i = None
        for c_i, cluster_vec in enumerate(cluter_mean_vec):
            d = dist_raw(cluster_vec, new_user)
            if d < min_dist:
                min_dist = d
                min_cluster_i = c_i
        new_cluster_list.append(min_cluster_i)
    target_users['cluster'] = new_cluster_list
    print(target_users)

    return JsonResponse({'status': status.HTTP_200_OK})
