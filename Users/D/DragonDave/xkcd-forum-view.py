# Blank Pythonimport scraperwiki           
sourcescraper = 'xkcd-forum'
import cgi, os, scraperwiki

def politecrash(text="Sorry about that."):
    print """
<h1>Something went wrong.</h1>
<p>%s</p>
<p>If you want to raise the issue, email dave.mckee@gmail.com with the URL you used.</p>
"""%text
    exit()

try:
    query= dict(cgi.parse_qsl(os.getenv("QUERY_STRING", "")))
    comic=int(query['comic'])
except:
    politecrash("URLs are of the form https://views.scraperwiki.com/run/xkcd-forum-view/?comic=666")
try:
    scraperwiki.sqlite.attach(sourcescraper)
    data= scraperwiki.sqlite.select("url from swdata where number=%s"%comic)
except:
    politecrash("It's something to do with the SQL database.")
if not data:
    politecrash("""I can't find a forum discussion with that number on the website: if you want to create one, use the format '0928: "Title of Comic" """)
try:
    print """<html><head><meta HTTP-EQUIV="REFRESH" content="0; url=%s"></head><body>Redirecting you to <a href='%s'>the forums</a>...</html>""" % (data[0]['url'],data[0]['url'])
except Exception, e:
    politecrash("I've cocked something up, please email me with the text <b>'%s'</b> and the URL in your address bar."%e)
                