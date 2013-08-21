import scraperwiki
from BeautifulSoup import BeautifulSoup
import lxml.html
import mechanize
import datetime
import re

# Usage:
# caps = scraperwiki.utils.swimport('caps')
# search_form_url = 'http://www.planning.cityoflondon.gov.uk/tdc/DcApplication/application_searchform.aspx'
# scraper = caps.CapsScraper(search_form_url)
# scraper.run()


# dates
today = datetime.date.today()
weekago = today - datetime.timedelta(days=14)

class CapsScraper(object):
    def __init__(self, search_form_url):
        self.br = mechanize.Browser()
        self.search_form_url = search_form_url

    def run(self):
        for table_name in ['Received', 'Valid', 'Committee']:
            search_results = self.fill_in_search_form(table_name)
            self.scrape_search_result_table(search_results, table_name)
        
    def fill_in_search_form(self, table_name):
        self.br.open(self.search_form_url)
        self.br.select_form(name="searchform")
        self.br["srchDate%sStart" % table_name] = weekago.strftime('%d/%m/%Y')
        self.br["srchDate%sEnd" % table_name] = today.strftime('%d/%m/%Y')
        search_results = self.br.submit()
        assert self.br.viewing_html()
        return search_results

    def scrape_search_result_table(self, search_results, table_name):
        print 'Scraping table "%s"' % table_name
        page = search_results.read()
        bs = BeautifulSoup(page)
        rows_found = 0
        form_content = bs.find('td', {'class':'cFormContent'})
        if form_content:
            table_title = form_content.contents[0].replace('\r\n', '')
            table = bs.find('table', {'class':'cResultsForm'})
            for row in table.findAll('tr'):
                row_data = {}
                if len(row.findAll('th')) > 1:
                    titles = [heading.string for heading in row.findAll('th')]
                    assert titles[1] == 'Application Ref.'
                else:
                    assert len(row.contents) == len(titles), row.contents
                    for i, cell in enumerate(row.contents):
                        if cell.name == 'th' or cell.button:
                            continue
                        elif cell.name == 'td':
                            val = cell.string
                            if 'Date' in titles[i]:
                                val = datetime.datetime.strptime(val, '%d/%m/%Y')
                            row_data[titles[i]] = val
                    details_page_url = row.find('a')['href']
                    details, buttons = self.scrape_details_page(details_page_url)
                    row_data.update(details)
                    property_details_url = buttons.get('PropertyDetails')
                    if property_details_url:
                        property_details, property_buttons = self.scrape_details_page(property_details_url)
                        details.update(property_details)
                    postcode = scraperwiki.geo.extract_gb_postcode(row_data['Address'])
                    latlng = scraperwiki.geo.gb_postcode_to_latlng(postcode)
                    scraperwiki.datastore.save(unique_keys=['Application Ref.'], data=row_data, date=row_data['Date Received'], latlng=latlng)
                    rows_found += 1
        print 'Table "%s" provided %i results' % (table_name, rows_found)
        #TODO go to other pages of results

    def scrape_details_page(self, details_page_url):
        details = {}
        buttons = {}
        res = self.br.open(details_page_url)
        html = res.read()
        html = lxml.html.make_links_absolute(html, details_page_url)
        assert self.br.viewing_html()
        bs = BeautifulSoup(html)
        def get_tab_label(tab_name, field_name):
            return '%s - %s' % (tab_name, field_name.rstrip(':'))
        for class_ in ('cTabContentVis', 'cTabContentHidden'):
            for tab in bs.findAll('table', {'class':class_}):
                tab_name = tab['summary']
                if not tab_name:
                    bold = tab.find('b')
                    if bold:
                        tab_name = bold.string
                    else:
                        tab_name = tab['id']
                sub_table = tab.find('table')
                if sub_table:
                    tab = sub_table
                for row in tab.findAll('tr'):
                    for label in row.findAll('label'):
                        field_id = label['for']
                        if label.string:
                            key = get_tab_label(tab_name, label.string)
                            value_tag = row.find('input', id=field_id)
                            if value_tag:
                                value = value_tag['value']
                            else:
                                value_tag = row.find('textarea', id=field_id)
                                value = value_tag.string
                            details[key] = value
                    if not row.find('label'):
                        field_name = None
                        value = None
                        for td in row.findAll('td'):
                            if td.get('class') == 'cTdFieldName':
                                field_name = td.string
                            elif td.get('class') == 'cFormContentExtra':
                                # complicated map thing
                                break
                            else:
                                value_tag = td.find('input')
                                if value_tag and value_tag.get('class') != 'cButton':
                                    assert not value, 'Not sure how to handle multi values'
                                    value = value_tag['value']
                                else:
                                    value_tag = td.find('textarea')
                                    if value_tag:
                                        assert not value, 'Not sure how to handle multi values'
                                        value = value_tag.string
                        if field_name and value:
                            key = get_tab_label(tab_name, field_name)
                            details[key] = value
                    for link in row.findAll('a'):
                        if link.has_key('href'):
                            link_id = link.get('id')
                            if link_id:
                                buttons[link_id.lstrip('A_btn')] = link['href']
        return details, buttons

#print scraper.scrape_details_page('http://www.planning.cityoflondon.gov.uk/tdc/DcApplication/application_detailview.aspx?caseno=L8S8GQFH01100')
#print scraper.scrape_details_page('http://www.planning.cityoflondon.gov.uk/propdb/property/property_detailview.aspx?module=P3&pkeyval=ILTQQHFHN1000&dccaseno=L8S8GQFH01100&dcrefval=10/00677/MDC')
