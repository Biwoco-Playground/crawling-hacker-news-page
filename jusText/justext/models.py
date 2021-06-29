
class Block:
    content = ""
    content_length = 0
    stopwords_density = 0.0
    link_density = 0.0
    type = ""

    def __init__(
                self, content, 
                content_length, stopwords_density,
                link_density, type):
        self.content = content
        self.content_length = content_length
        self.stopwords_density = stopwords_density
        self.link_density = link_density
        self.type = type

    def __str__(self):
        return (
            "content:{0}\ncontent_length:{1}\nstopwords_density:{2}\nlink_density:{3}\ntype:{4}"
                                                            .format(
                                                                    self.content, self.content_length,
                                                                    self.stopwords_density, self.link_density,
                                                                    self.type))