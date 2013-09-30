# Blank Python
import scraperwiki
# import unidecode
import chardet
import scrapemark

print scrapemark.scrape("""
    {*<tr><td style="padding-top:10px;" valign="top" width="150"><a style="text-decoration:underline;"href="{{ links.url }}">{{ [links].title }}</a></td><td style="padding-top:10px;">{{ move_type }} {{ move_firm }} ({{ move_pos }})</td><td style="padding-top:10px;" align="right" valign="top" width="80">{{ move_date }}</td></tr>
    *}""",
url='http://manokarjera.cv.lt/career.aspx'
    )
# Blank Python
import scraperwiki
# import unidecode
import chardet
import scrapemark

print scrapemark.scrape("""
    {*<tr><td style="padding-top:10px;" valign="top" width="150"><a style="text-decoration:underline;"href="{{ links.url }}">{{ [links].title }}</a></td><td style="padding-top:10px;">{{ move_type }} {{ move_firm }} ({{ move_pos }})</td><td style="padding-top:10px;" align="right" valign="top" width="80">{{ move_date }}</td></tr>
    *}""",
url='http://manokarjera.cv.lt/career.aspx'
    )
