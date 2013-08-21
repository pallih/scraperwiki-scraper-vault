# -*- coding: utf-8 -*-
# encoding=utf-8
import re
import urllib
import scraperwiki

def desclinks(x):
    firstlink = x
    htmlfile = urllib.urlopen(firstlink)
    htmltext = htmlfile.read()
    regex = '<a class="name" href="(.+?)">'
    pattern = re.compile(regex)
    price = re.findall(pattern,htmltext)
    price[:] = [s.replace('/', 'http://m.alza.sk/') for s in price]
    price[:] = [t.replace('htm', 'htm?d=desc') for t in price]
    links = price
    return links




links = desclinks("http://m.alza.sk/chladenie/vodne/kompletne-sety/18849473-p20.htm")


i=0
while i<len(links):
    htmlfile = urllib.urlopen(links[i])
    htmltext = htmlfile.read()
    regex = re.compile("Parametre a špecifikácie(?:(?!</div>).)*|Parametry a specifikace:(?:(?!</div>).)*|Pro procesory:(?:(?!</div>).)*|Parametry a specifkace:(?:(?!</div>).)*|Jadro:(?:(?!</div>).)*",re.DOTALL)
    konec = re.findall(regex,htmltext)
    dude = ''.join(konec)
    lol = dude.decode("UTF-8")
    print lol
          
    scraperwiki.sqlite.save(unique_keys=[], data={"LongDesc":lol})
    i+=1