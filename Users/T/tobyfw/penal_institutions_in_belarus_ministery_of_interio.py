import lxml.html          
import scraperwiki 

html = scraperwiki.scrape("http://mvd.gov.by/main.aspx?guid=3501").decode("utf-8")
root = lxml.html.fromstring(html)

div = root.cssselect("div.content")[0]  

# prisons and colonies 
for strong in div.cssselect("strong"):     
     if len(strong.text.strip()) > 0: 
            institution = strong.text
            address = ""
            telephone = ""
    
            divAddress = strong.getparent().getnext()
            if divAddress == None:
                divAddress = strong.getparent().getparent().getnext()

            if divAddress <> None:
                address = divAddress.text_content()

                divTelephone1 = divAddress.getnext()
                if divTelephone1 <> None:
                    telephone = divTelephone1.text_content()

                    divTelephone2 = divTelephone1.getnext()
                    if divTelephone2 <> None:
                        telephone = telephone + "\n" + divTelephone2.text_content()

            if address == "":
                continue

            data = {
                'Institution' : institution,
                'Address' : address,
                'Telephone' : telephone
            }
            scraperwiki.sqlite.save(unique_keys=['Institution'], data=data)



