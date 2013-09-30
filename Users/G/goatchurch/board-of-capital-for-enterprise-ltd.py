"""Parses the staff of Capital for Enterprise Ltd, including bios which can later be archived and
natural language processed to find out how many have careers solely within venture capital industry"""

import scraperwiki
import re
import urlparse


#<div class="tpitem">
#<img src="/images/PeterS1.jpg"  class="photo" alt="Peter Shortt" width="68" height="85" /><p><strong>Peter Shortt</strong></p>
#  <p>Peter is...</p>
#  <p>In the...</p><hr width="100%" size="2" />
#  <p></p>
#</div>

#<div class="titem">
#<h3><span>Equity Team</span></h3>
#</div>

def ParseTeampage(urlteampage, team):
    result = [ ]
    teampage = scraperwiki.scrape(urlteampage)
    for teamitem in re.findall('(?s)<div class="(tpitem|titem)">\s*(.*?)</div>', teampage):
        if re.match("\s*<h3>", teamitem[1]):
            team = re.match("\s*<h3>(?:<span>)?(.*?)(?:</span>)?</h3>", teamitem[1]).group(1)
            #print "Team", team
            continue
        lteamitem = re.sub("</?span.*?>", "", teamitem[1])
        mheading = re.match('(?:<img src="(.*?)"\s*class="photo" alt="(.*?)".*?>)?\s*<p>\s*<strong>(.*?)(?:\s*\((.*?)\))?</strong>(?:</p>|<br />|\s)*', lteamitem)
        teammember = { }
        teammember["name"] = mheading.group(3)
        if mheading.group(4):
            teammember["position"] = mheading.group(4)

        mtail = re.search('<hr.*?>(?:</?p>|\s|<br />)*$', lteamitem)
        if mtail:
            biosection = lteamitem[mheading.end(0):mtail.start(0)]
        else:
            biosection = lteamitem[mheading.end(0):]

        # process and make sure this text only has <p> values
        p = re.sub("</?p>|<br />", "NL;", biosection.strip())
        p = re.sub("\s+", " ", p)
        p = re.sub("^NL;|NL;$", "", p).strip()
        p = re.sub("NL;(?:\s|NL;)*", "NL;", p)
        p = re.sub("NL;", "\n\n", p)
        teammember["bio"] = p
        teammember["team"] = team
        #print teammember
        result.append(teammember)
    return result
    

def Getteampages():
    "Verifies the links to the two tables come from the people page"
    urlpeoplepages = "http://www.capitalforenterprise.gov.uk/our_people"
    peoplepages = scraperwiki.scrape(urlpeoplepages)
    mnonexecs = re.search('<a href="(/our_people/board)">Non-Executive Board Members</a>', peoplepages)
    urlnonexecs = urlparse.urljoin(urlpeoplepages, mnonexecs.group(1))
    mexecteam = re.search('<a href="(/our_people/fund)">Executive Team</a>', peoplepages)
    urlexecteam = urlparse.urljoin(urlpeoplepages, mexecteam.group(1))
    return urlnonexecs, urlexecteam


# main function
urlnonexecs, urlexecteam = Getteampages()
print urlnonexecs, urlexecteam
r1 = ParseTeampage(urlnonexecs, "nonexec")
r2 = ParseTeampage(urlexecteam, "execs")
r1.extend(r2)
for r in r1:
    scraperwiki.sqlite.save(["name"], r)


"""Parses the staff of Capital for Enterprise Ltd, including bios which can later be archived and
natural language processed to find out how many have careers solely within venture capital industry"""

import scraperwiki
import re
import urlparse


#<div class="tpitem">
#<img src="/images/PeterS1.jpg"  class="photo" alt="Peter Shortt" width="68" height="85" /><p><strong>Peter Shortt</strong></p>
#  <p>Peter is...</p>
#  <p>In the...</p><hr width="100%" size="2" />
#  <p></p>
#</div>

#<div class="titem">
#<h3><span>Equity Team</span></h3>
#</div>

def ParseTeampage(urlteampage, team):
    result = [ ]
    teampage = scraperwiki.scrape(urlteampage)
    for teamitem in re.findall('(?s)<div class="(tpitem|titem)">\s*(.*?)</div>', teampage):
        if re.match("\s*<h3>", teamitem[1]):
            team = re.match("\s*<h3>(?:<span>)?(.*?)(?:</span>)?</h3>", teamitem[1]).group(1)
            #print "Team", team
            continue
        lteamitem = re.sub("</?span.*?>", "", teamitem[1])
        mheading = re.match('(?:<img src="(.*?)"\s*class="photo" alt="(.*?)".*?>)?\s*<p>\s*<strong>(.*?)(?:\s*\((.*?)\))?</strong>(?:</p>|<br />|\s)*', lteamitem)
        teammember = { }
        teammember["name"] = mheading.group(3)
        if mheading.group(4):
            teammember["position"] = mheading.group(4)

        mtail = re.search('<hr.*?>(?:</?p>|\s|<br />)*$', lteamitem)
        if mtail:
            biosection = lteamitem[mheading.end(0):mtail.start(0)]
        else:
            biosection = lteamitem[mheading.end(0):]

        # process and make sure this text only has <p> values
        p = re.sub("</?p>|<br />", "NL;", biosection.strip())
        p = re.sub("\s+", " ", p)
        p = re.sub("^NL;|NL;$", "", p).strip()
        p = re.sub("NL;(?:\s|NL;)*", "NL;", p)
        p = re.sub("NL;", "\n\n", p)
        teammember["bio"] = p
        teammember["team"] = team
        #print teammember
        result.append(teammember)
    return result
    

def Getteampages():
    "Verifies the links to the two tables come from the people page"
    urlpeoplepages = "http://www.capitalforenterprise.gov.uk/our_people"
    peoplepages = scraperwiki.scrape(urlpeoplepages)
    mnonexecs = re.search('<a href="(/our_people/board)">Non-Executive Board Members</a>', peoplepages)
    urlnonexecs = urlparse.urljoin(urlpeoplepages, mnonexecs.group(1))
    mexecteam = re.search('<a href="(/our_people/fund)">Executive Team</a>', peoplepages)
    urlexecteam = urlparse.urljoin(urlpeoplepages, mexecteam.group(1))
    return urlnonexecs, urlexecteam


# main function
urlnonexecs, urlexecteam = Getteampages()
print urlnonexecs, urlexecteam
r1 = ParseTeampage(urlnonexecs, "nonexec")
r2 = ParseTeampage(urlexecteam, "execs")
r1.extend(r2)
for r in r1:
    scraperwiki.sqlite.save(["name"], r)


