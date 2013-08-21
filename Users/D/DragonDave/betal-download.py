import scraperwiki
import cStringIO
import codecs
import cgi, os, csv, sys, json
import collections
import copy

# currently this is implemented as a view for quick response to changes
# but it could be done as a scraper or an api download
# or even where the data is saved and then redirected to the api link for download from itself
# the select must list the columns explicitly to get the order as desired

# http://docs.python.org/library/csv.html#csv-examples
# Seriously, why is stuff in the standard library not unicode-aware?

class UnicodeCSVWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)
    
def getname(base, i):
    if type(i)==int:
        return "%s_%02d"%(base, i)
    else:
        return "%s_%s"%(base, i)

def getpaths(fragment,sofar=[]):
    """returns a list of lists; (1, a) means x[1]['a'] is a good target"""
    if type(fragment) not in [dict, list, collections.OrderedDict]:
        return
    try:
        keys=fragment.keys()
    except AttributeError: # not a dic
        keys=range(len(fragment))
    for key in keys:
        s=list(sofar)
        s.extend([key])
        if type(fragment[key]) in [dict, list, collections.OrderedDict]:
            for i in getpaths(fragment[key], s):
                yield i
        else:
            yield s

def pullout(item,commands):
    """recursively gets items in getpaths format"""
    if commands:
        try:
            chunk = item[commands[0]]
        except IndexError:
            return ''
        except KeyError:
            return ''
        newcomm = commands[1:]
        return pullout(chunk, newcomm) or ''
    else:
        return item or ''

def jsoncsv(filename,nicenames,colnames,encoding=None):
    #if pager:
    #    min=int(pager)*3000
    #    max=min+3000
    scraperwiki.utils.httpresponseheader("Content-Type", "text/csv")
    scraperwiki.utils.httpresponseheader("Content-Disposition", "attachment;filename=%s.csv" % filename)
    writer = UnicodeCSVWriter(sys.stdout)
    links=[x[0] for x in res['data']]
    if encoding:
        rawpages = (x[2].encode('latin-1').decode(encoding) for x in res['data']) 
    else:
        rawpages = (x[2] for x in res['data'])
    #if pager:
    #    pages=[json.loads(rawpage, object_pairs_hook=collections.OrderedDict)[0] for rawpage in rawpages][min:max]
    #else:
    pages=[json.loads(rawpage, object_pairs_hook=collections.OrderedDict)[0] for rawpage in rawpages]
        
    rawpages=None
    
    #for i in getpaths(pages[0]):
    #    print i, pullout(pages[0], i)

    # build list of potential columns
    biglist=[]
    for page in pages:
        for path in getpaths(page):
            if path not in biglist:
                biglist.append(path)

    # prune and sort
    newbiglist=[]
    for col in colnames:
        for i in biglist:
            if i[0]==col:
                newbiglist.append(i)

    # nice columnname 
    nicelist=copy.deepcopy(newbiglist)
    for item in nicelist:
        item[0]=nicenames[colnames.index(item[0])]
    names=[]
    for i in nicelist:
        names.append(u'_'.join([unicode(j) for j in i]))
    
    writer.writerow(names)
    
    # output rows
    for page in pages:
        rowdata=[pullout(page, i) for i in newbiglist]
        writer.writerow(rowdata)

    


def genericcsv(filename,nicenames,colnames):
    scraperwiki.utils.httpresponseheader("Content-Type", "text/csv")
    scraperwiki.utils.httpresponseheader("Content-Disposition", "attachment;filename=%s.csv" % filename)
    writer = UnicodeCSVWriter(sys.stdout)
    writer.writerow(nicenames)
    for link, ctype, jdata, err in res["data"]:
        ldata = json.loads(jdata)
        for data in ldata:
            for k in data:
                data[k] = data.get(k,'')
                if type(data[k]) != unicode: # TODO: if it's JSONy, process differently
                    print data[k]
                    data[k]=json.dumps(data[k])
            data["__link"]=link
            writer.writerow([data[i] for i in colnames])

try:
    qdict = dict(cgi.parse_qsl(os.getenv("QUERY_STRING")))
except:
    #print os.getenv("QUERY_STRING")
    qdict={'type':'dclg_data'}
    
scraperwiki.sqlite.attach("betal-populate")
#scraperwiki.sqlite.attach("betal-override")
scraperwiki.sqlite.attach("betal-parser")
#qselect = "SELECT raw.link, coalesce(override.type, raw.type) as ctype, output.data, output.err"
#qfrom = " FROM raw LEFT JOIN output on output.link=raw.link LEFT JOIN override on override.link=raw.link"
qselect = "SELECT raw.link, raw.type as ctype, output.data, output.err"
qfrom = " FROM raw LEFT JOIN output on output.link=raw.link"
qwhere = " WHERE output.data is not null" 
stype = qdict.get("type")
#pager = qdict.get("page")
if stype:
    qwhere += " AND ctype='"+stype+"'"
if qdict.get("limit"):
    qlimit = " LIMIT %s" % qdict.get("limit")
else:
    qlimit = ""
if qdict.get("offset"):
    qlimit += " OFFSET %s" % qdict.get("offset")
res = scraperwiki.sqlite.execute(qselect+qfrom+qwhere+qlimit)

if stype == "dclg_news":
    jsoncsv("dclg_news",
                ['link', 'title', 'body', 'meta', 'attachment', 'images', 'published'],
                ['link', 'title', 'markdown', 'metadata', 'attachments', 'images', 't_Published'])
    exit()

if stype == "dclg_speech":
    jsoncsv("dclg_speech",
                ['link', 'title', 'body', 'type', 'meta', 'attachment','orator','orator_title', 'orator_desc', 'orator_profile', 'location', 'date_of_statement', 'published', 'date_of_speech'],
                ['link', 'title', 'markdown', 't_Type', 'metadata', 'attachments','author_name','author_title','author_desc','author_profile','t_Location', 't_Date_of_statement', 't_Published', 't_Date_of_speech'])
    exit()

if stype == "dclg_news2":
    jsoncsv("dclg_news2",
                ['link', 'title', 'body', 'meta', 'attachment', 'images', 'published'],
                ['link', 'title', 'markdown', 'metadata', 'attachments', 'images', 't_Published'])
    exit()

if stype == "dclg_news3":
    jsoncsv("dclg_news3",
                ['link', 'title', 'body', 'meta', 'attachment', 'images', 'published'],
                ['link', 'title', 'markdown', 'metadata', 'attachments', 'images', 't_Published'])
    exit()

if stype == "dclg_speech2":
    jsoncsv("dclg_speech2",
                ['link', 'title', 'body', 'type', 'meta', 'attachment','orator','orator_title', 'orator_desc', 'orator_profile', 'location', 'date_of_statement', 'published', 'date_of_speech'],
                ['link', 'title', 'markdown', 't_Type', 'metadata', 'attachments','author_name','author_title','author_desc','author_profile','t_Location', 't_Date_of_statement', 't_Published', 't_Date_of_speech'])
    exit()


if stype == "fco_news":
    jsoncsv("fco_news",
                ['link', 'title', 'body', 'first published', 'last updated', 'summary', 'image'],
                ['link', 'title', 'markdown', 'date', 'updated', 'summary', 'images'])
    exit()

if stype == "fco_speech":
    jsoncsv("fco_speech",
                ['link', 'title', 'body', 'first published', 'summary', 'image', 'speaker', 'location', 'event'],
                ['link', 'title', 'markdown', 'date', 'summary', 'images', 'table!Speaker', 'table!Location', 'table!Event'])
    exit()
if stype == "2_fco_news":
    jsoncsv("2_fco_news",
                ['link', 'title', 'body', 'first published', 'last updated', 'summary', 'image'],
                ['link', 'title', 'markdown', 'date', 'updated', 'summary', 'images'])
    exit()

if stype == "2_fco_speech":
    jsoncsv("2_fco_speech",
                ['link', 'title', 'body', 'first published', 'summary', 'image', 'speaker', 'location', 'event'],
                ['link', 'title', 'markdown', 'date', 'summary', 'images', 'table!Speaker', 'table!Location', 'table!Event'])
    exit()

if stype == "dclg_consult":
    jsoncsv("dclg_consult",
                ['link', 'title', 'body', 'attachment', 'opening date', 'closing date','ISBN','person','addr','email'],
                ['link', 'title', 'markdown', 'attachments', 'Published','Closing date','ISBN','person','addr','email'])
    exit()

if stype == "dclg_data":
    jsoncsv("dclg_data",
                ['link', 'title', 'body', 'attachment', 'opening date', 'closing date','ISBN','person','addr','email'],
                ['link', 'title', 'markdown', 'attachments', 'Published','Closing date','ISBN','person','addr','email'])
    exit()


if stype == "dclg_pubs":
    jsoncsv("dclg_pubs",
                ['link', 'title', 'body', 'price', 'published date', 'type', 'ISBN', 'attachment'],
                ['link', 'title', 'markdown', 'Price', 'Published', 'Type(s)', 'ISBN', 'attachments'])
    exit()


if stype == "modconsult":
    jsoncsv("mod_consult",
                ['link', 'title', 'body','attachment','opening date', 'closing date', 'ref no', 'associated organisations', 'person', 'address', 'email', 'fax'],
                ['link', 'title', 'markdown','attachments','open_date','close_date','ref','assoc_org','person','address','email','fax'])
    exit()

if stype == "modnews":
    jsoncsv("mod_news",
                ['link', 'title', 'summary', 'body', 'image', 'associated organisations', 'first published'],
                ['link', 'title', 'summary', 'markdown', 'images', 'assoc_org', 'pub_date'])
    exit()

if stype == "modspeech":
    jsoncsv("mod_speeches",
                ['link', 'title', 'summary', 'body', 'person', 'date', 'location', 'first published'],
                ['link', 'title', 'summary', 'markdown', 'person', 'date', 'location', 'published'])
    exit()

if stype == "modpubs":
    jsoncsv("mod_pubs",
                ['link', 'title', 'body', 'type', 'isbn', 'attachment'],
                ['link', 'title', 'markdown', 'crumbs', '', 'links'],
            encoding = "UTF-8")
    exit()

if stype == "2_mod_news":
    jsoncsv("2_mod_news",
                ['link', 'title', 'summary', 'body', 'image', 'associated organisations', 'first published'],
                ['link', 'title', 'summary', 'markdown', 'images', 'assoc_org', 'pub_date'])
    exit()

if stype == "2_mod_speech":
    jsoncsv("2_mod_speech",
                ['link', 'title', 'summary', 'body', 'person', 'date', 'location', 'first published'],
                ['link', 'title', 'summary', 'markdown', 'person', 'date', 'location', 'published'])
    exit()

if stype == "2_mod_pubs":
    jsoncsv("2_mod_pubs",
                ['link', 'title', 'body', 'type', 'isbn', 'attachment'],
                ['link', 'title', 'markdown', 'crumbs', '', 'links'],
            encoding = "UTF-8")
    exit()


if stype == "consult":
    jsoncsv("bis_consult",
                ['link', 'title', 'summary','body','attachment','opening date', 'closing date', 'response date','person','organization','address','response form','response online','response email','response other'],
                ['link', 'title', 'abstract', 'markdown','attachments', 'opendate', 'closedate', 'responsedate', 'person', 'assoc_org','addr', 'resp_form','resp_online','resp_email','resp_other'])
    exit()

if stype == "news":
    jsoncsv("bis_news",
                ['link', 'title', 'summary','body','image_url','image_alt','first published'],
                ['link', 'title', 'abstract', 'markdown', 'image_url', 'image_alt', 'date'])
    exit()

if stype == "2_bis_con":
    jsoncsv("2_bis_con",
                ['link', 'title', 'summary','body','attachment','opening date', 'closing date', 'response date','person','organization','address','response form','response online','response email','response other'],
                ['link', 'title', 'abstract', 'markdown','attachments', 'opendate', 'closedate', 'responsedate', 'person', 'assoc_org','addr', 'resp_form','resp_online','resp_email','resp_other'])
    exit()

if stype == "2_bis_news":
    jsoncsv("2_bis_news",
                ['link', 'title', 'summary','body','image_url','image_alt','first published'],
                ['link', 'title', 'abstract', 'markdown', 'image_url', 'image_alt', 'date'])
    exit()


if stype == "pubs":
    jsoncsv("bis_pubs",
                ['link', 'title', 'body'],
                ['link', 'title', 'markdown'])
    exit()

if stype == "tradeanalysis":
    jsoncsv('bis_tradeanalysis',
               ['link','title','markdown','externals','help'],
               ['link','title','markdown','externals','help'])
    exit()

if stype == "farmexcise":
    jsoncsv('bis_farmexcise',
               ['link','title','markdown','externals','help'],
               ['link','title','markdown','externals','help'])
    exit()

if stype == "man_and_mar":
    jsoncsv('man_and_mar',
               ['link','title','markdown','externals','help'],
               ['link','title','markdown','externals','help'])
    exit()
if stype == "transadv":
    jsoncsv('transadv',
               ['link','title','markdown','externals','help'],
               ['link','title','markdown','externals','help'])
    exit()
if stype == "specialist":
    jsoncsv('specialist',
               ['link','title','markdown','externals','help'],
               ['link','title','markdown','externals','help'])
    exit()


if stype == "speeches":
    scraperwiki.utils.httpresponseheader("Content-Type", "text/csv")
    scraperwiki.utils.httpresponseheader("Content-Disposition", "attachment;filename=%s.csv" % "bis_speeches")
    writer = csv.writer(sys.stdout)
    writer.writerow(["date", "orator", "location", "title", "checked", "markdown", "link"])
    for link, ctype, jdata, err in res["data"]:
        ldata = json.loads(jdata)
        for data in ldata:
            for k in data:
                data[k] = unicode(data[k]).encode("utf8")
            writer.writerow([data["date"], data["orator"], data["location"], data["title"], data["checked"], data["markdown"], link])
    exit()


if stype == "2_bis_speech":
    scraperwiki.utils.httpresponseheader("Content-Type", "text/csv")
    scraperwiki.utils.httpresponseheader("Content-Disposition", "attachment;filename=%s.csv" % "2_bis_speech")
    writer = csv.writer(sys.stdout)
    writer.writerow(["date", "orator", "location", "title", "checked", "markdown", "link"])
    for link, ctype, jdata, err in res["data"]:
        ldata = json.loads(jdata)
        for data in ldata:
            for k in data:
                data[k] = unicode(data[k]).encode("utf8")
            writer.writerow([data["date"], data["orator"], data["location"], data["title"], data["checked"], data["markdown"], link])
    exit()


if stype == "pub_server":
    scraperwiki.utils.httpresponseheader("Content-Type", "text/csv")
    scraperwiki.utils.httpresponseheader("Content-Disposition", "attachment;filename=%s.csv" % "bis_pub_server")
    writer = csv.writer(sys.stdout)
    writer.writerow(["Title", "Summary", "Body", "Date", "URN", "ISBN", "Order URL", "Attachment", "Filename", "Price", "Language", "Pages", "Type", "Original URL", "Category", "Sub-Category"])
    for link, ctype, jdata, err in res["data"]:
        ldata = json.loads(jdata)
        for data in ldata:
            row = [ data["title"].encode("utf8"), data["summary"].encode("utf8"), "", 
                    data["date"], data["urn"], "", data["orderurl"], data["attachment"], data["title"].encode("utf8"), 
                    data.get("price", ""), data.get("language", ""), data.get("pages", ""), data.get("type", "").encode("utf8"),
                    data.get("originurl",""), data.get("cat", ""), data.get("subcat","")]
            writer.writerow(row)
    exit()

print "Don't know type", stype
