import scraperwiki
import lxml.html
import urllib
import simplejson


start_count = scraperwiki.sqlite.get_var("last_saved", 1) - 1
last_count = 0
count = scraperwiki.sqlite.get_var("last_counter", 0) + 1

scraperwiki.sqlite.attach( 'historic_hansard_sitting_days' )
historic_hansard_sitting_days = scraperwiki.sqlite.select("* from historic_hansard_sitting_days.swdata where count > " + str(start_count) + " order by count")
records = []

# historic_hansard_sitting_days = [{'url':'http://hansard.millbanksystems.com/sittings/1978/oct/24', 'count':1}]

for historic_hansard_sitting_day in historic_hansard_sitting_days:
    sitting_days_path = historic_hansard_sitting_day['url'] + '.js'
    sitting_days_list = simplejson.load(urllib.urlopen(sitting_days_path))    
    for sittings in sitting_days_list:
        for sitting_type in sittings.keys():
            for section in sittings[sitting_type]['top_level_sections']:
                section_key = section.keys()[0]
                section_structure = section[section_key]
                # check for blank or bogus slugs, starting with "-"?
                if section_structure['slug'] == '-':
                    slug_status = 'leading dash'
                elif section_structure['slug'] == '':
                    slug_status = 'blank'
                else:
                    slug_status = 'ok'

                full_url = historic_hansard_sitting_day['url'] + "/" + section_structure['slug']
                full_url = full_url.replace("/1/", "/01/").replace("/2/", "/02/").replace("/3/", "/03/").replace("/4/", "/04/").replace("/5/", "/05/").replace("/6/", "/06/").replace("/7/", "/07/").replace("/8/", "/08/").replace("/9/", "/09/")

                if sitting_type == 'house_of_commons_sitting':
                    full_url = full_url.replace("/sittings/", "/commons/")
                elif sitting_type == 'house_of_lords_sitting':
                    full_url = full_url.replace("/sittings/", "/lords/")
                elif sitting_type == 'commons_written_answers_sitting':
                    full_url = full_url.replace("/sittings/", "/written_answers/")
                elif sitting_type == 'lords_written_answers_sitting':
                    full_url = full_url.replace("/sittings/", "/written_answers/")
                elif sitting_type == 'westminster_hall_sitting':
                    full_url = full_url.replace("/sittings/", "/westminster_hall/")
                elif sitting_type == 'commons_written_statements_sitting':
                    full_url = full_url.replace("/sittings/", "/written_statements/")
                elif sitting_type == 'house_of_lords_report':
                    full_url = full_url.replace("/sittings/", "/lords_reports/")
                elif sitting_type == 'grand_committee_report_sitting':
                    full_url = full_url.replace("/sittings/", "/grand_committee_report/")

                data = {
                    'slug_status' : slug_status,
                    'url' : historic_hansard_sitting_day['url'],
                    'sitting' : sitting_type,
                    'section' : section_key,
                    'date' : section_structure['date'],
                    'end_column' : section_structure['end_column'],
                    'id' : section_structure['id'],
                    'parent_section_id' : section_structure['parent_section_id'],
                    'sitting_id' : section_structure['sitting_id'],
                    'slug' : section_structure['slug'],
                    'full_url' : full_url,
                    'start_column': section_structure['start_column'],
                    'title' : section_structure['title'],
                    'count' : count

                }
                count = count + 1
                records.append(data)
                if last_count != historic_hansard_sitting_day['count']:
                    scraperwiki.sqlite.save(['full_url'], records, verbose = 0)
                    scraperwiki.sqlite.save_var("last_saved", historic_hansard_sitting_day['count'])
                    last_count = historic_hansard_sitting_day['count']
                    scraperwiki.sqlite.save_var("last_counter", count, verbose = 0)

if last_count != historic_hansard_sitting_day['count']:
    scraperwiki.sqlite.save(['full_url'], records, verbose = 0)
    scraperwiki.sqlite.save_var("last_saved", historic_hansard_sitting_day['count'])
    last_count = historic_hansard_sitting_day['count']
    scraperwiki.sqlite.save_var("last_counter", count, verbose = 0)import scraperwiki
import lxml.html
import urllib
import simplejson


start_count = scraperwiki.sqlite.get_var("last_saved", 1) - 1
last_count = 0
count = scraperwiki.sqlite.get_var("last_counter", 0) + 1

scraperwiki.sqlite.attach( 'historic_hansard_sitting_days' )
historic_hansard_sitting_days = scraperwiki.sqlite.select("* from historic_hansard_sitting_days.swdata where count > " + str(start_count) + " order by count")
records = []

# historic_hansard_sitting_days = [{'url':'http://hansard.millbanksystems.com/sittings/1978/oct/24', 'count':1}]

for historic_hansard_sitting_day in historic_hansard_sitting_days:
    sitting_days_path = historic_hansard_sitting_day['url'] + '.js'
    sitting_days_list = simplejson.load(urllib.urlopen(sitting_days_path))    
    for sittings in sitting_days_list:
        for sitting_type in sittings.keys():
            for section in sittings[sitting_type]['top_level_sections']:
                section_key = section.keys()[0]
                section_structure = section[section_key]
                # check for blank or bogus slugs, starting with "-"?
                if section_structure['slug'] == '-':
                    slug_status = 'leading dash'
                elif section_structure['slug'] == '':
                    slug_status = 'blank'
                else:
                    slug_status = 'ok'

                full_url = historic_hansard_sitting_day['url'] + "/" + section_structure['slug']
                full_url = full_url.replace("/1/", "/01/").replace("/2/", "/02/").replace("/3/", "/03/").replace("/4/", "/04/").replace("/5/", "/05/").replace("/6/", "/06/").replace("/7/", "/07/").replace("/8/", "/08/").replace("/9/", "/09/")

                if sitting_type == 'house_of_commons_sitting':
                    full_url = full_url.replace("/sittings/", "/commons/")
                elif sitting_type == 'house_of_lords_sitting':
                    full_url = full_url.replace("/sittings/", "/lords/")
                elif sitting_type == 'commons_written_answers_sitting':
                    full_url = full_url.replace("/sittings/", "/written_answers/")
                elif sitting_type == 'lords_written_answers_sitting':
                    full_url = full_url.replace("/sittings/", "/written_answers/")
                elif sitting_type == 'westminster_hall_sitting':
                    full_url = full_url.replace("/sittings/", "/westminster_hall/")
                elif sitting_type == 'commons_written_statements_sitting':
                    full_url = full_url.replace("/sittings/", "/written_statements/")
                elif sitting_type == 'house_of_lords_report':
                    full_url = full_url.replace("/sittings/", "/lords_reports/")
                elif sitting_type == 'grand_committee_report_sitting':
                    full_url = full_url.replace("/sittings/", "/grand_committee_report/")

                data = {
                    'slug_status' : slug_status,
                    'url' : historic_hansard_sitting_day['url'],
                    'sitting' : sitting_type,
                    'section' : section_key,
                    'date' : section_structure['date'],
                    'end_column' : section_structure['end_column'],
                    'id' : section_structure['id'],
                    'parent_section_id' : section_structure['parent_section_id'],
                    'sitting_id' : section_structure['sitting_id'],
                    'slug' : section_structure['slug'],
                    'full_url' : full_url,
                    'start_column': section_structure['start_column'],
                    'title' : section_structure['title'],
                    'count' : count

                }
                count = count + 1
                records.append(data)
                if last_count != historic_hansard_sitting_day['count']:
                    scraperwiki.sqlite.save(['full_url'], records, verbose = 0)
                    scraperwiki.sqlite.save_var("last_saved", historic_hansard_sitting_day['count'])
                    last_count = historic_hansard_sitting_day['count']
                    scraperwiki.sqlite.save_var("last_counter", count, verbose = 0)

if last_count != historic_hansard_sitting_day['count']:
    scraperwiki.sqlite.save(['full_url'], records, verbose = 0)
    scraperwiki.sqlite.save_var("last_saved", historic_hansard_sitting_day['count'])
    last_count = historic_hansard_sitting_day['count']
    scraperwiki.sqlite.save_var("last_counter", count, verbose = 0)