from common.database import Database


class video(object):
    def __init__(self, account, tag, title, link, img, time):
        self.account = account
        self.tag = tag
        self.title = title
        self.link = link
        self.img = img
        self.time = time

    def save_to_DB(self):
        Database.insert(collection='video', data=self.to_json())

    def to_json(self):
        return {
            "account": self.account,
            "tag": self.tag,
            "title": self.title,
            "link": self.link,
            "img": self.img,
            "time": self.time
        }

    def find_video_data(account):
        user_video = Database.find(collection='video', query={"account": account})
        return user_video

    def find_video(account, title, link):
        video_data = Database.find(collection='video', query={"account": account, "title": title, "link": link})
        return video_data

    def remove_video(account, title, link):
        Database.remove(collection='video', query={"account": account, "title": title, "link": link})

    def find_favorite_tags(account):
        favorite_tags = Database.fine_distinct(collection='video', query={"account": account}, tag='tag')
        return favorite_tags
