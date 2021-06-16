from bs4 import BeautifulSoup
import requests
from itertools import zip_longest
import csv

jobs = []
co_location = []
post = []
links = []
working_hours = []

page_num = 0
while True:
    url = f'https://wuzzuf.net/search/jobs/?a=hpb&q=work%20from%20home&start={page_num}'
    src = requests.get(url)
    soup = BeautifulSoup(src.content, 'lxml')
    job_titles = soup.select('.css-m604qf a')
    page_limit = int(soup.find('strong').get_text())
    for i in job_titles:
        links.append(i['href'])
    
    if page_num > (page_limit // 15):
        print('All pages scraped\nNo more pages found')
        break
    page_num +=1
    print(f'page Number:{page_num}')

for link in links:
    page = requests.get(link)
    soup = BeautifulSoup(page.content, 'lxml')
    title = soup.find('h1', {'class':'css-f9uh36'})
    hiring = soup.find('strong', {'class':'css-9geu3q'})
    post_time = soup.find('span', {'class':'css-182mrdn'})
    shift = soup.find('span', {'class':'css-1nwobo-Label eoyjyou0'})

    jobs.append(title.text)
    co_location.append(hiring.text)
    post.append(post_time.text[6:])
    working_hours.append(shift.text)

lists = [jobs, working_hours, co_location, post, links]    
job_data = zip_longest(*lists)

with open('F:/Python Courses + projects/web-scraping project/wazzuf-Research.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Job Title','Working Period', 'Location' ,'Post Time', 'Links'])
    writer.writerows(job_data)

print('Project Completed')