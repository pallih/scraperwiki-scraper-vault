import scraperwiki
import urllib
import csv
import lxml.html
import urllib2
import json
import csv
import StringIO
import datetime
import dateutil.parser           

def parsemonths(d):
    d = d.strip()
    print d
    return dateutil.parser.parse(d, yearfirst=True, dayfirst=True).date()

def links(url): 
    #print url
    lines = urllib.urlopen(url.replace(' ','%20')).readlines()
    lines = [ l.decode('ISO-8859-1').encode('utf-8') for l in lines ]
    header = []
    clist = list(csv.reader(lines))
    while clist[0][1] == "":
        clist.pop(0)
    header = clist.pop(0)
    header = header[:9]
    for i in range(9):
        header[i] = header[i].strip()
    if header[8] == 'Descriptions':
        header[8] = 'Description'
    if header[7] == 'Amount £':
        header[7] = 'Amount'
    
    #print header
    
    
    for row in clist:
        if row[2] != "":        
            data = dict(zip(header, row)) 
            data['URL'] = url
            data['Date'] = parsemonths(data['Date'])
            #print data
    
        # Need expense type here because invoices are split into
        # separate categories, so transaction numbers are duplicated.
        scraperwiki.sqlite.save(unique_keys=['URL','Transaction Number','Expense Type'], data=data)

#This piece of code gets the csv files from the web page and puts it into the function
root = lxml.html.parse("http://www.cabinetoffice.gov.uk/resource-library/cabinet-office-spend-data").getroot()
anchors = root.cssselect("div.downloadfile a")

for el in anchors:
    anyurl = el.attrib.get("href")

    #print anyurl
    
    if ".csv" in anyurl:
        links(anyurl)

#This is all got from Google Refine#

def refine(data, operations):
    return urllib2.urlopen('http://refine.scraperwiki.com:8080/transform',
        urllib.urlencode(
            {'format': 'csv',
             'operations-string': operations,
             'data-string': data,
             'data-filetype': 'text/csv',
             'data-filename': 'cabinetspend.csv'
            }
        )).read()

operations ='''[
  {
    "op": "core/column-removal",
    "description": "Remove column date_scraped",
    "columnName": "date_scraped"
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
          "BT GLOBAL SERVICES"
        ],
        "to": "BT"
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
          "BT GLOBAL SERVICES."
        ],
        "to": "BT"
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
          "Central Office of In"
        ],
        "to": "CENTRAL OFFICE OF INFORMATION"
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
          "Central Office of Information"
        ],
        "to": "CENTRAL OFFICE OF INFORMATION"
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
          "CHARITIES EVALUATION SERVICES"
        ],
        "to": "Charities Evaluation Services"
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
          "CIVIL SERVICE BENEVOLENT FUND "
        ],
        "to": "CIVIL SERVICE BENEVOLENT FUND"
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
          "FUJITSU SERVICES LTD"
        ],
        "to": "FUJITSU SERVICES"
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
          "HM REVENUE AND CUSTOMS"
        ],
        "to": "HM REVENUE & CUSTOMS"
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
          "KING STURGE LLP "
        ],
        "to": "KING STURGE LLP"
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
          "MITIE BUSINESS SERVICES LTD"
        ],
        "to": "MITIE BUSINESS SERVICES"
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
          "National Association for Voluntary & Community Action"
        ],
        "to": "National Association for Voluntary and Community Action"
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
          "NATIONAL AUDIT OFFIC"
        ],
        "to": "National Audit Office"
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
          "NATIONAL WESTMINSTER BANK PLC (4715059005000009)"
        ],
        "to": "NATIONAL WESTMINSTER BANK PLC"
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
          "PRICEWATERHOUSE COOPERS"
        ],
        "to": "PRICEWATERHOUSE COOPERS LLP"
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
          "ROYAL LIVER ASSURANC"
        ],
        "to": "ROYAL LIVER ASSURANCE"
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
          "THE TREASURY SOLICITORS"
        ],
        "to": "THE TREASURY SOLICITOR"
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
          "TREASURER TO THE QUEEN "
        ],
        "to": "TREASURER TO THE QUEEN"
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
          "TREASURY SOLICITOR"
        ],
        "to": "THE TREASURY SOLICITOR"
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
          "Treasury Solicitors"
        ],
        "to": "THE TREASURY SOLICITOR"
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
          "VOLUNTEERING ENGLAND"
        ],
        "to": "Volunteering England"
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
          "WOMENS RESOURCE CENTRE"
        ],
        "to": "Women's Resource Centre"
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
          "BBC"
        ],
        "to": "BBC MONITORING"
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
          "BRITISH TELECOMMUNICATIONS PLC"
        ],
        "to": "BT"
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
          "BYTES TECHNOLOGY GRO"
        ],
        "to": "BYTES TECHNOLOGY GROUP"
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
          "BYTES SOFTWARE SERVICES"
        ],
        "to": "BYTES TECHNOLOGY GROUP"
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
          "CAPITA BUSINESS SERVICES LTD"
        ],
        "to": "CAPITA"
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
          "CAPITA RESOURCING LIMITED"
        ],
        "to": "CAPITA"
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
          "CAPITA SYMONDS (FORMERLY INVENTURES LTD)"
        ],
        "to": "CAPITA"
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
          "COI CENTRAL OFFICE OF INFORMATION"
        ],
        "to": "CENTRAL OFFICE OF INFORMATION"
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
          "CONSORTIUM OF LGB & T VCOS"
        ],
        "to": "CONSORTIUM LESBIAN, GAY, BISEXUAL & TRANSGENDERED VOLUNTARY AND COMMUNITY ORGANISATIONS"
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
          "CORPORATE DOCUMENT SERVICES LTD"
        ],
        "to": "CORPORATE DOCUMENT SERVICES LIMITED"
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
          "DEPARTMENT FOR BUSINESS INNOVATION AND SKILLS"
        ],
        "to": "DEPARTMENT FOR BUSINESS INNOVATION & SKILLS"
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
          "Department for Communities & Local Government"
        ],
        "to": "Department for Communities and Local Government"
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
          "DEPARTMENT FOR COMMUNITIES & LOCAL GOVERNMENT"
        ],
        "to": "Department for Communities and Local Government"
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
          "DEPARTMENT OF COMMUNITIES & LOCAL GOVERNMENT"
        ],
        "to": "Department for Communities and Local Government"
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
          "DLA PIPER UK LLP"
        ],
        "to": "DLA PIPER UK"
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
          "DLA PIPER"
        ],
        "to": "DLA PIPER UK"
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
          "ECONOMIC & SOCIAL RESEARCH COUNCIL"
        ],
        "to": "ECONOMIC AND SOCIAL RESEARCH COUNCIL"
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
          "ECOVERT FM"
        ],
        "to": "ECOVERT FM LTD"
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
          "FIELD FISHER WATERHO"
        ],
        "to": "FIELD FISHER WATERHOUSE"
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
          "H M REVENUE & CUSTOMS"
        ],
        "to": "HM REVENUE & CUSTOMS"
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
          "IBM UNITED KINGDOM L"
        ],
        "to": "IBM"
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
          "KING SURGE LLP"
        ],
        "to": "KING STURGE LLP"
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
          "LEXIS NEXIS BUTTERWORTHS"
        ],
        "to": "LEXISNEXIS"
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
          "LIVERPOOL CITY COUNC"
        ],
        "to": "LIVERPOOL CITY COUNCIL"
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
          "MITIE BUSINESS SERVICES"
        ],
        "to": "MITIE"
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
          "MITIE DOCUMENT SOLUTIONS"
        ],
        "to": "MITIE"
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
          "Parity Resources Ltd"
        ],
        "to": "Parity"
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
          "PARITY SOLUTIONS LTD"
        ],
        "to": "PARITY"
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
          "SECURITY SERVICES GROUP"
        ],
        "to": "SAFE SSG"
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
          "SERCO CONSULTING"
        ],
        "to": "SERCO LTD"
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
          "Spikes Cavill & Co"
        ],
        "to": "SPIKES CAVELL ANALYTIC LIMITED"
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
          "The Media Trust"
        ],
        "to": "Media Trust"
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
          "Media Trust"
        ],
        "to": "MEDIA TRUST"
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
          "NCVO"
        ],
        "to": "The National Council for Voluntary Organisations"
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
          "THE TREASURY SOLICITOR"
        ],
        "to": "TREASURY SOLICITORS DEPARTMENT"
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
          "TREASURY SOLICITORS DEPARTMENT "
        ],
        "to": "TREASURY SOLICITORS DEPARTMENT"
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
          "TREASURY SOLICITORS DEPT"
        ],
        "to": "TREASURY SOLICITORS DEPARTMENT"
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
          "TREASURY SOLICITORS DEPT 3861"
        ],
        "to": "TREASURY SOLICITORS DEPARTMENT"
      }
    ]
  }
]
'''
data = urllib2.urlopen('http://scraperwiki.com/api/1.0/datastore/sqlite?format=csv&name=cabinet_office_spend_data&query=select+*+from+`swdata`').read()

csv_file = StringIO.StringIO(refine(data, operations))

doc = csv.reader(csv_file)

headers = doc.next()

for line in doc:
    record = {'Description': line[0], 'Supplier': line[1], 'URL': line[2], 'Entity': line[3],'Expense Type': line[4],'Transaction Number': line[5],'Amount': float(line[6].replace(',', '')), 'Expense Area': line[7],'Date': line[8],'Departmental Family': line[9]}
    # Also need Expense Type here; see above.
    scraperwiki.sqlite.save(unique_keys=['URL','Transaction Number','Expense Type'],data=record, table_name="Refined")