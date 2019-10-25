# You can flex(YOUFLEX)

Movielens와 IMDB 데이터를 활용하여 개인 맞춤형 영화 추천을 하는 서비스입니다. Content-based 와 Collaborative Filtering 기술을 결합하여 Hybrid Recommender System을 개발하고, 이는 사용자 취향 기반의 영화 추천을 가능케 합니다. 또한, 영화 줄거리/리뷰를 통해 태그를 추출해내어 키워드 기반 영화검색이 가능한 서비스를 개발합니다.



## Prerequisite Steps

프로젝트를 실행하기 위해 필요한 단계들입니다. 



### Create Virtual Environment

프로젝트의 환경과 기존 로컬 환경을 분리하기 위한 가상환경을 생성합니다. 

```bash
# Path > bigdata-sub3
# 위의 위치에서 아래의 명령어를 실행 해주시면 됩니다.
    pip3 install -r requirements.txt
   
# virtualenv django-vue를 생성합니다
    virtualenv django-vue

# djangoAPI 디렉토리를 생성한 django-vue 로 이동합니다
    mv djangoAPI django-vue
```



### Activate Virtual Environment

생성한 가상환경을 활성화합니다. 해당 가상환경은, 서버를 실행하기 전에 반드시 활성화해야 합니다.

```bash
# Path > bigdata-sub3/django-vue
    # on Windows
        call scripts/activate
    # on Linux
        call bin/activate

# 위의 명령어를 실행하게 되면 CMD창이 아래와 같이 변하게 됩니다.
# (django-vue) C:\Users\......
```



### Install Required Packages

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
# 4. VSCode Extension Python 설치
# Eslint, Pylint 적용
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
    "explorer.confirmDragAndDrop": false,
    "less.lint.duplicateProperties": "warning",
    "scss.lint.duplicateProperties": "warning",
    "python.linting.pycodestyleEnabled": true,
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": false,
    "python.linting.ignorePatterns": [
        ".vscode/*.py",
        "**/site-packages/**/*.py",
        "**/*.pyc"
    ],
    "window.zoomLevel": 2,
    "vetur.format.options.tabSize": 4,
}
```



### 접속방법

- http://localhost:8000 을 통해서 확인할 수 있습니다.



## 관련자료 링크

자세한 사항은 관련 위키를 참조해주시면 감사하겠습니다. [프로젝트 관련 문서 위키]([https://lab.ssafy.com/Jo_yongseok/youflix/wikis/%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8-%EB%AA%85%EC%84%B8%EC%84%9C](https://lab.ssafy.com/Jo_yongseok/youflix/wikis/프로젝트-명세서))

아래는 프로젝트 진행 중 참고한 기술들에 대한 레퍼런스입니다.



> *Git Commit message 남기는 규칙**

- https://djkeh.github.io/articles/How-to-write-a-git-commit-message-kor/

> **우아한 형제 기술 블로그(Git 사용방법)**

- http://woowabros.github.io/experience/2017/10/30/baemin-mobile-git-branch-strategy.html

> **Django cache**

- https://docs.djangoproject.com/en/2.2/topics/cache/

