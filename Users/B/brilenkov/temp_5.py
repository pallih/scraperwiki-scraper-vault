import scraperwiki
import datetime
#print datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d")
import re
from BeautifulSoup import BeautifulSoup
email_pattern = re.compile(r'''(?:[A-Za-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[A-Za-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?\.)+[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[A-Za-z0-9-]*[A-Za-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])''',re.IGNORECASE)
#print ','.join(set(email_pattern.findall(str('jhabwfljav@egkjbwek.oiu'))))

body = '<span class="companylink big">A. L. Bazzini Company, Inc.</span><br /> 200 Food Center Drive<br /> Bronx,&nbsp; NY&nbsp;10474<br />  US<br /> <label>Phone: </label>718-842-8644<br /> <label>Fax: </label>718-842-8582<br /> <label>Contact: </label>Joann Marino<br />'

body = '''
    <div class="maincontainer">
        <div class="page_margins">                                    
            <div id="main">
                
                
                
                <div id="col1">
                    <div id="col1_content" class="clearfix">
                        
    <h1 class="pagetitle">Buyer's Guide - Company Information</h1>
    
    <span class="companylink big">A. L. Bazzini Company, Inc.</span><br />
    
    200 Food Center Drive<br />
        Bronx,&nbsp;
        NY&nbsp;
        10474<br />
        US<br />
    

    <label>Phone: </label>718-842-8644<br />
    
    <label>Fax: </label>718-842-8582<br />

    <label>Contact: </label>Joann Marino<br />
    
    <div class="detailseparator">Products</div>
    <div class="companycategory">
        <ul>
            
    <li><span class="toplevelcategory">Grocery Stock Items</span></li>
    
        <ul class="toplevel">
            
    <li><span >Dietetic, Health, Natural, and Organic Foods</span></li>
    
    <li><span >Dry Grocery</span></li>
    
        <ul >
            
    <li><span >Nuts and Dried Fruits</span></li>
    
    <li><span >Snack Foods, Dips, and Salsa</span></li>
    
        </ul>
    
    <li><span >Ethnic Foods</span></li>
    
        <ul >
            
    <li><span >Kosher</span></li>
    
        </ul>
    
    <li><span >Frozen Foods</span></li>
    
        <ul >
            
    <li><span >Fruits and Vegetables, Frozen</span></li>
    
        </ul>
    
    <li><span >General Merchandise, Non-Edible Grocery</span></li>
    
        <ul >
            
    <li><span >Gift Packs</span></li>
    
        </ul>
    
    <li><span >Produce and Floral</span></li>
    
        <ul >
            
    <li><span >Fresh Fruits and Vegetables</span></li>
    
        </ul>
    
        </ul>
    
        </ul>
    </div>

'''
soup = BeautifulSoup(body)
csp = soup.find('span',{'class':'companylink big'}).nextSibling.nextSibling.nextSibling.nextSibling.replace('&nbsp;','').split(',')
print csp[0]
#print csp[1]
print csp[1].strip().split(' ')[0].strip()
print csp[1].strip().split(' ')[-1].strip()

print soup.find('span',{'class':'companylink big'}).nextSibling.nextSibling.nextSibling.nextSibling.replace('&nbsp;','')#.nextSibling.nextSibling
print soup.find('div',{'id':'col1_content'}).find('label').text
print soup.find('div',{'id':'col1_content'}).find('label').nextSibling
labels = soup.find('div',{'id':'col1_content'}).findAll('label')
for label in labels:
    if 'Phone:' in label.text:
        print label.nextSibling
    elif 'Fax:' in label.text:
        print label.nextSibling
    elif 'Contact:' in label.text:
        print label.nextSibling

