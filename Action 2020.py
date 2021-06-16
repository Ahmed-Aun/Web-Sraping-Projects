from bs4 import BeautifulSoup
import requests

def list_data(data):
        if data.find('li'):
            return[li.get_text(' ', strip=True).replace('\xa0',' ') for li in data.find_all('li')]
        else:
            return data.get_text(' ', strip=True).replace('\xa0',' ')

def movie_data(url):
    src = requests.get(url)
    soup = BeautifulSoup(src.content, 'html.parser')
    table = soup.find('table')
    rows = table.find_all('tr')
   
    info = {}
    for index, row in enumerate(rows):
        if index ==0:
            info['title'] = row.find('th').get_text(' ', strip=True)
        elif index ==1:
            continue
        else:
            key = row.find('th').get_text(' ', strip=True)
            value = list_data(row.find('td'))
            info[key] = value
    return info


url = 'https://en.wikipedia.org/wiki/List_of_action_films_of_the_2020s'
src = requests.get(url)
soup = BeautifulSoup(src.content, 'html.parser')
movies = soup.select('.wikitable.sortable i a')


movies_info = []
for movie in movies:
    try:
        title = movie['title']
        base_link = 'https://en.wikipedia.org/'
        path = movie['href']
        link = base_link + path
        movies_info.append(movie_data(link))

    except Exception as e:
        print(movie.get_text)
        print(e)


print(movies_info[0])

