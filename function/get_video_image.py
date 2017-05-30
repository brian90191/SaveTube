import requests
from bs4 import BeautifulSoup
import re

request = requests.get("https://www.youtube.com/results?search_query=rachel+platten")
content = request.content
soup = BeautifulSoup(content, "html.parser")

nodes = soup.find_all('a', {"rel": "spf-prefetch"})
for element in nodes:
    video_title = element.get('title')
    video_link = 'https://www.youtube.com{}'.format(element.get('href'))
    img_value = element.get('href').split("=")[1]
    print(video_title)
    print(video_link)

    all_img = soup.find_all('img', {"data-ytimg": True, "height": True, "width": True, "onload": True})
    img = re.findall("https://i.ytimg.com/vi/{}/[\S]+".format(img_value), str(all_img))
    img_str = str(img).strip("[\"\']")
    video_img = img_str.replace("&amp;", "&")
    print(video_img)
