import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import pylab as pl

import json
from collections import Counter

import os
import sys
import django

sys.path.append('C:\\Users\\multicampus\\nnyong\\youflix\\django-vue\\djangoAPI')

os.environ.setdefault('DJANGO_SETTINGS_MODUlE','djangoAPI.settings')
django.setup()

from api.models import Movie, User, Profile, Rating, UserCluster

# user Cluster
user=np.load('../../data/mapper/latent_user.npy')
print(user)

# kmeans 클러스터링
kmeans=KMeans(n_clusters=7).fit(user)

df=pd.DataFrame(user)
df['cluster'] = kmeans.labels_
print(df)

# 각 군집별 평균값
kmeans_cluster_mean=df.groupby(['cluster']).mean()
print(kmeans_cluster_mean)

# mapper 불러오기. KEY:userid, value: index
mapper=open('../../data/mapper/userMapper.json').read()
mapper = json.loads(mapper)
# print(mapper)

for userid, index in mapper.items():
    print(userid)
    try:
        profile=Profile.objects.get(id=userid)
        cluster=df.loc[index]['cluster']
        profile.kmeans_cluster=cluster
        profile.save()
        UserCluster(user_id=int(userid)+1,kmeans_cluster=cluster).save()
    except:
        cluster=df.loc[index]['cluster']
        UserCluster(user_id=userid,kmeans_cluster=cluster).save()
