# For scrape Haodoo (http://www.haodoo.net)
import scraperwiki
import simplejson
import lxml.html
import sys
from urlparse import parse_qs
from urllib import urlencode
import traceback

base_url = 'http://www.haodoo.net'

def parse_books_from_html( html ):
    """
    Parse the url of each book from the book list page.
    The book's title and url will be stored in sqlite database provided by scraperwiki.
    """
    root = lxml.html.fromstring(html)
    for a in root.cssselect("a"):
        href = a.attrib['href']
        if href.startswith( '?' ):
            s = href[1:]
        else:
            s = href
        book_title = a.text_content()

        d = parse_qs( s )
        if d.has_key('M') and d['M'][0] in ('book', 'Share'):
            if d.has_key('P'):
                book_id = d['P'][0]
                book = { 'id': book_id, 'url': base_url + href, 'title': book_title }
                scraperwiki.sqlite.save(unique_keys=["id"], data=book, table_name="bookpages" )

def find_volume_id( onclick ):
    """
    Find book id from the given string.  The string actually is javascript function.
    """
    # find which kind of quote, ' or "
    quote = "'"
    start = onclick.find( quote )
    if start==-1:
        quote = '"'

    id = ''
    start = onclick.find( quote )
    end = onclick.rfind( quote )
    if start!=-1 and end!=-1:
        id = onclick[ start+1:end ]

    return id

def convert_to_dl_url( id, ext ):
    """
    According book_id and book type to generate download url.
    """
    result = base_url + "/?" + urlencode( {
        "M": "d",
        "P": id + "." + ext } )
    #print( "__convert_to_dl_url()=%s" % result )
    return result

def extract_set_title( html ):
    start_pos = html.find( 'SetTitle("' )
    if start_pos == -1:
        return ("", "")

    start_quote = html.find( '"', start_pos )
    if start_quote == -1:
        return ("", "")

    end_quote = html.find( '"', start_quote+1 )
    if end_quote == -1:
        return ("", "")

    set_title = html[ start_quote+1: end_quote-1 ]
    set_title = set_title.replace( '《', ',' )
    r = set_title.split(',')
    if len(r)!=2:
        return ("", "" )
    return r

def analysis_book_html_and_save( book, html ):
    doc = lxml.html.fromstring( html )
    volume_author, volume_name = extract_set_title( html )

    pdb_download_elements = doc.xpath( '//a[contains(@href, "pdb")]' )
    if len(pdb_download_elements):
        # old style page, only readonline and download link.
        save_item = pdb_download_elements[0]
        title = save_item.getprevious().text
        author = None
        if save_item is not None and save_item.getprevious() and save_item.getprevious().getprevious():
            author = save_item.getprevious().getprevious().text
        volume = {
            'id': book['id'],
            'bookid': book['id'],
        }
        if title:
            volume['title'] = title
        else:
            volume['title'] = volume_name
        if author:
            volume['author'] = author
        else:
            volume['author'] = volume_author

        scraperwiki.sqlite.save(
            unique_keys=["volumeid", "type"], 
            data={ 
                    "volumeid": book['id'], 
                    "type": "pdb", 
                    "link": base_url + "/" + save_item.attrib['href'] 
                },
            table_name="volumeexts" )
        scraperwiki.sqlite.save(unique_keys=["id"], data=volume, table_name="bookvolumes" )
    else:
        volume = None
        exts = []
        for save_item in doc.xpath('//input[contains(@type, "button")]'):
            onclick = save_item.get('onclick')
            id = find_volume_id( onclick )
            skip = False
            if "ReadOnline" in onclick or "ReadPdbOnline" in onclick:
                if volume is not None:
                    for ext in exts:
                        scraperwiki.sqlite.save(unique_keys=["volumeid", "type"], data=ext, table_name="volumeexts" )
                    scraperwiki.sqlite.save(unique_keys=["id"], data=volume, table_name="bookvolumes" )
                volume = {
                    'id': id,
                    'author': save_item.getprevious().text,
                    'title': save_item.getprevious().tail,
                    'bookid': book['id'],
                }
                exts = []
            elif "DownloadEpub" in onclick:
                dl_link = convert_to_dl_url( id, "epub" )
                exts.append( { "volumeid": id, "type": "epub", "link": dl_link } )
            elif "DownloadUpdb" in onclick:
                dl_link = convert_to_dl_url( id, "updb" )
                exts.append( { "volumeid": id, "type": "updb", "link": dl_link } )
            elif "DownloadPdb" in onclick:
                dl_link = convert_to_dl_url( id, "pdb" )
                exts.append( { "volumeid": id, "type": "pdb", "link": dl_link } )
        if volume:
            for ext in exts:
                scraperwiki.sqlite.save(unique_keys=["volumeid", "type"], data=ext, table_name="volumeexts" )
            scraperwiki.sqlite.save(unique_keys=["id"], data=volume, table_name="bookvolumes" )

#
# Main
#
def main():
    urls = [
        'http://www.haodoo.net/?M=hd&P=wisdom',
        'http://www.haodoo.net/?M=hd&P=history',
        'http://www.haodoo.net/?M=hd&P=martial',
        'http://www.haodoo.net/?M=hd&P=mystery',
        'http://www.haodoo.net/?M=hd&P=romance',
        'http://www.haodoo.net/?M=hd&P=scifi',
        'http://www.haodoo.net/?M=hd&P=fiction',
        ]

    skip_stage1 = False
    try:
        print( ">>> Stage 1 - Collecting all book urls <<<" )
        if not skip_stage1:
            for url in urls:
                html = scraperwiki.scrape(url)
    
                page = 1
                while True:
                    suburl = "{0}-{1}".format( url, page )
                    if html.find( suburl[suburl.find('?'):] ):
                        html = scraperwiki.scrape( suburl )
                        if html.find("<strong>404")!=-1:
                            break
                        parse_books_from_html( html )
                        page = page + 1
                    else:
                        break
        
        print( ">>> Stage 2 - Analysising all book urls <<<" )
        for book in scraperwiki.sqlite.select("* from bookpages"):
            # grab html
            html = scraperwiki.scrape( book['url'] )

            # analysis and store information into book
            analysis_book_html_and_save( book, html )

        print( ">>> State 3 - done <<<" )

    except Exception, e:
        print( "Got exception:" )
        print( e )
        print( traceback.format_exc() )

main()

