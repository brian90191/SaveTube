import requests
from flask import session
from bs4 import BeautifulSoup
import re
import youtube_dl
from modles.video import video

def find_search_content(search):
    request = requests.get("https://www.youtube.com/results?search_query={}".format(search))
    content = request.content
    soup = BeautifulSoup(content, "html.parser")
    return soup

def find_page_content(search):
    request = requests.get("https://www.youtube.com/results?{}".format(search))
    content = request.content
    soup = BeautifulSoup(content, "html.parser")
    return soup

def find_video(soup, all_item, i=1):
    nodes = soup.find_all('a', {"rel": "spf-prefetch"})
    for element in nodes:
        video_title = element.get('title')
        video_link = 'https://www.youtube.com{}'.format(element.get('href'))

        img_value = element.get('href').split("=")[1]
        all_img = soup.find_all('img', {"data-ytimg": True, "height": True, "width": True, "onload": True})
        img = re.findall("https://i.ytimg.com/vi/{}/[\S]+".format(img_value), str(all_img))
        img_str = str(img).strip("[\"\']")
        video_img = img_str.replace("&amp;", "&")

        # favorite information
        account = session['account']
        video_data = video.find_video(account, video_title, video_link)
        favorite = 0
        if video_data.count() <= 0:
            favorite = 0
        else:
            favorite = 1

        all_item['{}'.format(i)] = {"title": video_title, "link": video_link, "img": video_img, "favorite": favorite}
        i = i+1
    return all_item

def video_time(soup, all_item, i=1):
    time_nodes = soup.find_all('span', {"class": "video-time"})
    for time_element in time_nodes:
        time_text = time_element.text
        all_item.get('{}'.format(i))['time'] = time_text
        i=i+1
    return all_item

def every_video(soup):
    all_item = {}
    find_video(soup, all_item, i=1)
    video_time(soup, all_item, i=1)
    return all_item

def page_bar(soup):
    link_nodes = soup.find_all('a', {"class": True, "href": True, "data-visibility-tracking": True, "aria-label": True,
                                     "data-sessionlink": True})
    page = {}
    for element in link_nodes:
        link_text = element.text
        link = "{}".format(element.get('href'))
        page['{}'.format(link_text)] = link
    return page

def download_mp3(url):
    ydl_opts = {
        'outtmpl': '/media/%(title)s.%(ext)s',
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192'
        }]}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def download_mp4(url):
    ydl_opts = {'format': 'best', 'outtmpl': '/media/%(title)s.%(ext)s'}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

