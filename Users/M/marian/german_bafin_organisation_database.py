# This scraper should extract company data from http://ww2.bafin.de/database/InstInfo/
#
# CAUTION! This is work in progress.

import scraperwiki
import mechanize
import sys

def save_names_from_list(html):
    institute_matches = re.findall('institutId=([0-9]+)">([^<]+)<\/a>', html, flags=re.IGNORECASE)
    for inst in institute_matches:
        record = {'bafin_institute_id': inst[0], 'name': inst[1].decode('ISO-8859-1')}
        scraperwiki.sqlite.save(unique_keys=["bafin_institute_id"], data=record)

def main():
    # gather entry urls
    letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    letter_urls = []
    for letter in letters:
        letter_urls.append('http://ww2.bafin.de/database/InstInfo/sucheForm.do?institutName='+ letter +'&6578706f7274=1&d-4012550-e=1')
    letter_urls.append('http://ww2.bafin.de/database/InstInfo/sucheForm.do?sondersucheInstitut=true&6578706f7274=1&d-4012550-e=1')
    
    br = mechanize.Browser()
    br.set_handle_robots(False)

    # iterate over all available entry urls
    for letter_url in letter_urls:
        response = br.open(letter_url)
        csv_content = response.read()
        linecount = 0
        for line in csv_content.split('\n'):
            if linecount == 0:
                # header row
                items = line.split(';')
                if len(items) != 7:
                    print "Error 1: CSV header row should have 7 items, but has " + str(len(items))
                    sys.exit(1)
                else:
                    if items[0] != 'REFERENZ':
                        print "Error 2: Unexpected CSV header field " + items[0] + " instead of REFERENZ"
                        sys.exit(1)
                    elif items[1] != 'NAME':
                        print "Error 2: Unexpected CSV header field " + items[1] + " instead of NAME"
                        sys.exit(1)
                    elif items[2] != 'PLZ':
                        print "Error 2: Unexpected CSV header field " + items[2] + " instead of PLZ"
                        sys.exit(1)
                    elif items[3] != 'ORT':
                        print "Error 2: Unexpected CSV header field " + items[3] + " instead of ORT"
                        sys.exit(1)
                    elif items[4] != 'STRASSE':
                        print "Error 2: Unexpected CSV header field " + items[4] + " instead of STRASSE"
                        sys.exit(1)
                    elif items[5] != 'LAND':
                        print "Error 2: Unexpected CSV header field " + items[5] + " instead of LAND"
                        sys.exit(1)
                    elif items[6] != 'GATTUNG':
                        print "Error 2: Unexpected CSV header field " + items[6] + " instead of GATTUNG"
                        sys.exit(1)
            else:
                # other rows
                if line != '':
                    items = line.split(';')
                    record = {
                        'bafin_institute_id': items[0],
                        'name': items[1].decode('ISO-8859-1'),
                        'postalcode': items[2].decode('ISO-8859-1'),
                        'city': items[3].decode('ISO-8859-1'),
                        'address': items[4].decode('ISO-8859-1'),
                        'country': items[5].decode('ISO-8859-1'),
                        'type': items[6].decode('ISO-8859-1')
                    }
                    #print record
                    scraperwiki.sqlite.save(unique_keys=["bafin_institute_id"], data=record)
            linecount += 1
main()# This scraper should extract company data from http://ww2.bafin.de/database/InstInfo/
#
# CAUTION! This is work in progress.

import scraperwiki
import mechanize
import sys

def save_names_from_list(html):
    institute_matches = re.findall('institutId=([0-9]+)">([^<]+)<\/a>', html, flags=re.IGNORECASE)
    for inst in institute_matches:
        record = {'bafin_institute_id': inst[0], 'name': inst[1].decode('ISO-8859-1')}
        scraperwiki.sqlite.save(unique_keys=["bafin_institute_id"], data=record)

def main():
    # gather entry urls
    letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    letter_urls = []
    for letter in letters:
        letter_urls.append('http://ww2.bafin.de/database/InstInfo/sucheForm.do?institutName='+ letter +'&6578706f7274=1&d-4012550-e=1')
    letter_urls.append('http://ww2.bafin.de/database/InstInfo/sucheForm.do?sondersucheInstitut=true&6578706f7274=1&d-4012550-e=1')
    
    br = mechanize.Browser()
    br.set_handle_robots(False)

    # iterate over all available entry urls
    for letter_url in letter_urls:
        response = br.open(letter_url)
        csv_content = response.read()
        linecount = 0
        for line in csv_content.split('\n'):
            if linecount == 0:
                # header row
                items = line.split(';')
                if len(items) != 7:
                    print "Error 1: CSV header row should have 7 items, but has " + str(len(items))
                    sys.exit(1)
                else:
                    if items[0] != 'REFERENZ':
                        print "Error 2: Unexpected CSV header field " + items[0] + " instead of REFERENZ"
                        sys.exit(1)
                    elif items[1] != 'NAME':
                        print "Error 2: Unexpected CSV header field " + items[1] + " instead of NAME"
                        sys.exit(1)
                    elif items[2] != 'PLZ':
                        print "Error 2: Unexpected CSV header field " + items[2] + " instead of PLZ"
                        sys.exit(1)
                    elif items[3] != 'ORT':
                        print "Error 2: Unexpected CSV header field " + items[3] + " instead of ORT"
                        sys.exit(1)
                    elif items[4] != 'STRASSE':
                        print "Error 2: Unexpected CSV header field " + items[4] + " instead of STRASSE"
                        sys.exit(1)
                    elif items[5] != 'LAND':
                        print "Error 2: Unexpected CSV header field " + items[5] + " instead of LAND"
                        sys.exit(1)
                    elif items[6] != 'GATTUNG':
                        print "Error 2: Unexpected CSV header field " + items[6] + " instead of GATTUNG"
                        sys.exit(1)
            else:
                # other rows
                if line != '':
                    items = line.split(';')
                    record = {
                        'bafin_institute_id': items[0],
                        'name': items[1].decode('ISO-8859-1'),
                        'postalcode': items[2].decode('ISO-8859-1'),
                        'city': items[3].decode('ISO-8859-1'),
                        'address': items[4].decode('ISO-8859-1'),
                        'country': items[5].decode('ISO-8859-1'),
                        'type': items[6].decode('ISO-8859-1')
                    }
                    #print record
                    scraperwiki.sqlite.save(unique_keys=["bafin_institute_id"], data=record)
            linecount += 1
main()# This scraper should extract company data from http://ww2.bafin.de/database/InstInfo/
#
# CAUTION! This is work in progress.

import scraperwiki
import mechanize
import sys

def save_names_from_list(html):
    institute_matches = re.findall('institutId=([0-9]+)">([^<]+)<\/a>', html, flags=re.IGNORECASE)
    for inst in institute_matches:
        record = {'bafin_institute_id': inst[0], 'name': inst[1].decode('ISO-8859-1')}
        scraperwiki.sqlite.save(unique_keys=["bafin_institute_id"], data=record)

def main():
    # gather entry urls
    letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    letter_urls = []
    for letter in letters:
        letter_urls.append('http://ww2.bafin.de/database/InstInfo/sucheForm.do?institutName='+ letter +'&6578706f7274=1&d-4012550-e=1')
    letter_urls.append('http://ww2.bafin.de/database/InstInfo/sucheForm.do?sondersucheInstitut=true&6578706f7274=1&d-4012550-e=1')
    
    br = mechanize.Browser()
    br.set_handle_robots(False)

    # iterate over all available entry urls
    for letter_url in letter_urls:
        response = br.open(letter_url)
        csv_content = response.read()
        linecount = 0
        for line in csv_content.split('\n'):
            if linecount == 0:
                # header row
                items = line.split(';')
                if len(items) != 7:
                    print "Error 1: CSV header row should have 7 items, but has " + str(len(items))
                    sys.exit(1)
                else:
                    if items[0] != 'REFERENZ':
                        print "Error 2: Unexpected CSV header field " + items[0] + " instead of REFERENZ"
                        sys.exit(1)
                    elif items[1] != 'NAME':
                        print "Error 2: Unexpected CSV header field " + items[1] + " instead of NAME"
                        sys.exit(1)
                    elif items[2] != 'PLZ':
                        print "Error 2: Unexpected CSV header field " + items[2] + " instead of PLZ"
                        sys.exit(1)
                    elif items[3] != 'ORT':
                        print "Error 2: Unexpected CSV header field " + items[3] + " instead of ORT"
                        sys.exit(1)
                    elif items[4] != 'STRASSE':
                        print "Error 2: Unexpected CSV header field " + items[4] + " instead of STRASSE"
                        sys.exit(1)
                    elif items[5] != 'LAND':
                        print "Error 2: Unexpected CSV header field " + items[5] + " instead of LAND"
                        sys.exit(1)
                    elif items[6] != 'GATTUNG':
                        print "Error 2: Unexpected CSV header field " + items[6] + " instead of GATTUNG"
                        sys.exit(1)
            else:
                # other rows
                if line != '':
                    items = line.split(';')
                    record = {
                        'bafin_institute_id': items[0],
                        'name': items[1].decode('ISO-8859-1'),
                        'postalcode': items[2].decode('ISO-8859-1'),
                        'city': items[3].decode('ISO-8859-1'),
                        'address': items[4].decode('ISO-8859-1'),
                        'country': items[5].decode('ISO-8859-1'),
                        'type': items[6].decode('ISO-8859-1')
                    }
                    #print record
                    scraperwiki.sqlite.save(unique_keys=["bafin_institute_id"], data=record)
            linecount += 1
main()# This scraper should extract company data from http://ww2.bafin.de/database/InstInfo/
#
# CAUTION! This is work in progress.

import scraperwiki
import mechanize
import sys

def save_names_from_list(html):
    institute_matches = re.findall('institutId=([0-9]+)">([^<]+)<\/a>', html, flags=re.IGNORECASE)
    for inst in institute_matches:
        record = {'bafin_institute_id': inst[0], 'name': inst[1].decode('ISO-8859-1')}
        scraperwiki.sqlite.save(unique_keys=["bafin_institute_id"], data=record)

def main():
    # gather entry urls
    letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    letter_urls = []
    for letter in letters:
        letter_urls.append('http://ww2.bafin.de/database/InstInfo/sucheForm.do?institutName='+ letter +'&6578706f7274=1&d-4012550-e=1')
    letter_urls.append('http://ww2.bafin.de/database/InstInfo/sucheForm.do?sondersucheInstitut=true&6578706f7274=1&d-4012550-e=1')
    
    br = mechanize.Browser()
    br.set_handle_robots(False)

    # iterate over all available entry urls
    for letter_url in letter_urls:
        response = br.open(letter_url)
        csv_content = response.read()
        linecount = 0
        for line in csv_content.split('\n'):
            if linecount == 0:
                # header row
                items = line.split(';')
                if len(items) != 7:
                    print "Error 1: CSV header row should have 7 items, but has " + str(len(items))
                    sys.exit(1)
                else:
                    if items[0] != 'REFERENZ':
                        print "Error 2: Unexpected CSV header field " + items[0] + " instead of REFERENZ"
                        sys.exit(1)
                    elif items[1] != 'NAME':
                        print "Error 2: Unexpected CSV header field " + items[1] + " instead of NAME"
                        sys.exit(1)
                    elif items[2] != 'PLZ':
                        print "Error 2: Unexpected CSV header field " + items[2] + " instead of PLZ"
                        sys.exit(1)
                    elif items[3] != 'ORT':
                        print "Error 2: Unexpected CSV header field " + items[3] + " instead of ORT"
                        sys.exit(1)
                    elif items[4] != 'STRASSE':
                        print "Error 2: Unexpected CSV header field " + items[4] + " instead of STRASSE"
                        sys.exit(1)
                    elif items[5] != 'LAND':
                        print "Error 2: Unexpected CSV header field " + items[5] + " instead of LAND"
                        sys.exit(1)
                    elif items[6] != 'GATTUNG':
                        print "Error 2: Unexpected CSV header field " + items[6] + " instead of GATTUNG"
                        sys.exit(1)
            else:
                # other rows
                if line != '':
                    items = line.split(';')
                    record = {
                        'bafin_institute_id': items[0],
                        'name': items[1].decode('ISO-8859-1'),
                        'postalcode': items[2].decode('ISO-8859-1'),
                        'city': items[3].decode('ISO-8859-1'),
                        'address': items[4].decode('ISO-8859-1'),
                        'country': items[5].decode('ISO-8859-1'),
                        'type': items[6].decode('ISO-8859-1')
                    }
                    #print record
                    scraperwiki.sqlite.save(unique_keys=["bafin_institute_id"], data=record)
            linecount += 1
main()