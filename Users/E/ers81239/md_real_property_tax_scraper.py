import scraperwiki
import lxml.html
import urllib



def detect_table_type(table):
    #returns a string of table type
    #print table
    
    
    #weed out tables that contain other tables:
    if table.cssselect("table table"): 
        print "parent"
        return "parent"
    
    for td in table.cssselect('td.detailbold'):
        text  = td.text_content().strip()
        if text == "Account Identifier:":
            return "Account Info"
        elif text == "Owner Name:":
            return "Owner Info"
        elif text == "Premises Address":
            return "Premises Info"
        elif text == "Map":
            return "Map Info"
        elif text == "Special Tax Areas":
            return "Special Tax Info"
        elif text == "Primary Structure Built":
            return "Structure Info 1"
        elif text == "Stories":
            return "Structure Info 2"
        elif text == "Base Value":
            return "Value Info"
        elif text == "Seller:":
            return "Transfer Info"
        elif text == "Partial Exempt Assessments":
            return "Exemption Info 1"
        elif text == "Tax Exempt:":
            return "Exemption Info 2"
                

    return "unknown"



def get_data_from_simple_table(table):
    #this function returns a list of key/value pairs from the table when the table is like this:
    #<td style=detailbold>key</td><td style=detail>value</td>
    data = table.cssselect('td.detailbold, td.detail')
    #we should have gotten an even number of td's back
    assert len(data) % 2 == 0
    retval = []
    for x in range(len(data)/2):
        retval.append((data[x*2].text_content().strip(":"), data[x*2+1].text_content()))
    return retval


def get_data_from_table(table):
    #returns a list of key/value pairs from the table
    #Produces a list of tuples
    table_type = detect_table_type(table)
    #print "Table: " + table_type
    if table_type == "Account Info":
        data = table.cssselect('td.detailbold')
        return [(data[0].text_content(), data[1].text_content())]

    elif table_type == "Owner Info":
        return get_data_from_simple_table(table)

    
    elif table_type == "Premises Info":
        #It isn't clear if 6 or 7 will ever have data, but keeping them just in case.
        data = table.cssselect('td.detailbold, td.detail')
        premises_address = (data[2].text_content(), data[4].text_content(), data[6].text_content())
        legal_description = (data[3].text_content(), data[5].text_content(), data[7].text_content())
        return [ ("Premises Address",premises_address), ("Legal Descriotion", legal_description) ]
        

    elif table_type == "Map Info":
        #0-8 are field names that match 11-19
        #9 and 10  go together as do 20 and 21.
        
 
        data = table.cssselect('td.detailbold, td.detail')

        retval = []
        for k in range(9):
            retval.append( (data[k].text_content(), data[k+11].text_content()) )
        retval.append( (data[9].text_content().strip(":"), data[10].text_content()) )
        retval.append( (data[20].text_content().strip(":"), data[21].text_content()) )


        return retval 



        

    elif table_type == "Special Tax Info":
        #This would have been a simple table except it has an excess td at the front.
        data = table.cssselect('td.detailbold, td.detail')
        retval = []
        retval.append( (data[1].text_content().strip(":"), data[2].text_content()) )
        retval.append( (data[3].text_content().strip(":"), data[4].text_content()) )
        retval.append( (data[5].text_content().strip(":"), data[6].text_content()) )
        return retval



    elif table_type == "Structure Info 1":
        data = table.cssselect('td.detailbold, td.detail')
        retval = []
        retval.append( (data[0].text_content().strip(":"), data[4].text_content()) )
        retval.append( (data[1].text_content().strip(":"), data[5].text_content()) )
        retval.append( (data[2].text_content().strip(":"), data[6].text_content()) )
        retval.append( (data[3].text_content().strip(":"), data[7].text_content()) )
        return retval
        


    elif table_type == "Structure Info 2":
        #interestingly, this is identical to Structure Info 1
        data = table.cssselect('td.detailbold, td.detail')
        retval = []
        retval.append( (data[0].text_content().strip(":"), data[4].text_content()) )
        retval.append( (data[1].text_content().strip(":"), data[5].text_content()) )
        retval.append( (data[2].text_content().strip(":"), data[6].text_content()) )
        retval.append( (data[3].text_content().strip(":"), data[7].text_content()) )
        return retval    

    elif table_type == "Value Info":
        #This one is unique. 
        # [(Base Value, [(Land, xxxx), (Improvements, xxxx), (Total, xxxx), (Preferential Land, xxx)]),
        #  (Value As Of X/Y/X, [(Land, xxxx), (Improvements, xxxx), (Total, xxxx), (Preferential Land, xxx)]),
        #  (Phase-in Assessment  As Of X/Y/Z, [(Land, xxxx), (Improvements, xxxx), (Total, xxxx), (Preferential Land, xxx)]),
        #  (Phase-in Assessment  As Of X/Y/Z, [(Land, xxxx), (Improvements, xxxx), (Total, xxxx), (Preferential Land, xxx)])
        #  

        #Initially, I'm going to assume that every property gets the same number of columns here.
        retval = []
        data = [td.text_content() for td in table.cssselect('td.detailbold, td.detail')]
        retval.append(  ("Base Value", [ ("Land", data[7]), ("Improvements", data[10]), ("Total", data[13]), ("Preferential Land", data[18]) ]) )
        offset = 1
        retval.append(  ("Value " + data[3], [ ("Land", data[7 + offset]), ("Improvements", data[10 + offset]), ("Total", data[13 + offset]), ("Preferential Land", data[18 + offset]) ] ) )
        offset = 2
        retval.append( ("Phase-in Assessment " + data[4], [ ("Land", None), ("Improvements", None), ("Total", data[13 + offset]), ("Preferential Land", data[18 + offset]) ] ) )
        offset = 3
        retval.append( ("Phase-in Assessment " + data[4], [ ("Land", None), ("Improvements", None), ("Total", data[13 + offset]), ("Preferential Land", data[18 + offset]) ] ) )

        return retval


    elif table_type == "Transfer Info":
        #The unique thing here is that there will be multiples of these for each sale
        #That should be handled by the caller.  In the meantime, its a simple table.
        return get_data_from_simple_table(table)




    elif table_type == "Exemption Info 1xxxx":
        #5 is a class, 6 goes to first date, 7 to second date
        #TODO: (Skipping for now, because I don't care that much about this data (lazy)

        #for (k, td) in enumerate(table.cssselect('td.detailbold, td.detail')):
        #    print str(k) + ": " + td.text_content()    
        pass


    else:
        return [("error", "Table type " + table_type + " wasn't handled.")]


# TODO:  Finish off the Exemption Info Section (See other TODO below)
# TODO:  Make it so it actaully stores the data


# http://sdatcert3.resiusa.org/rp_rewrite/results.aspx?County=19&SearchType=STREET&StreetNumber=&StreetName=charles

# Get 1 property
#html = scraperwiki.scrape("http://sdatcert3.resiusa.org/rp_rewrite/details.aspx?AccountNumber=03%20030512%20%20%20%20%20%20%20%20&County=19&SearchType=STREET")
#get it a different way

    
#Main

#this is the range of maps to search:
account_numbers = range(30512,30513)
account_numbers = range(30510,30550)

for account_number in account_numbers:

        #fortmat account_number for inclusion in the url  
        acct_string = str(account_number).rjust(6,"0")
        #TODO: below I'm assuming that the district is also the first two numbers of the account number.
        district_string = acct_string[0:2]

        url = "http://sdatcert3.resiusa.org/rp_rewrite/details.aspx?County=19&SearchType=ACCT&District={district}&AccountNumber={account}".format(district=district_string, account=acct_string) 
        print url

        html = scraperwiki.scrape(url)
        root = lxml.html.fromstring(html)
            
            

        data = {}


        for table in root.cssselect('table table'):
            for item in  get_data_from_table(table):
                data[item[0]] = item[1]      
        print data
        
        
        
