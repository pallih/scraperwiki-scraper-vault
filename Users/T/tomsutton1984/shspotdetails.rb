require 'nokogiri'
require 'open-uri'

ScraperWiki::attach("shspot")           
urls = ScraperWiki::select("IMO, URL from shspot.swdata where length(IMO) <75 and length(IMO) >0 order by IMO")

for ship in urls
  url = ship["URL"]
  page = Nokogiri::HTML(open(url))

  if page.at_css('td:nth-child(3) table:nth-child(2) tr:nth-child(3) td , td:nth-child(3) table:nth-child(2) tr:nth-child(2) td')
      ship = page.css('.whiteboxstroke tr:nth-child(1) td:nth-child(4) .inboxLink').inner_text
      imo = page.css('tr:nth-child(2) td:nth-child(4) .inboxLink').inner_text
      description = page.css('tr:nth-child(5) td').inner_text
      vesselType = page.css('td:nth-child(3) table:nth-child(2) .whiteboxstroke tr:nth-child(1) td:nth-child(2)').inner_text
      grossTonnage = page.css('td:nth-child(3) table:nth-child(2) tr:nth-child(2) td:nth-child(2)').inner_text
      summerDWT = page.css('td:nth-child(3) table:nth-child(2) tr:nth-child(3) td:nth-child(2)').inner_text
      length = page.css('td:nth-child(3) table:nth-child(2) tr:nth-child(4) td:nth-child(2)').inner_text
      beam = page.css('td:nth-child(3) table:nth-child(2) tr:nth-child(5) td:nth-child(2)').inner_text
      draught = page.css('td:nth-child(3) table:nth-child(2) tr:nth-child(6) td:nth-child(2)').inner_text

      homePort = page.css('table:nth-child(6) .whiteboxstroke tr:nth-child(1) .inboxLink').inner_text
      classSociety = page.css('table:nth-child(6) tr:nth-child(2) .inboxLink').inner_text
      buildYear = page.css('table:nth-child(6) tr:nth-child(3) .inboxLink').inner_text
      builder = page.css('table:nth-child(6) tr:nth-child(4) .inboxLink').inner_text
      owner = page.css('table:nth-child(6) tr:nth-child(5) .inboxLink').inner_text
      manager = page.css('table:nth-child(6) tr:nth-child(6) .inboxLink').inner_text

  else

      ship = page.css('.whiteboxstroke tr:nth-child(1) td:nth-child(4) .inboxLink').inner_text
      imo = page.css('tr:nth-child(2) td:nth-child(4) .inboxLink').inner_text
      description = page.css('tr:nth-child(5) td').inner_text
      vesselType = 'unknown'
      grossTonnage = 'unknown'
      summerDWT = 'unknown'
      length = 'unknown'
      beam = 'unknown'
      draught = 'unknown'
      homePort = 'unknown'
      classSociety = 'unknown'
      buildYear = 'unknown'
      builder = 'unknown'
      owner = 'unknown'
      manager = 'unknown'

  end

    record = {
      Ship: ship,
      IMO: imo,
      Description: description,
      VesselType: vesselType,
      GrossTonnage: grossTonnage,
      SummerDWT: summerDWT,
      Length: length,
      Beam: beam,
      Draught: draught,
      HomePort: homePort,
      ClassSociety: classSociety,
      BuildYear: buildYear,
      Builder: builder,
      Owner: owner,
      Manager: manager
    }

    # Print out the data we've gathered
    p record

    # Finally, save the record to the datastore - 'Product' is our unique key
    ScraperWiki.save_sqlite([:Ship], record)
end

require 'nokogiri'
require 'open-uri'

ScraperWiki::attach("shspot")           
urls = ScraperWiki::select("IMO, URL from shspot.swdata where length(IMO) <75 and length(IMO) >0 order by IMO")

for ship in urls
  url = ship["URL"]
  page = Nokogiri::HTML(open(url))

  if page.at_css('td:nth-child(3) table:nth-child(2) tr:nth-child(3) td , td:nth-child(3) table:nth-child(2) tr:nth-child(2) td')
      ship = page.css('.whiteboxstroke tr:nth-child(1) td:nth-child(4) .inboxLink').inner_text
      imo = page.css('tr:nth-child(2) td:nth-child(4) .inboxLink').inner_text
      description = page.css('tr:nth-child(5) td').inner_text
      vesselType = page.css('td:nth-child(3) table:nth-child(2) .whiteboxstroke tr:nth-child(1) td:nth-child(2)').inner_text
      grossTonnage = page.css('td:nth-child(3) table:nth-child(2) tr:nth-child(2) td:nth-child(2)').inner_text
      summerDWT = page.css('td:nth-child(3) table:nth-child(2) tr:nth-child(3) td:nth-child(2)').inner_text
      length = page.css('td:nth-child(3) table:nth-child(2) tr:nth-child(4) td:nth-child(2)').inner_text
      beam = page.css('td:nth-child(3) table:nth-child(2) tr:nth-child(5) td:nth-child(2)').inner_text
      draught = page.css('td:nth-child(3) table:nth-child(2) tr:nth-child(6) td:nth-child(2)').inner_text

      homePort = page.css('table:nth-child(6) .whiteboxstroke tr:nth-child(1) .inboxLink').inner_text
      classSociety = page.css('table:nth-child(6) tr:nth-child(2) .inboxLink').inner_text
      buildYear = page.css('table:nth-child(6) tr:nth-child(3) .inboxLink').inner_text
      builder = page.css('table:nth-child(6) tr:nth-child(4) .inboxLink').inner_text
      owner = page.css('table:nth-child(6) tr:nth-child(5) .inboxLink').inner_text
      manager = page.css('table:nth-child(6) tr:nth-child(6) .inboxLink').inner_text

  else

      ship = page.css('.whiteboxstroke tr:nth-child(1) td:nth-child(4) .inboxLink').inner_text
      imo = page.css('tr:nth-child(2) td:nth-child(4) .inboxLink').inner_text
      description = page.css('tr:nth-child(5) td').inner_text
      vesselType = 'unknown'
      grossTonnage = 'unknown'
      summerDWT = 'unknown'
      length = 'unknown'
      beam = 'unknown'
      draught = 'unknown'
      homePort = 'unknown'
      classSociety = 'unknown'
      buildYear = 'unknown'
      builder = 'unknown'
      owner = 'unknown'
      manager = 'unknown'

  end

    record = {
      Ship: ship,
      IMO: imo,
      Description: description,
      VesselType: vesselType,
      GrossTonnage: grossTonnage,
      SummerDWT: summerDWT,
      Length: length,
      Beam: beam,
      Draught: draught,
      HomePort: homePort,
      ClassSociety: classSociety,
      BuildYear: buildYear,
      Builder: builder,
      Owner: owner,
      Manager: manager
    }

    # Print out the data we've gathered
    p record

    # Finally, save the record to the datastore - 'Product' is our unique key
    ScraperWiki.save_sqlite([:Ship], record)
end

