#This scraper does entity extraction on groups identified by https://scraperwiki.com/scrapers/all_party_groups_2/

import scraperwiki
import simplejson
import urllib,re
from time import sleep

import os, cgi
try:
    qsenv = dict(cgi.parse_qsl(os.getenv("QUERY_STRING")))
    calaisKey=qsenv["CALAISKEY"]
except:
    print "Couldn't get Calais Key"
    exit(-1)

scraperwiki.sqlite.attach("all_party_groups_2")

#---- helper library
#---http://code.google.com/p/python-calais/
"""
python-calais v.1.4 -- Python interface to the OpenCalais API
Author: Jordan Dimov (jdimov@mlke.net)
Last-Update: 01/12/2009
"""

import httplib, urllib, re
import simplejson as json
from StringIO import StringIO

PARAMS_XML = """
<c:params xmlns:c="http://s.opencalais.com/1/pred/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"> <c:processingDirectives %s> </c:processingDirectives> <c:userDirectives %s> </c:userDirectives> <c:externalMetadata %s> </c:externalMetadata> </c:params>
"""

STRIP_RE = re.compile('<script.*?</script>|<noscript.*?</noscript>|<style.*?</style>', re.IGNORECASE)

__version__ = "1.4"

class AppURLopener(urllib.FancyURLopener):
    version = "Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.0.5) Gecko/2008121623 Ubuntu/8.10 (intrepid)Firefox/3.0.5" # Lie shamelessly to Wikipedia.
urllib._urlopener = AppURLopener()

class Calais():
    """
    Python class that knows how to talk to the OpenCalais API.  Use the analyze() and analyze_url() methods, which return CalaisResponse objects.  
    """
    api_key = None
    processing_directives = {"contentType":"TEXT/RAW", "outputFormat":"application/json", "reltagBaseURL":None, "calculateRelevanceScore":"true", "enableMetadataType":None, "discardMetadata":None, "omitOutputtingOriginalText":"true"}
    user_directives = {"allowDistribution":"false", "allowSearch":"false", "externalID":None}
    external_metadata = {}

    def __init__(self, api_key, submitter="python-calais client v.%s" % __version__):
        self.api_key = api_key
        self.user_directives["submitter"]=submitter

    def _get_params_XML(self):
        return PARAMS_XML % (" ".join('c:%s="%s"' % (k,v) for (k,v) in self.processing_directives.items() if v), " ".join('c:%s="%s"' % (k,v) for (k,v) in self.user_directives.items() if v), " ".join('c:%s="%s"' % (k,v) for (k,v) in self.external_metadata.items() if v))

    def rest_POST(self, content):
        params = urllib.urlencode({'licenseID':self.api_key, 'content':content, 'paramsXML':self._get_params_XML()})
        headers = {"Content-type":"application/x-www-form-urlencoded"}
        conn = httplib.HTTPConnection("api.opencalais.com:80")
        conn.request("POST", "/enlighten/rest/", params, headers)
        response = conn.getresponse()
        data = response.read()
        conn.close()
        return (data)

    def get_random_id(self):
        """
        Creates a random 10-character ID for your submission.  
        """
        import string
        from random import choice
        chars = string.letters + string.digits
        np = ""
        for i in range(10):
            np = np + choice(chars)
        return np

    def get_content_id(self, text):
        """
        Creates a SHA1 hash of the text of your submission.  
        """
        import hashlib
        h = hashlib.sha1()
        h.update(text)
        return h.hexdigest()

    def preprocess_html(self, html):
        html = html.replace('\n', '')
        html = STRIP_RE.sub('', html)
        return html

    def analyze(self, content, content_type="TEXT/RAW", external_id=None):
        if not (content and  len(content.strip())):
            return None
        self.processing_directives["contentType"]=content_type
        if external_id:
            self.user_directives["externalID"] = external_id
        return CalaisResponse(self.rest_POST(content))

    def analyze_url(self, url):
        f = urllib.urlopen(url)
        html = self.preprocess_html(f.read())
        return self.analyze(html, content_type="TEXT/HTML", external_id=url)

    def analyze_file(self, fn):
        import mimetypes
        try:
            filetype = mimetypes.guess_type(fn)[0]
        except:
            raise ValueError("Can not determine file type for '%s'" % fn)
        if filetype == "text/plain":
            content_type="TEXT/RAW"
            f = open(fn)
            content = f.read()
            f.close()
        elif filetype == "text/html":
            content_type = "TEXT/HTML"
            f = open(fn)
            content = self.preprocess_html(f.read())
            f.close()
        else:
            raise ValueError("Only plaintext and HTML files are currently supported.  ")
        return self.analyze(content, content_type=content_type, external_id=fn)

class CalaisResponse():
    """
    Encapsulates a parsed Calais response and provides easy pythonic access to the data.
    """
    raw_response = None
    simplified_response = None
    
    def __init__(self, raw_result):
        try:
            self.raw_response = json.load(StringIO(raw_result))
        except:
            raise ValueError(raw_result)
        self.simplified_response = self._simplify_json(self.raw_response)
        self.__dict__['doc'] = self.raw_response['doc']
        for k,v in self.simplified_response.items():
            self.__dict__[k] = v

    def _simplify_json(self, json):
        result = {}
        # First, resolve references
        for element in json.values():
            for k,v in element.items():
                if isinstance(v, unicode) and v.startswith("http://") and json.has_key(v):
                    element[k] = json[v]
        for k, v in json.items():
            if v.has_key("_typeGroup"):
                group = v["_typeGroup"]
                if not result.has_key(group):
                    result[group]=[]
                del v["_typeGroup"]
                v["__reference"] = k
                result[group].append(v)
        return result

    def print_summary(self):
        if not hasattr(self, "doc"):
            return None
        info = self.doc['info']
        print "Calais Request ID: %s" % info['calaisRequestID']
        if info.has_key('externalID'): 
            print "External ID: %s" % info['externalID']
        if info.has_key('docTitle'):
            print "Title: %s " % info['docTitle']
        print "Language: %s" % self.doc['meta']['language']
        print "Extractions: "
        for k,v in self.simplified_response.items():
            print "\t%d %s" % (len(v), k)

    def print_entities(self):
        if not hasattr(self, "entities"):
            return None
        for item in self.entities:
            print "%s: %s (%.2f)" % (item['_type'], item['name'], item['relevance'])

    def print_topics(self):
        if not hasattr(self, "topics"):
            return None
        for topic in self.topics:
            print topic['categoryName']

    def print_relations(self):
        if not hasattr(self, "relations"):
            return None
        for relation in self.relations:
            print relation['_type']
            for k,v in relation.items():
                if not k.startswith("_"):
                    if isinstance(v, unicode):
                        print "\t%s:%s" % (k,v)
                    elif isinstance(v, dict) and v.has_key('name'):
                        print "\t%s:%s" % (k, v['name'])
#--------

apgdata=scraperwiki.sqlite.select("* from all_party_groups_2.groups")
try:
    donedata=scraperwiki.sqlite.select("`Group` from groups")
except: donedata=[]

done=[]
for row in donedata:
    done.append(row['Group'])
print done

calais = Calais(calaisKey, submitter="python-calais ouseful")

def dropper(table):
    if table!='':
        try: scraperwiki.sqlite.execute('drop table "'+table+'"')
        except: pass


def getYdata(txt,s=1):
    sleep(s)
    query = 'select * from contentanalysis.analyze where text = "'+txt+'"'
    print query
    try:
        url= 'http://query.yahooapis.com/v1/public/yql?q='+ urllib.quote(query)+'&format=json'
        yData=simplejson.load(urllib.urlopen(url))
        if 'error' in yData: yData=''
        elif yData['query']['count']==0:
            yData=''
    except: yData=''
    return yData

def patcher():
    rdata=scraperwiki.sqlite.select("* from groups")
    count=0
    for row in rdata:
        if row['Benefits']=="None.": continue
        txt=' '.join( [ row['Benefits'], row['Purpose'], row['Group'] ])
        if 'yData' not in row or row['yData']==None or row['yData']=='':
            yData=getYdata(txt)
            if yData=='': count=count+1
            else: count=0
        else:
            yData=simplejson.loads(row['yData'])
        #{"query": {"count": 0, "lang": "en-US", "results": null, "created": "2012-12-15T20:33:34Z"}}
            if yData['query']['count']==0:
                yData=getYdata(txt)
                if yData=='': count=count+1
                else: count=0
        if count>10:
            print "pulling back..."
            exit(-1)
        if yData!='':
            row['yData']=simplejson.dumps(yData)
            scraperwiki.sqlite.save(unique_keys=['Group'], table_name='groups', data=row,verbose=0)

def patcher2():
    #{"language": [{"__reference": "http://d.opencalais.com/dochash-1/18f7985a-cbe9-3a47-bcee-50175a44107c/lid/DefaultLangId", "language": "http://d.opencalais.com/lid/DefaultLangId/InputTextTooShort"}]}
    rdata=scraperwiki.sqlite.select("* from groups")
    for row in rdata:
        if row['Benefits']=="None.":
            print 'skipping...'
        else:
            sleep(1)
            #txt=' '.join( [ row['Benefits'],row['Benefits'] ])
            txt=' '.join( [ row['Benefits'], row['Purpose'], row['Group'] ])
            cData=simplejson.loads(row['cData'])
            #print cData
            #This doesn't catch the right thing:-(
            if 'entities' not in cData and 'topics' not in cData:
                print "No entities or topics"
                try:
                    result = calais.analyze(txt)
                    cData=result.simplified_response
            
                    if 'entities' in cData or 'topics' in cData:
                        row['cData']=simplejson.dumps(yData)
                        scraperwiki.sqlite.save(unique_keys=['Group'], table_name='groups', data=row,verbose=0)
                except: pass
#exit(-1)

for row in apgdata:
    if row['Group'] not in done:
        if row['Benefits']!="None.":
            sleep(1)
            txt=' '.join( [ row['Benefits'], row['Purpose'], row['Group'] ])
            try:
                result = calais.analyze(txt)
                cData=result.simplified_response
                row['cData']=simplejson.dumps(cData)
            except: row['cData']=''
            yData=getYdata(txt,0)
            row['yData']=simplejson.dumps(yData)
        scraperwiki.sqlite.save(unique_keys=['Group'], table_name='groups', data=row,verbose=0)


#entity mapper
data=scraperwiki.sqlite.select("* from groups")
#dropper('calaisEntities')
#dropper('allEntities')
def calaisParser():
    for cDataRaw in data:
        dd=[]
        #print cDataRaw['cData']
    
        if cDataRaw['cData']!=None:
            cData=simplejson.loads(cDataRaw['cData'])
            if 'entities' in cData:
                #print "trying"
                try:
                    for entity in cData['entities']:
                        d={}
                        if entity["_type"] in ["Company" , "Organization","PublishedMedium","Facility"]:
                            if (entity["name"],entity["_type"]) not in dd:
                                d["name"]=entity["name"]
                                d["typ"]=entity["_type"]
                                d['group']=cDataRaw['Group']
                                dd.append( (entity["name"],entity["_type"]) )
                                scraperwiki.sqlite.save(unique_keys=['name','typ'], table_name='calaisEntities', data=d,verbose=0)
                                d['src']='calais'
                                scraperwiki.sqlite.save(unique_keys=['name','typ','src'], table_name='allEntities', data=d)
                except: pass
#calaisParser()
def yParser():
    for yDataRaw in data:
        #print yDataRaw['yData']
        if yDataRaw['yData'] !=None: yData=simplejson.loads(yDataRaw['yData'])
        else: yData={'query':{}}
        #print yData
        if 'results' in yData['query'] and yData['query']['results']!=None:
            #print 'a',yData
            for row in yData['query']['results']['entities']['entity']:
                if 'types' in row and type(row) is dict:
                    if type(row['types']) is dict:
                        if 'type' in row['types']:
                                d={}
                                d['group']=yDataRaw['Group']
                                if type(row['types']['type']) is dict:
                                    if row['types']['type']['content']=="/organization":
                                        d["name"]=row['text']['content']
                                        d["typ"]=row['types']['type']['content']
                                        #print 'b',row['text']['content'],row['types']['type']['content']
                                        scraperwiki.sqlite.save(unique_keys=['name','typ'], table_name='yEntities', data=d,verbose=0)
                                        d['src']='yql'
                                        scraperwiki.sqlite.save(unique_keys=['name','typ','src'], table_name='allEntities', data=d)
                                else:
                                    for rrow in row['types']['type']:
                                        if 'content' in rrow and rrow['content']=="/organization":
                                            #print 'b',row['text']['content'],rrow['content']
                                            d["name"]=row['text']['content']
                                            d["typ"]=rrow['content']
                                            scraperwiki.sqlite.save(unique_keys=['name','typ'], table_name='yEntities', data=d,verbose=0)
                                            d['src']='yql'
                                            scraperwiki.sqlite.save(unique_keys=['name','typ','src'], table_name='allEntities', data=d)

yParser()
#result.print_entities()
#result.print_relations() 
#print result.entities
#print result.simplified_response


patcher()
patcher2()


