
class Block:
    content = ""
    content_length = 0
    stopwords_density = 0.0
    link_density = 0.0
    CLASS = ""

    def __init__(
                self, content, 
                content_length, stopwords_density):
        self.content = content
        self.content_length = content_length
        self.stopwords_density = stopwords_density

    def __str__(self):
        return (
            "content:{0}\ncontent_length:{1}\nstopwords_density:{2}\nlink_density:{3}\nCLASS:{4}"
                                                            .format(
                                                                    self.content, self.content_length,
                                                                    self.stopwords_density, self.link_density,
                                                                    self.CLASS))