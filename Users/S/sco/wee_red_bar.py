import scraperwiki
import itertools
import lxml.html
import urllib2

def extract_event(date_cell, title_cell):
    '''
    Returns and event dict containing event information as strings extracted
    from the given date_cell and title_cell.
    '''
    
    def title_text(xpath_expr):
        '''
        Returns the text content of the first element returned by the given
        XPath expression relative to title_cell. Returns empty if the
        Xpath expression returns an empty list.
        '''
        if len(title_cell.xpath(xpath_expr)) == 0:
            return  ''
        return title_cell.xpath(xpath_expr)[0].text_content()
    
    time_and_price = title_text('./h3')
    time = None
    price = None
    print time_and_price
    if time_and_price is not None:
        if u'\u2022' in time_and_price:
            time, price = (data.strip() for data in time_and_price.split(u'\u2022'))
        else:
            time = time_and_price

    return {
        'date': date_cell.text_content(),
        'name': title_text('./h1'),
        'time': time,
        'price': price
    }

def first_elem_is_whitespace(li):
    '''
    Returns True if the first element of the given list is whitespace; False
    otherwise. Used to filter empty rows from the scraped table.
    '''
    return li[0].text_content().isspace()

def get_events():
    '''
    Returns a list of event dicts scraped from the Wee Red Bar's web site.
    '''
    markup = urllib2.urlopen('http://www.weeredbar.co.uk/listings.htm').read()
    doc = lxml.html.fromstring(markup)
    data_columns = zip(doc.cssselect('#left_column'), doc.cssselect('#main_column'))
    data_rows = itertools.ifilterfalse(first_elem_is_whitespace, data_columns)
    return itertools.starmap(extract_event, data_rows)

for event in get_events():
    scraperwiki.sqlite.save(unique_keys=['date', 'time'], data=event)
import scraperwiki
import itertools
import lxml.html
import urllib2

def extract_event(date_cell, title_cell):
    '''
    Returns and event dict containing event information as strings extracted
    from the given date_cell and title_cell.
    '''
    
    def title_text(xpath_expr):
        '''
        Returns the text content of the first element returned by the given
        XPath expression relative to title_cell. Returns empty if the
        Xpath expression returns an empty list.
        '''
        if len(title_cell.xpath(xpath_expr)) == 0:
            return  ''
        return title_cell.xpath(xpath_expr)[0].text_content()
    
    time_and_price = title_text('./h3')
    time = None
    price = None
    print time_and_price
    if time_and_price is not None:
        if u'\u2022' in time_and_price:
            time, price = (data.strip() for data in time_and_price.split(u'\u2022'))
        else:
            time = time_and_price

    return {
        'date': date_cell.text_content(),
        'name': title_text('./h1'),
        'time': time,
        'price': price
    }

def first_elem_is_whitespace(li):
    '''
    Returns True if the first element of the given list is whitespace; False
    otherwise. Used to filter empty rows from the scraped table.
    '''
    return li[0].text_content().isspace()

def get_events():
    '''
    Returns a list of event dicts scraped from the Wee Red Bar's web site.
    '''
    markup = urllib2.urlopen('http://www.weeredbar.co.uk/listings.htm').read()
    doc = lxml.html.fromstring(markup)
    data_columns = zip(doc.cssselect('#left_column'), doc.cssselect('#main_column'))
    data_rows = itertools.ifilterfalse(first_elem_is_whitespace, data_columns)
    return itertools.starmap(extract_event, data_rows)

for event in get_events():
    scraperwiki.sqlite.save(unique_keys=['date', 'time'], data=event)
