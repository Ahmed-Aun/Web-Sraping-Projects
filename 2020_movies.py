from bs4 import BeautifulSoup as bs
import requests


def get_content_value(row_data):
    if row_data.find('li'):
        return [li.get_text(' ', strip=True).replace('\xa0', ' ') for li in row_data.find_all('li')]
    else:
        return row_data.get_text(' ', strip=True).replace('\xa0', ' ')


def get_info_box(url):
    page = requests.get(url)
    soup = bs(page.content, 'html.parser')
    info_box = soup.find(class_='infobox vevent')
    info_rows = info_box.find_all('tr')

    movie_info = {}

    for index, row in enumerate(info_rows):
        if index == 0:
            movie_info['title'] = row.find('th').get_text(' ', strip=True)
        elif index == 1:
            continue
        else:
            content_key = row.find('th').get_text(' ', strip=True)
            content_value = get_content_value(row.find('td'))
            movie_info[content_key] = content_value

    return movie_info


page = requests.get('https://en.wikipedia.org/wiki/List_of_American_films_of_2020')
soup = bs(page.content, 'html.parser')
movies = soup.select('.wikitable.sortable i a')

base_path = 'https://en.wikipedia.org/'
movie_list = []

for index, movie in enumerate(movies):
    try:
        path = movie['href']
        full_path = base_path + path
        title = movie['title']
        movie_list.append(get_info_box(full_path))

        '''
        print(title)
        print(path)
        print()
        '''
    except Exception as e:
        print(movie.get_text)
        print(e)

## saving data ##
import json

def save_data(name, data):
    with open(name, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_data(name):
    with open(name, encoding='utf-8') as f:
        return json.load(f)

save_data('Movies-2020.json', movie_list)
