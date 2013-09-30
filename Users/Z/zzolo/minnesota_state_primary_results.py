import scraperwiki
import mechanize
import csv
import re

# List of downloaded files here:
# http://electionresults.sos.state.mn.us/ENR/Select/Download/2

# File and column descriptions:
# http://electionresults.sos.state.mn.us/ENR/Select/DownloadFileFormats/2

# Candidate ID is not actually a universal identifier, but is really
# a party code with an ID relative to that office/race

# Office ID is not actually identifiable either, as some questions have
# the same ID

urls = {
    'us_senate': 'http://electionresults.sos.state.mn.us/ENR/Results/MediaResult/2?mediafileid=23',
    'us_house': 'http://electionresults.sos.state.mn.us/ENR/Results/MediaResult/2?mediafileid=24',
    'state_senate': 'http://electionresults.sos.state.mn.us/ENR/Results/MediaResult/2?mediafileid=30',
    'state_house': 'http://electionresults.sos.state.mn.us/ENR/Results/MediaResult/2?mediafileid=20',
    'supreme_appeal_courts': 'http://electionresults.sos.state.mn.us/ENR/Results/MediaResult/2?mediafileid=37',
    'district_courts': 'http://electionresults.sos.state.mn.us/ENR/Results/MediaResult/2?mediafileid=44',
    'county': 'http://electionresults.sos.state.mn.us/ENR/Results/MediaResult/2?mediafileid=88', # Includes questions
    'municipal': 'http://electionresults.sos.state.mn.us/ENR/Results/MediaResult/2?mediafileid=1', # Includes questions
    'school_board': 'http://electionresults.sos.state.mn.us/ENR/Results/MediaResult/2?mediafileid=7' # Includes questions
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
    print 'Total for %s: %s' % (u, count)import scraperwiki
import mechanize
import csv
import re

# List of downloaded files here:
# http://electionresults.sos.state.mn.us/ENR/Select/Download/2

# File and column descriptions:
# http://electionresults.sos.state.mn.us/ENR/Select/DownloadFileFormats/2

# Candidate ID is not actually a universal identifier, but is really
# a party code with an ID relative to that office/race

# Office ID is not actually identifiable either, as some questions have
# the same ID

urls = {
    'us_senate': 'http://electionresults.sos.state.mn.us/ENR/Results/MediaResult/2?mediafileid=23',
    'us_house': 'http://electionresults.sos.state.mn.us/ENR/Results/MediaResult/2?mediafileid=24',
    'state_senate': 'http://electionresults.sos.state.mn.us/ENR/Results/MediaResult/2?mediafileid=30',
    'state_house': 'http://electionresults.sos.state.mn.us/ENR/Results/MediaResult/2?mediafileid=20',
    'supreme_appeal_courts': 'http://electionresults.sos.state.mn.us/ENR/Results/MediaResult/2?mediafileid=37',
    'district_courts': 'http://electionresults.sos.state.mn.us/ENR/Results/MediaResult/2?mediafileid=44',
    'county': 'http://electionresults.sos.state.mn.us/ENR/Results/MediaResult/2?mediafileid=88', # Includes questions
    'municipal': 'http://electionresults.sos.state.mn.us/ENR/Results/MediaResult/2?mediafileid=1', # Includes questions
    'school_board': 'http://electionresults.sos.state.mn.us/ENR/Results/MediaResult/2?mediafileid=7' # Includes questions
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