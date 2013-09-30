import scraperwiki
from lxml import html

from urllib2 import urlopen, Request, URLError
import re
import string
from lxml.html.soupparser import fromstring

START_URL = "http://gwweb.jica.go.jp/km/ProjectView.nsf/NaviProPj?OpenNavigator"
COUNTRY_URL = "http://gwweb.jica.go.jp/%s/VW02040102?OpenView&ExpandView&RestrictToCategory=%s"
PROJECT_URL = "http://gwweb.jica.go.jp%s&ExpandSection=6"

def clean_script_data(data):
    betterdata = data.lstrip("""
<!--
""")
    betterdata = betterdata.rstrip("""

// -->""")
    
    return betterdata

def cleanup(data):
    # remove linebreaks and annoying characters that will mess up the CSV file
    data = re.sub('"|\n|\r', "", data)
    return data

def get_country_data(name, addr):
    try:
        data = scraperwiki.scrape(COUNTRY_URL % (addr, name))
        # Using BeautifulSoup for better character encoding detection
        print "Trying to get country data..."
        data = data.decode("Shift_JIS", "ignore")
        root = html.fromstring(data)
        print "Got country data..."
        #print data
        # some countries contain no data
        # 3rd table contains the country name until "－"
        # 5th table contains the data if it exists (in a table 4a, i.e. nested within table 4), or else says the document cannot be found.
        
        country_name_table = root.cssselect("table")[2]
        country_name = cleanup(name)
        data_wrapper_table = root.cssselect("table")[4]
        #print (data_wrapper_table.text_content().encode("utf-8", "ignore"))
        # check if there is a table inside the data table... (nb data_wrapper_table will return itself as well)
        try:
            data_table = data_wrapper_table.cssselect("table")[1]
            print "Found data table for country " + country_name
            # headers are in <tr><th>
            # then budget years are in <tr valign="top"><td colspan="7" nowrap>
            # everything else is in <tr>
            data_table_data = data_table.cssselect("table tr")
            for row in data_table_data:
                # discard header and budget year categories
                if ((row.cssselect("tr th")) or (row.cssselect("tr td['colspan']"))):
                    print "ignoring header row"
                else:
                    try:
                        project = {}
                        project['country'] = country_name
                        try:
                            project['date'] = cleanup(row.cssselect("td")[1].cssselect("font")[0].text_content())
                        except IndexError:
                            pass
                        # This should not be protected against IndexError - if this happens, then escape out of this project, as this data is required for everything else...
                        project_name_url = row.cssselect("td")[2].cssselect("font a")[0]
                        project['url'] = cleanup(project_name_url.attrib['href'])
                        project['name'] = cleanup(project_name_url.text_content())
                        try:
                            project['program_name'] = cleanup(row.cssselect("td")[3].cssselect("font")[0].text_content())
                        except IndexError:
                            pass
                        try:
                            project['dept_office'] = cleanup(row.cssselect("td")[4].cssselect("font")[0].text_content())
                        except IndexError:
                            pass
                        try:
                            project['theme'] = cleanup(row.cssselect("td")[5].cssselect("font")[0].text_content())
                        except IndexError:
                            pass
                        
                        data = scraperwiki.scrape(PROJECT_URL % (project['url']))
                        # Using BeautifulSoup for better character encoding detection
                        print "Trying to get project data..."
                        data = data.decode("Shift_JIS", "ignore")
                        root = html.fromstring(data)
                        # need to get table 25
                        project_table = root.cssselect("table")[25]
                        try:
                            project['as_of'] = cleanup(project_table.cssselect("tr")[0].cssselect("td")[3].cssselect("table tr")[0].cssselect("td")[3].text_content())
                        except IndexError:
                            pass
                        try:
                            project['title_en'] = cleanup(project_table.cssselect("tr")[6].cssselect("td")[3].text_content())
                        except IndexError:
                            pass
                        try:
                            project['country_en'] = cleanup(project_table.cssselect("tr")[8].cssselect("td")[3].text_content())
                        except IndexError:
                            pass
                        try:
                            project['proj_type_en'] = cleanup(project_table.cssselect("tr")[10].cssselect("td")[3].text_content())
                        except IndexError:
                            pass
                        try:
                            project['field_en'] = cleanup(project_table.cssselect("tr")[12].cssselect("td")[3].text_content())
                        except IndexError:
                            pass
                        try:
                            project['sector_en'] = cleanup(project_table.cssselect("tr")[14].cssselect("td")[3].text_content())
                        except IndexError:
                            pass
                        try:
                            project['project_site_en'] = cleanup(project_table.cssselect("tr")[16].cssselect("td")[3].text_content())
                        except IndexError:
                            pass
                        # new project table
                        project_table = root.cssselect("table")[27]
                        try:
                            project['start_date'] = cleanup(project_table.cssselect("tr")[0].cssselect("td")[3].text_content())
                        except IndexError:
                            pass
                        try:
                            project['end_date'] = cleanup(project_table.cssselect("tr")[0].cssselect("td")[5].text_content())
                        except IndexError:
                            pass
                        project_table = root.cssselect("table")[28]
                        try:
                            project['implementing_org'] = cleanup(project_table.cssselect("tr")[0].cssselect("td")[3].text_content())
                        except IndexError:
                            pass
                        scraperwiki.sqlite.save(unique_keys=['url'],
                                data=project)
                    except IndexError:
                        pass
        except IndexError:
            print "Found no data for country " + country_name
            pass
    except URLError, e:
        pass

def get_line_data(line):
    if re.match('^Country_Tbl.+\(', line):
        data = re.match('^Country_Tbl.+\("(.+)","(.+)","(.+)"', line)
        country_name = data.group(1)
        country_addr = data.group(2)
        country_code = data.group(3)

        country_data = {
            'country_name': country_name.encode('utf-8'),
            'country_code': country_code.encode('utf-8'),
            'country_addr': country_addr.encode('utf-8')
        }
        print country_name
        print country_code
        return country_data
    else:
        return False

def get_countries():
    data = scraperwiki.scrape(START_URL)
    # Use beautifulsoup for better character encoding detection
    root = fromstring(data)
    script = root.cssselect("script")[3]
    script_data = clean_script_data(script.text_content())
    for line in script_data.splitlines():
        count = 0
        get_data = get_line_data(line)
        if (get_line_data(line)):
            # for each country...
            print "Going for country data..."
            get_country_data(get_data['country_name'], get_data['country_addr'])
        count = count + 1

get_countries()
import scraperwiki
from lxml import html

from urllib2 import urlopen, Request, URLError
import re
import string
from lxml.html.soupparser import fromstring

START_URL = "http://gwweb.jica.go.jp/km/ProjectView.nsf/NaviProPj?OpenNavigator"
COUNTRY_URL = "http://gwweb.jica.go.jp/%s/VW02040102?OpenView&ExpandView&RestrictToCategory=%s"
PROJECT_URL = "http://gwweb.jica.go.jp%s&ExpandSection=6"

def clean_script_data(data):
    betterdata = data.lstrip("""
<!--
""")
    betterdata = betterdata.rstrip("""

// -->""")
    
    return betterdata

def cleanup(data):
    # remove linebreaks and annoying characters that will mess up the CSV file
    data = re.sub('"|\n|\r', "", data)
    return data

def get_country_data(name, addr):
    try:
        data = scraperwiki.scrape(COUNTRY_URL % (addr, name))
        # Using BeautifulSoup for better character encoding detection
        print "Trying to get country data..."
        data = data.decode("Shift_JIS", "ignore")
        root = html.fromstring(data)
        print "Got country data..."
        #print data
        # some countries contain no data
        # 3rd table contains the country name until "－"
        # 5th table contains the data if it exists (in a table 4a, i.e. nested within table 4), or else says the document cannot be found.
        
        country_name_table = root.cssselect("table")[2]
        country_name = cleanup(name)
        data_wrapper_table = root.cssselect("table")[4]
        #print (data_wrapper_table.text_content().encode("utf-8", "ignore"))
        # check if there is a table inside the data table... (nb data_wrapper_table will return itself as well)
        try:
            data_table = data_wrapper_table.cssselect("table")[1]
            print "Found data table for country " + country_name
            # headers are in <tr><th>
            # then budget years are in <tr valign="top"><td colspan="7" nowrap>
            # everything else is in <tr>
            data_table_data = data_table.cssselect("table tr")
            for row in data_table_data:
                # discard header and budget year categories
                if ((row.cssselect("tr th")) or (row.cssselect("tr td['colspan']"))):
                    print "ignoring header row"
                else:
                    try:
                        project = {}
                        project['country'] = country_name
                        try:
                            project['date'] = cleanup(row.cssselect("td")[1].cssselect("font")[0].text_content())
                        except IndexError:
                            pass
                        # This should not be protected against IndexError - if this happens, then escape out of this project, as this data is required for everything else...
                        project_name_url = row.cssselect("td")[2].cssselect("font a")[0]
                        project['url'] = cleanup(project_name_url.attrib['href'])
                        project['name'] = cleanup(project_name_url.text_content())
                        try:
                            project['program_name'] = cleanup(row.cssselect("td")[3].cssselect("font")[0].text_content())
                        except IndexError:
                            pass
                        try:
                            project['dept_office'] = cleanup(row.cssselect("td")[4].cssselect("font")[0].text_content())
                        except IndexError:
                            pass
                        try:
                            project['theme'] = cleanup(row.cssselect("td")[5].cssselect("font")[0].text_content())
                        except IndexError:
                            pass
                        
                        data = scraperwiki.scrape(PROJECT_URL % (project['url']))
                        # Using BeautifulSoup for better character encoding detection
                        print "Trying to get project data..."
                        data = data.decode("Shift_JIS", "ignore")
                        root = html.fromstring(data)
                        # need to get table 25
                        project_table = root.cssselect("table")[25]
                        try:
                            project['as_of'] = cleanup(project_table.cssselect("tr")[0].cssselect("td")[3].cssselect("table tr")[0].cssselect("td")[3].text_content())
                        except IndexError:
                            pass
                        try:
                            project['title_en'] = cleanup(project_table.cssselect("tr")[6].cssselect("td")[3].text_content())
                        except IndexError:
                            pass
                        try:
                            project['country_en'] = cleanup(project_table.cssselect("tr")[8].cssselect("td")[3].text_content())
                        except IndexError:
                            pass
                        try:
                            project['proj_type_en'] = cleanup(project_table.cssselect("tr")[10].cssselect("td")[3].text_content())
                        except IndexError:
                            pass
                        try:
                            project['field_en'] = cleanup(project_table.cssselect("tr")[12].cssselect("td")[3].text_content())
                        except IndexError:
                            pass
                        try:
                            project['sector_en'] = cleanup(project_table.cssselect("tr")[14].cssselect("td")[3].text_content())
                        except IndexError:
                            pass
                        try:
                            project['project_site_en'] = cleanup(project_table.cssselect("tr")[16].cssselect("td")[3].text_content())
                        except IndexError:
                            pass
                        # new project table
                        project_table = root.cssselect("table")[27]
                        try:
                            project['start_date'] = cleanup(project_table.cssselect("tr")[0].cssselect("td")[3].text_content())
                        except IndexError:
                            pass
                        try:
                            project['end_date'] = cleanup(project_table.cssselect("tr")[0].cssselect("td")[5].text_content())
                        except IndexError:
                            pass
                        project_table = root.cssselect("table")[28]
                        try:
                            project['implementing_org'] = cleanup(project_table.cssselect("tr")[0].cssselect("td")[3].text_content())
                        except IndexError:
                            pass
                        scraperwiki.sqlite.save(unique_keys=['url'],
                                data=project)
                    except IndexError:
                        pass
        except IndexError:
            print "Found no data for country " + country_name
            pass
    except URLError, e:
        pass

def get_line_data(line):
    if re.match('^Country_Tbl.+\(', line):
        data = re.match('^Country_Tbl.+\("(.+)","(.+)","(.+)"', line)
        country_name = data.group(1)
        country_addr = data.group(2)
        country_code = data.group(3)

        country_data = {
            'country_name': country_name.encode('utf-8'),
            'country_code': country_code.encode('utf-8'),
            'country_addr': country_addr.encode('utf-8')
        }
        print country_name
        print country_code
        return country_data
    else:
        return False

def get_countries():
    data = scraperwiki.scrape(START_URL)
    # Use beautifulsoup for better character encoding detection
    root = fromstring(data)
    script = root.cssselect("script")[3]
    script_data = clean_script_data(script.text_content())
    for line in script_data.splitlines():
        count = 0
        get_data = get_line_data(line)
        if (get_line_data(line)):
            # for each country...
            print "Going for country data..."
            get_country_data(get_data['country_name'], get_data['country_addr'])
        count = count + 1

get_countries()
