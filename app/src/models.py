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
        return (
            "id:{0}\ntitle:{1}\ncontent_url:{2}\npoints:{3}\n"
            + "created_date:{4}\nauthor:{5}\nnumber_comments:{6}"
                .format(
                        self.id, self.title,
                        self.content_url, self.points,
                        self.created_date, self.author,
                        self.number_comments,))
