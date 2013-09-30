""" Scrapes all objects contained within the NHS Data Dictionary () into a relational database.

Further information to follow. This isn't going to happen overnight.
"""

import scraperwiki



def get_all_index_urls()

    # Using class leftmenuglossary on <ul> - return a dict A: <A-url>, or just a list? (Is what letter they start with at all important?)
    return 0

def get_object_urls_by_page()

    # Takes in an index URL from the list/dict returned by get_all_index_URLs()
    # Returns a list of URLs for the individual objects that are listed on that page
    # May need to split this list up by Item Type at this point.  
    # I.e. return a dict 'Supporting Information':[list of URLs for SI things]...
    
    # It might be possible to do this step recursively: if this fn takes in the full list of index page URLs, 
    # it could return <results for p0> + get_object_urls_by_page(list[1:])
    return 0

def parse_DD_object_page()

    # Might need separate functions for classes, elements, attributes, etc
    # Need to work out data structure before I can go further with this, so I know how to scrape the bits of this page into different variables

def main()

    # Seed URL from which everything /should/ be able to follow automatically.
    # Should this be global?
    seed_DD_url = 'http://www.datadictionary.nhs.uk/items_index_0_child.asp'

    index_urls = get_all_index_urls(seed_DD_url)

    # I feel like there should be a neat recursive way to do this... 
    for page in index_urls:
        object_urls = get_object_urls_by_page(page)

    # Now split up what I've got so I have one variable containing URLs for all Classes, one variable for URLs for all Elements, etc
    
    for dd_object in list_of_classes:
        # Do the proper scraping bit, to get things into correct places, and add to datastore
        # I think writing to datastore periodically as I get a chunk of information for one object, is likely to be better than 
        # trying to scrape the whole site into python variables then write to datastore altogether at the end.
        # Could even explore multithreading: once I've got the URLs for classes, elements, attributes etc, I could set each of those things going simulatenously?


""" Scrapes all objects contained within the NHS Data Dictionary () into a relational database.

Further information to follow. This isn't going to happen overnight.
"""

import scraperwiki



def get_all_index_urls()

    # Using class leftmenuglossary on <ul> - return a dict A: <A-url>, or just a list? (Is what letter they start with at all important?)
    return 0

def get_object_urls_by_page()

    # Takes in an index URL from the list/dict returned by get_all_index_URLs()
    # Returns a list of URLs for the individual objects that are listed on that page
    # May need to split this list up by Item Type at this point.  
    # I.e. return a dict 'Supporting Information':[list of URLs for SI things]...
    
    # It might be possible to do this step recursively: if this fn takes in the full list of index page URLs, 
    # it could return <results for p0> + get_object_urls_by_page(list[1:])
    return 0

def parse_DD_object_page()

    # Might need separate functions for classes, elements, attributes, etc
    # Need to work out data structure before I can go further with this, so I know how to scrape the bits of this page into different variables

def main()

    # Seed URL from which everything /should/ be able to follow automatically.
    # Should this be global?
    seed_DD_url = 'http://www.datadictionary.nhs.uk/items_index_0_child.asp'

    index_urls = get_all_index_urls(seed_DD_url)

    # I feel like there should be a neat recursive way to do this... 
    for page in index_urls:
        object_urls = get_object_urls_by_page(page)

    # Now split up what I've got so I have one variable containing URLs for all Classes, one variable for URLs for all Elements, etc
    
    for dd_object in list_of_classes:
        # Do the proper scraping bit, to get things into correct places, and add to datastore
        # I think writing to datastore periodically as I get a chunk of information for one object, is likely to be better than 
        # trying to scrape the whole site into python variables then write to datastore altogether at the end.
        # Could even explore multithreading: once I've got the URLs for classes, elements, attributes etc, I could set each of those things going simulatenously?


