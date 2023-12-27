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
SITELOGO = '/images/profile.png'
FAVICON = '/images/favicon.ico'
SITESUBTITLE = "Programación (principalmente) en C++"
SITEDESCRIPTION = "Ejemplos de algoritmos, curiosidades, y cosas que voy descubriendo mientras desarrollo aplicaciones."
I18N_TEMPLATES_LANG = "es"
DEFAULT_LANG = "es"
OG_LOCALE = "es_ES"
LOCALE = "es_ES"
BROWSER_COLOR = '#333333'

# License
CC_LICENSE = {
    "name": "Creative Commons Attribution-ShareAlike",
    "version": "4.0",
    "slug": "by-sa",
    "local_icons": True,
}

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
LINKS = (('Pelican', 'https://getpelican.com/'),('Python.org', 'https://www.python.org/'),)

# Social widget
SOCIAL = (('stack-overflow', 'https://stackoverflow.com/users/218774/j-calleja'), ("github", "https://github.com/jcallejap"),)
COPYRIGHT_YEAR = datetime.now().year
DEFAULT_PAGINATION = 3

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True