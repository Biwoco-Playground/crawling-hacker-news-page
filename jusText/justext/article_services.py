from lxml.html.clean import Cleaner


MAX_LINK_DENSITY_DEFAULT = 0.2
LENGTH_LOW_DEFAULT = 70
LENGTH_HIGH_DEFAULT = 200
STOPWORDS_LOW_DEFAULT = 0.30
STOPWORDS_HIGH_DEFAULT = 0.32
NO_HEADINGS_DEFAULT = False
# Short and near-good headings within MAX_HEADING_DISTANCE characters before
# a good paragraph are classified as good unless --no-headings is specified.
MAX_HEADING_DISTANCE_DEFAULT = 200


def preprocess(str_html):     
    options = {
        "processing_instructions": False,
        "remove_unknown_tags": True,
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
                        "iframe", "select"),
    }
    cleaner = Cleaner(**options)

    return cleaner.clean_html(str_html)