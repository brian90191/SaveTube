import requests
from bs4 import BeautifulSoup

request = requests.get("https://www.youtube.com/results?search_query=rachel+platten")
content = request.content
soup = BeautifulSoup(content, "html.parser")
print(soup)


