# Liberally copied/pasted from http://scraperwiki.com/scrapers/cabinet_office_spend_data/edit/

import scraperwiki
import lxml.html
import urllib
import csv
import dateutil.parser
import urllib2
import StringIO

def parsemonths(d):
    d = d.strip()
    print d
    return dateutil.parser.parse(d, yearfirst=True, dayfirst=True).date()

def links(url):
    lines = urllib.urlopen(url.replace(' ','%20')).readlines()
    lines = [ l.decode('ISO-8859-1').encode('utf-8') for l in lines ]
    header = []
    clist = list(csv.reader(lines))
    while clist[0][1] == "":
        clist.pop(0)
    header = clist.pop(0)
    header = header[:8]
    for i in range(8):
        header[i] = header[i].strip()

    # Rename/capitalize for consistency with Cabinet Office
    if header[0] == 'Department family':
        header[0] = 'Departmental Family'
    if header[3] == 'Expense type':
        header[3] = 'Expense Type'
    if header[4] == 'Expense area':
        header[4] = 'Expense Area'
    if header[6] == 'Transaction number':
        header[6] = 'Transaction Number'
    
    for row in clist:
        if row[2] != "":        
            data = dict(zip(header, row)) 
            data['URL'] = url
            data['Date'] = parsemonths(data['Date'])
    
        # Need 'Expense Type' in here because HMRC splits invoices up,
        # so has duplicate transaction numbers.
        scraperwiki.sqlite.save(unique_keys=['URL','Transaction Number','Expense Type'], data=data)

def refine(data, operations):
    return urllib2.urlopen('http://refine.scraperwiki.com:8080/transform',
    urllib.urlencode({'format': 'csv',
       'operations-string': operations,
       'data-string': data,
       'data-filetype': 'text/csv',
       'data-filename': 'hmrcspending.csv'})).read()


# Raw string to avoid backslash problems.
operations = r'''
[
  {
    "op": "core/text-transform",
    "description": "Text transform on cells in column Amount using expression grel:value.replace(/[^0-9.-E]/,'').toNumber()",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "Amount",
    "expression": "grel:value.replace(/[^0-9.-E]/,'').toNumber()",
    "onError": "store-error",
    "repeat": false,
    "repeatCount": 10
  },
  {
    "op": "core/mass-edit",
    "description": "Mass edit cells in column Supplier",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "Supplier",
    "expression": "value",
    "edits": [
      {
        "fromBlank": false,
        "fromError": false,
        "from": [
          "West Lothian Council",
          "WEST LOTHIAN COUNCIL"
        ],
        "to": "West Lothian Council"
      },
      {
        "fromBlank": false,
        "fromError": false,
        "from": [
          "Banner Business Services Ltd",
          "Banner Business Services Ltd "
        ],
        "to": "Banner Business Services Ltd"
      },
      {
        "fromBlank": false,
        "fromError": false,
        "from": [
          "Specialist Computer Ctr",
          "Specialist Computer Ctr "
        ],
        "to": "Specialist Computer Ctr"
      },
      {
        "fromBlank": false,
        "fromError": false,
        "from": [
          "J Winsley Ltd",
          "J. Winsley Ltd"
        ],
        "to": "J Winsley Ltd"
      },
      {
        "fromBlank": false,
        "fromError": false,
        "from": [
          "OPEX CORPORATION",
          "Opex Corporation"
        ],
        "to": "Opex Corporation"
      },
      {
        "fromBlank": false,
        "fromError": false,
        "from": [
          "Adare Halcyon Limited",
          "Adare Halcyon Limited "
        ],
        "to": "Adare Halcyon Limited"
      },
      {
        "fromBlank": false,
        "fromError": false,
        "from": [
          "Adare Halcyon Ltd",
          "Adare Halcyon Ltd "
        ],
        "to": "Adare Halcyon Limited"
      }
    ]
  },
  {
    "op": "core/mass-edit",
    "description": "Mass edit cells in column Supplier",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "Supplier",
    "expression": "value",
    "edits": [
      {
        "fromBlank": false,
        "fromError": false,
        "from": [
          "Department of the Environment",
          "Department of the Enviroment"
        ],
        "to": "Department of the Environment"
      }
    ]
  },
  {
    "op": "core/mass-edit",
    "description": "Mass edit cells in column Supplier",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "Supplier",
    "expression": "value",
    "edits": [
      {
        "fromBlank": false,
        "fromError": false,
        "from": [
          "Foreign and Commonwealth Office",
          "Foreign and Commonwealth"
        ],
        "to": "Foreign and Commonwealth Office"
      },
      {
        "fromBlank": false,
        "fromError": false,
        "from": [
          "Paragon UK (Print) Ltd",
          "Paragon UK (Print)"
        ],
        "to": "Paragon UK (Print) Ltd"
      }
    ]
  },
  {
    "op": "core/mass-edit",
    "description": "Mass edit cells in column Supplier",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "Supplier",
    "expression": "value",
    "edits": [
      {
        "fromBlank": false,
        "fromError": false,
        "from": [
          "RBSG Central 10000607",
          "RBSG Central"
        ],
        "to": "RBSG Central"
      },
      {
        "fromBlank": false,
        "fromError": false,
        "from": [
          "City Of Edinburgh Council",
          "City of Edinburgh Council - 3900401"
        ],
        "to": "City Of Edinburgh Council"
      }
    ]
  },
  {
    "op": "core/mass-edit",
    "description": "Mass edit cells in column Expense Area",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "Expense Area",
    "expression": "value",
    "edits": [
      {
        "fromBlank": false,
        "fromError": false,
        "from": [
          "Knowledge Analysis & Intelligence",
          "Knowledge, Analysis & Intelligence"
        ],
        "to": "Knowledge, Analysis & Intelligence"
      }
    ]
  },
  {
    "op": "core/mass-edit",
    "description": "Mass edit cells in column Expense Type",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "Expense Type",
    "expression": "value",
    "edits": [
      {
        "fromBlank": false,
        "fromError": false,
        "from": [
          "Data Output Production",
          "Data output production"
        ],
        "to": "Data Output Production"
      },
      {
        "fromBlank": false,
        "fromError": false,
        "from": [
          "Prof bodies subs",
          "Prof bodies Subs"
        ],
        "to": "Prof bodies subs"
      },
      {
        "fromBlank": false,
        "fromError": false,
        "from": [
          "Commission Fees",
          "Commission Fees "
        ],
        "to": "Commission Fees"
      },
      {
        "fromBlank": false,
        "fromError": false,
        "from": [
          "GSI Line Rental",
          "GSI Line Rental "
        ],
        "to": "GSI Line Rental"
      },
      {
        "fromBlank": false,
        "fromError": false,
        "from": [
          "STEPS Facility Payments (FUP) ",
          "STEPS Facility Payments (FUP)"
        ],
        "to": "STEPS Facility Payments (FUP)"
      },
      {
        "fromBlank": false,
        "fromError": false,
        "from": [
          "Court Fees",
          "Court Fees  "
        ],
        "to": "Court Fees"
      }
    ]
  },
  {
    "op": "core/mass-edit",
    "description": "Mass edit cells in column Expense Type",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "Expense Type",
    "expression": "value",
    "edits": [
      {
        "fromBlank": false,
        "fromError": false,
        "from": [
          "Travel agencies ",
          "Travel agencies"
        ],
        "to": "Travel agencies"
      }
    ]
  },
  {
    "op": "core/mass-edit",
    "description": "Mass edit cells in column Expense Type",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "Expense Type",
    "expression": "value",
    "edits": [
      {
        "fromBlank": false,
        "fromError": false,
        "from": [
          "Fixed Telephony Services to HMRC and VOA",
          "Fixed Telephony Service to HMRC and VOA"
        ],
        "to": "Fixed Telephony Services to HMRC and VOA"
      }
    ]
  },
  {
    "op": "core/mass-edit",
    "description": "Mass edit cells in column Expense Type",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "Expense Type",
    "expression": "value",
    "edits": [
      {
        "fromBlank": false,
        "fromError": false,
        "from": [
          "County Court Proceed",
          "County Court Proceedings"
        ],
        "to": "County Court Proceedings"
      },
      {
        "fromBlank": false,
        "fromError": false,
        "from": [
          "Subscriptions to Pub",
          "Subscriptions to Publications"
        ],
        "to": "Subscriptions to Publications"
      },
      {
        "fromBlank": false,
        "fromError": false,
        "from": [
          "Storage Seized Goods",
          "Storage of Seized Goods"
        ],
        "to": "Storage of Seized Goods"
      }
    ]
  },
  {
    "op": "core/mass-edit",
    "description": "Mass edit cells in column Departmental Family",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "Departmental Family",
    "expression": "value",
    "edits": [
      {
        "fromBlank": false,
        "fromError": false,
        "from": [
          "Department family"
        ],
        "to": "HMRC"
      }
    ]
  }
]
'''

data_url = "http://www.hmrc.gov.uk/transparency/spending-over-25k.htm"
root = lxml.html.parse(data_url).getroot()
anchors = root.cssselect("ul a")

for el in anchors:
    el.make_links_absolute(data_url)
    anyurl = el.attrib.get("href")
    
    if ".csv" in anyurl:
        links(anyurl)

data = urllib2.urlopen('http://scraperwiki.com/api/1.0/datastore/sqlite?format=csv&name=hmrc_spending&query=select+*+from+`swdata`').read()

csv_file = StringIO.StringIO(refine(data, operations))

doc = csv.reader(csv_file)

headers = doc.next()

for line in doc:
    record = {'Supplier': line[0], 'URL': line[1], 'Entity': line[2],'Expense Type': line[3],'Transaction Number': line[4],'Amount': line[5], 'Expense Area': line[6],'Date': line[7],'Departmental Family': line[8]}
    # Also need Expense Type here; see above.
    scraperwiki.sqlite.save(unique_keys=['URL','Transaction Number','Expense Type'],data=record, table_name="Refined")# Liberally copied/pasted from http://scraperwiki.com/scrapers/cabinet_office_spend_data/edit/

import scraperwiki
import lxml.html
import urllib
import csv
import dateutil.parser
import urllib2
import StringIO

def parsemonths(d):
    d = d.strip()
    print d
    return dateutil.parser.parse(d, yearfirst=True, dayfirst=True).date()

def links(url):
    lines = urllib.urlopen(url.replace(' ','%20')).readlines()
    lines = [ l.decode('ISO-8859-1').encode('utf-8') for l in lines ]
    header = []
    clist = list(csv.reader(lines))
    while clist[0][1] == "":
        clist.pop(0)
    header = clist.pop(0)
    header = header[:8]
    for i in range(8):
        header[i] = header[i].strip()

    # Rename/capitalize for consistency with Cabinet Office
    if header[0] == 'Department family':
        header[0] = 'Departmental Family'
    if header[3] == 'Expense type':
        header[3] = 'Expense Type'
    if header[4] == 'Expense area':
        header[4] = 'Expense Area'
    if header[6] == 'Transaction number':
        header[6] = 'Transaction Number'
    
    for row in clist:
        if row[2] != "":        
            data = dict(zip(header, row)) 
            data['URL'] = url
            data['Date'] = parsemonths(data['Date'])
    
        # Need 'Expense Type' in here because HMRC splits invoices up,
        # so has duplicate transaction numbers.
        scraperwiki.sqlite.save(unique_keys=['URL','Transaction Number','Expense Type'], data=data)

def refine(data, operations):
    return urllib2.urlopen('http://refine.scraperwiki.com:8080/transform',
    urllib.urlencode({'format': 'csv',
       'operations-string': operations,
       'data-string': data,
       'data-filetype': 'text/csv',
       'data-filename': 'hmrcspending.csv'})).read()


# Raw string to avoid backslash problems.
operations = r'''
[
  {
    "op": "core/text-transform",
    "description": "Text transform on cells in column Amount using expression grel:value.replace(/[^0-9.-E]/,'').toNumber()",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "Amount",
    "expression": "grel:value.replace(/[^0-9.-E]/,'').toNumber()",
    "onError": "store-error",
    "repeat": false,
    "repeatCount": 10
  },
  {
    "op": "core/mass-edit",
    "description": "Mass edit cells in column Supplier",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "Supplier",
    "expression": "value",
    "edits": [
      {
        "fromBlank": false,
        "fromError": false,
        "from": [
          "West Lothian Council",
          "WEST LOTHIAN COUNCIL"
        ],
        "to": "West Lothian Council"
      },
      {
        "fromBlank": false,
        "fromError": false,
        "from": [
          "Banner Business Services Ltd",
          "Banner Business Services Ltd "
        ],
        "to": "Banner Business Services Ltd"
      },
      {
        "fromBlank": false,
        "fromError": false,
        "from": [
          "Specialist Computer Ctr",
          "Specialist Computer Ctr "
        ],
        "to": "Specialist Computer Ctr"
      },
      {
        "fromBlank": false,
        "fromError": false,
        "from": [
          "J Winsley Ltd",
          "J. Winsley Ltd"
        ],
        "to": "J Winsley Ltd"
      },
      {
        "fromBlank": false,
        "fromError": false,
        "from": [
          "OPEX CORPORATION",
          "Opex Corporation"
        ],
        "to": "Opex Corporation"
      },
      {
        "fromBlank": false,
        "fromError": false,
        "from": [
          "Adare Halcyon Limited",
          "Adare Halcyon Limited "
        ],
        "to": "Adare Halcyon Limited"
      },
      {
        "fromBlank": false,
        "fromError": false,
        "from": [
          "Adare Halcyon Ltd",
          "Adare Halcyon Ltd "
        ],
        "to": "Adare Halcyon Limited"
      }
    ]
  },
  {
    "op": "core/mass-edit",
    "description": "Mass edit cells in column Supplier",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "Supplier",
    "expression": "value",
    "edits": [
      {
        "fromBlank": false,
        "fromError": false,
        "from": [
          "Department of the Environment",
          "Department of the Enviroment"
        ],
        "to": "Department of the Environment"
      }
    ]
  },
  {
    "op": "core/mass-edit",
    "description": "Mass edit cells in column Supplier",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "Supplier",
    "expression": "value",
    "edits": [
      {
        "fromBlank": false,
        "fromError": false,
        "from": [
          "Foreign and Commonwealth Office",
          "Foreign and Commonwealth"
        ],
        "to": "Foreign and Commonwealth Office"
      },
      {
        "fromBlank": false,
        "fromError": false,
        "from": [
          "Paragon UK (Print) Ltd",
          "Paragon UK (Print)"
        ],
        "to": "Paragon UK (Print) Ltd"
      }
    ]
  },
  {
    "op": "core/mass-edit",
    "description": "Mass edit cells in column Supplier",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "Supplier",
    "expression": "value",
    "edits": [
      {
        "fromBlank": false,
        "fromError": false,
        "from": [
          "RBSG Central 10000607",
          "RBSG Central"
        ],
        "to": "RBSG Central"
      },
      {
        "fromBlank": false,
        "fromError": false,
        "from": [
          "City Of Edinburgh Council",
          "City of Edinburgh Council - 3900401"
        ],
        "to": "City Of Edinburgh Council"
      }
    ]
  },
  {
    "op": "core/mass-edit",
    "description": "Mass edit cells in column Expense Area",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "Expense Area",
    "expression": "value",
    "edits": [
      {
        "fromBlank": false,
        "fromError": false,
        "from": [
          "Knowledge Analysis & Intelligence",
          "Knowledge, Analysis & Intelligence"
        ],
        "to": "Knowledge, Analysis & Intelligence"
      }
    ]
  },
  {
    "op": "core/mass-edit",
    "description": "Mass edit cells in column Expense Type",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "Expense Type",
    "expression": "value",
    "edits": [
      {
        "fromBlank": false,
        "fromError": false,
        "from": [
          "Data Output Production",
          "Data output production"
        ],
        "to": "Data Output Production"
      },
      {
        "fromBlank": false,
        "fromError": false,
        "from": [
          "Prof bodies subs",
          "Prof bodies Subs"
        ],
        "to": "Prof bodies subs"
      },
      {
        "fromBlank": false,
        "fromError": false,
        "from": [
          "Commission Fees",
          "Commission Fees "
        ],
        "to": "Commission Fees"
      },
      {
        "fromBlank": false,
        "fromError": false,
        "from": [
          "GSI Line Rental",
          "GSI Line Rental "
        ],
        "to": "GSI Line Rental"
      },
      {
        "fromBlank": false,
        "fromError": false,
        "from": [
          "STEPS Facility Payments (FUP) ",
          "STEPS Facility Payments (FUP)"
        ],
        "to": "STEPS Facility Payments (FUP)"
      },
      {
        "fromBlank": false,
        "fromError": false,
        "from": [
          "Court Fees",
          "Court Fees  "
        ],
        "to": "Court Fees"
      }
    ]
  },
  {
    "op": "core/mass-edit",
    "description": "Mass edit cells in column Expense Type",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "Expense Type",
    "expression": "value",
    "edits": [
      {
        "fromBlank": false,
        "fromError": false,
        "from": [
          "Travel agencies ",
          "Travel agencies"
        ],
        "to": "Travel agencies"
      }
    ]
  },
  {
    "op": "core/mass-edit",
    "description": "Mass edit cells in column Expense Type",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "Expense Type",
    "expression": "value",
    "edits": [
      {
        "fromBlank": false,
        "fromError": false,
        "from": [
          "Fixed Telephony Services to HMRC and VOA",
          "Fixed Telephony Service to HMRC and VOA"
        ],
        "to": "Fixed Telephony Services to HMRC and VOA"
      }
    ]
  },
  {
    "op": "core/mass-edit",
    "description": "Mass edit cells in column Expense Type",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "Expense Type",
    "expression": "value",
    "edits": [
      {
        "fromBlank": false,
        "fromError": false,
        "from": [
          "County Court Proceed",
          "County Court Proceedings"
        ],
        "to": "County Court Proceedings"
      },
      {
        "fromBlank": false,
        "fromError": false,
        "from": [
          "Subscriptions to Pub",
          "Subscriptions to Publications"
        ],
        "to": "Subscriptions to Publications"
      },
      {
        "fromBlank": false,
        "fromError": false,
        "from": [
          "Storage Seized Goods",
          "Storage of Seized Goods"
        ],
        "to": "Storage of Seized Goods"
      }
    ]
  },
  {
    "op": "core/mass-edit",
    "description": "Mass edit cells in column Departmental Family",
    "engineConfig": {
      "facets": [],
      "mode": "row-based"
    },
    "columnName": "Departmental Family",
    "expression": "value",
    "edits": [
      {
        "fromBlank": false,
        "fromError": false,
        "from": [
          "Department family"
        ],
        "to": "HMRC"
      }
    ]
  }
]
'''

data_url = "http://www.hmrc.gov.uk/transparency/spending-over-25k.htm"
root = lxml.html.parse(data_url).getroot()
anchors = root.cssselect("ul a")

for el in anchors:
    el.make_links_absolute(data_url)
    anyurl = el.attrib.get("href")
    
    if ".csv" in anyurl:
        links(anyurl)

data = urllib2.urlopen('http://scraperwiki.com/api/1.0/datastore/sqlite?format=csv&name=hmrc_spending&query=select+*+from+`swdata`').read()

csv_file = StringIO.StringIO(refine(data, operations))

doc = csv.reader(csv_file)

headers = doc.next()

for line in doc:
    record = {'Supplier': line[0], 'URL': line[1], 'Entity': line[2],'Expense Type': line[3],'Transaction Number': line[4],'Amount': line[5], 'Expense Area': line[6],'Date': line[7],'Departmental Family': line[8]}
    # Also need Expense Type here; see above.
    scraperwiki.sqlite.save(unique_keys=['URL','Transaction Number','Expense Type'],data=record, table_name="Refined")