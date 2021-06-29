import stopwords_manager
import utils

from lxml.html.clean import Cleaner
from lxml.html import fromstring
from models import Block


MAX_LINK_DENSITY = 0.2
LENGTH_LOW = 10
LENGTH_HIGH = 30
STOPWORDS_LOW = 0.20
STOPWORDS_HIGH = 0.32
PARAGRAPH_TAGS = [
    'body', 'blockquote', 'caption', 'center', 'col', 'colgroup', 'dd',
    'div', 'dl', 'dt', 'fieldset', 'form', 'legend', 'optgroup', 'option',
    'p', 'pre', 'table', 'td', 'textarea', 'tfoot', 'th', 'thead', 'tr',
    'ul', 'li', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
]
MAIN_TAGS = ['h1', 'h2']


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
        if (current_tag in PARAGRAPH_TAGS):
            text = tag.text
            if (text is not None):
                content = text.split(" ")
                total_words = len(content)
                count_stopwords = 0
                for sub in content:
                    if sub in stopwords:
                        count_stopwords += 1
                stopwords_density = count_stopwords/total_words
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
                type = ""
                if current_tag in MAIN_TAGS:
                    type = "good"
                else:
                    type = classify_block(
                                            link_density, total_words, 
                                            stopwords_density)
                
                block = Block(
                            text, total_words, 
                            stopwords_density, link_density,
                            type)
                blocks.append(block)
            
    return blocks


def classify_block(
                link_density, length, 
                stopwords_density):
    if link_density > MAX_LINK_DENSITY:
        return 'bad'

    if length < LENGTH_LOW:
        if link_density > 0:
            return 'bad'
        else:
            return 'short'

    if stopwords_density > STOPWORDS_HIGH:
        if length > LENGTH_HIGH:
            return 'good'
        else:
            return 'near-good'
            
    if stopwords_density > STOPWORDS_LOW:
        return 'near-good'
    else:
        return 'bad'


def get_main_content(blocks):
    main_content = ""
    index = 0
    for block in blocks:
        block_type = block.type
        # print(block)
        # print("---------")
        block.type = get_context_sensitive_class(blocks, block_type, index)
        # print(block)
        # print("---------")
        if block.type == 'good':
            main_content += block.content + "\n"
        index += 1

    main_content = utils.normalize_whitespace(main_content)
    return main_content


def get_context_sensitive_class(blocks, block_type, index):
    if block_type == 'bad':
        return 'bad'
    if block_type == 'good':
        return 'good'
    if block_type == 'near-good':
        prev_block_type = get_prev_good_or_bad_block(blocks, index)
        next_block_type = get_next_good_or_bad_block(blocks, index)
        if prev_block_type == 'good' or next_block_type == 'good':
            return 'good'
        else:
            return 'bad'
    if block_type == 'short':
        prev_block_type = get_prev_good_or_bad_block(blocks, index)
        next_block_type = get_next_good_or_bad_block(blocks, index)
        if prev_block_type == 'bad' and next_block_type == 'bad':
            return 'bad'
        if prev_block_type == 'good' and next_block_type == 'good':
            return 'good'
        if prev_block_type == 'bad' and next_block_type == 'good':
            if get_prev_non_short_block(blocks, index) == 'near-good':
                return 'good'
            else:
                return 'bad'
        if next_block_type == 'bad' and prev_block_type == 'good':
            if get_next_non_short_block(blocks, index) == 'near-good':
                return 'good'
            else:
                return 'bad'


def get_prev_good_or_bad_block(blocks, index):
    i = index
    while i > 0:
        i -= 1
        block_type = blocks[i].type
        if block_type == 'good':
            return block_type
    return 'bad'


def get_next_good_or_bad_block(blocks, index):
    i = index
    len_blocks = len(blocks)
    while i < len_blocks - 1:
        i += 1
        block_type = blocks[i].type
        if block_type == 'good':
            return block_type
    return 'bad'


def get_prev_non_short_block(blocks, index):
    i = index
    while i > 0:
        i -= 1
        block_type = blocks[i].type
        if block_type != 'short':
            return block_type
    return 'bad'


def get_next_non_short_block(blocks, index):
    i = index
    len_blocks = len(blocks)
    while i < len_blocks - 1:
        i += 1
        block_type = blocks[i].type
        if block_type != 'short':
            return block_type
    return 'bad'