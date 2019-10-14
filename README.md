# You can flex(YOUFLEX)

Movielens와 IMDB 데이터를 활용하여 개인 맞춤형 영화 추천을 하는 서비스입니다.
Collaborative Filtering 알고리즘을 사용하여, 대규모 데이터 처리를 원활하게 합니다.


## Initial Setting

프로젝트를 실행하기 위해 필요한 단계들입니다. 

### Create virtual environment

```bash
# Path > bigdata-sub3
# 위의 위치에서 아래의 명령어를 실행 해주시면 됩니다.
    pip3 install -r requirements.txt
   
# virtualenv django-vue를 생성합니다
    virtualenv django-vue

# djangoAPI 디렉토리를 생성한 django-vue 로 이동합니다
    mv djangoAPI django-vue
```



### Activate virtual environment

```bash
# Path > bigdata-sub3/django-vue
    # on Windows
        call scripts/activate
    # on Linux
        call bin/activate

# 위의 명령어를 실행하게 되면 CMD창이 아래와 같이 변하게 됩니다.
# (django-vue) C:\Users\......
```



### Install required packages

```bash
# Virtual environment를 활성화한 상태여야 합니다.
# Path > bigdata-sub3/django-vue/djangoAPI
    pip3 install -r requirements.txt

# Path > bigdata-sub3/frontend
    npm install
    npm install -g eslint --save
```



### Setup django server

```bash
# Path > youflix/django-vue/djangoAPI
    python manage.py makemigrations
    python manage.py migrate
    
# Path > youflix/django-vue/djangoAPI
* 사전에 pycache에 앞에 숫자 있는 파일을 삭제
    python .\manage.py loaddata ./json/Total.json
```



### Development Server On

```bash
# 총 2개의 cmd가 필요합니다
# cmd 1
# Virtual environment를 활성화한 상태여야 합니다.
# Path > bigdata-sub3/django-vue/djangoAPI
   py manage.py runserver
   
# cmd 2
# Path > bigdata-sub3/frontend
   cd django-vue/djangoAPI/frontend
   npm run serve
```



### Production Server On

```bash
# cmd 1
# Path > bigdata-sub3/frontend
   cd django-vue/djangoAPI/frontend
   npm run build
   
# cmd 2
# Virtual environment를 활성화한 상태여야 합니다.
# Path > bigdata-sub3/django-vue/djangoAPI
   py manage.py runserver
```



### VSCode Linter Setting

```bash
# 1. Ctrl + , 를 이용해 Setting 창 열기
# 2. 우측 상단에 있는 Open Settings(UI) 버튼을 클릭, Settings.json 열기
# 3. 아래의 내용 삽입하기

{
    "editor.tabCompletion": "on",
    "eslint.alwaysShowStatus": true,
    "eslint.validate": [
        "javascript",
        "javascriptreact",
        {
            "autoFix": false,
            "language": "vue"
        }
    ],
    "less.lint.duplicateProperties": "warning",
    "scss.lint.duplicateProperties": "warning",    
}
```



### 접속방법

- http://localhost:8000 을 통해서 확인할 수 있습니다.



## 관련자료 링크

> **Git Commit message 남기는 규칙**

- https://djkeh.github.io/articles/How-to-write-a-git-commit-message-kor/



 저희팀의 경우 아래와 같이 Commit Format을 정하였습니다.

```bash
[ISSUE번호] [implement|update|merge|...] [개요]

# content
1. 구현한 내용을 상세히 입력

# To-Do
1. 이 후 해야할 일을 기입

# issue
[closed|fixed|...] #[이슈번호] - [남길내용]
```



> **우아한 형제 기술 블로그(Git 사용방법)**

- http://woowabros.github.io/experience/2017/10/30/baemin-mobile-git-branch-strategy.html

> **Django cache**

- https://docs.djangoproject.com/en/2.2/topics/cache/





## Templete

- https://onepagelove.com/templates/free-templates



## API

> **The movie DataBase**

- https://www.themoviedb.org/documentation/api?language=en-US

## DB 삭제 후 재생성
### Json 파일 목록 및 load 순서
collection
company
country
genre
language
keyword
movie
6000user
6000profile
cast
crew
rating

* 사전에 pycache에 앞에 숫자 있는 파일을 삭제.

1. django-vue/djangoAPI/에 data, json 폴더를 넣고
2. djangoAPI 디렉토리에서 makemigrations, migrate 실행
3. python manage.py loaddata ./json/파일이름.json을 실행(위의 명령대로)

위치> \bigdata-sub3\django-vue\djangoAPI

python .\manage.py loaddata ./json/collection.json
python .\manage.py loaddata ./json/company.json
python .\manage.py loaddata ./json/country.json
python .\manage.py loaddata ./json/genre.json
python .\manage.py loaddata ./json/language.json
python .\manage.py loaddata ./json/keyword.json
python .\manage.py loaddata ./json/movie.json

python .\manage.py loaddata ./json/6000user.json
python .\manage.py loaddata ./json/6000profile.json
python .\manage.py loaddata ./json/cast.json
python .\manage.py loaddata ./json/crew.json