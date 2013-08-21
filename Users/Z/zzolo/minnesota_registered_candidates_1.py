import scraperwiki
import mechanize
import csv
import re

# Set to True to only do a few rows of data
test = False
count = 0

# In order to get primary results, we use another scraper
scraperwiki.sqlite.attach('minnesota_state_primary_results')

# Unfortunately, the text download needs some POST data, so we fake
# a form submission
url = 'http://candidates.sos.state.mn.us/'

br = mechanize.Browser()
br.set_handle_robots(False) # no robots 
br.set_handle_refresh(False) # can sometimes hang without this 
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
response = br.open(url)
br.select_form(nr=0)
br.set_all_readonly(False)
br['__EVENTTARGET'] ='ctl00$ContentPlaceHolder1$lbStateMediaFile'
br['__EVENTARGUMENT'] = ''
br.find_control("ctl00$ContentPlaceHolder1$btnOfficeTitle").disabled = True
br.find_control("ctl00$ContentPlaceHolder1$btnSearchByOfficeLevel").disabled = True
br.find_control("ctl00$ContentPlaceHolder1$btnSearchByCandidateName").disabled = True
response2 = br.submit()

# Now go through the data
candidates = csv.reader(response2, delimiter=';', quotechar='|')
for row in candidates:
    # Testing, maybe
    count = count + 1
    if test and count > 100:
        continue

    # For some (awesome) reason, there are extra semicolons in
    # some addresses.  This may be that people entered them, or
    # they represent line breaks.  This is very hackish
    if len(row) == 21 and row[8] != 'MN':
        row[6] = row[6] + row[7]
        popped = row.pop(7)
    if len(row) == 21 and row[8] == 'MN':
        row[10] = row[10] + row[11]
        popped = row.pop(11)
    if len(row) == 22 and row[8] == 'MN':
        row[10] = row[10] + row[11] + row[12]
        popped = row.pop(11)
        popped = row.pop(11)

    # Add http if needed
    if not(row[15].startswith('http')) and row[15] != '':
        row[15] = 'http://' + row[15]
    if row[6] == 'NOT REQUIRED':
        row[6] = ''

    # Determine boundary ID, see http://boundaries.minnpost.com
    b_id = ''
    office_type = ''
    seats_available = 1
    if row[3] == 'U.S. President & Vice President':
        b_id = 'united-states-of-america-country-2012'
        office_type = 'U.S. President and Vice President'
    elif row[3] in ['U.S. Senator', 'Chief Justice - Supreme Court']:
        b_id = 'minnesota-state-2011'
        if row[3] == 'U.S. Senator':
            office_type = 'U.S. Senator'
        else:
            office_type = 'Chief Justice of Supreme Court'
    else:
        match = re.match(r'U\.S\. Representative District ([0-9]+)', row[3], re.IGNORECASE)
        if match is not None:
            b_id = match.group(1) + '-congressional-district-2012'
            office_type = 'U.S. Representative'

        match = re.match(r'State Senator District ([0-9]+)', row[3], re.IGNORECASE)
        if match is not None:
            b_id = match.group(1) + '-state-senate-district-2012'
            office_type = 'State Senator'

        match = re.match(r'State Representative District ([0-9]+[a-zA-Z]+)', row[3], re.IGNORECASE)
        if match is not None:
            b_id = match.group(1).lower() + '-state-house-district-2012'
            office_type = 'State Representative'

        match = re.match(r'Associate Justice - Supreme Court [0-9]+', row[3], re.IGNORECASE)
        if match is not None:
            b_id = 'minnesota-state-2011'
            office_type = 'Associate Justice of Supreme Court'

        match = re.match(r'Judge - Court of Appeals [0-9]+', row[3], re.IGNORECASE)
        if match is not None:
            b_id = 'minnesota-state-2011'
            office_type = 'Court of Appeals Judge'

        match = re.match(r'Judge - ([0-9]+)[A-Za-z]{2} District Court ([0-9]+)', row[3], re.IGNORECASE)
        if match is not None:
            b_id = match.group(1) + '-district-court-2012'
            # Add leading zero
            if len(match.group(1)) == 1:
                b_id = '0' + b_id
            office_type = 'District Court Judge'

        match = re.match(r'County Commissioner District ([0-9]+)', row[3], re.IGNORECASE)
        if match is not None:
            b_id = row[4] + '-0' + match.group(1) + '-county-commissioner-district-2012'
            office_type = 'County Commissioner'

        match = re.match(r'Soil And Water Supervisor District ([0-9]+)', row[3], re.IGNORECASE)
        if match is not None:
            #b_id = row[4] + '-0' + match.group(1) + '-soil-and-water-district-2012'
            office_type = 'Soil and Water Supervisor'

        match = re.match(r'Special Election For Soil And Water Supervisor District ([0-9]+)', row[3], re.IGNORECASE)
        if match is not None:
            #b_id = row[4] + '-0' + match.group(1) + '-soil-and-water-district-2012'
            office_type = 'Soil and Water Supervisor'

        match = re.match(r'Special Election For County Commissioner District ([0-9]+)', row[3], re.IGNORECASE)
        if match is not None:
            #b_id = row[4] + '-0' + match.group(1) + '-county-commissioner-district-2012'
            office_type = 'County Commissioner'

        match = re.match(r'County Park Commissioner District ([0-9]+)', row[3], re.IGNORECASE)
        if match is not None:
            #b_id = row[4] + '-0' + match.group(1) + '-county-commissioner-districts-2012'
            office_type = 'County Park Commissioner'


    # Try to get a first and last name
    first = ''
    last = ''
    if row[3] == 'U.S. President & Vice President':
        cands = row[1].split(' AND ')
        split = cands[0].split()
        last = split[-1]
        first = cands[0][0:len(cands[0]) - len(last)]
    else:
        split = row[1].split()
        last = split[-1]
        first = row[1][0:len(row[1]) - len(last)]

    # Make a unique id
    name_id = re.sub(r'\W+', '', row[1])
    id = row[0] + '-' + row[5] + '-' + name_id

    # Make address
    residence_address = ''
    if row[6]:
        residence_address = row[6] + ' \r\n ' + row[7] + ', ' + row[8] + ' ' + row[9]
    campaign_address = ''
    if row[10]:
        campaign_address = row[10] + ' \r\n ' + row[11] + ', ' + row[12] + ' ' + row[13]

    # Translate for full politcal party name
    parties = {
        'CP': 'Constitution',
        'DFL': 'Democratic-Farmer-Labor',
        'EDP': 'Ecology Democracy Party',
        'GR': 'Grassroots',
        'Green': 'Green',
        'IND': 'Independent',
        'MOP': 'Minnesota Open Progressives',
        'NP': 'Nonpartisan',
        'R': 'Republican',
        'IP': 'Independence',
        'D': 'Democratic',
        'SWP': 'Socialist Workers Party',
        'GP': 'Green party',
        'SL': 'Socialist Labor Party',
        'CG': 'Constitutional Government Party',
        'JP': 'Justice Party',
        'LIB': 'Libertarian Party'
    }
    party_name = ''
    if row[5] and row[5] in parties:
        party_name = parties[row[5]]


    # Now we need to reconcile primary data to see who has won
    primary_id = ''
    primary_percentage = 0
    primary_won = 0
    dropout = 0
    perc_q = """
s.percentage, s.id
FROM minnesota_state_primary_results.swdata AS s
WHERE s.office_id = '%s'
  AND county_id = '%s'
  AND s.name_id = '%s'
    """

    # Non-partisan elections mean that the primary picks the top 2
    if row[5] == 'NP':
        winners_q = """
s.id
FROM minnesota_state_primary_results.swdata AS s
  JOIN (
    SELECT s.id
    FROM minnesota_state_primary_results.swdata AS s
    WHERE s.office_id = '%s'
      AND s.county_id = '%s'
      AND party_id = 'NP'
    ORDER BY CAST(percentage AS FLOAT) DESC
    LIMIT 2
  ) AS a
  ON s.id = a.id
WHERE s.name_id = '%s'
        """
    else:
        winners_q = """
s.id
FROM minnesota_state_primary_results.swdata AS s
  JOIN (
    SELECT s.office_group_id, MAX(CAST(percentage AS FLOAT)) as top_perc
    FROM minnesota_state_primary_results.swdata AS s
    GROUP BY s.office_group_id
  ) AS a
  ON CAST(s.percentage AS FLOAT) = a.top_perc
  AND s.office_group_id = a.office_group_id
WHERE s.office_id = '%s'
  AND s.county_id = '%s'
  AND s.name_id = '%s'
        """

    perc_q = perc_q % (row[0], row[4], name_id)
    perc = scraperwiki.sqlite.select(perc_q)
    if len(perc) > 0:
        primary_percentage = perc[0]['percentage']
        primary_id = perc[0]['id']

    winners_q = winners_q % (row[0], row[4], name_id)
    winner = scraperwiki.sqlite.select(winners_q)
    if len(winner) > 0:
        primary_won = 1

    if primary_percentage > 0 and primary_won == 0:
        dropout = 1
    
    # Create data row
    data = {
        'id': id,
        'office_id': row[0],
        'candidate': row[1],
        # 2 is office id repeated
        'office': row[3],
        'county_id': row[4],
        'party': row[5],
        'residence_street': row[6],
        'residence_city': row[7],
        'residence_state': row[8],
        'residence_zip': row[9],
        'residence_address': residence_address,
        'campaign_street': row[10],
        'campaign_city': row[11],
        'campaign_state': row[12],
        'campaign_zip': row[13],
        'campaign_address': campaign_address,
        'phone': row[14], 
        'website': row[15], 
        'email': row[16],
        'rmate_website': row[17], 
        'rmate_email': row[18], 
        'rmate_phone': row[19],
        'name_id': name_id,
        'party_name': party_name,
        'boundary_id': b_id,
        'first_name': first,
        'last_name': last,
        'office_type': office_type,
        'seats_available': seats_available,
        'election_date': '2012-11-06',
        'primary_date': '2012-08-14',
        'dropout': dropout,
        'primary_id': primary_id,
        'primary_percentage': primary_percentage, 
        'primary_won': primary_won
    }
    scraperwiki.sqlite.save(unique_keys=['id'], data=data)

