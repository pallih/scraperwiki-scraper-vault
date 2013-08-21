import scraperwiki
import lxml.html
import json

BASE_URL = "http://www.tdcj.state.tx.us/stat/"

MTURK_JSON_URL = "http://static.texastribune.org.s3.amazonaws.com/data/tdcj/mturk_death_row_info_by_tdcj_no_2011_08_31.json"
MTURK_DATA = json.loads(scraperwiki.scrape(MTURK_JSON_URL))
MIN_SUMMARY_LENGTH = 10

def get_best_mturk_data(tdcj_no):
    tdcj_no = tdcj_no.strip()
    if not tdcj_no in MTURK_DATA:
        return {}
    mturk_data = MTURK_DATA[tdcj_no]
    if len(mturk_data) < 2:
        return mturk_data[0]
    if (len(mturk_data[0]['summary']) < MIN_SUMMARY_LENGTH and
        len(mturk_data[1]['summary']) > len(mturk_data[0]['summary'])):
        return mturk_data[1]
    return mturk_data[0]

def merge_mturk_data(data):
    """
    Merge in info from prisoner images posted on Mechanical Turk.
    Each image was posted twice, so try to use the best result.
    """
    mturk_data = get_best_mturk_data(data['tdcj_no'])
    for key in mturk_data:
        assert key in data
        data[key] = mturk_data[key]

def new_line_replace(entry):
    return entry.strip()

def scrape_statement(href):
    print href
    # Only use the last part of the HREF
    if '/' in href:
        href = href[href.rfind('/')+1:]
        print '->', href
    # nostatement.html is a special case
    if href in ("nostatement.htm", "nostatement.html"):
        return "This offender declined to make a last statement."
    # Otherwise the statement is in the TD of the third row
    html = scraperwiki.scrape(BASE_URL + href)
    root = lxml.html.fromstring(html)
    return root.cssselect("table.last td")[2].text_content()

def scrape_info(href):
    if href.endswith("#"):
        href = href[:-1]
    if not href.endswith(".jpg"):
        if '/' in href:
            href = href[href.rfind('/')+1:]
        html = scraperwiki.scrape(BASE_URL + href)
        root = lxml.html.fromstring(html)
        top_data = root.cssselect(".basic_info_right")
        bottom_data = root.cssselect(".extended_info_bottom")
        datapass = {
            'occupation': new_line_replace(bottom_data[0].text_content()),
            'priors': new_line_replace(bottom_data[1].text_content()),
            'dob': new_line_replace(top_data[2].text_content()),
            'received_date': new_line_replace(top_data[3].text_content()),
            'offense_date': new_line_replace(top_data[6].text_content()),
            'summary': new_line_replace(bottom_data[2].text_content()),
            'counties': new_line_replace(top_data[8].text_content())
        }
        print datapass
        return datapass
    else:
        datapass = {
            'occupation': "image",
            'priors': "image",
            'dob': "image",
            'received_date': "image",
            'offense_date': "image",
            'summary': "image",
            'counties': "image"
        }
        print "Image!"
        return datapass

def scrape_executions():
    html = scraperwiki.scrape(BASE_URL + "executedoffenders.htm")
    #print html
    root = lxml.html.fromstring(html)
    for tr in root.cssselect("#start_main_content table tr"):
        tds = tr.cssselect("td")
        if not tds:
            continue
        data = {
            'execution_no': tds[0].text_content(),
            'first_name': tds[4].text_content(),
            'last_name': tds[3].text_content(),
            'tdcj_no': tds[5].text_content(),
            'age': tds[6].text_content(),
            'execution_date': tds[7].text_content(),
            'race': tds[8].text_content(),
            'county': tds[9].text_content(),
        }
        
        # Don't retrieve the statement/info again
        saved_data = scraperwiki.sqlite.select("* from swdata where execution_no = ?", data['execution_no'])
        if saved_data:
            merged_data = saved_data[0]
            if merged_data['summary'] == 'image' or not (merged_data['summary'] or '').strip():
                merge_mturk_data(merged_data)
                print 'merged', merged_data
                scraperwiki.sqlite.save(unique_keys=['execution_no'], data=merged_data)
            continue

        links_information = tds[1].cssselect("a")
        if links_information:
            href_info = links_information[0].get("href")
            data.update(scrape_info(href_info))
        links_statement = tds[2].cssselect("a")
        if links_statement:
            href_state = links_statement[0].get("href")
            data['statement'] = scrape_statement(href_state)
        merge_mturk_data(data)
        print data
        scraperwiki.sqlite.save(unique_keys=['execution_no'], data=data)

scrape_executions()
