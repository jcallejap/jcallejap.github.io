from datetime import datetime

AUTHOR = 'jcallejap'
SITENAME = 'Programando en tiempo real'
SITEURL = ''

PATH = 'content'

TIMEZONE = 'Europe/Rome'
DEFAULT_LANG = 'es'

OUTPUT_PATH = 'output/'

# Theme related
THEME = 'Flex'
FAVICON = SITEURL + "/images/favicon.ico"
I18N_TEMPLATES_LANG = "es"
DEFAULT_LANG = "es"
OG_LOCALE = "es_ES"
LOCALE = "es_ES"

# Main Menu
MAIN_MENU = True
MENUITEMS = (
    ("Archives", "/archives"),
    ("Categories", "/categories"),
    ("Tags", "/tags"),
)

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('Pelican', 'https://getpelican.com/'),
         ('Python.org', 'https://www.python.org/'),)

# Social widget
SOCIAL = (('StackOverflow', 'https://stackoverflow.com/users/218774/j-calleja'),)

DEFAULT_PAGINATION = 4
COPYRIGHT_YEAR = datetime.now().year

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True