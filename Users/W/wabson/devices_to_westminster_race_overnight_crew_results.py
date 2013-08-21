import scraperwiki
import cgi, os
import json
from datetime import datetime, timedelta, date

sourcescraper = 'devizes_to_westminster_results'
scraperwiki.sqlite.attach(sourcescraper)
scraperwiki.sqlite.attach('easter_dates')

default_year = date.today().year

locations = ['devizes', 'pewsey', 'hford', 'newbury', 'aldermaston', 'reading', 'marsh', 'marlow', 'bray', 'windsor', 'shepperton', 'teddington', 'westminster']

# Distances of each checkpoint in km
distances = {
    'devizes': 0.0,
    'pewsey': 19.227889994,
    'hford': 41.4827534204,
    'newbury': 55.5393448573,
    'aldermaston': 69.5968471956,
    'reading': 87.4062952057,
    'marsh': 98.6132040826,
    'marlow': 113.422632976,
    'bray': 127.201653799,
    'windsor': 140.881688903,
    'shepperton': 156.575465378,
    'teddington': 173.967656418,
    'westminster': 201.332868591
}

def km_to_mi(d):
    return d * 0.621371192

def get_easter_date(year):
    row = scraperwiki.sqlite.select("* from easter_dates.swdata where year = %s" % (year))[0]
    return date(row['year'], row['month'], row['day'])

def daytime_to_datetime(year, daytime):
    days = ['Fri', 'Sat', 'Sun', 'Mon']
    start_date = get_easter_date(year) - timedelta(days=-2) # We need the date of Good Friday, not Sunday
    parts = daytime.split(' ')
    if len(parts) == 2:
        day = parts[0]
        timeparts = parts[1].split(':')
        if len(timeparts) == 3:
            return (datetime(start_date.year, start_date.month, start_date.day, int(timeparts[0]), int(timeparts[1]), int(timeparts[2]))) + (timedelta(days=days.index(day)))
    return None

def calculate_crew_data(year, row):
    lastdist = 0.0
    lasttime = None
    cdata = {}
    missing_locs = [] # any stages for which timing data is missing
    for loc in locations:
        stage_data = None
        retired = str(row['time_%s' % (loc)]).startswith('rtd')
        stime = daytime_to_datetime(year, row['time_%s' % (loc)].replace('rtd ', ''))
        # TODO check if time is marked as retired
        if (stime is not None):
            sdist = distances[loc]
            stage_dist = sdist - lastdist
            stage_time = stime - lasttime if lasttime is not None else None
            stage_speed = stage_dist / (stage_time.seconds / 3600.0) if stage_time is not None else None
            stage_data = {
                'split_dist': sdist,
                'split_time': stime,
                'stage_dist': stage_dist,
                'stage_time': stage_time,
                'stage_speed': stage_speed,
                'retired': retired
            }
            cdata[loc] = stage_data

            lastdist = sdist
            lasttime = stime
        else:
            missing_locs.append(loc)

        if stage_data is not None and len(missing_locs) > 0:
            for loc in missing_locs:
                cdata[loc] = stage_data
            missing_locs = []

    return cdata

def calculate_mean_data(data):
    total_boats = 0
    location_totals = dict(zip(locations, [{'dist': 0.0, 'time': timedelta(0), 'speed': 0.0} for l in locations]))
    for bn in data.keys():
        crew_data = data[bn]
        if not crew_data['retired']:
            for loc in crew_data['locations'].keys():
                crew_location = crew_data['locations'][loc]
                if (crew_location['stage_dist'] > 0.0):
                    location_totals[loc]['dist'] = crew_location['stage_dist']
                    location_totals[loc]['time'] += crew_location['stage_time']
                    location_totals[loc]['speed'] += crew_location['stage_speed']
            total_boats += 1
    if total_boats > 0:
        return dict(zip(locations, [{'stage_dist': location_totals[l]['dist'] / float(total_boats), 'stage_time': (location_totals[l]['time'].seconds / 3600.0) / float(total_boats), 'stage_speed': location_totals[l]['speed'] / float(total_boats)} for l in locations]))
    else:
        return None

def get_result_locations(datalocations):
    return [{'name': loc, 'speed': km_to_mi(datalocations[loc]['stage_speed']) if datalocations[loc]['stage_speed'] is not None else 0.0, 'retired': datalocations[loc]['retired']} for loc in locations]

def print_result_locations(datalocations):
    print '<table border="1">'
    for loc in locations:
        if loc in datalocations:
            print "<tr>"
            print '<td>%s</td>' % (loc)
            #print '<td>%.1f</td>' % (km_to_mi(data[loc]['split_dist']))
            #print '<td>%.1f</td>' % (km_to_mi(data[loc]['stage_dist']))
            #print '<td>%s</td>' % (data[loc]['split_time'])
            #print '<td>%s</td>' % (data[loc]['stage_time'] if data[loc]['stage_time'] is not None else '')
            print '<td>%.2f%s</td>' % (km_to_mi(datalocations[loc]['stage_speed']) if datalocations[loc]['stage_speed'] is not None else 0.0, " (retired)" if 'retired' in datalocations[loc] and datalocations[loc]['retired'] else '')
            print "</tr>"
    print "</table>"

paramdict = dict(cgi.parse_qsl(os.getenv("QUERY_STRING", "")))
year = paramdict['y'] if 'y' in paramdict else default_year
boat_nums = paramdict['bn'].split(',')

def print_result(boat_num, data):
    print '<h2>Boat number %s%s</h2>' % (boat_num, ' (Retired)' if data['retired'] else '')
    print_result_locations(data['locations'])

def get_position_data():
    if 'bn' in paramdict:
        boat_nums = paramdict['bn'].split(',')
        query = "locations.*, firstname_1, firstname_2, surname_1, surname_2, club_1, club_2, class_position as position, elapsed_time from devizes_to_westminster_results.locations JOIN devizes_to_westminster_results.class_results on locations.boat_number=class_results.boat_number where class_results.year = '%s'" % (int(year))
        if boat_nums[0] != "all":
            query += ' and class_results.boat_number IN (%s)' % ('%s' % (int(boat_nums[0])) + ' '.join([(", %s" % int(bn)) for bn in boat_nums[1:]]))
        return scraperwiki.sqlite.select(query)

def print_html():
    print "<html>"
    print "<head>"
    print "<title>Devices to Westminster Race Overnight Crew Results</title>"
    print "</head>"
    print "<body>"
    print '<div id="hd">'
    print "<h1>Devices to Westminster Race Overnight Crew Results</h1>"
    print '</div>'
    print '<div id="bd">'
    
    dist = 0.0
    lastname = ""
    units = "mi"
    
    # Put together parameters and build the data
    if 'bn' in paramdict:
        rows = get_position_data()
        data = dict(zip([row['boat_number'] for row in rows], [{'locations': calculate_crew_data(year, row), 'retired': row['status'].startswith('rtd'), 'disqualified': row['status'].startswith('dsq')} for row in rows]))
        
        if boat_nums[0] != "all":
            for bn in data.keys():
                print_result(bn, data[bn])

        if len(data) > 1:
            md = calculate_mean_data(data)
            if md is not None:
                print "<h2>Average for all non-retired boats</h2>"
                print_result_locations(md)
    else:
        print '<form method="get" action=".">'
        print 'Enter boat number(s), separated by commas: <input type="text" name="bn" /><br />'
        print '<input type="submit" value="Submit" />'
        print '</form>'
    
    print '</body>'
    print '</html>'

def build_crew_data(row):
    crews = []
    crews.append({'firstname': row['firstname_1'], 'surname': row['surname_1'], 'club': row['club_1']})
    if row['surname_2'] is not None and row['surname_2'] != '':
        crews.append({'firstname': row['firstname_2'], 'surname': row['surname_2'], 'club': row['club_2']})
    return crews

def print_json():
    scraperwiki.utils.httpresponseheader("Content-Type", "application/json")
    if 'bn' in paramdict:
        rows = get_position_data()
        data = dict(zip([row['boat_number'] for row in rows], [{'crew': build_crew_data(row), 'position': row['position'], 'time': row['elapsed_time'], 'locations': calculate_crew_data(year, row), 'retired': row['status'].startswith('rtd'), 'disqualified': row['status'].startswith('dsq')} for row in rows]))
        if boat_nums[0] != "all":
            print json.dumps({'results': [{'boat_number': bn, 'position': data[bn]['position'] , 'time': data[bn]['time'], 'crew': data[bn]['crew'], 'locations': get_result_locations(data[bn]['locations'])} for bn in data.keys()], 'year': year}, indent=4)

if 'format' in paramdict and paramdict['format'] == 'json':
    print_json()
else:
    print_html()