import stopwords_manager
import re
import utils

from lxml.html.clean import Cleaner
from lxml.html import fromstring
from models import Block


MAX_LINK_DENSITY = 0.2
LENGTH_LOW = 10
LENGTH_HIGH = 30
STOPWORDS_LOW = 0.30
STOPWORDS_HIGH = 0.32
PARAGRAPH_TAGS = [
    'body', 'blockquote', 'caption', 'center', 'col', 'colgroup', 'dd',
    'div', 'dl', 'dt', 'fieldset', 'form', 'legend', 'optgroup', 'option',
    'p', 'pre', 'table', 'td', 'textarea', 'tfoot', 'th', 'thead', 'tr',
    'ul', 'li', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
]


def preprocess(str_html):     
    options = {
            "processing_instructions": False,
            "remove_unknown_tags": False,
            "safe_attrs_only": False,
            "page_structure": False,
            "annoying_tags": False,
            "frames": False,
            "meta": False,
            "links": False,
            "javascript": False,
            "scripts": True,
            "comments": True,
            "style": True,
            "embedded": True,
            "forms": True,
            "kill_tags": (
                        "head", "header", 
                        "nav", "figure", 
                        "noscript", "footer",
                        "iframe", "select"),}
    
    cleaner = Cleaner(**options)

    return cleaner.clean_html(str_html)


def divide_blocks(str_html):
    blocks = []
    tree = fromstring(str_html)
    language_code = tree.xpath("//html/@lang")[0]
    language = stopwords_manager.map_language(language_code)
    stopwords = stopwords_manager.get_stoplist(language)
    for tag in tree.iter():
        current_tag = tag.tag
        if current_tag in PARAGRAPH_TAGS:
            text = tag.text
            if text is not None:
                content = text.split(" ")
                total_words = len(content)
                count_stopwords = 0
                for sub in content:
                    if sub in stopwords:
                        count_stopwords += 1
                stopwords_density = count_stopwords/total_words

                block = Block(
                            text, total_words, 
                            stopwords_density)

                count_a = 0
                link_density = 0
                for child in tag:
                    if (child == 'a'
                        and total_words
                        and len(child.text)):
                        count_a += 1
                        link_density += len(child.text)/total_words

                if count_a > 0:
                    link_density /= count_a

                block.link_density = link_density
                block.CLASS = classify_block(
                                            link_density, total_words, 
                                            stopwords_density)
                blocks.append(block)
            
    return blocks


def classify_block(
                link_density, length, 
                stopwords_density):

    if link_density > MAX_LINK_DENSITY:
        return 'bad'

    # short blocks
    if length < LENGTH_LOW:
        if link_density > 0:
            return 'bad'
        else:
            return 'short'

    # medium and long blocks
    if stopwords_density > STOPWORDS_HIGH:
        if length > LENGTH_HIGH:
            return 'good'
        else:
            return 'near-good'
    if stopwords_density > STOPWORDS_LOW:
        return 'near-good'
    else:
        return 'bad'

