import urllib
import csv
import md5
import scraperwiki


url = "http://www.cabinetoffice.gov.uk/sites/default/files/resources/co-meetings-aug-sept-2010.csv"
# I have started just looking at data from one source.
# I am assuming, (dangerously), that the column headings are:
#   a) the same, and 
#   b( in the same order
# for different departments

data = csv.DictReader(urllib.urlopen(url))

# Fudge to cope with possibility of blank row between header and first data row
started=False

# Inspection of the data file suggests that when we start considering a Minister's appointments,
#   we leave the Minister cell blank to mean "same as above".
# If we want to put the Minister's name into each row, we need to watch for that. 
minister=''

for d in data:
    if not started and d['Minister']=='':
        # Skip blank lines between header and data rows
        continue
    elif d['Minister']!='':
        # A new Minister is identified, so this becomes the current Minister of interest
        if not started:
            started=True
        minister=d['Minister']
    elif d['Date']=='' and d['Purpose of meeting']=='' and d['Name of External Organisation']=='':
        # Inspection of the original data file suggests that there may be notes at the end of the CSV file...
        # One convention appears to be that notes are separated from data rows by at least one blank row
        # If we detect a blank row within the dataset, then we assume we're at data's end
        # Of course, if there are legitimate blank rows within the later, we won't scrape any of the following data
        # We probably shouldn't discount the notes, but how would we handle them?!
        break
    print minister,d['Date'],d['Purpose of meeting'],d['Name of External Organisation']
    id='::'.join([minister,d['Date'],d['Purpose of meeting'],d['Name of External Organisation']])
    # The md5 function creates a unique ID for the meeting
    id=md5.new(id).hexdigest()
    # Some of the original files contain some Latin-1 characters (such as right single quote, rather than apostrophe)
    #   that make things fall over unless we handle them...
    purpose=d['Purpose of meeting'].decode('latin1').encode('utf-8')
    record={'id':id,'Minister':minister,'date':d['Date'],'purpose':purpose,'lobbiest':d['Name of External Organisation'].decode('latin1').encode('utf-8')}
    # Note that in some cases there may be multiple lobbiests, separated by a comma, in the same record.
    # It might make sense to generate a meeting MD5 id using the original record data, but actually store
    #   a separate record for each lobbiest in the meeting (i.e. have lobbiests and lobbiest columns) by separating on ','
    # That said, there are also records where a comma separates part of the title or affiliation of an individual lobbiest.
    # A robust convention for separating different lobbiests in the same meeting (e.g. ';' rather than ',') would help

    scraperwiki.datastore.save(["id"], record) 

for d in data:
    #use up the generator, close the file, allow garbage collection?
    continue
