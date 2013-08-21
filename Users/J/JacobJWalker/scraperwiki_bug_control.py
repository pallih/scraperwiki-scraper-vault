#!/usr/bin/env python

'''
The following Python Script is used as the "control group" when testing the new ScraperWiki for bugs, 
to see if the same code causes a bug in the Classic ScraperWiki and the new one
'''

import scraperwiki
import requests


try: 
    current_routine = scraperwiki.sqlite.get_var('last_routine')
    if current_routine == None:
        current_routine = 'A Routine'
        scraperwiki.sqlite.save_var('last_routine', 'A Routine')
except:
    current_routine = 'A Routine'
    scraperwiki.sqlite.save_var('last_routine', 'A Routine')

try:
    current_page = scraperwiki.sqlite.get_var('last_page')
    if current_page == None:
        current_page = 0
except Exception as inst:
    print inst
    current_page = 0

current_page = current_page + 1
scraperwiki.sqlite.save_var('last_page', current_page)
