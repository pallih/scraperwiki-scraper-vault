import scraperwiki
import scrapemark
import urllib2


#html = urllib2.urlopen("http://www.thinkdigit.com/author/Kshitij_Sobti_47.html").read()


scraped = scrapemark.scrape(
"""
<div id="maindiv">
{*
    <div><div><a class="headlines" href="">{{ [title] }}</a></div></div>
*}
</div>
""",
url="http://www.thinkdigit.com/author/Kshitij_Sobti_47.html"
)

print scraped
import scraperwiki
import scrapemark
import urllib2


#html = urllib2.urlopen("http://www.thinkdigit.com/author/Kshitij_Sobti_47.html").read()


scraped = scrapemark.scrape(
"""
<div id="maindiv">
{*
    <div><div><a class="headlines" href="">{{ [title] }}</a></div></div>
*}
</div>
""",
url="http://www.thinkdigit.com/author/Kshitij_Sobti_47.html"
)

print scraped
