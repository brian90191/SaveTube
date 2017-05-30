import requests
from bs4 import BeautifulSoup
import re

request = requests.get("https://www.youtube.com/results?search_query=rachel+platten")
content = request.content
soup = BeautifulSoup(content, "html.parser")

#<a href="/results?q=rachel+platten&amp;sp=SBTqAwA%253D" class="yt-uix-button yt-uix-sessionlink yt-uix-button-default yt-uix-button-size-default" data-visibility-tracking="CCMQnKQBGAEiEwicueCVsK3SAhVmFVgKHUx7A70o9CQ" data-sessionlink="itct=CCMQnKQBGAEiEwicueCVsK3SAhVmFVgKHUx7A70o9CQ" aria-label="前往第 2 頁"><span class="yt-uix-button-content">2</span></a>
link_nodes = soup.find_all('a', {"class": True, "href": True, "data-visibility-tracking": True, "aria-label": True, "data-sessionlink": True})
page = {}
for element in link_nodes:
    link_text = element.text
    link = "https://www.youtube.com{}".format(element.get('href'))
    page['{}'.format(link_text)] = link

print(page)
