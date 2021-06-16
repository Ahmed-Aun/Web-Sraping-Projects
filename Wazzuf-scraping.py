import lxml 
import requests
from bs4 import BeautifulSoup
import csv
from itertools import zip_longest

jobs = []
hiring_co = []
co_adress = []
work_time = []
links = []
post = []

page_num = 0
while True:
    try:
        url = f'https://wuzzuf.net/search/jobs/?a=navbg%7Cspbg&q=data%20analysis&start={page_num}'
        src = requests.get(url)
        soup = BeautifulSoup(src.content, 'lxml')
        job_titles = soup.select('.css-m604qf a')
        hirings = soup.select('.css-1s8r46l a')
        addresses = soup.select('.css-1s8r46l span')
        shifts = soup.select('.css-1w0948b a span')
        post_time = soup.select('.css-4c4ojb')
        page_limit = int(soup.find('strong').text)

        for i in range(len(job_titles)):
            jobs.append(job_titles[i].text)
            links.append(job_titles[i]['href'])
            hiring_co.append(hirings[i].text)
            co_adress.append(addresses[i].text)
            work_time.append(shifts[i].text)
            #post.append(post_time[i].text)

        if page_num > (page_limit // 15):
            print('All pages are scraped, There are No more Pages Found')
            break
        page_num +=1
        print(f'page Number: {page_num} Finished')

    except:
        print('Error !!! The while loop not wroking.......!')
        break

lists = [jobs, post, hiring_co, co_adress, work_time, links]    
job_data = zip_longest(*lists)

with open('F:/Python Courses + projects/web-scraping project/wazzuf-Test.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Job title', 'Post Time', 'Hiring Company', 'Comapny Address', 'Shift', 'Links'])
    writer.writerows(job_data)
print('Project Completed \nGood Data Collection')

