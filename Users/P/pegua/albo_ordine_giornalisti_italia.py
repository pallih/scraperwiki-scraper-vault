import scraperwiki
import urllib2
import lxml.etree
import dateutil.parser

           
def getlist_from_pdf_and_save( url, tablename ):
    pdfdata = urllib2.urlopen(url).read()
    #print "The pdf file has %d bytes" % len(pdfdata)

    xmldata = scraperwiki.pdftoxml(pdfdata)
    #print "After converting to xml it has %d bytes" % len(xmldata)
    #print "The first 100000 characters are: ", xmldata[:100000]

    root = lxml.etree.fromstring(xmldata)
    pages = list(root)

    #print "The pages are numbered:", [ page.attrib.get("number")  for page in pages ]

    consecutive_equal_top_text_tag = 0;
    last_top_attribute = "-1000";


    data = {}
    for page in pages:
        for el in page:
            if( el.tag == "text" ):
                if( consecutive_equal_top_text_tag == 0 ):
                    last_top_attribute = el.get("top");
                    if( el[0].text != "NOMINATIVO" and el[0].text != "DATA DI NASCITA" and el[0].text != "ORDINE" and el[0].text != "DATA DI ISCRIZIONE" and el[0].text != "DATA DI NASCITA" ):
                        #print "Getting new name"
                        data["nominativo"] = el[0].text
                        consecutive_equal_top_text_tag = 1;
                    continue
                if( consecutive_equal_top_text_tag == 1 ):
                    if( last_top_attribute == el.get("top") ):
                        data["data_di_nascita"] = dateutil.parser.parse(el[0].text, dayfirst=True).date()
                        consecutive_equal_top_text_tag = 2;
                    else:
                        consecutive_equal_top_text_tag = 0;
                    continue;
                if( consecutive_equal_top_text_tag == 2 ):
                    if( last_top_attribute == el.get("top") ):
                        data["ordine"] = el[0].text
                        consecutive_equal_top_text_tag = 3;
                    else:
                        consecutive_equal_top_text_tag = 0;
                    continue;
                if( consecutive_equal_top_text_tag == 3 ):
                    if( last_top_attribute == el.get("top") ):
                        data["data_di_iscrizione"] = dateutil.parser.parse(el[0].text, dayfirst=True).date()
                        #print data
                        scraperwiki.sqlite.save(unique_keys=['nominativo','data_di_nascita','data_di_iscrizione'], data=data,table_name=tablename)
                        #save data!!!
                         
                    consecutive_equal_top_text_tag = 0;
                    continue;
 




#url_professionisti = "http://www.odg.it/files/Professionisti_02.pdf"
url_pubblicisti1 = "http://www.odg.it/files/Pubblicisti_a_l_01.pdf"
url_pubblicisti2 = "http://www.odg.it/files/pubblicisti_m_z_02.pdf"

#getlist_from_pdf_and_save(url_professionisti,"professionisti")
getlist_from_pdf_and_save(url_pubblicisti1,"pubblicisti")
getlist_from_pdf_and_save(url_pubblicisti2,"pubblicisti")

import scraperwiki
import urllib2
import lxml.etree
import dateutil.parser

           
def getlist_from_pdf_and_save( url, tablename ):
    pdfdata = urllib2.urlopen(url).read()
    #print "The pdf file has %d bytes" % len(pdfdata)

    xmldata = scraperwiki.pdftoxml(pdfdata)
    #print "After converting to xml it has %d bytes" % len(xmldata)
    #print "The first 100000 characters are: ", xmldata[:100000]

    root = lxml.etree.fromstring(xmldata)
    pages = list(root)

    #print "The pages are numbered:", [ page.attrib.get("number")  for page in pages ]

    consecutive_equal_top_text_tag = 0;
    last_top_attribute = "-1000";


    data = {}
    for page in pages:
        for el in page:
            if( el.tag == "text" ):
                if( consecutive_equal_top_text_tag == 0 ):
                    last_top_attribute = el.get("top");
                    if( el[0].text != "NOMINATIVO" and el[0].text != "DATA DI NASCITA" and el[0].text != "ORDINE" and el[0].text != "DATA DI ISCRIZIONE" and el[0].text != "DATA DI NASCITA" ):
                        #print "Getting new name"
                        data["nominativo"] = el[0].text
                        consecutive_equal_top_text_tag = 1;
                    continue
                if( consecutive_equal_top_text_tag == 1 ):
                    if( last_top_attribute == el.get("top") ):
                        data["data_di_nascita"] = dateutil.parser.parse(el[0].text, dayfirst=True).date()
                        consecutive_equal_top_text_tag = 2;
                    else:
                        consecutive_equal_top_text_tag = 0;
                    continue;
                if( consecutive_equal_top_text_tag == 2 ):
                    if( last_top_attribute == el.get("top") ):
                        data["ordine"] = el[0].text
                        consecutive_equal_top_text_tag = 3;
                    else:
                        consecutive_equal_top_text_tag = 0;
                    continue;
                if( consecutive_equal_top_text_tag == 3 ):
                    if( last_top_attribute == el.get("top") ):
                        data["data_di_iscrizione"] = dateutil.parser.parse(el[0].text, dayfirst=True).date()
                        #print data
                        scraperwiki.sqlite.save(unique_keys=['nominativo','data_di_nascita','data_di_iscrizione'], data=data,table_name=tablename)
                        #save data!!!
                         
                    consecutive_equal_top_text_tag = 0;
                    continue;
 




#url_professionisti = "http://www.odg.it/files/Professionisti_02.pdf"
url_pubblicisti1 = "http://www.odg.it/files/Pubblicisti_a_l_01.pdf"
url_pubblicisti2 = "http://www.odg.it/files/pubblicisti_m_z_02.pdf"

#getlist_from_pdf_and_save(url_professionisti,"professionisti")
getlist_from_pdf_and_save(url_pubblicisti1,"pubblicisti")
getlist_from_pdf_and_save(url_pubblicisti2,"pubblicisti")

