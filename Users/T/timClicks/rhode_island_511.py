from scrapemark import scrape
from scraperwiki import sqlite

url="http://511.dot.ri.gov/lb/default.asp?area=statewide&display=allAdvisories&date=&textOnly=true"

pattern = """
{*
<tr class='label'>{{ [events].type }}-{{ [events].road }}</tr>
<tr class='event'><td><b>{{ [events].subtitle }}</b><br>{{ [events].description }}<br>{* Comment:{{ [events].comment }} *} <br>{* last updated{{ [events].last_updated_at }} *}</tr>
*}
"""

sqlite.save(['subtitle'], data=scrape(pattern, url=url)['events'])