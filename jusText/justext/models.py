from html.parser import HTMLParser


PARAGRAPH_TAGS = [
    'body', 'blockquote', 'caption', 'center', 'col', 'colgroup', 'dd',
    'div', 'dl', 'dt', 'fieldset', 'form', 'legend', 'optgroup', 'option',
    'p', 'pre', 'table', 'td', 'textarea', 'tfoot', 'th', 'thead', 'tr',
    'ul', 'li', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
]


class BuildingBlocksParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []
        self.language = ""
        self.current_tag = ""
        self.tags = []


    def handle_starttag(self, tag, attrs):
        if tag == "html":
            for key, value in attrs:
                if key != "lang":
                    continue
                self.language = value
        self.current_tag = tag
        if tag in PARAGRAPH_TAGS:
            self.tags.append(tag)
            self.parts.append("<" + tag + ">")
        else:
            pass


    def handle_endtag(self, tag):
        if tag in PARAGRAPH_TAGS:
            self.tags.remove(tag)
            self.parts.append("</" + tag + ">")
        else:
            pass


    def handle_data(self, data):
        if (self.current_tag in PARAGRAPH_TAGS
            or self.tags):
            self.parts.append(data)
        else:
            pass
        