import urllib2
import lxml.etree
import datetime
import re

# Uses the Wikipedia API  http://en.wikipedia.org/w/api.php
# to scrape a single page (with redirects)
# Also parses all templates within the page

# Future work needs to look up all pages of a particular category 
# (maybe iterating down through the sub-categories) so we can get, for example, all caves or mountains
# or all Wikipedia contributors who can program
#   http://en.wikipedia.org/wiki/Category:User_python (753 total)
#   http://en.wikipedia.org/wiki/Category:User_php    (1225 total)
#   http://en.wikipedia.org/wiki/Category:User_ruby   (401 total)
#   http://en.wikipedia.org/wiki/Category:User_java   (1202 total)


def GetWikipediaPage(title):
    rvprop = "timestamp|user|comment|content"
    url = "http://en.wikipedia.org/w/api.php?action=query&format=xml&prop=revisions&redirects=yes&titles=%s&rvprop=%s" % (title, rvprop)
    doc = lxml.etree.parse(urllib2.urlopen(url))
    root = doc.getroot()
    print lxml.etree.tostring(root)
    page = root.find(".//page")
    if "missing" in page.attrib:
        return None
    rev = page.find(".//rev")

    title = page.get("title")
    timestamp = datetime.datetime.strptime(rev.get("timestamp"), "%Y-%m-%dT%H:%M:%SZ")
    content = rev.text
    templates = ParseTemplates(content)

    return { "title":title, "timestamp":timestamp, "content":content, "templates":templates }


# parse out the {{ template | key=value | ... }} elements from a wikipedia page
# this is the raw material used by dbPedia.  The 0 key is always the name of the template.
def ParseTemplParams(bracket, templ, bracketclose):
    res = { }
    for i, param in enumerate(templ):
        k, e, v = re.match("(?s)([^=]*)(=?)(.*)$", param).groups()
        if e:
            res[k.strip()] = v.strip()
        else:
            res[i] = k.strip()
    return res
        
def ParseTemplates(text):
    res = [ ]
    templstack = [ ]
    for tt in re.split("(\{\{\{|\}\}\}|\{\{|\}\}|\[\[|\]\]|\|)", text):
        if tt in ["{{{", "{{", "[["]:
            templstack.append([tt, [ [ ] ] ])
        elif templstack and tt in ["}}}", "}}", "]]"]:
            templstack[-1][1][-1] = "".join(templstack[-1][1][-1])
            templstack[-1].append(tt)
            if len(templstack) == 1:
                if templstack[-1][0] == "{{":
                    res.append(ParseTemplParams(templstack[-1][0], templstack[-1][1], templstack[-1][2]))
            else:
                templstack[-2][1][-1].append(templstack[-1][0])
                templstack[-2][1][-1].append("|".join(templstack[-1][1]))
                templstack[-2][1][-1].append(templstack[-1][2])
            del templstack[-1]
        elif tt == "|" and templstack:
            templstack[-1][1][-1] = "".join(templstack[-1][1][-1])
            templstack[-1][1].append([ ])
        elif templstack:
            templstack[-1][1][-1].append(tt)
    return res


# example page
print GetWikipediaPage("UN")


