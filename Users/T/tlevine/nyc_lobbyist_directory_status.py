#from urllib import urlencode
from json import loads
from urllib2 import urlopen
from scraperwiki.sqlite import attach,select
attach('nyc_lobbyist_directory_browser')

QUERIES={
  "summary":"""
    SELECT
      sum(reimbursement) AS "Total Reimbursement"
    , sum(compensation) AS "Total Compensation"
    FROM
      `clients_details`
    WHERE
      `detailId`="Total"
    """
, "completed":"""
    SELECT
      count(`href`) AS "completed"
    FROM
      `links`
    WHERE
      `href`<(
        SELECT
          `value_blob`
        FROM
          `swvariables`
        WHERE
          `name`="previous_href"
      )
  """
, "total":"""
    SELECT
     count(`href`) AS "total"
    FROM
      `links`
  """
}

def q(key):
  return select('\n'.join(QUERIES[key].split('\n')[2:]))

def q1(key):
  return q(key)[0][key]

def estimate_remaining_years(portion_finished,starttime=1328677200):
  "1328418000 is Sunday. But let's do Wednesday to account for how it's running faster now."
  from time import time
  days_so_far=(time()-starttime)/(24*3600)
  days_remaining=days_so_far/portion_finished
  return days_remaining/365.25

def estimate_total_gb(portion_finished,currentsize):
  return (currentsize/portion_finished)/1000000000.0

def getcodeinfo():
  d=loads(urlopen("https://api.scraperwiki.com/api/1.0/scraper/getinfo?format=jsondict&name=nyc_lobbyist_directory_browser&version=-1&quietfields=code%7Crunevents%7Cuserroles%7Chistory").read())
  return d[0]['datasummary'] #['tables']

codeinfo=getcodeinfo()
records_count=str(codeinfo["total_rows"])+" rows"
db_size=str(int(codeinfo["filesize"]/1000000))+' megabytes'

money=q('summary')[0]
money['Total Reimbursement']="$"+str(int(money['Total Reimbursement']/1000000))+" million"
money['Total Compensation']="$"+str(round(float(money['Total Compensation']/1000000000),1))+" billion"

portion_finished=float(q1('completed'))/float(q1('total'))
percent_finished_str=unicode(round(100*portion_finished,2))+"%"

remaining_years=unicode(int(estimate_remaining_years(portion_finished)))
total_gb=unicode(int(estimate_total_gb(portion_finished,codeinfo["filesize"])))


main="".join([
  "<p>The scrape is "+percent_finished_str+" complete.</p>"
, "<p>The database contains "+records_count+" and takes up "+db_size+".</p>"
, "<p>It includes records regarding "
  , money["Total Reimbursement"]+" of reimbursement and "
  , money["Total Compensation"]+" of compensation."
  , "</p>"
, "<p>"
  , "I estimate that a full scrape of the current website will take "
  , remaining_years+" years "
  , "and will result in a "+total_gb+"-gigabyte database."
, "</p>"
, "<p>Of course, the new records will probably be added to the site before this scrape is finished.</p>"
#, '<p>Read more <a href="https://scraperwiki.com/scrapers/nyc_lobbyist_directory_browser/">here</a>.</p>'
])

print """
<style>
#main{ width: 100%; max-width: 600px; display: block; margin: 50px auto; }
#scraperwikipane { display: none; }
</style>
<div id="main">
<header>
"""
#<h1>NYC Lobbyist Scraper</h1>
print """
</header>
"""+main+"""
</div>
"""