#!/usr/bin/python

import scraperwiki
import os
import re
import urllib2
from pyPdf import PdfFileWriter, PdfFileReader

bus_file = 'http://www.cota.com/Schedules.aspx'

def find_routes():
    # Get a list of all the current bus route pdf files
    regex1 = re.compile('title="Current Route" href="assets/Riding-Cota/Schedules/Current/(\w.+)">')
    routes = regex1.findall(urllib2.urlopen(bus_file).read())
    return routes

def create_url_list(routes):
    # Convert the bus route pdf list into the actual URLs at cota.com for the route pdf files
    url_list = []
    for route in sorted(routes):
        # Need to fix this so it adds 0 before any routes that don't start with a 0 and somehow changes it back again below
        if route == "83.pdf":
             route = "083.pdf"
        if route == "39.pdf":
             route = "039.pdf"
        if route == "21.pdf":
             route = "021.pdf"
        if route == "16S.pdf":
             route = "016S.pdf"
        if route == "15.pdf":
             route = "015.pdf"
        url_list.append(['http://www.cota.com/assets/Riding-Cota/Schedules/Current/%s' % route, route])
    return sorted(url_list)

def merge_pdf(url_list):
    # Download each PDF and merge them into one giant PDF, post this giant PDF to anonfiles.com, add URL to scraperwiki database
    output = PdfFileWriter()
    for url in url_list:

        if url[0] == "http://www.cota.com/assets/Riding-Cota/Schedules/Current/083.pdf":
             url[0] = "http://www.cota.com/assets/Riding-Cota/Schedules/Current/83.pdf"
             url[1] = "83.pdf"
        if url[0] == "http://www.cota.com/assets/Riding-Cota/Schedules/Current/039.pdf":
             url[0] = "http://www.cota.com/assets/Riding-Cota/Schedules/Current/39.pdf"
             url[1] = "39.pdf"
        if url[0] == "http://www.cota.com/assets/Riding-Cota/Schedules/Current/021.pdf":
             url[0] = "http://www.cota.com/assets/Riding-Cota/Schedules/Current/21.pdf"
             url[1] = "21.pdf"
        if url[0] == "http://www.cota.com/assets/Riding-Cota/Schedules/Current/016S.pdf":
             url[0] = "http://www.cota.com/assets/Riding-Cota/Schedules/Current/16S.pdf"
             url[1] = "16S.pdf"
        if url[0] == "http://www.cota.com/assets/Riding-Cota/Schedules/Current/015.pdf":
             url[0] = "http://www.cota.com/assets/Riding-Cota/Schedules/Current/15.pdf"
             url[1] = "15.pdf"

        pdf_file = os.system("wget %s" % url[0])
        input1 = PdfFileReader(file('/tmp/%s' % url[1], "rb"))
        numPages  = input1.getNumPages()
        print "number of pages = %s" % (numPages)
        page1 = input1.getPage(0)
        page2 = input1.getPage(1)
        output.addPage(page1)
        output.addPage(page2)

        if numPages == 3:
            page3 = input1.getPage(2)
            output.addPage(page3)

    final_page_count = output.getNumPages()
    print "Number of Pages in Final = %s" % (final_page_count)

    outputStream = file("/tmp/bus.pdf", "wb")
    output.write(outputStream)
    outputStream.close()

    reply = os.system('curl -kF "file=@bus.pdf;filename=bus.pdf" https://anonfiles.com/api/hotlink -o "reply.txt"')

    with open('reply.txt', 'r') as f:
        read_data = f.read()

    data_dict = {
                   'Title':'Link to COTA Bus Schedule',
                   'URL':read_data,
                }
    scraperwiki.sqlite.save(unique_keys=['Title', 'URL'], data=data_dict)

# Run it!
merge_pdf(create_url_list(find_routes()))

#!/usr/bin/python

import scraperwiki
import os
import re
import urllib2
from pyPdf import PdfFileWriter, PdfFileReader

bus_file = 'http://www.cota.com/Schedules.aspx'

def find_routes():
    # Get a list of all the current bus route pdf files
    regex1 = re.compile('title="Current Route" href="assets/Riding-Cota/Schedules/Current/(\w.+)">')
    routes = regex1.findall(urllib2.urlopen(bus_file).read())
    return routes

def create_url_list(routes):
    # Convert the bus route pdf list into the actual URLs at cota.com for the route pdf files
    url_list = []
    for route in sorted(routes):
        # Need to fix this so it adds 0 before any routes that don't start with a 0 and somehow changes it back again below
        if route == "83.pdf":
             route = "083.pdf"
        if route == "16S.pdf":
             route = "016S.pdf"
        url_list.append(['http://www.cota.com/assets/Riding-Cota/Schedules/Current/%s' % route, route])
    return sorted(url_list)

def merge_pdf(url_list):
    # Download each PDF and merge them into one giant PDF, post this giant PDF to anonfiles.com, add URL to scraperwiki database
    output = PdfFileWriter()
    for url in url_list:

        if url[0] == "http://www.cota.com/assets/Riding-Cota/Schedules/Current/083.pdf":
             url[0] = "http://www.cota.com/assets/Riding-Cota/Schedules/Current/83.pdf"
             url[1] = "83.pdf"
        if url[0] == "http://www.cota.com/assets/Riding-Cota/Schedules/Current/016S.pdf":
             url[0] = "http://www.cota.com/assets/Riding-Cota/Schedules/Current/16S.pdf"
             url[1] = "16S.pdf"

        pdf_file = os.system("wget %s" % url[0])
        input1 = PdfFileReader(file('/tmp/%s' % url[1], "rb"))
        numPages  = input1.getNumPages()
        print "number of pages = %s" % (numPages)
        page1 = input1.getPage(0)
        page2 = input1.getPage(1)
        output.addPage(page1)
        output.addPage(page2)

        if numPages == 3:
            page3 = input1.getPage(2)
            output.addPage(page3)

    final_page_count = output.getNumPages()
    print "Number of Pages in Final = %s" % (final_page_count)

    outputStream = file("/tmp/bus.pdf", "wb")
    output.write(outputStream)
    outputStream.close()

    reply = os.system('curl -kF "file=@bus.pdf;filename=bus.pdf" https://anonfiles.com/api/hotlink -o "reply.txt"')

    with open('reply.txt', 'r') as f:
        read_data = f.read()

    data_dict = {
                   'Title':'Link to COTA Bus Schedule',
                   'URL':read_data,
                }
    scraperwiki.sqlite.save(unique_keys=['Title', 'URL'], data=data_dict)

# Run it!
merge_pdf(create_url_list(find_routes()))

