# YOUFLIX(Your flix)

This project is movie recommendation system based on switching hybrid recommendation system. The switching hybrid recommendation system is commonly considered as combination of model-based CF(Collaborative Filtering) and CB(Content-based Recommendation).

<img src="img/logo.png" width="300" height="300">



Please check more detail description of CF and CB through below links

- Repository of CF
- Repository of CB



## Getting Started

You can see all prerequisites to test this project in this link



## Description

As we mentioned, switching hybrid recommendation system is used to recommend movies to users. We define three cases for users, newbie, light user and heavy user to apply this algorithm. Here is overview of the recommendation algorithm.

![](img/algorithm.png)

CB recommendation performs well in the case a user rates few movies, compared with model-based CF. In contrast, model-based CF shows high performance when the user rates many movies.  Hence, in our system, CB is for light user and model-based CF is for heavy user. 







> *Git Commit message 남기는 규칙**

- https://djkeh.github.io/articles/How-to-write-a-git-commit-message-kor/

> **우아한 형제 기술 블로그(Git 사용방법)**

- http://woowabros.github.io/experience/2017/10/30/baemin-mobile-git-branch-strategy.html

> **Django cache**

- https://docs.djangoproject.com/en/2.2/topics/cache/

