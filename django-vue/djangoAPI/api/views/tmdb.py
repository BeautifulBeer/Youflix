import requests


def getMovieInfo(title='Toy Story', year=1995, type='select', id='', lang='en-US'):
    movie_info = None

    api_key = '63d90ec0954c1ebf2734054204f89bf5'
    base_url = 'https://api.themoviedb.org/3/'

    if type == 'select':
        tmdb_request = requests.get('%ssearch/movie?api_key=%s&language=%s&query=%s&year=%i' % (base_url, api_key, lang, title, year))
    elif type == 'select2':
        tmdb_request = requests.get('%ssearch/movie?api_key=%s&language=%s&query=%s' % (base_url, api_key, lang, title))
    elif type == 'video':
        tmdb_request = requests.get('%smovie/%i/videos?api_key=%s&language=%s' % (base_url, id, api_key, lang))
    elif type == 'detail':
        tmdb_request = requests.get('%smovie/%i?api_key=%s&language=%s' % (base_url, id, api_key, lang))

    if tmdb_request.status_code == 200:
        movie_info = tmdb_request.json()

    # print(movie_info)
    # with open('movie.json','w+',newline='',encoding='utf8') as json_file:
    #     json.dump(movies_detail, json_file)
    return movie_info
