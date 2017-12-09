#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Robert Ou, Ivan Xia'
SITENAME = 'EE206A Fall 2017 Project'
SITEURL = ''

THEME = 'themes/pelican-bootstrap3'

PATH = 'content'

TIMEZONE = 'UTC'

DEFAULT_LANG = 'en'

CC_LICENSE = 'CC-BY'

DEFAULT_PAGINATION = False

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

# Links at the top
DISPLAY_PAGES_ON_MENU = False
MENUITEMS = (
    ('Background and motivation', '/pages/background-and-motivation.html'),
    ('Design', '/pages/design.html'),
    ('Implementation', '/pages/implementation.html'),
    ('Results', '/pages/results.html'),
    ('Conclusions', '/pages/conclusions.html'),
    ('Team', '/pages/team.html'),
)
