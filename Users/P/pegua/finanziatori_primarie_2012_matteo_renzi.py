import scraperwiki
import lxml.html

#function to import a single donation
def import_donation(donation_string,dict_list):
    if( donation_string == "" ):
        return
    don_dict = {}
    #should be better to user regex, quick hack instead
    try:
        donor = donation_string.split('-')[0].strip()
        money = donation_string.split('-')[1].strip()
        money_text = money.replace("&#8364;","").strip()
        money_int = int(money_text.split(',')[0])
    except ValueError:
        print "Value error, check if known exception"
        if( donation_string  == 'ROSAMARIA FOGLIA -CORSANI - 10,00&#8364;' ):
            donor = 'ROSAMARIA FOGLIA -CORSANI'
            money_text = "10,00"
            money_int = 10
        elif( donation_string == 'FIORINA MAGRI-PICCIONI - 50,00&#8364;' ):
            donor = 'FIORINA MAGRI-PICCIONI'
            money_text = "50,00"
            money_int = 50
        elif( donation_string == 'ANNA-MARIE HILLING - 10,00&#8364;' ):
            donor = 'ANNA-MARIE HILLING'
            money_text = "10,00"
            money_int = 10
        else:
            print "Exception " + donation_string + " not known" 
  
    don_dict["donor"] = donor;
    don_dict["amount_text"] = money_text;
    don_dict["amount_int"] = money_int;
    don_dict["donation_text"] = donation_string;
    #scraperwiki.sqlite.save([],don_dict,table_name="donations")
    dict_list.append(don_dict);

# Blank Python
URL = "http://www.matteorenzi.it/trasparenza-sui-finanziatori"

#Drop data already here
scraperwiki.sqlite.execute("drop table if exists donations")


#creating table schema
try:     
    scraperwiki.sqlite.execute("""         
        create table donations
        (        
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            donor TEXT,
            amount_int  INTEGER,
            amount_text TEXT,
            donation_text TEXT
        )     
        """) 
except:   
    print "Table probably already exists."

dict_list = [];

#Download html
html = scraperwiki.scrape(URL)

root = lxml.html.fromstring(html)

item_page = root.cssselect("div.item-page")[0]

p_donors =  item_page.cssselect("p")[1];

p_donors_childs = p_donors.getchildren()

print p_donors.text[:-1];

import_donation(p_donors.text[:-1].upper(),dict_list)

for br_donor in p_donors_childs:
    import_donation(lxml.html.tostring(br_donor).replace("<br>","").upper(),dict_list)

print dict_list
scraperwiki.sqlite.save([],dict_list,table_name="donations")

#tapullo

import scraperwiki
import lxml.html

#function to import a single donation
def import_donation(donation_string,dict_list):
    if( donation_string == "" ):
        return
    don_dict = {}
    #should be better to user regex, quick hack instead
    try:
        donor = donation_string.split('-')[0].strip()
        money = donation_string.split('-')[1].strip()
        money_text = money.replace("&#8364;","").strip()
        money_int = int(money_text.split(',')[0])
    except ValueError:
        print "Value error, check if known exception"
        if( donation_string  == 'ROSAMARIA FOGLIA -CORSANI - 10,00&#8364;' ):
            donor = 'ROSAMARIA FOGLIA -CORSANI'
            money_text = "10,00"
            money_int = 10
        elif( donation_string == 'FIORINA MAGRI-PICCIONI - 50,00&#8364;' ):
            donor = 'FIORINA MAGRI-PICCIONI'
            money_text = "50,00"
            money_int = 50
        elif( donation_string == 'ANNA-MARIE HILLING - 10,00&#8364;' ):
            donor = 'ANNA-MARIE HILLING'
            money_text = "10,00"
            money_int = 10
        else:
            print "Exception " + donation_string + " not known" 
  
    don_dict["donor"] = donor;
    don_dict["amount_text"] = money_text;
    don_dict["amount_int"] = money_int;
    don_dict["donation_text"] = donation_string;
    #scraperwiki.sqlite.save([],don_dict,table_name="donations")
    dict_list.append(don_dict);

# Blank Python
URL = "http://www.matteorenzi.it/trasparenza-sui-finanziatori"

#Drop data already here
scraperwiki.sqlite.execute("drop table if exists donations")


#creating table schema
try:     
    scraperwiki.sqlite.execute("""         
        create table donations
        (        
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            donor TEXT,
            amount_int  INTEGER,
            amount_text TEXT,
            donation_text TEXT
        )     
        """) 
except:   
    print "Table probably already exists."

dict_list = [];

#Download html
html = scraperwiki.scrape(URL)

root = lxml.html.fromstring(html)

item_page = root.cssselect("div.item-page")[0]

p_donors =  item_page.cssselect("p")[1];

p_donors_childs = p_donors.getchildren()

print p_donors.text[:-1];

import_donation(p_donors.text[:-1].upper(),dict_list)

for br_donor in p_donors_childs:
    import_donation(lxml.html.tostring(br_donor).replace("<br>","").upper(),dict_list)

print dict_list
scraperwiki.sqlite.save([],dict_list,table_name="donations")

#tapullo

