import requests
from bs4 import BeautifulSoup
import re

request = requests.get("https://www.youtube.com/results?search_query=rachel+platten")
content = request.content
soup = BeautifulSoup(content, "html.parser")

#<span class="video-time" aria-hidden="true">3:26</span>
time_nodes = soup.find_all('span', {"class": "video-time"})
for time_element in time_nodes:
    time_text = time_element.text
    print(time_text)
