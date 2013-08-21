# -*- coding: UTF-8 -*-
#
##############################################################################
#
# == ENGLISH ==
# (italiano sotto)
#
# === LICENCE ===
# Copyright (C) 2013 Cristian Consonni
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
# If not, see <http://www.gnu.org/licenses/>.
#
# === INFO ===
#
#
# == ITALIANO == 
#
# === LICENZA ===
# Questo scraper è rilasciato con licenza GPL (v.sopra)
#
# === INFO ===
#
##############################################################################

import scraperwiki
import urllib2
from urlparse import urlparse, parse_qs
import re
import time
import lxml
import lxml.html as html

MAXTRIES = 20
def get_page(url):
    fpage = None
    i=1
    while (not fpage) or (i > MAXTRIES):
        try:
            fpage = urllib2.urlopen(url)
        except Exception as e:
            print '%s' %str(e)
            fpage = None
            i=i+1

    return fpage

def save_data(archivio):
    ntry=1
    saveres = False
    while (not saveres) or (ntry > MAXTRIES):
        try:
            scraperwiki.sqlite.save(['id'], archivio, table_name="archivi", verbose=2)
            saveres = True
        except Exception as e:
            print "Could not write on the database: %s" %str(e)
            saveres = False
            ntry += 1
            time.sleep(5)
    return saveres

def remove_br_tags(data,rmwith=''):
    p = re.compile(r'<br.*?>')
    return p.sub(rmwith, data)


SEARCHURL='http://san.beniculturali.it/web/san/trovarchivi?' \
        'p_p_id=trova_archivi_WAR_prjsanportlet_INSTANCE_Jc3O&p_p_lifecycle=1&p_p_state=normal' \
        '&p_p_mode=view&p_p_col_id=box_contenuto&p_p_col_count=1&page={page}&servizi=indifferente' \
        '&tipologia=0&comune=&action=init&lettera=&denominazione=&provincia=&regione=&step=filtra&testo='

BASEURL='http://san.beniculturali.it/web/san/'

maxidd=-1
try:
    scraperwiki.sqlite.attach("swdata")
    data = scraperwiki.sqlite.select('max(pageid) AS max FROM archivi')
    print data
    maxidd=int(data[0]['max'])
except Exception as e:
    print "No table, starting from zero"

if maxidd < 1:
    maxidd=1

maxidd=1
TOTARCHIVI=8440
PERPAGE=25
i = 0
for s in range(maxidd,TOTARCHIVI+1,PERPAGE):
    searchurl = SEARCHURL.format(page=s)
    print 'SEARCHURL:', searchurl
    
    fpage=get_page(searchurl)
    assert fpage

    page = fpage.read()

    archivio = dict()
    doc = html.document_fromstring(page)
    contenuto = doc.xpath("//div[@id='risultato_ricerca']/div[@class='paragrafi']")
    for div in contenuto:
        if div.getchildren()[0].tag != 'h2':
            continue
        city = div.text_content().strip().split(',')[-1].strip()
        archivio['city'] = city
        print city
        item = div.getchildren()[0].getchildren()[0].items()
        print item
        link = item[0][1]
        title = item[2][1]
        archivio['name'] = title
        archivio['link'] = BASEURL + link
        archivio['id'] = i
        i += 1
        save_data(archivio)