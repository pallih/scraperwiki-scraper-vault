# David Jones, Climate Code Foundation
# 2010-11-15
# Hello

"""
Notes for Monday's Python Northwest (Manchester) meeting.

Background

ccc-gistemp http://code.google.com/p/ccc-gistemp/
ccc-gistemp makes graphs of global temperature change starting from weather station data.

Major data source is GHCN: http://www.ncdc.noaa.gov/ghcnm/
and USHCN: http://cdiac.ornl.gov/epubs/ndp/ushcn/ushcn.html


Project

Would like to add scraped data from other sources.  Eventually, creating a
community sourced climate data network.

Outputs would be: data, maps, graphs (and quality flags).

Right now, would like:

Kielder and Alice Holt (Forestry Commission, UK) http://www.whatdotheyknow.com/request/weather_data_kielder_and_alice_h
Botanical Gardens (University of Cambridge, UK) http://www.whatdotheyknow.com/request/temperature_data_from_botanical

Going forward, other sources, higher resolution, and other elements:

National Met Agencies:

Environment Canada (some of this is done).
Met Office (UK)
Deautscher Wetterdienst (DWD) (in German): http://www.dwd.de/bvbw/appmanager/bvbw/dwdwwwDesktop?_nfpb=true&_pageLabel=_dwdwww_klima_umwelt_klimadaten_deutschland&T82002gsbDocumentPath=Navigation%2FOeffentlichkeit%2FKlima__Umwelt%2FKlimadaten%2Fkldaten__kostenfrei%2Fhome__nkdzdaten__node.html%3F__nnn%3Dtrue

Miscellaneous sources

NORDKLIM
SCAR READER
Kielder wind speeds http://www.whatdotheyknow.com/request/kielder_castle_weather_station_w
http://www.wmo.int/pages/prog/www/ois/rbsn-rbcn/rbsn-rbcn-home.htm (.xls files keeps moving!)

So far, I have monthly data for Canada and Met Office from the web, maps for USHCN, Nordklim.

See: Canada: http://scraperwiki.com/scrapers/canada-climate-data/
 NORDKLIM http://scraperwiki.com/views/nordklim-map/
 USHCN http://scraperwiki.com/views/ushcn-map/

The Canada scraper massively under samples the stations.  On the
Environment Canada website, try
doing an unrestricted search of a territory, and return all results.

At the moment Monthly data is more useful than daily data, but daily
can be turned into monthly.  Lots of Canada stations seem to have daily
data but not monthly (presumably for QA/QC reasons).

Data formats

I'm increasingly thinking that my favourite format should be a JSON record (for each station):

{"tmin": {"2010-01": -1.2, "2010-06": 8.7}, "name": "manchester ringway"}

This example has only 2 monthly values for tmin.  Adding other elements would be a matter of having a value for tmean, tmax, precipitation, and so on.  Of note: temperature series is a dictionary of (month,value) pairs.  ISO 8601 format for times: monthly: "2010-11"; daily: "2010-11-15" or "2010-319" (whichever the data comes in).

I still thing the above is a nice format, but ScraperWiki can't store it like that.
So we use one "row" for each station*element combination where element is 'tminD'
(daily minimum temperature), 'tmeanM' (monthly mean of daily mean temperature), and so
on.

{"element": "tmeanD", "id": "CAE2101100_", "2010-03": -5.4, "2009-01": -8.7}

This format leads to a very large number of "keys" for each row (one key per month, or
one key per day for daily series).  But ScraperWiki seems to cope.


Calculation of Monthly Means (Technical and dull)

There are lots of ways to do this.  WMO 100 (3rd ed) recommends no more than 10 daily values missing in a month, and no more than 5 consecutive missing.  WCDP 10 recommends a "3/5" rule: no more than 3 consecutive missing, and no more than 5 missing in total.  Note that both of those documents recommend calculating monthly mean temp from daily mean temp, daily mean temp being (min+max)/2, so it could be possible to have a monthly min and max, but no mean.
"""

# Sorry, no actual scraper here.
