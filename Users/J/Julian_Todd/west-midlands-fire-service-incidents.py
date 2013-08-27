import urllib
import re

# Issues.  
#  Date formats are pretty variable
#  Times only start to be quoted in August
#  Times are usually from the day before.  Not live.

def ParsePage(url):
    html = urllib.urlopen(url).read()
    #print html
    mtext = re.search('(?s)<h3>([^<]*)</h3>\s*<h1>([^<]*)</h1>\s*(.*?)</div>', html)
    d, title, text = mtext.groups()
    text = re.sub("(?:\s*<p>|\s*</p>|\s*<br\s*/?>)+", "--newline--", text)
    text = re.sub("\s+", " ", text)
    text = re.sub("(?:&nbsp;|\s)+", " ", text)
    text = re.split("--newline--", text)
    text = [t.strip()  for t in text  if t.strip()]
    print d, text, title
    
    
def Scrape(cs):
    url = "http://www.wmfs.net/Media/Incidents/?currentSlot=%d" % cs
    html = urllib.urlopen(url).read()
    dds = re.findall('<a href="(http://www.wmfs.net/Media/Incidents/Details/\?contentId=\d+)">', html)
    for dd in dds:
        ParsePage(dd)
        
for cs in range(1, 20):
    Scrape(cs)
    
import urllib
import re

# Issues.  
#  Date formats are pretty variable
#  Times only start to be quoted in August
#  Times are usually from the day before.  Not live.

def ParsePage(url):
    html = urllib.urlopen(url).read()
    #print html
    mtext = re.search('(?s)<h3>([^<]*)</h3>\s*<h1>([^<]*)</h1>\s*(.*?)</div>', html)
    d, title, text = mtext.groups()
    text = re.sub("(?:\s*<p>|\s*</p>|\s*<br\s*/?>)+", "--newline--", text)
    text = re.sub("\s+", " ", text)
    text = re.sub("(?:&nbsp;|\s)+", " ", text)
    text = re.split("--newline--", text)
    text = [t.strip()  for t in text  if t.strip()]
    print d, text, title
    
    
def Scrape(cs):
    url = "http://www.wmfs.net/Media/Incidents/?currentSlot=%d" % cs
    html = urllib.urlopen(url).read()
    dds = re.findall('<a href="(http://www.wmfs.net/Media/Incidents/Details/\?contentId=\d+)">', html)
    for dd in dds:
        ParsePage(dd)
        
for cs in range(1, 20):
    Scrape(cs)
    
import urllib
import re

# Issues.  
#  Date formats are pretty variable
#  Times only start to be quoted in August
#  Times are usually from the day before.  Not live.

def ParsePage(url):
    html = urllib.urlopen(url).read()
    #print html
    mtext = re.search('(?s)<h3>([^<]*)</h3>\s*<h1>([^<]*)</h1>\s*(.*?)</div>', html)
    d, title, text = mtext.groups()
    text = re.sub("(?:\s*<p>|\s*</p>|\s*<br\s*/?>)+", "--newline--", text)
    text = re.sub("\s+", " ", text)
    text = re.sub("(?:&nbsp;|\s)+", " ", text)
    text = re.split("--newline--", text)
    text = [t.strip()  for t in text  if t.strip()]
    print d, text, title
    
    
def Scrape(cs):
    url = "http://www.wmfs.net/Media/Incidents/?currentSlot=%d" % cs
    html = urllib.urlopen(url).read()
    dds = re.findall('<a href="(http://www.wmfs.net/Media/Incidents/Details/\?contentId=\d+)">', html)
    for dd in dds:
        ParsePage(dd)
        
for cs in range(1, 20):
    Scrape(cs)
    
import urllib
import re

# Issues.  
#  Date formats are pretty variable
#  Times only start to be quoted in August
#  Times are usually from the day before.  Not live.

def ParsePage(url):
    html = urllib.urlopen(url).read()
    #print html
    mtext = re.search('(?s)<h3>([^<]*)</h3>\s*<h1>([^<]*)</h1>\s*(.*?)</div>', html)
    d, title, text = mtext.groups()
    text = re.sub("(?:\s*<p>|\s*</p>|\s*<br\s*/?>)+", "--newline--", text)
    text = re.sub("\s+", " ", text)
    text = re.sub("(?:&nbsp;|\s)+", " ", text)
    text = re.split("--newline--", text)
    text = [t.strip()  for t in text  if t.strip()]
    print d, text, title
    
    
def Scrape(cs):
    url = "http://www.wmfs.net/Media/Incidents/?currentSlot=%d" % cs
    html = urllib.urlopen(url).read()
    dds = re.findall('<a href="(http://www.wmfs.net/Media/Incidents/Details/\?contentId=\d+)">', html)
    for dd in dds:
        ParsePage(dd)
        
for cs in range(1, 20):
    Scrape(cs)
    
import urllib
import re

# Issues.  
#  Date formats are pretty variable
#  Times only start to be quoted in August
#  Times are usually from the day before.  Not live.

def ParsePage(url):
    html = urllib.urlopen(url).read()
    #print html
    mtext = re.search('(?s)<h3>([^<]*)</h3>\s*<h1>([^<]*)</h1>\s*(.*?)</div>', html)
    d, title, text = mtext.groups()
    text = re.sub("(?:\s*<p>|\s*</p>|\s*<br\s*/?>)+", "--newline--", text)
    text = re.sub("\s+", " ", text)
    text = re.sub("(?:&nbsp;|\s)+", " ", text)
    text = re.split("--newline--", text)
    text = [t.strip()  for t in text  if t.strip()]
    print d, text, title
    
    
def Scrape(cs):
    url = "http://www.wmfs.net/Media/Incidents/?currentSlot=%d" % cs
    html = urllib.urlopen(url).read()
    dds = re.findall('<a href="(http://www.wmfs.net/Media/Incidents/Details/\?contentId=\d+)">', html)
    for dd in dds:
        ParsePage(dd)
        
for cs in range(1, 20):
    Scrape(cs)
    
import urllib
import re

# Issues.  
#  Date formats are pretty variable
#  Times only start to be quoted in August
#  Times are usually from the day before.  Not live.

def ParsePage(url):
    html = urllib.urlopen(url).read()
    #print html
    mtext = re.search('(?s)<h3>([^<]*)</h3>\s*<h1>([^<]*)</h1>\s*(.*?)</div>', html)
    d, title, text = mtext.groups()
    text = re.sub("(?:\s*<p>|\s*</p>|\s*<br\s*/?>)+", "--newline--", text)
    text = re.sub("\s+", " ", text)
    text = re.sub("(?:&nbsp;|\s)+", " ", text)
    text = re.split("--newline--", text)
    text = [t.strip()  for t in text  if t.strip()]
    print d, text, title
    
    
def Scrape(cs):
    url = "http://www.wmfs.net/Media/Incidents/?currentSlot=%d" % cs
    html = urllib.urlopen(url).read()
    dds = re.findall('<a href="(http://www.wmfs.net/Media/Incidents/Details/\?contentId=\d+)">', html)
    for dd in dds:
        ParsePage(dd)
        
for cs in range(1, 20):
    Scrape(cs)
    
import urllib
import re

# Issues.  
#  Date formats are pretty variable
#  Times only start to be quoted in August
#  Times are usually from the day before.  Not live.

def ParsePage(url):
    html = urllib.urlopen(url).read()
    #print html
    mtext = re.search('(?s)<h3>([^<]*)</h3>\s*<h1>([^<]*)</h1>\s*(.*?)</div>', html)
    d, title, text = mtext.groups()
    text = re.sub("(?:\s*<p>|\s*</p>|\s*<br\s*/?>)+", "--newline--", text)
    text = re.sub("\s+", " ", text)
    text = re.sub("(?:&nbsp;|\s)+", " ", text)
    text = re.split("--newline--", text)
    text = [t.strip()  for t in text  if t.strip()]
    print d, text, title
    
    
def Scrape(cs):
    url = "http://www.wmfs.net/Media/Incidents/?currentSlot=%d" % cs
    html = urllib.urlopen(url).read()
    dds = re.findall('<a href="(http://www.wmfs.net/Media/Incidents/Details/\?contentId=\d+)">', html)
    for dd in dds:
        ParsePage(dd)
        
for cs in range(1, 20):
    Scrape(cs)
    
import urllib
import re

# Issues.  
#  Date formats are pretty variable
#  Times only start to be quoted in August
#  Times are usually from the day before.  Not live.

def ParsePage(url):
    html = urllib.urlopen(url).read()
    #print html
    mtext = re.search('(?s)<h3>([^<]*)</h3>\s*<h1>([^<]*)</h1>\s*(.*?)</div>', html)
    d, title, text = mtext.groups()
    text = re.sub("(?:\s*<p>|\s*</p>|\s*<br\s*/?>)+", "--newline--", text)
    text = re.sub("\s+", " ", text)
    text = re.sub("(?:&nbsp;|\s)+", " ", text)
    text = re.split("--newline--", text)
    text = [t.strip()  for t in text  if t.strip()]
    print d, text, title
    
    
def Scrape(cs):
    url = "http://www.wmfs.net/Media/Incidents/?currentSlot=%d" % cs
    html = urllib.urlopen(url).read()
    dds = re.findall('<a href="(http://www.wmfs.net/Media/Incidents/Details/\?contentId=\d+)">', html)
    for dd in dds:
        ParsePage(dd)
        
for cs in range(1, 20):
    Scrape(cs)
    
