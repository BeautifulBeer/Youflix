
from surprise import Reader, Dataset, SVD, accuracy
from surprise.model_selection import KFold

reader = Reader()
ratings = pd.read_csv('./input/ratings_small.csv')
ratings.head()


# In[74]:


data = Dataset.load_from_df(ratings[['userId', 'movieId', 'rating']], reader)

# data.split(n_folds=5)

# svd = SVD()
# evaluate(svd, data, measures=['RMSE', 'MAE'])

kf = KFold(n_splits=5)
algo = SVD()

for trainset, testset in kf.split(data):
    
    algo.fit(trainset)
    predictions = algo.test(testset)
    
    accuracy.rmse(predictions, verbose=True)
    accuracy.mae(predictions, verbose=True)
    print("")


# In[75]:


trainset = data.build_full_trainset()
svd.fit(trainset)


# In[76]:


ratings[ratings['userId'] == 672]


# In[86]:


svd.predict(672, 60, 4)


# In[ ]:




