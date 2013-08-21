import scraperwiki
import os, cgi, re, sys
import urllib


def Main():
    sqs = os.getenv("QUERY_STRING", "")
    qs = cgi.parse_qs(sqs)

    language = qs.get("language", [""])[0]
    line = qs.get("line", [""])[0]
    character = int(qs.get("character", [-1])[0])

    if not language:
        print "<h2>Missing parameters</h2>"
        return

    #if language == "html":
    #    scraperwiki.utils.httpresponseheader("Location", "/html_cheat_sheet/?%s" % sqs)
    #    sys.exit(0)


    word = getselectedword(line, character)
    
    
    if re.match("http://\S*$", word) and language == "python":
        scraperwiki.utils.httpresponseheader("Location", "http://scraperwikiviews.com/run/lxml-cheat-sheet/?url=%s" % urllib.quote(word))
        return

    if language == "python":
        print "<h2>You're asking for help with <b>%s</b></h2>" % re.sub("<", "&lt;", word)
        print "<pre>%s</pre>" % re.sub("<", "&lt;", os.popen('echo "help(\\"%s\\")" | python' % word).read())
        return

    if language == "html":
        print "<h2>Choose your HTML help service</h2>"
        lis = [ ("sqlite_html_cheat_sheet", "Interactive sqlite cheat sheet"), 
                ("jquery_cheat_sheet", "Quick help with JQuery"), 
                ("raphaeljs_cheat_sheet", "Quick help with interactive RaphaelJS graphics"), 
              ]
        print "<ul>"
        for lia, lim in lis:
            print '<li><a href="/run/%s">%s</a></li>' % (lia, lim)
        print "</ul>"
        return

    print "<h2>You're asking for help with <b>%s</b></h2>" % re.sub("<", "&lt;", word)
    print "In language %s" % language
    return




def getselectedword(line, character):
    ip = character
    while ip >= 1 and re.match("[\w\.]", line[ip-1]):
        ip -= 1
    ie = character
    while ie < len(line) and re.match("\w", line[ie]):
        ie += 1
    word = line[ip:ie]

    # search for quotes
    while ip >= 1 and line[ip-1] not in ('"', "'"):
        ip -= 1
    while ie < len(line) and line[ie] not in ('"', "'"):
        ie += 1
    if ip >= 1 and ie < len(line) and line[ip-1] in ('"', "'") and line[ip-1] == line[ie]:
        word = line[ip:ie] 

    return word    


Main()


import scraperwiki
import os, cgi, re, sys
import urllib


def Main():
    sqs = os.getenv("QUERY_STRING", "")
    qs = cgi.parse_qs(sqs)

    language = qs.get("language", [""])[0]
    line = qs.get("line", [""])[0]
    character = int(qs.get("character", [-1])[0])

    if not language:
        print "<h2>Missing parameters</h2>"
        return

    #if language == "html":
    #    scraperwiki.utils.httpresponseheader("Location", "/html_cheat_sheet/?%s" % sqs)
    #    sys.exit(0)


    word = getselectedword(line, character)
    
    
    if re.match("http://\S*$", word) and language == "python":
        scraperwiki.utils.httpresponseheader("Location", "http://scraperwikiviews.com/run/lxml-cheat-sheet/?url=%s" % urllib.quote(word))
        return

    if language == "python":
        print "<h2>You're asking for help with <b>%s</b></h2>" % re.sub("<", "&lt;", word)
        print "<pre>%s</pre>" % re.sub("<", "&lt;", os.popen('echo "help(\\"%s\\")" | python' % word).read())
        return

    if language == "html":
        print "<h2>Choose your HTML help service</h2>"
        lis = [ ("sqlite_html_cheat_sheet", "Interactive sqlite cheat sheet"), 
                ("jquery_cheat_sheet", "Quick help with JQuery"), 
                ("raphaeljs_cheat_sheet", "Quick help with interactive RaphaelJS graphics"), 
              ]
        print "<ul>"
        for lia, lim in lis:
            print '<li><a href="/run/%s">%s</a></li>' % (lia, lim)
        print "</ul>"
        return

    print "<h2>You're asking for help with <b>%s</b></h2>" % re.sub("<", "&lt;", word)
    print "In language %s" % language
    return




def getselectedword(line, character):
    ip = character
    while ip >= 1 and re.match("[\w\.]", line[ip-1]):
        ip -= 1
    ie = character
    while ie < len(line) and re.match("\w", line[ie]):
        ie += 1
    word = line[ip:ie]

    # search for quotes
    while ip >= 1 and line[ip-1] not in ('"', "'"):
        ip -= 1
    while ie < len(line) and line[ie] not in ('"', "'"):
        ie += 1
    if ip >= 1 and ie < len(line) and line[ip-1] in ('"', "'") and line[ip-1] == line[ie]:
        word = line[ip:ie] 

    return word    


Main()


import scraperwiki
import os, cgi, re, sys
import urllib


def Main():
    sqs = os.getenv("QUERY_STRING", "")
    qs = cgi.parse_qs(sqs)

    language = qs.get("language", [""])[0]
    line = qs.get("line", [""])[0]
    character = int(qs.get("character", [-1])[0])

    if not language:
        print "<h2>Missing parameters</h2>"
        return

    #if language == "html":
    #    scraperwiki.utils.httpresponseheader("Location", "/html_cheat_sheet/?%s" % sqs)
    #    sys.exit(0)


    word = getselectedword(line, character)
    
    
    if re.match("http://\S*$", word) and language == "python":
        scraperwiki.utils.httpresponseheader("Location", "http://scraperwikiviews.com/run/lxml-cheat-sheet/?url=%s" % urllib.quote(word))
        return

    if language == "python":
        print "<h2>You're asking for help with <b>%s</b></h2>" % re.sub("<", "&lt;", word)
        print "<pre>%s</pre>" % re.sub("<", "&lt;", os.popen('echo "help(\\"%s\\")" | python' % word).read())
        return

    if language == "html":
        print "<h2>Choose your HTML help service</h2>"
        lis = [ ("sqlite_html_cheat_sheet", "Interactive sqlite cheat sheet"), 
                ("jquery_cheat_sheet", "Quick help with JQuery"), 
                ("raphaeljs_cheat_sheet", "Quick help with interactive RaphaelJS graphics"), 
              ]
        print "<ul>"
        for lia, lim in lis:
            print '<li><a href="/run/%s">%s</a></li>' % (lia, lim)
        print "</ul>"
        return

    print "<h2>You're asking for help with <b>%s</b></h2>" % re.sub("<", "&lt;", word)
    print "In language %s" % language
    return




def getselectedword(line, character):
    ip = character
    while ip >= 1 and re.match("[\w\.]", line[ip-1]):
        ip -= 1
    ie = character
    while ie < len(line) and re.match("\w", line[ie]):
        ie += 1
    word = line[ip:ie]

    # search for quotes
    while ip >= 1 and line[ip-1] not in ('"', "'"):
        ip -= 1
    while ie < len(line) and line[ie] not in ('"', "'"):
        ie += 1
    if ip >= 1 and ie < len(line) and line[ip-1] in ('"', "'") and line[ip-1] == line[ie]:
        word = line[ip:ie] 

    return word    


Main()


import scraperwiki
import os, cgi, re, sys
import urllib


def Main():
    sqs = os.getenv("QUERY_STRING", "")
    qs = cgi.parse_qs(sqs)

    language = qs.get("language", [""])[0]
    line = qs.get("line", [""])[0]
    character = int(qs.get("character", [-1])[0])

    if not language:
        print "<h2>Missing parameters</h2>"
        return

    #if language == "html":
    #    scraperwiki.utils.httpresponseheader("Location", "/html_cheat_sheet/?%s" % sqs)
    #    sys.exit(0)


    word = getselectedword(line, character)
    
    
    if re.match("http://\S*$", word) and language == "python":
        scraperwiki.utils.httpresponseheader("Location", "http://scraperwikiviews.com/run/lxml-cheat-sheet/?url=%s" % urllib.quote(word))
        return

    if language == "python":
        print "<h2>You're asking for help with <b>%s</b></h2>" % re.sub("<", "&lt;", word)
        print "<pre>%s</pre>" % re.sub("<", "&lt;", os.popen('echo "help(\\"%s\\")" | python' % word).read())
        return

    if language == "html":
        print "<h2>Choose your HTML help service</h2>"
        lis = [ ("sqlite_html_cheat_sheet", "Interactive sqlite cheat sheet"), 
                ("jquery_cheat_sheet", "Quick help with JQuery"), 
                ("raphaeljs_cheat_sheet", "Quick help with interactive RaphaelJS graphics"), 
              ]
        print "<ul>"
        for lia, lim in lis:
            print '<li><a href="/run/%s">%s</a></li>' % (lia, lim)
        print "</ul>"
        return

    print "<h2>You're asking for help with <b>%s</b></h2>" % re.sub("<", "&lt;", word)
    print "In language %s" % language
    return




def getselectedword(line, character):
    ip = character
    while ip >= 1 and re.match("[\w\.]", line[ip-1]):
        ip -= 1
    ie = character
    while ie < len(line) and re.match("\w", line[ie]):
        ie += 1
    word = line[ip:ie]

    # search for quotes
    while ip >= 1 and line[ip-1] not in ('"', "'"):
        ip -= 1
    while ie < len(line) and line[ie] not in ('"', "'"):
        ie += 1
    if ip >= 1 and ie < len(line) and line[ip-1] in ('"', "'") and line[ip-1] == line[ie]:
        word = line[ip:ie] 

    return word    


Main()


import scraperwiki
import os, cgi, re, sys
import urllib


def Main():
    sqs = os.getenv("QUERY_STRING", "")
    qs = cgi.parse_qs(sqs)

    language = qs.get("language", [""])[0]
    line = qs.get("line", [""])[0]
    character = int(qs.get("character", [-1])[0])

    if not language:
        print "<h2>Missing parameters</h2>"
        return

    #if language == "html":
    #    scraperwiki.utils.httpresponseheader("Location", "/html_cheat_sheet/?%s" % sqs)
    #    sys.exit(0)


    word = getselectedword(line, character)
    
    
    if re.match("http://\S*$", word) and language == "python":
        scraperwiki.utils.httpresponseheader("Location", "http://scraperwikiviews.com/run/lxml-cheat-sheet/?url=%s" % urllib.quote(word))
        return

    if language == "python":
        print "<h2>You're asking for help with <b>%s</b></h2>" % re.sub("<", "&lt;", word)
        print "<pre>%s</pre>" % re.sub("<", "&lt;", os.popen('echo "help(\\"%s\\")" | python' % word).read())
        return

    if language == "html":
        print "<h2>Choose your HTML help service</h2>"
        lis = [ ("sqlite_html_cheat_sheet", "Interactive sqlite cheat sheet"), 
                ("jquery_cheat_sheet", "Quick help with JQuery"), 
                ("raphaeljs_cheat_sheet", "Quick help with interactive RaphaelJS graphics"), 
              ]
        print "<ul>"
        for lia, lim in lis:
            print '<li><a href="/run/%s">%s</a></li>' % (lia, lim)
        print "</ul>"
        return

    print "<h2>You're asking for help with <b>%s</b></h2>" % re.sub("<", "&lt;", word)
    print "In language %s" % language
    return




def getselectedword(line, character):
    ip = character
    while ip >= 1 and re.match("[\w\.]", line[ip-1]):
        ip -= 1
    ie = character
    while ie < len(line) and re.match("\w", line[ie]):
        ie += 1
    word = line[ip:ie]

    # search for quotes
    while ip >= 1 and line[ip-1] not in ('"', "'"):
        ip -= 1
    while ie < len(line) and line[ie] not in ('"', "'"):
        ie += 1
    if ip >= 1 and ie < len(line) and line[ip-1] in ('"', "'") and line[ip-1] == line[ie]:
        word = line[ip:ie] 

    return word    


Main()


import scraperwiki
import os, cgi, re, sys
import urllib


def Main():
    sqs = os.getenv("QUERY_STRING", "")
    qs = cgi.parse_qs(sqs)

    language = qs.get("language", [""])[0]
    line = qs.get("line", [""])[0]
    character = int(qs.get("character", [-1])[0])

    if not language:
        print "<h2>Missing parameters</h2>"
        return

    #if language == "html":
    #    scraperwiki.utils.httpresponseheader("Location", "/html_cheat_sheet/?%s" % sqs)
    #    sys.exit(0)


    word = getselectedword(line, character)
    
    
    if re.match("http://\S*$", word) and language == "python":
        scraperwiki.utils.httpresponseheader("Location", "http://scraperwikiviews.com/run/lxml-cheat-sheet/?url=%s" % urllib.quote(word))
        return

    if language == "python":
        print "<h2>You're asking for help with <b>%s</b></h2>" % re.sub("<", "&lt;", word)
        print "<pre>%s</pre>" % re.sub("<", "&lt;", os.popen('echo "help(\\"%s\\")" | python' % word).read())
        return

    if language == "html":
        print "<h2>Choose your HTML help service</h2>"
        lis = [ ("sqlite_html_cheat_sheet", "Interactive sqlite cheat sheet"), 
                ("jquery_cheat_sheet", "Quick help with JQuery"), 
                ("raphaeljs_cheat_sheet", "Quick help with interactive RaphaelJS graphics"), 
              ]
        print "<ul>"
        for lia, lim in lis:
            print '<li><a href="/run/%s">%s</a></li>' % (lia, lim)
        print "</ul>"
        return

    print "<h2>You're asking for help with <b>%s</b></h2>" % re.sub("<", "&lt;", word)
    print "In language %s" % language
    return




def getselectedword(line, character):
    ip = character
    while ip >= 1 and re.match("[\w\.]", line[ip-1]):
        ip -= 1
    ie = character
    while ie < len(line) and re.match("\w", line[ie]):
        ie += 1
    word = line[ip:ie]

    # search for quotes
    while ip >= 1 and line[ip-1] not in ('"', "'"):
        ip -= 1
    while ie < len(line) and line[ie] not in ('"', "'"):
        ie += 1
    if ip >= 1 and ie < len(line) and line[ip-1] in ('"', "'") and line[ip-1] == line[ie]:
        word = line[ip:ie] 

    return word    


Main()


import scraperwiki
import os, cgi, re, sys
import urllib


def Main():
    sqs = os.getenv("QUERY_STRING", "")
    qs = cgi.parse_qs(sqs)

    language = qs.get("language", [""])[0]
    line = qs.get("line", [""])[0]
    character = int(qs.get("character", [-1])[0])

    if not language:
        print "<h2>Missing parameters</h2>"
        return

    #if language == "html":
    #    scraperwiki.utils.httpresponseheader("Location", "/html_cheat_sheet/?%s" % sqs)
    #    sys.exit(0)


    word = getselectedword(line, character)
    
    
    if re.match("http://\S*$", word) and language == "python":
        scraperwiki.utils.httpresponseheader("Location", "http://scraperwikiviews.com/run/lxml-cheat-sheet/?url=%s" % urllib.quote(word))
        return

    if language == "python":
        print "<h2>You're asking for help with <b>%s</b></h2>" % re.sub("<", "&lt;", word)
        print "<pre>%s</pre>" % re.sub("<", "&lt;", os.popen('echo "help(\\"%s\\")" | python' % word).read())
        return

    if language == "html":
        print "<h2>Choose your HTML help service</h2>"
        lis = [ ("sqlite_html_cheat_sheet", "Interactive sqlite cheat sheet"), 
                ("jquery_cheat_sheet", "Quick help with JQuery"), 
                ("raphaeljs_cheat_sheet", "Quick help with interactive RaphaelJS graphics"), 
              ]
        print "<ul>"
        for lia, lim in lis:
            print '<li><a href="/run/%s">%s</a></li>' % (lia, lim)
        print "</ul>"
        return

    print "<h2>You're asking for help with <b>%s</b></h2>" % re.sub("<", "&lt;", word)
    print "In language %s" % language
    return




def getselectedword(line, character):
    ip = character
    while ip >= 1 and re.match("[\w\.]", line[ip-1]):
        ip -= 1
    ie = character
    while ie < len(line) and re.match("\w", line[ie]):
        ie += 1
    word = line[ip:ie]

    # search for quotes
    while ip >= 1 and line[ip-1] not in ('"', "'"):
        ip -= 1
    while ie < len(line) and line[ie] not in ('"', "'"):
        ie += 1
    if ip >= 1 and ie < len(line) and line[ip-1] in ('"', "'") and line[ip-1] == line[ie]:
        word = line[ip:ie] 

    return word    


Main()


