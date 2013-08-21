import scraperwiki

# code lovingly stolen from https://scraperwiki.com/views/uk_postcode_lookup/edit/

def Fetchdata(postcode):
    if postcode[:2] == "BT":
        try:
            scraperwiki.sqlite.attach('ni_postcodes_from_codepoint', "nipost")
        except:
            pass # presumably already exists? TODO: make this a less general exception! And the case below, too.
        lres = scraperwiki.sqlite.select('* from nipost.swdata where Postcode = ? limit 1', postcode)
        grid = 'IE'
    else:
        try:
            scraperwiki.sqlite.attach('uk_postcodes_from_codepoint', "ukpost")
        except:
            pass # exists?
        lres = scraperwiki.sqlite.select('* from ukpost.swdata where Postcode = ? limit 1', postcode)
        grid = 'GB'

    if not lres:
        return None

    res = lres[0]
    return tuple(scraperwiki.geo.os_easting_northing_to_latlng(res["Eastings"], res["Northings"], grid))

