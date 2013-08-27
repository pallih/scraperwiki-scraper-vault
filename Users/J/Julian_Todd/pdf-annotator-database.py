import scraperwiki
import os
import cgi
import sys
import json
import datetime
import urllib
import re

pdfannfields = ["pdfurl text", "pdfhash text", "pagenumber integer", "user text", "date text", "status text", "content text", 
                "x integer", "y integer", "x2 integer", "y2 integer", "imgwidth integer", "imgheight integer", "prevrowid integer"]
#sqlitecommand("execute", "drop table if exists pdfannotations")
#sqlitecommand("execute", "create table pdfannotations (%s)" % ",".join(pdfannfields))


def MainJsonserve(qs):
    pdfurl = qs.get("pdfurl")[0]
    pagenumber = int(qs.get("pagenumber")[0])

    if "user" not in qs:
        result = scraperwiki.sqlite.execute("select rowid, user, date, status, content, x, y, x2, y2 from pdfannotations where pdfurl=? and pagenumber=?", 
                      (pdfurl, pagenumber))
        dresult = [ dict(zip(result["keys"], d))  for d in result["data"] ]
        print json.dumps(dresult)
        return

    user = qs["user"][0]
    x, y, x2, y2 = int(qs["x"][0]), int(qs["y"][0]), int(qs["x2"][0]), int(qs["y2"][0])
    imgwidth, imgheight = int(qs["imgwidth"][0]), int(qs["imgheight"][0])
    content = qs["content"][0]
    scraperwiki.sqlite.execute("insert into pdfannotations values (?,?,?,?,?,?,?,?,?,?,?,?,?,?)", 
                  (pdfurl, "notused", pagenumber, user, datetime.datetime.now().isoformat(), "unknown", content, 
                   x, y, x2, y2, imgwidth, imgheight, -1))

    scraperwiki.sqlite.commit()
    # would be handy to return the rowid here
    print json.dumps({"status":"Okay"})


def MainIndexPage():
    result = scraperwiki.sqlite.execute("select pdfurl, pagenumber, user, date, content from pdfannotations order by pdfurl, pagenumber, y")
    print "<h2>Annotated pages so far</h2>"
    
    grpdocs = { }
    for row in result["data"]:
        pdfurl = row[0]
        pagenumber = row[1]
        if pdfurl not in grpdocs:
            grpdocs[pdfurl] = { }
        if pagenumber not in grpdocs[pdfurl]:
            grpdocs[pdfurl][pagenumber] = [ ]
        grpdocs[pdfurl][pagenumber].append(row[2:])

    for pdfurl, pages in grpdocs.items():
        print '<h4>%s <a href="%s">[pdf-doc]</a></h4>' % (pdfurl, pdfurl)
        for pagenumber, boxes in pages.items():
            annurl = 'http://scraperwikiviews.com/run/pdf-annotator/?pdfurl=%s&pagenumber=%d' % (urllib.quote(pdfurl), pagenumber)
            print '<p><a href="%s" target="_blank"><b>Page %d [annotator frontend]</b></a></p>' % (annurl, pagenumber)
            print '<ul>'
            for box in boxes:
                content = re.sub("<", "&lt;", box[2])
                if len(content) > 30:
                    content = content[:28]+" ..."
                print '<li>%s (<em>%s</em>) - %s</li>' % (box[0], box[1][:10], content)
            print '</ul>'
    return
    

    print '<form action="http://scraperwikiviews.com/run/pdf-annotator/">'
    print '<input type="text" name="pdfurl" value="">'
    print '<input type="text" name="pagenumber" value="1" style="display:none">'
    print '<input type="submit" value="Annotate another document"></form>'

try:
    qs = cgi.parse_qs(os.getenv("URLQUERY", ""))
    if "pdfurl" in qs:
        MainJsonserve(qs)
    else:
        MainIndexPage()
except ValueError:
    print "Usage: pdfurl=[document.pdf]&pagenumber=[123] "
except TypeError:
    print "Usage: pdfurl=[document.pdf]&pagenumber=[123] "
except KeyError:
    print "Usage: url=[document.pdf]&pagenumber=[123]&x=[1]&y=[2]&x2=[6]&y2=[7]&imgwidth=800&imgheight=1200&content=[description]"



import scraperwiki
import os
import cgi
import sys
import json
import datetime
import urllib
import re

pdfannfields = ["pdfurl text", "pdfhash text", "pagenumber integer", "user text", "date text", "status text", "content text", 
                "x integer", "y integer", "x2 integer", "y2 integer", "imgwidth integer", "imgheight integer", "prevrowid integer"]
#sqlitecommand("execute", "drop table if exists pdfannotations")
#sqlitecommand("execute", "create table pdfannotations (%s)" % ",".join(pdfannfields))


def MainJsonserve(qs):
    pdfurl = qs.get("pdfurl")[0]
    pagenumber = int(qs.get("pagenumber")[0])

    if "user" not in qs:
        result = scraperwiki.sqlite.execute("select rowid, user, date, status, content, x, y, x2, y2 from pdfannotations where pdfurl=? and pagenumber=?", 
                      (pdfurl, pagenumber))
        dresult = [ dict(zip(result["keys"], d))  for d in result["data"] ]
        print json.dumps(dresult)
        return

    user = qs["user"][0]
    x, y, x2, y2 = int(qs["x"][0]), int(qs["y"][0]), int(qs["x2"][0]), int(qs["y2"][0])
    imgwidth, imgheight = int(qs["imgwidth"][0]), int(qs["imgheight"][0])
    content = qs["content"][0]
    scraperwiki.sqlite.execute("insert into pdfannotations values (?,?,?,?,?,?,?,?,?,?,?,?,?,?)", 
                  (pdfurl, "notused", pagenumber, user, datetime.datetime.now().isoformat(), "unknown", content, 
                   x, y, x2, y2, imgwidth, imgheight, -1))

    scraperwiki.sqlite.commit()
    # would be handy to return the rowid here
    print json.dumps({"status":"Okay"})


def MainIndexPage():
    result = scraperwiki.sqlite.execute("select pdfurl, pagenumber, user, date, content from pdfannotations order by pdfurl, pagenumber, y")
    print "<h2>Annotated pages so far</h2>"
    
    grpdocs = { }
    for row in result["data"]:
        pdfurl = row[0]
        pagenumber = row[1]
        if pdfurl not in grpdocs:
            grpdocs[pdfurl] = { }
        if pagenumber not in grpdocs[pdfurl]:
            grpdocs[pdfurl][pagenumber] = [ ]
        grpdocs[pdfurl][pagenumber].append(row[2:])

    for pdfurl, pages in grpdocs.items():
        print '<h4>%s <a href="%s">[pdf-doc]</a></h4>' % (pdfurl, pdfurl)
        for pagenumber, boxes in pages.items():
            annurl = 'http://scraperwikiviews.com/run/pdf-annotator/?pdfurl=%s&pagenumber=%d' % (urllib.quote(pdfurl), pagenumber)
            print '<p><a href="%s" target="_blank"><b>Page %d [annotator frontend]</b></a></p>' % (annurl, pagenumber)
            print '<ul>'
            for box in boxes:
                content = re.sub("<", "&lt;", box[2])
                if len(content) > 30:
                    content = content[:28]+" ..."
                print '<li>%s (<em>%s</em>) - %s</li>' % (box[0], box[1][:10], content)
            print '</ul>'
    return
    

    print '<form action="http://scraperwikiviews.com/run/pdf-annotator/">'
    print '<input type="text" name="pdfurl" value="">'
    print '<input type="text" name="pagenumber" value="1" style="display:none">'
    print '<input type="submit" value="Annotate another document"></form>'

try:
    qs = cgi.parse_qs(os.getenv("URLQUERY", ""))
    if "pdfurl" in qs:
        MainJsonserve(qs)
    else:
        MainIndexPage()
except ValueError:
    print "Usage: pdfurl=[document.pdf]&pagenumber=[123] "
except TypeError:
    print "Usage: pdfurl=[document.pdf]&pagenumber=[123] "
except KeyError:
    print "Usage: url=[document.pdf]&pagenumber=[123]&x=[1]&y=[2]&x2=[6]&y2=[7]&imgwidth=800&imgheight=1200&content=[description]"



import scraperwiki
import os
import cgi
import sys
import json
import datetime
import urllib
import re

pdfannfields = ["pdfurl text", "pdfhash text", "pagenumber integer", "user text", "date text", "status text", "content text", 
                "x integer", "y integer", "x2 integer", "y2 integer", "imgwidth integer", "imgheight integer", "prevrowid integer"]
#sqlitecommand("execute", "drop table if exists pdfannotations")
#sqlitecommand("execute", "create table pdfannotations (%s)" % ",".join(pdfannfields))


def MainJsonserve(qs):
    pdfurl = qs.get("pdfurl")[0]
    pagenumber = int(qs.get("pagenumber")[0])

    if "user" not in qs:
        result = scraperwiki.sqlite.execute("select rowid, user, date, status, content, x, y, x2, y2 from pdfannotations where pdfurl=? and pagenumber=?", 
                      (pdfurl, pagenumber))
        dresult = [ dict(zip(result["keys"], d))  for d in result["data"] ]
        print json.dumps(dresult)
        return

    user = qs["user"][0]
    x, y, x2, y2 = int(qs["x"][0]), int(qs["y"][0]), int(qs["x2"][0]), int(qs["y2"][0])
    imgwidth, imgheight = int(qs["imgwidth"][0]), int(qs["imgheight"][0])
    content = qs["content"][0]
    scraperwiki.sqlite.execute("insert into pdfannotations values (?,?,?,?,?,?,?,?,?,?,?,?,?,?)", 
                  (pdfurl, "notused", pagenumber, user, datetime.datetime.now().isoformat(), "unknown", content, 
                   x, y, x2, y2, imgwidth, imgheight, -1))

    scraperwiki.sqlite.commit()
    # would be handy to return the rowid here
    print json.dumps({"status":"Okay"})


def MainIndexPage():
    result = scraperwiki.sqlite.execute("select pdfurl, pagenumber, user, date, content from pdfannotations order by pdfurl, pagenumber, y")
    print "<h2>Annotated pages so far</h2>"
    
    grpdocs = { }
    for row in result["data"]:
        pdfurl = row[0]
        pagenumber = row[1]
        if pdfurl not in grpdocs:
            grpdocs[pdfurl] = { }
        if pagenumber not in grpdocs[pdfurl]:
            grpdocs[pdfurl][pagenumber] = [ ]
        grpdocs[pdfurl][pagenumber].append(row[2:])

    for pdfurl, pages in grpdocs.items():
        print '<h4>%s <a href="%s">[pdf-doc]</a></h4>' % (pdfurl, pdfurl)
        for pagenumber, boxes in pages.items():
            annurl = 'http://scraperwikiviews.com/run/pdf-annotator/?pdfurl=%s&pagenumber=%d' % (urllib.quote(pdfurl), pagenumber)
            print '<p><a href="%s" target="_blank"><b>Page %d [annotator frontend]</b></a></p>' % (annurl, pagenumber)
            print '<ul>'
            for box in boxes:
                content = re.sub("<", "&lt;", box[2])
                if len(content) > 30:
                    content = content[:28]+" ..."
                print '<li>%s (<em>%s</em>) - %s</li>' % (box[0], box[1][:10], content)
            print '</ul>'
    return
    

    print '<form action="http://scraperwikiviews.com/run/pdf-annotator/">'
    print '<input type="text" name="pdfurl" value="">'
    print '<input type="text" name="pagenumber" value="1" style="display:none">'
    print '<input type="submit" value="Annotate another document"></form>'

try:
    qs = cgi.parse_qs(os.getenv("URLQUERY", ""))
    if "pdfurl" in qs:
        MainJsonserve(qs)
    else:
        MainIndexPage()
except ValueError:
    print "Usage: pdfurl=[document.pdf]&pagenumber=[123] "
except TypeError:
    print "Usage: pdfurl=[document.pdf]&pagenumber=[123] "
except KeyError:
    print "Usage: url=[document.pdf]&pagenumber=[123]&x=[1]&y=[2]&x2=[6]&y2=[7]&imgwidth=800&imgheight=1200&content=[description]"



import scraperwiki
import os
import cgi
import sys
import json
import datetime
import urllib
import re

pdfannfields = ["pdfurl text", "pdfhash text", "pagenumber integer", "user text", "date text", "status text", "content text", 
                "x integer", "y integer", "x2 integer", "y2 integer", "imgwidth integer", "imgheight integer", "prevrowid integer"]
#sqlitecommand("execute", "drop table if exists pdfannotations")
#sqlitecommand("execute", "create table pdfannotations (%s)" % ",".join(pdfannfields))


def MainJsonserve(qs):
    pdfurl = qs.get("pdfurl")[0]
    pagenumber = int(qs.get("pagenumber")[0])

    if "user" not in qs:
        result = scraperwiki.sqlite.execute("select rowid, user, date, status, content, x, y, x2, y2 from pdfannotations where pdfurl=? and pagenumber=?", 
                      (pdfurl, pagenumber))
        dresult = [ dict(zip(result["keys"], d))  for d in result["data"] ]
        print json.dumps(dresult)
        return

    user = qs["user"][0]
    x, y, x2, y2 = int(qs["x"][0]), int(qs["y"][0]), int(qs["x2"][0]), int(qs["y2"][0])
    imgwidth, imgheight = int(qs["imgwidth"][0]), int(qs["imgheight"][0])
    content = qs["content"][0]
    scraperwiki.sqlite.execute("insert into pdfannotations values (?,?,?,?,?,?,?,?,?,?,?,?,?,?)", 
                  (pdfurl, "notused", pagenumber, user, datetime.datetime.now().isoformat(), "unknown", content, 
                   x, y, x2, y2, imgwidth, imgheight, -1))

    scraperwiki.sqlite.commit()
    # would be handy to return the rowid here
    print json.dumps({"status":"Okay"})


def MainIndexPage():
    result = scraperwiki.sqlite.execute("select pdfurl, pagenumber, user, date, content from pdfannotations order by pdfurl, pagenumber, y")
    print "<h2>Annotated pages so far</h2>"
    
    grpdocs = { }
    for row in result["data"]:
        pdfurl = row[0]
        pagenumber = row[1]
        if pdfurl not in grpdocs:
            grpdocs[pdfurl] = { }
        if pagenumber not in grpdocs[pdfurl]:
            grpdocs[pdfurl][pagenumber] = [ ]
        grpdocs[pdfurl][pagenumber].append(row[2:])

    for pdfurl, pages in grpdocs.items():
        print '<h4>%s <a href="%s">[pdf-doc]</a></h4>' % (pdfurl, pdfurl)
        for pagenumber, boxes in pages.items():
            annurl = 'http://scraperwikiviews.com/run/pdf-annotator/?pdfurl=%s&pagenumber=%d' % (urllib.quote(pdfurl), pagenumber)
            print '<p><a href="%s" target="_blank"><b>Page %d [annotator frontend]</b></a></p>' % (annurl, pagenumber)
            print '<ul>'
            for box in boxes:
                content = re.sub("<", "&lt;", box[2])
                if len(content) > 30:
                    content = content[:28]+" ..."
                print '<li>%s (<em>%s</em>) - %s</li>' % (box[0], box[1][:10], content)
            print '</ul>'
    return
    

    print '<form action="http://scraperwikiviews.com/run/pdf-annotator/">'
    print '<input type="text" name="pdfurl" value="">'
    print '<input type="text" name="pagenumber" value="1" style="display:none">'
    print '<input type="submit" value="Annotate another document"></form>'

try:
    qs = cgi.parse_qs(os.getenv("URLQUERY", ""))
    if "pdfurl" in qs:
        MainJsonserve(qs)
    else:
        MainIndexPage()
except ValueError:
    print "Usage: pdfurl=[document.pdf]&pagenumber=[123] "
except TypeError:
    print "Usage: pdfurl=[document.pdf]&pagenumber=[123] "
except KeyError:
    print "Usage: url=[document.pdf]&pagenumber=[123]&x=[1]&y=[2]&x2=[6]&y2=[7]&imgwidth=800&imgheight=1200&content=[description]"



import scraperwiki
import os
import cgi
import sys
import json
import datetime
import urllib
import re

pdfannfields = ["pdfurl text", "pdfhash text", "pagenumber integer", "user text", "date text", "status text", "content text", 
                "x integer", "y integer", "x2 integer", "y2 integer", "imgwidth integer", "imgheight integer", "prevrowid integer"]
#sqlitecommand("execute", "drop table if exists pdfannotations")
#sqlitecommand("execute", "create table pdfannotations (%s)" % ",".join(pdfannfields))


def MainJsonserve(qs):
    pdfurl = qs.get("pdfurl")[0]
    pagenumber = int(qs.get("pagenumber")[0])

    if "user" not in qs:
        result = scraperwiki.sqlite.execute("select rowid, user, date, status, content, x, y, x2, y2 from pdfannotations where pdfurl=? and pagenumber=?", 
                      (pdfurl, pagenumber))
        dresult = [ dict(zip(result["keys"], d))  for d in result["data"] ]
        print json.dumps(dresult)
        return

    user = qs["user"][0]
    x, y, x2, y2 = int(qs["x"][0]), int(qs["y"][0]), int(qs["x2"][0]), int(qs["y2"][0])
    imgwidth, imgheight = int(qs["imgwidth"][0]), int(qs["imgheight"][0])
    content = qs["content"][0]
    scraperwiki.sqlite.execute("insert into pdfannotations values (?,?,?,?,?,?,?,?,?,?,?,?,?,?)", 
                  (pdfurl, "notused", pagenumber, user, datetime.datetime.now().isoformat(), "unknown", content, 
                   x, y, x2, y2, imgwidth, imgheight, -1))

    scraperwiki.sqlite.commit()
    # would be handy to return the rowid here
    print json.dumps({"status":"Okay"})


def MainIndexPage():
    result = scraperwiki.sqlite.execute("select pdfurl, pagenumber, user, date, content from pdfannotations order by pdfurl, pagenumber, y")
    print "<h2>Annotated pages so far</h2>"
    
    grpdocs = { }
    for row in result["data"]:
        pdfurl = row[0]
        pagenumber = row[1]
        if pdfurl not in grpdocs:
            grpdocs[pdfurl] = { }
        if pagenumber not in grpdocs[pdfurl]:
            grpdocs[pdfurl][pagenumber] = [ ]
        grpdocs[pdfurl][pagenumber].append(row[2:])

    for pdfurl, pages in grpdocs.items():
        print '<h4>%s <a href="%s">[pdf-doc]</a></h4>' % (pdfurl, pdfurl)
        for pagenumber, boxes in pages.items():
            annurl = 'http://scraperwikiviews.com/run/pdf-annotator/?pdfurl=%s&pagenumber=%d' % (urllib.quote(pdfurl), pagenumber)
            print '<p><a href="%s" target="_blank"><b>Page %d [annotator frontend]</b></a></p>' % (annurl, pagenumber)
            print '<ul>'
            for box in boxes:
                content = re.sub("<", "&lt;", box[2])
                if len(content) > 30:
                    content = content[:28]+" ..."
                print '<li>%s (<em>%s</em>) - %s</li>' % (box[0], box[1][:10], content)
            print '</ul>'
    return
    

    print '<form action="http://scraperwikiviews.com/run/pdf-annotator/">'
    print '<input type="text" name="pdfurl" value="">'
    print '<input type="text" name="pagenumber" value="1" style="display:none">'
    print '<input type="submit" value="Annotate another document"></form>'

try:
    qs = cgi.parse_qs(os.getenv("URLQUERY", ""))
    if "pdfurl" in qs:
        MainJsonserve(qs)
    else:
        MainIndexPage()
except ValueError:
    print "Usage: pdfurl=[document.pdf]&pagenumber=[123] "
except TypeError:
    print "Usage: pdfurl=[document.pdf]&pagenumber=[123] "
except KeyError:
    print "Usage: url=[document.pdf]&pagenumber=[123]&x=[1]&y=[2]&x2=[6]&y2=[7]&imgwidth=800&imgheight=1200&content=[description]"



import scraperwiki
import os
import cgi
import sys
import json
import datetime
import urllib
import re

pdfannfields = ["pdfurl text", "pdfhash text", "pagenumber integer", "user text", "date text", "status text", "content text", 
                "x integer", "y integer", "x2 integer", "y2 integer", "imgwidth integer", "imgheight integer", "prevrowid integer"]
#sqlitecommand("execute", "drop table if exists pdfannotations")
#sqlitecommand("execute", "create table pdfannotations (%s)" % ",".join(pdfannfields))


def MainJsonserve(qs):
    pdfurl = qs.get("pdfurl")[0]
    pagenumber = int(qs.get("pagenumber")[0])

    if "user" not in qs:
        result = scraperwiki.sqlite.execute("select rowid, user, date, status, content, x, y, x2, y2 from pdfannotations where pdfurl=? and pagenumber=?", 
                      (pdfurl, pagenumber))
        dresult = [ dict(zip(result["keys"], d))  for d in result["data"] ]
        print json.dumps(dresult)
        return

    user = qs["user"][0]
    x, y, x2, y2 = int(qs["x"][0]), int(qs["y"][0]), int(qs["x2"][0]), int(qs["y2"][0])
    imgwidth, imgheight = int(qs["imgwidth"][0]), int(qs["imgheight"][0])
    content = qs["content"][0]
    scraperwiki.sqlite.execute("insert into pdfannotations values (?,?,?,?,?,?,?,?,?,?,?,?,?,?)", 
                  (pdfurl, "notused", pagenumber, user, datetime.datetime.now().isoformat(), "unknown", content, 
                   x, y, x2, y2, imgwidth, imgheight, -1))

    scraperwiki.sqlite.commit()
    # would be handy to return the rowid here
    print json.dumps({"status":"Okay"})


def MainIndexPage():
    result = scraperwiki.sqlite.execute("select pdfurl, pagenumber, user, date, content from pdfannotations order by pdfurl, pagenumber, y")
    print "<h2>Annotated pages so far</h2>"
    
    grpdocs = { }
    for row in result["data"]:
        pdfurl = row[0]
        pagenumber = row[1]
        if pdfurl not in grpdocs:
            grpdocs[pdfurl] = { }
        if pagenumber not in grpdocs[pdfurl]:
            grpdocs[pdfurl][pagenumber] = [ ]
        grpdocs[pdfurl][pagenumber].append(row[2:])

    for pdfurl, pages in grpdocs.items():
        print '<h4>%s <a href="%s">[pdf-doc]</a></h4>' % (pdfurl, pdfurl)
        for pagenumber, boxes in pages.items():
            annurl = 'http://scraperwikiviews.com/run/pdf-annotator/?pdfurl=%s&pagenumber=%d' % (urllib.quote(pdfurl), pagenumber)
            print '<p><a href="%s" target="_blank"><b>Page %d [annotator frontend]</b></a></p>' % (annurl, pagenumber)
            print '<ul>'
            for box in boxes:
                content = re.sub("<", "&lt;", box[2])
                if len(content) > 30:
                    content = content[:28]+" ..."
                print '<li>%s (<em>%s</em>) - %s</li>' % (box[0], box[1][:10], content)
            print '</ul>'
    return
    

    print '<form action="http://scraperwikiviews.com/run/pdf-annotator/">'
    print '<input type="text" name="pdfurl" value="">'
    print '<input type="text" name="pagenumber" value="1" style="display:none">'
    print '<input type="submit" value="Annotate another document"></form>'

try:
    qs = cgi.parse_qs(os.getenv("URLQUERY", ""))
    if "pdfurl" in qs:
        MainJsonserve(qs)
    else:
        MainIndexPage()
except ValueError:
    print "Usage: pdfurl=[document.pdf]&pagenumber=[123] "
except TypeError:
    print "Usage: pdfurl=[document.pdf]&pagenumber=[123] "
except KeyError:
    print "Usage: url=[document.pdf]&pagenumber=[123]&x=[1]&y=[2]&x2=[6]&y2=[7]&imgwidth=800&imgheight=1200&content=[description]"



import scraperwiki
import os
import cgi
import sys
import json
import datetime
import urllib
import re

pdfannfields = ["pdfurl text", "pdfhash text", "pagenumber integer", "user text", "date text", "status text", "content text", 
                "x integer", "y integer", "x2 integer", "y2 integer", "imgwidth integer", "imgheight integer", "prevrowid integer"]
#sqlitecommand("execute", "drop table if exists pdfannotations")
#sqlitecommand("execute", "create table pdfannotations (%s)" % ",".join(pdfannfields))


def MainJsonserve(qs):
    pdfurl = qs.get("pdfurl")[0]
    pagenumber = int(qs.get("pagenumber")[0])

    if "user" not in qs:
        result = scraperwiki.sqlite.execute("select rowid, user, date, status, content, x, y, x2, y2 from pdfannotations where pdfurl=? and pagenumber=?", 
                      (pdfurl, pagenumber))
        dresult = [ dict(zip(result["keys"], d))  for d in result["data"] ]
        print json.dumps(dresult)
        return

    user = qs["user"][0]
    x, y, x2, y2 = int(qs["x"][0]), int(qs["y"][0]), int(qs["x2"][0]), int(qs["y2"][0])
    imgwidth, imgheight = int(qs["imgwidth"][0]), int(qs["imgheight"][0])
    content = qs["content"][0]
    scraperwiki.sqlite.execute("insert into pdfannotations values (?,?,?,?,?,?,?,?,?,?,?,?,?,?)", 
                  (pdfurl, "notused", pagenumber, user, datetime.datetime.now().isoformat(), "unknown", content, 
                   x, y, x2, y2, imgwidth, imgheight, -1))

    scraperwiki.sqlite.commit()
    # would be handy to return the rowid here
    print json.dumps({"status":"Okay"})


def MainIndexPage():
    result = scraperwiki.sqlite.execute("select pdfurl, pagenumber, user, date, content from pdfannotations order by pdfurl, pagenumber, y")
    print "<h2>Annotated pages so far</h2>"
    
    grpdocs = { }
    for row in result["data"]:
        pdfurl = row[0]
        pagenumber = row[1]
        if pdfurl not in grpdocs:
            grpdocs[pdfurl] = { }
        if pagenumber not in grpdocs[pdfurl]:
            grpdocs[pdfurl][pagenumber] = [ ]
        grpdocs[pdfurl][pagenumber].append(row[2:])

    for pdfurl, pages in grpdocs.items():
        print '<h4>%s <a href="%s">[pdf-doc]</a></h4>' % (pdfurl, pdfurl)
        for pagenumber, boxes in pages.items():
            annurl = 'http://scraperwikiviews.com/run/pdf-annotator/?pdfurl=%s&pagenumber=%d' % (urllib.quote(pdfurl), pagenumber)
            print '<p><a href="%s" target="_blank"><b>Page %d [annotator frontend]</b></a></p>' % (annurl, pagenumber)
            print '<ul>'
            for box in boxes:
                content = re.sub("<", "&lt;", box[2])
                if len(content) > 30:
                    content = content[:28]+" ..."
                print '<li>%s (<em>%s</em>) - %s</li>' % (box[0], box[1][:10], content)
            print '</ul>'
    return
    

    print '<form action="http://scraperwikiviews.com/run/pdf-annotator/">'
    print '<input type="text" name="pdfurl" value="">'
    print '<input type="text" name="pagenumber" value="1" style="display:none">'
    print '<input type="submit" value="Annotate another document"></form>'

try:
    qs = cgi.parse_qs(os.getenv("URLQUERY", ""))
    if "pdfurl" in qs:
        MainJsonserve(qs)
    else:
        MainIndexPage()
except ValueError:
    print "Usage: pdfurl=[document.pdf]&pagenumber=[123] "
except TypeError:
    print "Usage: pdfurl=[document.pdf]&pagenumber=[123] "
except KeyError:
    print "Usage: url=[document.pdf]&pagenumber=[123]&x=[1]&y=[2]&x2=[6]&y2=[7]&imgwidth=800&imgheight=1200&content=[description]"



import scraperwiki
import os
import cgi
import sys
import json
import datetime
import urllib
import re

pdfannfields = ["pdfurl text", "pdfhash text", "pagenumber integer", "user text", "date text", "status text", "content text", 
                "x integer", "y integer", "x2 integer", "y2 integer", "imgwidth integer", "imgheight integer", "prevrowid integer"]
#sqlitecommand("execute", "drop table if exists pdfannotations")
#sqlitecommand("execute", "create table pdfannotations (%s)" % ",".join(pdfannfields))


def MainJsonserve(qs):
    pdfurl = qs.get("pdfurl")[0]
    pagenumber = int(qs.get("pagenumber")[0])

    if "user" not in qs:
        result = scraperwiki.sqlite.execute("select rowid, user, date, status, content, x, y, x2, y2 from pdfannotations where pdfurl=? and pagenumber=?", 
                      (pdfurl, pagenumber))
        dresult = [ dict(zip(result["keys"], d))  for d in result["data"] ]
        print json.dumps(dresult)
        return

    user = qs["user"][0]
    x, y, x2, y2 = int(qs["x"][0]), int(qs["y"][0]), int(qs["x2"][0]), int(qs["y2"][0])
    imgwidth, imgheight = int(qs["imgwidth"][0]), int(qs["imgheight"][0])
    content = qs["content"][0]
    scraperwiki.sqlite.execute("insert into pdfannotations values (?,?,?,?,?,?,?,?,?,?,?,?,?,?)", 
                  (pdfurl, "notused", pagenumber, user, datetime.datetime.now().isoformat(), "unknown", content, 
                   x, y, x2, y2, imgwidth, imgheight, -1))

    scraperwiki.sqlite.commit()
    # would be handy to return the rowid here
    print json.dumps({"status":"Okay"})


def MainIndexPage():
    result = scraperwiki.sqlite.execute("select pdfurl, pagenumber, user, date, content from pdfannotations order by pdfurl, pagenumber, y")
    print "<h2>Annotated pages so far</h2>"
    
    grpdocs = { }
    for row in result["data"]:
        pdfurl = row[0]
        pagenumber = row[1]
        if pdfurl not in grpdocs:
            grpdocs[pdfurl] = { }
        if pagenumber not in grpdocs[pdfurl]:
            grpdocs[pdfurl][pagenumber] = [ ]
        grpdocs[pdfurl][pagenumber].append(row[2:])

    for pdfurl, pages in grpdocs.items():
        print '<h4>%s <a href="%s">[pdf-doc]</a></h4>' % (pdfurl, pdfurl)
        for pagenumber, boxes in pages.items():
            annurl = 'http://scraperwikiviews.com/run/pdf-annotator/?pdfurl=%s&pagenumber=%d' % (urllib.quote(pdfurl), pagenumber)
            print '<p><a href="%s" target="_blank"><b>Page %d [annotator frontend]</b></a></p>' % (annurl, pagenumber)
            print '<ul>'
            for box in boxes:
                content = re.sub("<", "&lt;", box[2])
                if len(content) > 30:
                    content = content[:28]+" ..."
                print '<li>%s (<em>%s</em>) - %s</li>' % (box[0], box[1][:10], content)
            print '</ul>'
    return
    

    print '<form action="http://scraperwikiviews.com/run/pdf-annotator/">'
    print '<input type="text" name="pdfurl" value="">'
    print '<input type="text" name="pagenumber" value="1" style="display:none">'
    print '<input type="submit" value="Annotate another document"></form>'

try:
    qs = cgi.parse_qs(os.getenv("URLQUERY", ""))
    if "pdfurl" in qs:
        MainJsonserve(qs)
    else:
        MainIndexPage()
except ValueError:
    print "Usage: pdfurl=[document.pdf]&pagenumber=[123] "
except TypeError:
    print "Usage: pdfurl=[document.pdf]&pagenumber=[123] "
except KeyError:
    print "Usage: url=[document.pdf]&pagenumber=[123]&x=[1]&y=[2]&x2=[6]&y2=[7]&imgwidth=800&imgheight=1200&content=[description]"



