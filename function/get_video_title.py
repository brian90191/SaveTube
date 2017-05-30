import requests
from bs4 import BeautifulSoup

request = requests.get("https://www.youtube.com/results?search_query=rachel+platten")
content = request.content
soup = BeautifulSoup(content, "html.parser")

nodes = soup.find_all('a', {"rel": "spf-prefetch"})
for element in nodes:
    video_title = element.get('title')
    video_link = 'https://www.youtube.com{}'.format(element.get('href'))
    print(video_title)
    print(video_link)
