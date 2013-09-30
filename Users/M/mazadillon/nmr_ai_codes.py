import scraperwiki
import os
import re

def scrape_codes(url):
    pdf = scraperwiki.scrape(url) # Fetch the pdf file from the given URL
    f = open('doc.pdf', 'w') # Save it locally
    f.write(pdf)
    f.close()
    
    text = os.system('pdf2txt.py -n doc.pdf > doc.txt') # Run pdf2txt.py on the local PDF
    f = open('doc.txt', 'r') # Read in the resulting txt file
    reg = re.split(' ([A-Z ]{2}[0-9]{2,4}) ',f.read()) # Split the file by AI code
    match = re.compile('^[A-Z ]{2}[0-9]{4}$')
    
    data = [dict(info='')]
    i = 0
    for line in reg: # Loop through the lines
        if match.match(line): # Merge all lines that don't start with an AI code
            i += 1
            data.append(dict(info=''))
            data[i]['code'] = line
        else:
            #print data[i]
            data[i]['info'] = data[i]['info'] + line
    
    for bull in data:
        if 'code' in bull:
            info = bull['info'].split('\x0c',1) # Get rid of junk off the end of lines
            info = info[0].split('New AI Codes issued',1)
            info = re.split('\s+',info[0]) # Split into individual words
            count = len(info) - 1
            bull['country'] = ''
            while bull['country'] == '': # Work out which order fields are in (format changed on older files)
                if re.match('^[A-Z]{3}$',info[count]): # Is country code the last field?
                    if re.match('^[0-9]{1,2}$',info[count-2]): # Is breed code the field 2 before that?
                        bull['country'] = info[count]
                        bull['hbn'] = info[count-1]
                        bull['breed'] = info[count-2]
                        bull['shortname'] = info[count-3]
                        count = count - 3
                    elif re.match('^[0-9]{1,2}$',info[count-1]): # Or is breed code immediatley before?
                        bull['country'] = info[count]
                        try:
                            bull['hbn'] = info[count+1]
                        except IndexError:
                            bull['hbn'] = ''
                        bull['breed'] = info[count-1]
                        bull['shortname'] = info[count-2]
                        count = count - 2
                count = count - 1
                if count < 0:
                    break
            bull['name'] = ''
            while count >= 0: # Loop through words at begining to make variable length bull name
                bull['name'] = info[count] + ' ' + bull['name']
                count = count - 1
            del bull['info']
            scraperwiki.sqlite.save(['code'], bull) # Save to database

data = scraperwiki.scrape('http://www.nmr.co.uk/ai-codes') # Scrape list of PDFs
docs = re.findall('(/images/[\sA-Z0-9a-z_/-]*name\.pdf)',data) # Find file names

for doc in docs: # Loop through PDF file names
    done = scraperwiki.sqlite.select('* from docs WHERE path = "'+doc+'"') # Has it been scanned already?
    if len(done) == 0:
        scrape_codes('http://www.nmr.co.uk'+doc) # Scan the PDF
        scraperwiki.sqlite.save(['path'], {'path':doc},'docs') # Save the path as having been scanned
    else:
        print 'Skipping previously scanned file: '+doc
import scraperwiki
import os
import re

def scrape_codes(url):
    pdf = scraperwiki.scrape(url) # Fetch the pdf file from the given URL
    f = open('doc.pdf', 'w') # Save it locally
    f.write(pdf)
    f.close()
    
    text = os.system('pdf2txt.py -n doc.pdf > doc.txt') # Run pdf2txt.py on the local PDF
    f = open('doc.txt', 'r') # Read in the resulting txt file
    reg = re.split(' ([A-Z ]{2}[0-9]{2,4}) ',f.read()) # Split the file by AI code
    match = re.compile('^[A-Z ]{2}[0-9]{4}$')
    
    data = [dict(info='')]
    i = 0
    for line in reg: # Loop through the lines
        if match.match(line): # Merge all lines that don't start with an AI code
            i += 1
            data.append(dict(info=''))
            data[i]['code'] = line
        else:
            #print data[i]
            data[i]['info'] = data[i]['info'] + line
    
    for bull in data:
        if 'code' in bull:
            info = bull['info'].split('\x0c',1) # Get rid of junk off the end of lines
            info = info[0].split('New AI Codes issued',1)
            info = re.split('\s+',info[0]) # Split into individual words
            count = len(info) - 1
            bull['country'] = ''
            while bull['country'] == '': # Work out which order fields are in (format changed on older files)
                if re.match('^[A-Z]{3}$',info[count]): # Is country code the last field?
                    if re.match('^[0-9]{1,2}$',info[count-2]): # Is breed code the field 2 before that?
                        bull['country'] = info[count]
                        bull['hbn'] = info[count-1]
                        bull['breed'] = info[count-2]
                        bull['shortname'] = info[count-3]
                        count = count - 3
                    elif re.match('^[0-9]{1,2}$',info[count-1]): # Or is breed code immediatley before?
                        bull['country'] = info[count]
                        try:
                            bull['hbn'] = info[count+1]
                        except IndexError:
                            bull['hbn'] = ''
                        bull['breed'] = info[count-1]
                        bull['shortname'] = info[count-2]
                        count = count - 2
                count = count - 1
                if count < 0:
                    break
            bull['name'] = ''
            while count >= 0: # Loop through words at begining to make variable length bull name
                bull['name'] = info[count] + ' ' + bull['name']
                count = count - 1
            del bull['info']
            scraperwiki.sqlite.save(['code'], bull) # Save to database

data = scraperwiki.scrape('http://www.nmr.co.uk/ai-codes') # Scrape list of PDFs
docs = re.findall('(/images/[\sA-Z0-9a-z_/-]*name\.pdf)',data) # Find file names

for doc in docs: # Loop through PDF file names
    done = scraperwiki.sqlite.select('* from docs WHERE path = "'+doc+'"') # Has it been scanned already?
    if len(done) == 0:
        scrape_codes('http://www.nmr.co.uk'+doc) # Scan the PDF
        scraperwiki.sqlite.save(['path'], {'path':doc},'docs') # Save the path as having been scanned
    else:
        print 'Skipping previously scanned file: '+doc
