"""Tables of election campaign spending and links to scans of invoices submitted 
by the parties.  

Should run daily and give alerts when data changes due to a new set of invoices
coming on-line."""

import scraperwiki
from scraperwiki import datastore
import re

def ExtractInvoices(data, col1, col2):
    mreturn = re.search('(?i)<a href="(.*?)">Return(?: |&nbsp;)\(PDF\)</a>', col1)
    assert mreturn, col1
    data["Return PDF"] = mreturn.group(1)
    if not re.search("Not submitted|No invoice", col2):
        minvoices = re.search('(?i)<a href="(.*?)">Invoices \(PDF\)</a>', col2)
        assert minvoices, col2
        data["Invoices PDF"] = minvoices.group(1)
    

# parses table1 and table3
def ParseTable1(tbody):
    outputlist = [ ]
    rows = re.findall("(?is)<tr.*?>(.*?)</tr>", tbody)

    secondrow = [ re.sub("<.*?>|\s|&nbsp;", "", v)  for v in re.findall("(?is)<td.*?>(.*?)</td>", rows[1]) ]
    #print secondrow # == ['England', 'Scotland', 'Wales', ('NorthernIreland',) 'Total']

    for row in rows[2:]:
        cols = re.findall("(?is)<td.*?>(.*?)</td>", row)
        partyname = re.sub("</?(?:STRONG|P|B)>", "", cols[0]).strip()
        data = { "Party":partyname }
        
        # parties which have not declared their spending
        if re.search("Return due|Return not submitted", cols[1]):
            pass

        # parties which list their spending by country
        else:
            itotal = len(secondrow)
            amounts = dict(zip(secondrow, [ int("0" + re.sub(",|&nbsp;", "", v))  for v in cols[1:itotal+1]]))
            sumtotal = sum([amounts[country]  for country in secondrow[:-1] ])
            assert abs(sumtotal - amounts["Total"]) <= 1, (sumtotal, amounts, cols)

            for country in secondrow[:-1]:
                data[country + " Spend"] = amounts[country]

            assert len(cols) == itotal+3, cols
            ExtractInvoices(data, cols[itotal+1], cols[itotal+2])
        outputlist.append(data)
    return outputlist


def ParseTable2(tbody):
    outputlist = [ ]
    rows = re.findall("(?is)<tr.*?>(.*?)</tr>", tbody)

    secondrow = [ re.sub("<.*?>|\s|&nbsp;", "", v)  for v in re.findall("(?is)<td.*?>(.*?)</td>", rows[1]) ]
    #print secondrow

    for row in rows[2:]:
        cols = re.findall("(?is)<td.*?>(.*?)</td>", row)
        partyname = re.sub("<.*?>", "", cols[0]).strip()
        candidatename = re.sub("<.*?>", "", cols[1]).strip()
        data = { "Party":partyname, "Candidate":candidatename }
        if candidatename != "Jim Nicholson":
            partyspend, candidatespend, totalspend = [ int(re.sub(",|<.*?>", "", v))  for v in cols[2:5] ]
            ExtractInvoices(data, cols[5], cols[6])
            assert totalspend == partyspend + candidatespend, cols
            data["Party Spend"] = partyspend
            data["Candidate Spend"] = candidatespend
        else:
            pass # two returns in this column.  skip for now
            
        outputlist.append(data)
    return outputlist


# get the main page with the 3 tables           
campaignurl = "http://www.electoralcommission.org.uk/party-finance/party-finance-analysis/campaign-expenditure-2009"
a = scraperwiki.scrape(campaignurl)

# there are 3 tables of different things
tbodies = re.findall("(?is)<tbody>(.*?)</tbody>", a)
assert len(tbodies) == 3

outputlist1 = ParseTable1(tbodies[0])
outputlist2 = ParseTable2(tbodies[1])
outputlist3 = ParseTable1(tbodies[2])

# load up the data
outputlist = outputlist1[:]
outputlist.extend(outputlist2)
outputlist.extend(outputlist3)
for partydata in outputlist:
    datastore.save(unique_keys=['Party'], data=partydata)

"""Tables of election campaign spending and links to scans of invoices submitted 
by the parties.  

Should run daily and give alerts when data changes due to a new set of invoices
coming on-line."""

import scraperwiki
from scraperwiki import datastore
import re

def ExtractInvoices(data, col1, col2):
    mreturn = re.search('(?i)<a href="(.*?)">Return(?: |&nbsp;)\(PDF\)</a>', col1)
    assert mreturn, col1
    data["Return PDF"] = mreturn.group(1)
    if not re.search("Not submitted|No invoice", col2):
        minvoices = re.search('(?i)<a href="(.*?)">Invoices \(PDF\)</a>', col2)
        assert minvoices, col2
        data["Invoices PDF"] = minvoices.group(1)
    

# parses table1 and table3
def ParseTable1(tbody):
    outputlist = [ ]
    rows = re.findall("(?is)<tr.*?>(.*?)</tr>", tbody)

    secondrow = [ re.sub("<.*?>|\s|&nbsp;", "", v)  for v in re.findall("(?is)<td.*?>(.*?)</td>", rows[1]) ]
    #print secondrow # == ['England', 'Scotland', 'Wales', ('NorthernIreland',) 'Total']

    for row in rows[2:]:
        cols = re.findall("(?is)<td.*?>(.*?)</td>", row)
        partyname = re.sub("</?(?:STRONG|P|B)>", "", cols[0]).strip()
        data = { "Party":partyname }
        
        # parties which have not declared their spending
        if re.search("Return due|Return not submitted", cols[1]):
            pass

        # parties which list their spending by country
        else:
            itotal = len(secondrow)
            amounts = dict(zip(secondrow, [ int("0" + re.sub(",|&nbsp;", "", v))  for v in cols[1:itotal+1]]))
            sumtotal = sum([amounts[country]  for country in secondrow[:-1] ])
            assert abs(sumtotal - amounts["Total"]) <= 1, (sumtotal, amounts, cols)

            for country in secondrow[:-1]:
                data[country + " Spend"] = amounts[country]

            assert len(cols) == itotal+3, cols
            ExtractInvoices(data, cols[itotal+1], cols[itotal+2])
        outputlist.append(data)
    return outputlist


def ParseTable2(tbody):
    outputlist = [ ]
    rows = re.findall("(?is)<tr.*?>(.*?)</tr>", tbody)

    secondrow = [ re.sub("<.*?>|\s|&nbsp;", "", v)  for v in re.findall("(?is)<td.*?>(.*?)</td>", rows[1]) ]
    #print secondrow

    for row in rows[2:]:
        cols = re.findall("(?is)<td.*?>(.*?)</td>", row)
        partyname = re.sub("<.*?>", "", cols[0]).strip()
        candidatename = re.sub("<.*?>", "", cols[1]).strip()
        data = { "Party":partyname, "Candidate":candidatename }
        if candidatename != "Jim Nicholson":
            partyspend, candidatespend, totalspend = [ int(re.sub(",|<.*?>", "", v))  for v in cols[2:5] ]
            ExtractInvoices(data, cols[5], cols[6])
            assert totalspend == partyspend + candidatespend, cols
            data["Party Spend"] = partyspend
            data["Candidate Spend"] = candidatespend
        else:
            pass # two returns in this column.  skip for now
            
        outputlist.append(data)
    return outputlist


# get the main page with the 3 tables           
campaignurl = "http://www.electoralcommission.org.uk/party-finance/party-finance-analysis/campaign-expenditure-2009"
a = scraperwiki.scrape(campaignurl)

# there are 3 tables of different things
tbodies = re.findall("(?is)<tbody>(.*?)</tbody>", a)
assert len(tbodies) == 3

outputlist1 = ParseTable1(tbodies[0])
outputlist2 = ParseTable2(tbodies[1])
outputlist3 = ParseTable1(tbodies[2])

# load up the data
outputlist = outputlist1[:]
outputlist.extend(outputlist2)
outputlist.extend(outputlist3)
for partydata in outputlist:
    datastore.save(unique_keys=['Party'], data=partydata)

