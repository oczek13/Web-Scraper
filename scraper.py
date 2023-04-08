import string
import requests
import os

from bs4 import BeautifulSoup

pages = int(input())
article_type = input()

template_url = "https://www.nature.com/nature/articles?sort=PubDate&year=2020"

for i in range(pages):
    folder_path = 'Page_' + str(i + 1)
    print(folder_path)
    os.mkdir(folder_path)
    url = template_url + "&page=" + str(i + 1)
    r = requests.get(url)

    if r.status_code == 200:
        soup = BeautifulSoup(r.content, 'html.parser')
        p1 = soup.find_all('span', {'class': 'c-meta__type'}, text=article_type)
        titles = []
        links = []
        for i in p1:
            titles.append(i.find_parent('article').find('a').text)
            links.append(i.find_parent('article').find('a').get('href'))

        template_link = string.Template("http://nature.com$link")
        full_links = []

        for j in range(len(links)):
            full_links.append(template_link.substitute(link=links[j]))
            re = requests.get(full_links[j])

            table = titles[j].maketrans("", "", string.punctuation + "'")
            title = titles[j].translate(table)
            title = title.strip().replace(' ', '_')

            soup1 = BeautifulSoup(re.content, 'html.parser')
            content = soup1.find('p', {'class': 'article__teaser'})

            file = open(folder_path + "\%s.txt" % title, 'wb')
            file.write(content.get_text().encode('utf-8'))
            file.close()
    else:
        print("Invalid page!")
