#!/usr/bin/env python


###############################################################################
# Copyright (c) 2010,2011 Floor Terra <floort@gmail.com>
# 
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
# 
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
###############################################################################

import mechanize
from BeautifulSoup import BeautifulSoup
import urllib2
import json
import sys
import pickle

BASE_URL = "http://www.cbpweb.nl/asp/"
SEARCH_FORM = BASE_URL + "ORSearch.asp"

SHARED_STACK = "stack.pickle"
CHARS = " !\"'(9876543210zyxwvutsrqponmlkjihgfedcba"

def get_item():
    items = pickle.load(open(SHARED_STACK))
    i = items.pop()
    pickle.dump(items, open(SHARED_STACK, "w"))
    return i

def add_items(items):
    i = pickle.load(open(SHARED_STACK))
    i += items
    pickle.dump(i, open(SHARED_STACK, "w"))

def clean(s):
    return strip_tags(str(s)).strip()

def strip_tags(s):
    start = s.find("<")
    if start == -1:
        return s # No tags
    end = s.find(">", start)+1
    return s[:start]+strip_tags(s[end:])


def list_postcode(pc=""):
    if len(pc) < 2:
        return False # Should give at least 2 digits
    # Start a new browseer
    br = mechanize.Browser()
    br.open(SEARCH_FORM)
    # Select the right form
    br.select_form("searchform")
    # Because the page is obfuscated, just fill in all the fields.
    for name in br.form._pairs():
        br[name[0]] = pc
    # Mark the "search by postcode" radio button
    br["level0"] = ["3"]
    # For now, just return the raw page with results
    resp = br.submit().read()
    if resp.find("Er zijn meer dan 50 meldingen gevonden.") > -1:
        return False
    elif resp.find("Er zijn geen meldingen gevonden") > -1:
        return None
    return resp

def list_name(name=""):
    if len(name) < 3:
        return False # Should give at least 3 digits
    # Start a new browseer
    br = mechanize.Browser()
    br.open(SEARCH_FORM)
    # Select the right form
    br.select_form("searchform")
    # Because the page is obfuscated, just fill in all the fields.
    for n in br.form._pairs():
        br[n[0]] = "%s%%" % (name)
    # Mark the "search by postcode" radio button
    br["level0"] = ["1"]
    # For now, just return the raw page with results
    resp = br.submit().read()
    if resp.find("Er zijn meer dan 50 meldingen gevonden.") > -1:
        return False
    elif resp.find("Er zijn geen meldingen gevonden") > -1:
        return None
    return resp


def list_companies_from_page(page):
    companies = []
    soup = BeautifulSoup(page)
    table = soup.find("table", {"border":"1"})
    rows = table.findAll("tr")[1:]
    for row in rows:
        colls = row.findAll("td")
        companies.append({
                "name": colls[0].find("a").string,
                "url": BASE_URL+colls[0].find("a")["href"],
        })
    return companies


def get_company_info(company):
    page = BeautifulSoup(urllib2.urlopen(company["url"]).read())
    company["meldingen"] = {}
    for row in page.find("table", {"class": "list"}).findAll("tr")[1:]:
        colls = row.findAll("td")
        id = colls[1].string
        url = BASE_URL + colls[0].find("a")["href"]
        description = colls[0].find("a").string
        melding = get_detailed_info(url)
        melding["url"] = url
        melding["description"] = description
        company["meldingen"][id] = melding
    return company

def parse_persoonsgegevens_table(table):
    persoonsgegevens = {}
    rows = table.findAll("tr", recursive=False)
    for r in range(1, len(rows)-1, 3):
        name = clean(rows[r].findAll("td")[1])
        value = clean(rows[r+1].findAll("td")[1])
        persoonsgegevens[name] = value
        if rows:
            persoonsgegevens["bijzonder"] = clean(rows[-1].findAll("td")[1])
    return persoonsgegevens

def parse_addres_table(table):
    addres = {}
    rows = table.findAll("tr", recursive=False)
    for r in range(len(rows)):
        colls = rows[r].findAll("td")
        name = clean(colls[0])
        value = clean(str(colls[1]).replace("<br />", "\n"))
        addres[name] = value
    return addres


def get_detailed_info(url):
    f = urllib2.urlopen(url, timeout=4)
    page = BeautifulSoup(f.read())
    info = {}
    print "PAGE:", url
    rows = page.find("table", {"class": "list"}).findAll("tr", recursive=False)
    i = 0
    while i < len(rows):
        colls = rows[i].findAll("td", recursive=False)
        if clean(colls[0]) == "Ontvanger(s)":
            values = []
            if colls[0].has_key("rowspan"):
                if len(colls) > 1:
                    values.append(clean(colls[1]))
                rs = int(colls[0]["rowspan"])
                for j in xrange(1,rs):
                    values.append(clean(rows[i+j]))
                i += rs - 1
            else:
                print "ERROR: no rowspan!"
            info["ontvangers"] = values
        elif clean(colls[0]) == "Meldingsnummer":
            info["id"] = int(clean(colls[1]))
        elif clean(colls[0]) == "Naam verwerking":
            info["naam_verwerking"] = clean(colls[1])
        elif clean(colls[0]) == "Verantwoordelijke(n)":
            values = []
            if colls[0].has_key("rowspan"):
                if len(colls) > 1:
                    values.append(parse_addres_table(colls[1].find("table")))
                rs = int(colls[0]["rowspan"])
                for j in range(1, rs):
                    values.append(parse_addres_table(rows[i+j].find("table")))
                i += rs - 1
            else:
                print "ERROR!"
            info["verantwoordelijken"] = values
        elif clean(colls[0]) == "Doel(en) van verwerking":
            values = []
            if colls[0].has_key("rowspan"):
                if len(colls) > 1:
                    values.append(clean(colls[1]))
                rs = int(colls[0]["rowspan"])
                for j in xrange(1,rs):
                    values.append(clean(rows[i+j]))
                i += rs - 1
            else:
                print "ERROR: no rowspan!"
            info["doelen"] = values
        elif clean(colls[0]) == "Betrokkene(n)":
            betrokkenen = {}
            done = False
            while not done:
                colls = rows[i+1].findAll("td", recursive=False)
                name = clean(colls[0])
                value = parse_persoonsgegevens_table(colls[1].find("table"))
                betrokkenen[name] = value
                if clean(rows[i+2]) != "":
                    done = True
                i += 2
            i -= 1
            info["betrokkenen"] = betrokkenen
        elif clean(colls[0]) == "Doorgifte buiten EU":
            v = clean(colls[1].string)
            if v == "J": v = True
            elif v == "N": v = False
            info["doorgifte_buiten_eu"] = v
        elif clean(colls[0]) == "Doorgifte passend":
            v = clean(colls[1])
            if v == "J": v = True
            elif v == "N": v = False
            info["doorgifte_passend"] = v
        else:
            print "UNKNOWN: " + clean(colls[0])
        i += 1
    return info


if __name__ == "__main__":
    try:
        f = open(SHARED_STACK, "r")
        f.close()
    except:
        print "Creating new stack"
        stack = [a+b+c for a in CHARS for b in CHARS for c in CHARS]
        pickle.dump(stack, open(SHARED_STACK, "w"))
    companies = []
    name  = get_item()
    print "Trying \"%s\"" % (name)
    page = list_name(name)
    if page == None:
        print "No pages found for '%s'" % (name)
        sys.exit()
    if not page:
        add_items([name+"%s" % (c) for c in CHARS])
        sys.exit()
    comp = list_companies_from_page(page)
    for c in comp:
        companies.append(get_company_info(c))
    print "Dumping data/%s.json" % (name)
    f = open("data/%s.json" % (name), "wb")
    json.dump(companies, f, indent=2)
    f.close()#!/usr/bin/env python


###############################################################################
# Copyright (c) 2010,2011 Floor Terra <floort@gmail.com>
# 
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
# 
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
###############################################################################

import mechanize
from BeautifulSoup import BeautifulSoup
import urllib2
import json
import sys
import pickle

BASE_URL = "http://www.cbpweb.nl/asp/"
SEARCH_FORM = BASE_URL + "ORSearch.asp"

SHARED_STACK = "stack.pickle"
CHARS = " !\"'(9876543210zyxwvutsrqponmlkjihgfedcba"

def get_item():
    items = pickle.load(open(SHARED_STACK))
    i = items.pop()
    pickle.dump(items, open(SHARED_STACK, "w"))
    return i

def add_items(items):
    i = pickle.load(open(SHARED_STACK))
    i += items
    pickle.dump(i, open(SHARED_STACK, "w"))

def clean(s):
    return strip_tags(str(s)).strip()

def strip_tags(s):
    start = s.find("<")
    if start == -1:
        return s # No tags
    end = s.find(">", start)+1
    return s[:start]+strip_tags(s[end:])


def list_postcode(pc=""):
    if len(pc) < 2:
        return False # Should give at least 2 digits
    # Start a new browseer
    br = mechanize.Browser()
    br.open(SEARCH_FORM)
    # Select the right form
    br.select_form("searchform")
    # Because the page is obfuscated, just fill in all the fields.
    for name in br.form._pairs():
        br[name[0]] = pc
    # Mark the "search by postcode" radio button
    br["level0"] = ["3"]
    # For now, just return the raw page with results
    resp = br.submit().read()
    if resp.find("Er zijn meer dan 50 meldingen gevonden.") > -1:
        return False
    elif resp.find("Er zijn geen meldingen gevonden") > -1:
        return None
    return resp

def list_name(name=""):
    if len(name) < 3:
        return False # Should give at least 3 digits
    # Start a new browseer
    br = mechanize.Browser()
    br.open(SEARCH_FORM)
    # Select the right form
    br.select_form("searchform")
    # Because the page is obfuscated, just fill in all the fields.
    for n in br.form._pairs():
        br[n[0]] = "%s%%" % (name)
    # Mark the "search by postcode" radio button
    br["level0"] = ["1"]
    # For now, just return the raw page with results
    resp = br.submit().read()
    if resp.find("Er zijn meer dan 50 meldingen gevonden.") > -1:
        return False
    elif resp.find("Er zijn geen meldingen gevonden") > -1:
        return None
    return resp


def list_companies_from_page(page):
    companies = []
    soup = BeautifulSoup(page)
    table = soup.find("table", {"border":"1"})
    rows = table.findAll("tr")[1:]
    for row in rows:
        colls = row.findAll("td")
        companies.append({
                "name": colls[0].find("a").string,
                "url": BASE_URL+colls[0].find("a")["href"],
        })
    return companies


def get_company_info(company):
    page = BeautifulSoup(urllib2.urlopen(company["url"]).read())
    company["meldingen"] = {}
    for row in page.find("table", {"class": "list"}).findAll("tr")[1:]:
        colls = row.findAll("td")
        id = colls[1].string
        url = BASE_URL + colls[0].find("a")["href"]
        description = colls[0].find("a").string
        melding = get_detailed_info(url)
        melding["url"] = url
        melding["description"] = description
        company["meldingen"][id] = melding
    return company

def parse_persoonsgegevens_table(table):
    persoonsgegevens = {}
    rows = table.findAll("tr", recursive=False)
    for r in range(1, len(rows)-1, 3):
        name = clean(rows[r].findAll("td")[1])
        value = clean(rows[r+1].findAll("td")[1])
        persoonsgegevens[name] = value
        if rows:
            persoonsgegevens["bijzonder"] = clean(rows[-1].findAll("td")[1])
    return persoonsgegevens

def parse_addres_table(table):
    addres = {}
    rows = table.findAll("tr", recursive=False)
    for r in range(len(rows)):
        colls = rows[r].findAll("td")
        name = clean(colls[0])
        value = clean(str(colls[1]).replace("<br />", "\n"))
        addres[name] = value
    return addres


def get_detailed_info(url):
    f = urllib2.urlopen(url, timeout=4)
    page = BeautifulSoup(f.read())
    info = {}
    print "PAGE:", url
    rows = page.find("table", {"class": "list"}).findAll("tr", recursive=False)
    i = 0
    while i < len(rows):
        colls = rows[i].findAll("td", recursive=False)
        if clean(colls[0]) == "Ontvanger(s)":
            values = []
            if colls[0].has_key("rowspan"):
                if len(colls) > 1:
                    values.append(clean(colls[1]))
                rs = int(colls[0]["rowspan"])
                for j in xrange(1,rs):
                    values.append(clean(rows[i+j]))
                i += rs - 1
            else:
                print "ERROR: no rowspan!"
            info["ontvangers"] = values
        elif clean(colls[0]) == "Meldingsnummer":
            info["id"] = int(clean(colls[1]))
        elif clean(colls[0]) == "Naam verwerking":
            info["naam_verwerking"] = clean(colls[1])
        elif clean(colls[0]) == "Verantwoordelijke(n)":
            values = []
            if colls[0].has_key("rowspan"):
                if len(colls) > 1:
                    values.append(parse_addres_table(colls[1].find("table")))
                rs = int(colls[0]["rowspan"])
                for j in range(1, rs):
                    values.append(parse_addres_table(rows[i+j].find("table")))
                i += rs - 1
            else:
                print "ERROR!"
            info["verantwoordelijken"] = values
        elif clean(colls[0]) == "Doel(en) van verwerking":
            values = []
            if colls[0].has_key("rowspan"):
                if len(colls) > 1:
                    values.append(clean(colls[1]))
                rs = int(colls[0]["rowspan"])
                for j in xrange(1,rs):
                    values.append(clean(rows[i+j]))
                i += rs - 1
            else:
                print "ERROR: no rowspan!"
            info["doelen"] = values
        elif clean(colls[0]) == "Betrokkene(n)":
            betrokkenen = {}
            done = False
            while not done:
                colls = rows[i+1].findAll("td", recursive=False)
                name = clean(colls[0])
                value = parse_persoonsgegevens_table(colls[1].find("table"))
                betrokkenen[name] = value
                if clean(rows[i+2]) != "":
                    done = True
                i += 2
            i -= 1
            info["betrokkenen"] = betrokkenen
        elif clean(colls[0]) == "Doorgifte buiten EU":
            v = clean(colls[1].string)
            if v == "J": v = True
            elif v == "N": v = False
            info["doorgifte_buiten_eu"] = v
        elif clean(colls[0]) == "Doorgifte passend":
            v = clean(colls[1])
            if v == "J": v = True
            elif v == "N": v = False
            info["doorgifte_passend"] = v
        else:
            print "UNKNOWN: " + clean(colls[0])
        i += 1
    return info


if __name__ == "__main__":
    try:
        f = open(SHARED_STACK, "r")
        f.close()
    except:
        print "Creating new stack"
        stack = [a+b+c for a in CHARS for b in CHARS for c in CHARS]
        pickle.dump(stack, open(SHARED_STACK, "w"))
    companies = []
    name  = get_item()
    print "Trying \"%s\"" % (name)
    page = list_name(name)
    if page == None:
        print "No pages found for '%s'" % (name)
        sys.exit()
    if not page:
        add_items([name+"%s" % (c) for c in CHARS])
        sys.exit()
    comp = list_companies_from_page(page)
    for c in comp:
        companies.append(get_company_info(c))
    print "Dumping data/%s.json" % (name)
    f = open("data/%s.json" % (name), "wb")
    json.dump(companies, f, indent=2)
    f.close()