import scraperwiki
import lxml.html

BASE_URL = "http://www.tdcj.state.tx.us/stat/"

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
    if href[len(href)-1:] == "#":
        href = href[:len(href)-1]
    img_check = href[len(href)-4:]
    if img_check != ".jpg":
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
        if scraperwiki.sqlite.select("* from swdata where execution_no = ?", data['execution_no']):
            continue

        links_information = tds[1].cssselect("a")
        if links_information:
            href_info = links_information[0].get("href")
            data.update(scrape_info(href_info))
        links_statement = tds[2].cssselect("a")
        if links_statement:
            href_state = links_statement[0].get("href")
            data['statement'] = scrape_statement(href_state)
        print data
        scraperwiki.sqlite.save(unique_keys=['execution_no'], data=data)

scrape_executions()
