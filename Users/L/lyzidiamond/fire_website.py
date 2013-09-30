import scraperwiki
import lxml.html
import time

html = scraperwiki.scrape("http://thefire.org/cases/all")
root = lxml.html.fromstring(html)

months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
days = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31']
years = ['1999', '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015']

for el in root.cssselect("div.post a"):
    case_name = el.text
    case_name_tuple = case_name.partition(":")
    # sets school_name
    if 'College' in case_name_tuple[0]:
        school_name = case_name_tuple[0]
    elif 'University' in case_name_tuple[0]:
        school_name = case_name_tuple[0]
    else:
        school_name = ""
    # finds school_location
    school_location = ''
    if school_name != "":
        location_search_term = school_name.replace(' ', '+')
        location_search_url = 'http://thefire.org/spotlight/search/?schoolname=' + location_search_term
        schoolHtml = scraperwiki.scrape(location_search_url)
        schoolRoot = lxml.html.fromstring(schoolHtml)
        for element in schoolRoot.cssselect("div.simplePageContainer a"):
            if element.text == school_name:
                locationUrl_append = element.attrib['href']
                locationUrl = "http://thefire.org" + locationUrl_append
                locationHtml = scraperwiki.scrape(locationUrl)
                locationRoot = lxml.html.fromstring(locationHtml)
                for element1 in locationRoot.cssselect("div.simplePagerContainer p"):
                    print element1
#                    if locationText in locationString:
#                        location_tuple = locationString.partition(":")
#                        school_location.append(location_tuple[0])
    # sets case_url
    case_url_append = el.attrib['href']
    case_url = "http://thefire.org" + case_url_append
    # sets case id
    case_url_append_tuple = case_url_append.partition("/case/")
    case_id_tuple = (case_url_append_tuple[2]).partition(".")
    case_id = case_id_tuple[0]
    # gets case dates
    html2 = scraperwiki.scrape(case_url)
    root2 = lxml.html.fromstring(html2)
    date_list = []
    for el in root2.cssselect("div.post li a"):
        punc_date = el.tail
        punc_date_words = punc_date.split()
        for num in range(len(punc_date_words)):
            if punc_date_words[num] in months:
                date_month = punc_date_words[num]
                date_day = punc_date_words[num + 1].strip(',')
                if date_day in days:
                    date_year = punc_date_words[num + 2].strip(':')
                    if date_year in years:
                        pulled_date_string = date_month + " " + date_day + ", " + date_year
                        date_list.append(pulled_date_string)
    # converts to ISO dates
    iso_date_list = []
    for date1 in date_list:
        parsed_date = time.strptime(date1, "%B %d, %Y")
        str_parsed_year = str(parsed_date[0])
        str_parsed_month = str(parsed_date[1])
        str_parsed_day = str(parsed_date[2])
        iso_date = str_parsed_year + '-' + str_parsed_month + '-' + str_parsed_day
        iso_date_list.append(iso_date)
    # finds earliest date and converts back to Month Day, Year format
    if iso_date_list == []:
        date_string = ""
    else:
        iso_date_list_sorted = sorted(iso_date_list)
        case_date = iso_date_list_sorted[0]
        case_date_tuple = case_date.partition("-")
        year = case_date_tuple[0]
        month_and_day = case_date_tuple[2].partition("-")
        month = month_and_day[0]
        day = month_and_day[2]
        if month == '1':
            month_string = 'January'
        elif month == '2':
            month_string = 'February'
        elif month == '3':
            month_string = 'March'
        elif month == '4':
            month_string = 'April'
        elif month == '5':
            month_string = 'May'
        elif month == '6':
            month_string = 'June'
        elif month == '7':
            month_string = 'July'
        elif month == '8':
            month_string = 'August'
        elif month == '9':
            month_string = 'September'
        elif month == '10':
            month_string = 'October'
        elif month == '11':
            month_string = 'November'
        elif month == '12':
            month_string = 'December'
        date_string = month_string + " " + str(day) + ", " + str(year)
    
    data = {
        'case_id' : case_id_tuple[0],
        'school' : school_name,
        'school_location' : school_location,
        'case_name' : case_name_tuple[2],
        'case_url' : case_url,
        'case_date_iso' : case_date,
        'case_date' : date_string
    }
    scraperwiki.sqlite.save(unique_keys=['case_id'], data=data)import scraperwiki
import lxml.html
import time

html = scraperwiki.scrape("http://thefire.org/cases/all")
root = lxml.html.fromstring(html)

months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
days = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31']
years = ['1999', '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015']

for el in root.cssselect("div.post a"):
    case_name = el.text
    case_name_tuple = case_name.partition(":")
    # sets school_name
    if 'College' in case_name_tuple[0]:
        school_name = case_name_tuple[0]
    elif 'University' in case_name_tuple[0]:
        school_name = case_name_tuple[0]
    else:
        school_name = ""
    # finds school_location
    school_location = ''
    if school_name != "":
        location_search_term = school_name.replace(' ', '+')
        location_search_url = 'http://thefire.org/spotlight/search/?schoolname=' + location_search_term
        schoolHtml = scraperwiki.scrape(location_search_url)
        schoolRoot = lxml.html.fromstring(schoolHtml)
        for element in schoolRoot.cssselect("div.simplePageContainer a"):
            if element.text == school_name:
                locationUrl_append = element.attrib['href']
                locationUrl = "http://thefire.org" + locationUrl_append
                locationHtml = scraperwiki.scrape(locationUrl)
                locationRoot = lxml.html.fromstring(locationHtml)
                for element1 in locationRoot.cssselect("div.simplePagerContainer p"):
                    print element1
#                    if locationText in locationString:
#                        location_tuple = locationString.partition(":")
#                        school_location.append(location_tuple[0])
    # sets case_url
    case_url_append = el.attrib['href']
    case_url = "http://thefire.org" + case_url_append
    # sets case id
    case_url_append_tuple = case_url_append.partition("/case/")
    case_id_tuple = (case_url_append_tuple[2]).partition(".")
    case_id = case_id_tuple[0]
    # gets case dates
    html2 = scraperwiki.scrape(case_url)
    root2 = lxml.html.fromstring(html2)
    date_list = []
    for el in root2.cssselect("div.post li a"):
        punc_date = el.tail
        punc_date_words = punc_date.split()
        for num in range(len(punc_date_words)):
            if punc_date_words[num] in months:
                date_month = punc_date_words[num]
                date_day = punc_date_words[num + 1].strip(',')
                if date_day in days:
                    date_year = punc_date_words[num + 2].strip(':')
                    if date_year in years:
                        pulled_date_string = date_month + " " + date_day + ", " + date_year
                        date_list.append(pulled_date_string)
    # converts to ISO dates
    iso_date_list = []
    for date1 in date_list:
        parsed_date = time.strptime(date1, "%B %d, %Y")
        str_parsed_year = str(parsed_date[0])
        str_parsed_month = str(parsed_date[1])
        str_parsed_day = str(parsed_date[2])
        iso_date = str_parsed_year + '-' + str_parsed_month + '-' + str_parsed_day
        iso_date_list.append(iso_date)
    # finds earliest date and converts back to Month Day, Year format
    if iso_date_list == []:
        date_string = ""
    else:
        iso_date_list_sorted = sorted(iso_date_list)
        case_date = iso_date_list_sorted[0]
        case_date_tuple = case_date.partition("-")
        year = case_date_tuple[0]
        month_and_day = case_date_tuple[2].partition("-")
        month = month_and_day[0]
        day = month_and_day[2]
        if month == '1':
            month_string = 'January'
        elif month == '2':
            month_string = 'February'
        elif month == '3':
            month_string = 'March'
        elif month == '4':
            month_string = 'April'
        elif month == '5':
            month_string = 'May'
        elif month == '6':
            month_string = 'June'
        elif month == '7':
            month_string = 'July'
        elif month == '8':
            month_string = 'August'
        elif month == '9':
            month_string = 'September'
        elif month == '10':
            month_string = 'October'
        elif month == '11':
            month_string = 'November'
        elif month == '12':
            month_string = 'December'
        date_string = month_string + " " + str(day) + ", " + str(year)
    
    data = {
        'case_id' : case_id_tuple[0],
        'school' : school_name,
        'school_location' : school_location,
        'case_name' : case_name_tuple[2],
        'case_url' : case_url,
        'case_date_iso' : case_date,
        'case_date' : date_string
    }
    scraperwiki.sqlite.save(unique_keys=['case_id'], data=data)