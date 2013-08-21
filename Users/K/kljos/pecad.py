import scraperwiki
import urllib2, urllib
import sqlite3
import contextlib
from bs4 import *
import contextlib
import re
from time import sleep

#scraperwiki.sqlite.execute('DROP TABLE IF EXISTS modis;')
scraperwiki.sqlite.execute('CREATE TABLE IF NOT EXISTS modis (`id` VARCHAR, `date` VARCHAR, `aqua` VARCHAR PRIMARY KEY, `terra` VARCHAR);')

baseUrl = "http://lance-modis.eosdis.nasa.gov/imagery/subsets/RRGlobal_"
#FILES = ['r11c16', 'r11c17', 'r11c18', 'r11c19', 'r11c20', 'r11c21', 'r11c22', 'r11c23', 'r11c24', 'r11c25', 'r11c26', 'r11c27', 'r11c28', 'r11c29', 'r11c30', 'r11c31', 'r11c32', 'r11c33', 'r11c34', 'r11c35', 'r11c36', 'r12c05', 'r12c06', 'r12c07', 'r12c08', 'r12c09', 'r12c10', 'r12c11', 'r12c12', 'r12c13', 'r12c14', 'r12c15', 'r12c16', 'r12c17', 'r12c18', 'r12c19', 'r12c20', 'r12c21', 'r12c22', 'r12c23', 'r12c24', 'r12c25', 'r12c26', 'r12c27', 'r12c28', 'r12c29', 'r12c30', 'r12c31', 'r12c32', 'r12c33', 'r12c34', 'r12c35', 'r12c36', 'r13c05', 'r13c06', 'r13c07', 'r13c08', 'r13c09', 'r13c10', 'r13c11', 'r13c12', 'r13c13', 'r13c14', 'r13c15', 'r13c16', 'r13c17', 'r13c18', 'r13c19', 'r13c20', 'r13c21', 'r13c22', 'r13c23', 'r13c24', 'r13c25', 'r13c26', 'r13c27', 'r13c28', 'r13c29', 'r13c30', 'r13c31', 'r13c32', 'r13c33', 'r13c34', 'r13c35', 'r13c36', 'r14c05', 'r14c06', 'r14c07', 'r14c08', 'r14c09', 'r14c10', 'r14c11', 'r14c12', 'r14c13', 'r14c14', 'r14c15', 'r14c16', 'r14c17', 'r14c18', 'r14c19', 'r14c20', 'r14c21','r03c11', 'r03c12', 'r04c11', 'r04c12', 'r04c38', 'r04c39', 'r05c11', 'r05c12', 'r05c13', 'r05c14', 'r05c21', 'r05c22', 'r05c32', 'r05c33', 'r05c34', 'r05c35', 'r05c36', 'r05c37', 'r05c38', 'r05c39', 'r06c11', 'r06c12', 'r06c13', 'r06c14', 'r06c21', 'r06c22', 'r06c23', 'r06c24', 'r06c25', 'r06c32', 'r06c33', 'r06c34', 'r06c35', 'r06c36', 'r06c37', 'r06c38', 'r06c39', 'r07c11', 'r07c12', 'r07c13', 'r07c14', 'r07c15', 'r07c20', 'r07c21', 'r07c22', 'r07c23', 'r07c24', 'r07c25', 'r07c26', 'r07c32','r07c33', 'r07c34', 'r07c35', 'r07c36', 'r07c37', 'r07c38', 'r07c39', 'r08c11', 'r08c12', 'r08c13', 'r08c14', 'r08c15', 'r08c16', 'r08c17', 'r08c18', 'r08c19', 'r08c20', 'r08c21','r08c22', 'r08c23', 'r08c24', 'r08c25', 'r08c26', 'r08c32', 'r08c33', 'r08c34', 'r08c35', 'r08c36', 'r08c37', 'r08c38', 'r08c39', 'r09c10', 'r09c11', 'r09c12', 'r09c13', 'r09c14', 'r09c15', 'r09c16','r09c17', 'r09c18', 'r09c19', 'r09c20', 'r09c21', 'r09c22', 'r09c23', 'r09c24', 'r09c25','r09c26','r09c30', 'r09c31', 'r09c32', 'r09c33', 'r09c34', 'r09c35', 'r09c36', 'r09c37', 'r10c06', 'r10c07', 'r10c08', 'r10c09', 'r10c10', 'r10c11', 'r10c12', 'r10c13', 'r10c14', 'r10c15', 'r10c16', 'r10c17', 'r10c18', 'r10c19', 'r10c20', 'r10c21', 'r10c22', 'r10c23', 'r10c24', 'r10c25', 'r10c26', 'r10c27', 'r10c28', 'r10c29', 'r10c30', 'r10c31', 'r10c32', 'r10c33', 'r10c34', 'r10c35', 'r10c36', 'r11c06', 'r11c07', 'r11c08', 'r11c09', 'r11c10', 'r11c11', 'r11c12', 'r11c13', 'r11c14', 'r11c15', 'r14c22', 'r14c23', 'r14c24', 'r14c25', 'r14c26', 'r14c27', 'r14c28', 'r14c29', 'r14c30', 'r14c31', 'r14c32', 'r14c33', 'r14c34', 'r14c35', 'r14c36', 'r15c05', 'r15c06', 'r15c07', 'r15c08', 'r15c09', 'r15c10', 'r15c11', 'r15c12', 'r15c13', 'r15c14', 'r15c15', 'r15c16', 'r15c17', 'r15c18', 'r15c19', 'r15c20', 'r15c21', 'r15c22', 'r15c23', 'r15c24', 'r15c25', 'r15c26', 'r15c27', 'r15c28', 'r15c29', 'r15c30', 'r15c31', 'r15c32', 'r15c33', 'r15c34', 'r15c35', 'r15c36', 'r15c37', 'r15c38', 'r15c39', 'r16c00', 'r16c01', 'r16c02', 'r16c03', 'r16c04', 'r16c05', 'r16c06', 'r16c07', 'r16c08', 'r16c09', 'r16c10', 'r16c11', 'r16c12', 'r16c13', 'r16c14', 'r16c15', 'r16c16', 'r16c17', 'r16c18', 'r16c19', 'r16c20', 'r16c21', 'r16c22', 'r16c23', 'r16c24', 'r16c25', 'r16c26', 'r16c27', 'r16c28', 'r16c29', 'r16c30', 'r16c31', 'r16c32', 'r16c33', 'r16c34', 'r16c35', 'r16c36', 'r16c37', 'r16c38', 'r16c39', 'r17c00', 'r17c01', 'r17c02', 'r17c03', 'r17c04', 'r17c05', 'r17c06', 'r17c07', 'r17c08', 'r17c09', 'r17c10', 'r17c11', 'r17c12', 'r17c13', 'r17c14', 'r17c15', 'r17c16', 'r17c17', 'r17c18', 'r17c19', 'r17c20', 'r17c21', 'r17c22', 'r17c23', 'r17c24', 'r17c25', 'r17c26', 'r17c27', 'r17c28', 'r17c29', 'r17c30', 'r17c31', 'r17c32', 'r17c33', 'r17c34', 'r17c35', 'r17c36', 'r17c37', 'r17c38', 'r17c39', 'r18c00', 'r18c01', 'r18c02', 'r18c03', 'r18c08', 'r18c09', 'r18c10', 'r18c11', 'r18c12', 'r18c13', 'r18c14', 'r18c15', 'r18c16'] 
#FILES=['r07c33','r09c16','r17c00','r17c12','r17c13','r17c25','r17c37','r18c00','r18c08','r18c10','r18c16']

FILES=["r07c33", "r09c16", "r16c15", "r16c16", "r16c17", "r16c18", "r16c19", "r16c20", "r16c21", "r16c22", "r16c24", "r16c25", "r16c26", "r16c27", "r16c28", "r16c29", "r16c30", "r16c31", "r16c32", "r16c33", "r16c34", "r16c35", "r16c36", "r16c37", "r16c39", "r17c00", "r17c01", "r17c03", "r17c04", "r17c05", "r17c06", "r17c07", "r17c08", "r17c09", "r17c10", "r17c11", "r17c12", "r17c13", "r17c14", "r17c15", "r17c16", "r17c17", "r17c18", "r17c19", "r17c20", "r17c21", "r17c22", "r17c23", "r17c24", "r17c25", "r17c26", "r17c27", "r17c28", "r17c29", "r17c30", "r17c31", "r17c32", "r17c33", "r17c34", "r17c35", "r17c36", "r17c37", "r17c38", "r17c39", "r18c00", "r18c01", "r18c02", "r18c03"]
#FILES=["r18c08", "r18c09", "r18c10", "r18c11", "r18c12", "r18c13", "r18c14", "r18c15", "r18c16"]

for i in range(len(FILES)):

    url = baseUrl + FILES[i]
    print url
    request = urllib2.Request(url)
    opener = urllib2.build_opener()
    request.add_header('User-Agent', 'OpenAnything/1.0 +http://diveintopython.org/')
    x = opener.open(request).read()
    soup = BeautifulSoup(x)
    results = soup.body.find('a',attrs={'href':re.compile('2011')})
    url = baseUrl + FILES[i] + '/' + results['href']
    print url
    request = urllib2.Request(url)
    opener = urllib2.build_opener()
    request.add_header('User-Agent', 'OpenAnything/1.0 +http://diveintopython.org/')
    x = opener.open(request).read()
    soup = BeautifulSoup(x)
    dataLayer1 = soup.find('a', attrs={'href': re.compile('aqua\.250m\.jpg$')})
    dataLayer2 = soup.find('a', attrs={'href': re.compile('terra\.250m\.jpg$')})
    if dataLayer1 != None and dataLayer2 != None:
        record = {}
        record['aqua'] = baseUrl + FILES[i] + '/' + results['href'] + dataLayer1['href']
        record['terra'] = baseUrl + FILES[i] + '/' + results['href'] + dataLayer2['href']
        record['id'] = FILES[i]
        record['date'] = results['href'].replace('/','')
        try:
            scraperwiki.sqlite.execute("INSERT OR IGNORE into modis values( ?, ?, ?, ?)",(record["id"], record["date"],record["aqua"],record["terra"]))
            scraperwiki.sqlite.commit()
            print record
        except:
            print("fail")
    sleep(.25)
