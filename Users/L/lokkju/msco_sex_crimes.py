import scraperwiki
import os
import json
import sys
import urllib
import datetime

sourcescraper = 'mcso_inmate_booking_data_parse'

LIMIT = 50
OFFSET = 0
CRIMES = (
  "ABUSE CORPSE 2 (C Felony)",
  "ASSAULT 4 DV-FELONY (C Felony)",
  "ASSAULT I - DV (A Felony)",
  "ASSAULT II - DV (B Felony)",
  "ASSAULT III - DV (C Felony)",
  "ASSAULT IV - DV (A Misdemeanor)",
)

scraperwiki.sqlite.attach(sourcescraper, "src")

def all_charges():
    result = scraperwiki.sqlite.select("DISTINCT charge from charge ORDER BY charge ASC")
    charges = []
    for r in result:
        charges.append(r['charge'])
    return charges

def records():
    q_where = "WHERE 1=1"
    q_vars = []
    if len(CRIMES) > 0:
        q_where += " AND ( 1=0 "
        for c in CRIMES:
            q_where += " OR charge = ?"
        q_where += " ) "
    q_vars.extend(CRIMES)
    q_vars.append(OFFSET)
    q_vars.append(LIMIT*2)
    q_vars.append(LIMIT)
    q_str = "* from booking_detail where booking_id IN (SELECT DISTINCT booking_id FROM `case` WHERE id IN (SELECT DISTINCT case_id FROM charge %s LIMIT ?,?)) LIMIT ?" % q_where
    print q_str
    result = scraperwiki.sqlite.select(q_str,q_vars)
    for r in result:
        print r

#result = scraperwiki.sqlite.select("SELECT case_id FROM charge WHERE booking_date <= ? AND booking_date >= ?",
#(end_date.strftime("%s"),start_date.strftime("%s")))

records()import scraperwiki
import os
import json
import sys
import urllib
import datetime

sourcescraper = 'mcso_inmate_booking_data_parse'

LIMIT = 50
OFFSET = 0
CRIMES = (
  "ABUSE CORPSE 2 (C Felony)",
  "ASSAULT 4 DV-FELONY (C Felony)",
  "ASSAULT I - DV (A Felony)",
  "ASSAULT II - DV (B Felony)",
  "ASSAULT III - DV (C Felony)",
  "ASSAULT IV - DV (A Misdemeanor)",
)

scraperwiki.sqlite.attach(sourcescraper, "src")

def all_charges():
    result = scraperwiki.sqlite.select("DISTINCT charge from charge ORDER BY charge ASC")
    charges = []
    for r in result:
        charges.append(r['charge'])
    return charges

def records():
    q_where = "WHERE 1=1"
    q_vars = []
    if len(CRIMES) > 0:
        q_where += " AND ( 1=0 "
        for c in CRIMES:
            q_where += " OR charge = ?"
        q_where += " ) "
    q_vars.extend(CRIMES)
    q_vars.append(OFFSET)
    q_vars.append(LIMIT*2)
    q_vars.append(LIMIT)
    q_str = "* from booking_detail where booking_id IN (SELECT DISTINCT booking_id FROM `case` WHERE id IN (SELECT DISTINCT case_id FROM charge %s LIMIT ?,?)) LIMIT ?" % q_where
    print q_str
    result = scraperwiki.sqlite.select(q_str,q_vars)
    for r in result:
        print r

#result = scraperwiki.sqlite.select("SELECT case_id FROM charge WHERE booking_date <= ? AND booking_date >= ?",
#(end_date.strftime("%s"),start_date.strftime("%s")))

records()