"""
Scraper for the 2012 general election in Minnesota.  Main
results page can be found here:

http://electionresults.sos.state.mn.us/enr/ENR/Home/1
http://electionresults.sos.state.mn.us/ENR/Select/Download/1
"""
import scraperwiki
import lxml.html
import dateutil.parser
import csv
import re


urls = {
  'presidential': 'http://electionresults.sos.state.mn.us/ENR/Results/MediaResult/1?mediafileid=22',
  'us_senate': 'http://electionresults.sos.state.mn.us/ENR/Results/MediaResult/1?mediafileid=23',
  'us_house': 'http://electionresults.sos.state.mn.us/ENR/Results/MediaResult/1?mediafileid=24',
  'state_senate': 'http://electionresults.sos.state.mn.us/ENR/Results/MediaResult/1?mediafileid=30',
  'state_house': 'http://electionresults.sos.state.mn.us/ENR/Results/MediaResult/1?mediafileid=20',
  'amendments': 'http://electionresults.sos.state.mn.us/ENR/Results/MediaResult/1?mediafileid=66',
  'supreme_appeal_courts': 'http://electionresults.sos.state.mn.us/ENR/Results/MediaResult/1?mediafileid=37',
  'district_courts': 'http://electionresults.sos.state.mn.us/ENR/Results/MediaResult/1?mediafileid=44',
  'county': 'http://electionresults.sos.state.mn.us/ENR/Results/MediaResult/1?mediafileid=88', # Includes questions
  'municipal': 'http://electionresults.sos.state.mn.us/ENR/Results/MediaResult/1?mediafileid=1', # Includes questions
  'school_board': 'http://electionresults.sos.state.mn.us/ENR/Results/MediaResult/1?mediafileid=7', # Includes questions
  'hospital': 'http://electionresults.sos.state.mn.us/ENR/Results/MediaResult/1?mediafileid=90' # Includes questions
}

for u in urls:
  data = scraperwiki.scrape(urls[u])
  candidates = csv.reader(data.splitlines(), delimiter=';', quotechar='|')
  count = 0  

  for row in candidates:
    # Make name ID
    name_id = re.sub(r'\W+', '', row[7])
    office_name_id = re.sub(r'\W+', '', row[4])

    # To better match up with other data, we set a no county_id to 88 as
    # that is what MN SoS uses
    if not row[1]:
      row[1] = '88'

    data = {
      'id': u + '-' + row[1] + '-' + row[3] + '-' + row[6] + '-' + office_name_id + '-' + name_id,
      'office_type': u,
      'state': row[0],
      'county_id': row[1],
      'precinct': row[2],
      'office_id': row[3],
      'office_name': row[4],
      'fips_code': row[5],
      'candidate_id': row[6],
      'candidate': row[7],
      'suffix': row[8],
      'incumbent_code': row[9],
      'party_id': row[10],
      'precincts_reporting': row[11],
      'total_effected_precincts': row[12],
      'votes_candidate': row[13],
      'percentage': row[14],
      'total_votes_for_office': row[15],
      'name_id': name_id,
      'office_group_id': row[3] + '-' + row[1] + '-' + office_name_id + '-' + row[10]
    }
    scraperwiki.sqlite.save(unique_keys=['id'], data=data)
    count = count + 1

  # Output total for each category
  print 'Total for %s: %s' % (u, count)