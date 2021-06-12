from datetime import datetime


class Article:
    id = ""
    title = ""
    content_url = ""
    points = 0
    created_date = datetime.now().isoformat()
    author = ""
    number_comments = 0

    def __str__(self):
        str1 = "id:{0}\ntitle:{1}\ncontent_url:{2}\npoints:{3}\n".format(
            self.id,
            self.title,
            self.content_url,
            self.points
        )
        str2 = "created_date:{0}\nauthor:{1}\nnumber_comments:{2}".format(
            self.created_date,
            self.author,
            self.number_comments
        )
        full_str = str1+str2
        return full_str
