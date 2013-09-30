require "rubygems"
require "nokogiri"

def scrape_owinsp(url)
  html = ScraperWiki.scrape(url)
  html.force_encoding("WINDOWS-1252")
  html = html.encode("UTF-8")
  doc = Nokogiri::HTML(html)
end

# collect all known BRINs
ScraperWiki.attach("nl-edu-vestigingen-po-vo", "a")
brins_po = ScraperWiki.select("`brin-vest nr` from a.vestigingen_po").map do |row|
  row["BRIN-VEST NR"][0...4]
end.uniq
brins_vo = ScraperWiki.select("`brin-vestnr` from a.vestigingen_vo").map do |row|
  row["BRIN-VESTNR"][0...4]
end.uniq
brins = (brins_po + brins_vo).uniq.sort

# which BRINs do we already have?
known_brins = ScraperWiki.select("brin from owinsp_school_ids").map do |row|
  row["brin"]
end

# find school_ids (sch_id) for each BRIN
(brins - known_brins).each do |brin|
  doc = scrape_owinsp("http://toezichtkaart.owinsp.nl/zoekresultaat?p1=brin&p2=%3D&p3=#{ brin }")

  if stitle = doc.at_xpath("//h1[@class='stitle']")
    # query matched one school; school page returned
    name = stitle.content
    sch_id = html[/sch_id=([0-9]+)/,1].to_i
    sector = html[/sector=(PO|VO)/,1]
    postcode = doc.at_xpath("//div[@class='content_main']/p[@class='detpag']").content[/[0-9]{4} [A-Z]{2}/].delete("^0-9A-Z")
    ScraperWiki.save_sqlite(["sch_id"], {
      "brin"=>brin,
      "sch_id"=>sch_id,
      "sector"=>sector,
      "name"=>name,
      "postcode"=>postcode
    }, "owinsp_school_ids")

  elsif table = doc.at_xpath("//table[@summary='Zoekresultaat']")
    # more than one school found; results table returned
    table.xpath(".//li[@class='match']/noscript/a").map do |match_link|
      href = match_link["href"]
      sch_id = href[/sch_id=([0-9]+)/,1].to_i
      sector = href[/sector=(PO|VO)/,1]
      name, postcode = match_link.content.scan(/^(.+), ([0-9]{4}[A-Z]{2})$/).first
      ScraperWiki.save_sqlite(["sch_id"], {
        "brin"=>brin,
        "sch_id"=>sch_id,
        "sector"=>sector,
        "name"=>name,
        "postcode"=>postcode
      }, "owinsp_school_ids")
    end

  else
    # no school found
  end
end


def process_afdeling(sector, sch_id, doc)
  toezicht_div = doc.at_xpath("//div[div[@class='blockopen' and ul/li/noscript/a/strong='Toezichthistorie']]")
  href = toezicht_div.at_xpath("div/ul/li/noscript/a[strong='Toezichthistorie']")["href"]
  arr_id = href[/arr_id=([0-9.]*)/,1]

  # afdeling
  naam = doc.at_xpath("//h1[@class='stitle']").content
  samengevat = doc.at_xpath("//p[strong='Samengevat']").content.gsub(/\A\s*Samengevat\s*/m, "").gsub(/ *\n */, "\n").strip
  opboor_link = doc.at_xpath("//a[.='Opbrengstenoordeel']")
  if opboor_link
    brinvest = "%s%02d" % opboor_link["href"].scan(/p_brin=([A-Z0-9]{4}).+p_vestnr=([0-9]+)/).flatten
  else
    brinvest = nil
  end

  # toezichtkaart: toezichtvorm en oordeel
  toezichtkaart_div = doc.at_xpath("//div[@class='tzk' and h3/div/a[@href='http://www.onderwijsinspectie.nl/onderwerpen/Toezicht/Toezichtkaart']]")
  if toezichtkaart_div
    # huidig oordeel, toezicht
    oordeel = toezichtkaart_div.at_xpath("hr/following-sibling::div").content
    toezicht = toezichtkaart_div.at_xpath("h3").content.delete("^-A-Za-z0-9 ").strip
    datum = Date.strptime(toezicht[/[0-9]{2}-[0-9]{2}-[0-9]{4}/], "%d-%m-%Y")
  else
    oordeel = nil
    toezicht = nil
    datum = nil
  end

  ScraperWiki.save_sqlite(["sch_id","arr_id"], {
    "sector"=>sector,
    "sch_id"=>sch_id,
    "arr_id"=>arr_id,
    "brinvest"=>brinvest,
    "naam"=>naam,
    "samengevat"=>samengevat,
    "oordeel"=>oordeel,
    "toezicht"=>toezicht,
    "datum"=>datum
  }, "owinsp_school_toezichtkaart")

  # toezichthistorie
  toezicht_div.xpath(".//table[@summary='Rapporten']//li[@class='arrref']").each do |li|
    toezicht = li.content
    datum = Date.strptime(toezicht[/[0-9]{2}-[0-9]{2}-[0-9]{4}/], "%d-%m-%Y")

    ScraperWiki.save_sqlite(["sch_id","arr_id","toezicht","datum"], {
      "sector"=>sector,
      "sch_id"=>sch_id,
      "arr_id"=>arr_id,
      "brinvest"=>brinvest,
      "toezicht"=>toezicht,
      "datum"=>datum
    }, "owinsp_school_toezichthistorie")
  end
  
  # toezichtrapporten
  rapporten = doc.xpath(".//table[@summary='Rapporten']//span[@class='icoon_download']/a").map do |a|
    titel = a.content
    datum = Date.strptime(titel[/[0-9]{2}-[0-9]{2}-[0-9]{4}/], "%d-%m-%Y")
    pdf_id = a["href"][/id=([A-Za-z0-9]+)/,1]

    ScraperWiki.save_sqlite(["sch_id","arr_id","pdf_id"], {
      "sector"=>sector,
      "sch_id"=>sch_id,
      "arr_id"=>arr_id,
      "brinvest"=>brinvest,
      "pdf_id"=>pdf_id,
      "titel"=>titel,
      "datum"=>datum
    }, "owinsp_school_rapporten")
  end
end


# look at each school
ScraperWiki.select("sector, sch_id from owinsp_school_ids").each do |row|
  sector = row["sector"]
  sch_id = row["sch_id"]
  doc = scrape_owinsp("http://toezichtkaart.owinsp.nl/zoekresultaat?sector=#{ sector }&sch_id=#{ sch_id }.22&arr_id=-1")

  if table = doc.at_xpath("//table[@summary='Afdelingen']")
    # meerdere afdelingen
    arr_ids = table.xpath(".//noscript/a").map do |a|
      a["href"][/arr_id=([0-9.]*)/,1]
    end.compact.uniq.each do |arr_id|
      doc_arr = scrape_owinsp("http://toezichtkaart.owinsp.nl/zoekresultaat?sector=#{ sector }&sch_id=#{ sch_id }.22&arr_id=#{ arr_id }")
      process_afdeling(sector, sch_id, doc_arr)
    end
  elsif doc.at_xpath("//div[div[@class='blockopen' and ul/li/noscript/a/strong='Toezichthistorie']]")
    # een enkele afdeling
    process_afdeling(sector, sch_id, doc)
  end
end

require "rubygems"
require "nokogiri"

def scrape_owinsp(url)
  html = ScraperWiki.scrape(url)
  html.force_encoding("WINDOWS-1252")
  html = html.encode("UTF-8")
  doc = Nokogiri::HTML(html)
end

# collect all known BRINs
ScraperWiki.attach("nl-edu-vestigingen-po-vo", "a")
brins_po = ScraperWiki.select("`brin-vest nr` from a.vestigingen_po").map do |row|
  row["BRIN-VEST NR"][0...4]
end.uniq
brins_vo = ScraperWiki.select("`brin-vestnr` from a.vestigingen_vo").map do |row|
  row["BRIN-VESTNR"][0...4]
end.uniq
brins = (brins_po + brins_vo).uniq.sort

# which BRINs do we already have?
known_brins = ScraperWiki.select("brin from owinsp_school_ids").map do |row|
  row["brin"]
end

# find school_ids (sch_id) for each BRIN
(brins - known_brins).each do |brin|
  doc = scrape_owinsp("http://toezichtkaart.owinsp.nl/zoekresultaat?p1=brin&p2=%3D&p3=#{ brin }")

  if stitle = doc.at_xpath("//h1[@class='stitle']")
    # query matched one school; school page returned
    name = stitle.content
    sch_id = html[/sch_id=([0-9]+)/,1].to_i
    sector = html[/sector=(PO|VO)/,1]
    postcode = doc.at_xpath("//div[@class='content_main']/p[@class='detpag']").content[/[0-9]{4} [A-Z]{2}/].delete("^0-9A-Z")
    ScraperWiki.save_sqlite(["sch_id"], {
      "brin"=>brin,
      "sch_id"=>sch_id,
      "sector"=>sector,
      "name"=>name,
      "postcode"=>postcode
    }, "owinsp_school_ids")

  elsif table = doc.at_xpath("//table[@summary='Zoekresultaat']")
    # more than one school found; results table returned
    table.xpath(".//li[@class='match']/noscript/a").map do |match_link|
      href = match_link["href"]
      sch_id = href[/sch_id=([0-9]+)/,1].to_i
      sector = href[/sector=(PO|VO)/,1]
      name, postcode = match_link.content.scan(/^(.+), ([0-9]{4}[A-Z]{2})$/).first
      ScraperWiki.save_sqlite(["sch_id"], {
        "brin"=>brin,
        "sch_id"=>sch_id,
        "sector"=>sector,
        "name"=>name,
        "postcode"=>postcode
      }, "owinsp_school_ids")
    end

  else
    # no school found
  end
end


def process_afdeling(sector, sch_id, doc)
  toezicht_div = doc.at_xpath("//div[div[@class='blockopen' and ul/li/noscript/a/strong='Toezichthistorie']]")
  href = toezicht_div.at_xpath("div/ul/li/noscript/a[strong='Toezichthistorie']")["href"]
  arr_id = href[/arr_id=([0-9.]*)/,1]

  # afdeling
  naam = doc.at_xpath("//h1[@class='stitle']").content
  samengevat = doc.at_xpath("//p[strong='Samengevat']").content.gsub(/\A\s*Samengevat\s*/m, "").gsub(/ *\n */, "\n").strip
  opboor_link = doc.at_xpath("//a[.='Opbrengstenoordeel']")
  if opboor_link
    brinvest = "%s%02d" % opboor_link["href"].scan(/p_brin=([A-Z0-9]{4}).+p_vestnr=([0-9]+)/).flatten
  else
    brinvest = nil
  end

  # toezichtkaart: toezichtvorm en oordeel
  toezichtkaart_div = doc.at_xpath("//div[@class='tzk' and h3/div/a[@href='http://www.onderwijsinspectie.nl/onderwerpen/Toezicht/Toezichtkaart']]")
  if toezichtkaart_div
    # huidig oordeel, toezicht
    oordeel = toezichtkaart_div.at_xpath("hr/following-sibling::div").content
    toezicht = toezichtkaart_div.at_xpath("h3").content.delete("^-A-Za-z0-9 ").strip
    datum = Date.strptime(toezicht[/[0-9]{2}-[0-9]{2}-[0-9]{4}/], "%d-%m-%Y")
  else
    oordeel = nil
    toezicht = nil
    datum = nil
  end

  ScraperWiki.save_sqlite(["sch_id","arr_id"], {
    "sector"=>sector,
    "sch_id"=>sch_id,
    "arr_id"=>arr_id,
    "brinvest"=>brinvest,
    "naam"=>naam,
    "samengevat"=>samengevat,
    "oordeel"=>oordeel,
    "toezicht"=>toezicht,
    "datum"=>datum
  }, "owinsp_school_toezichtkaart")

  # toezichthistorie
  toezicht_div.xpath(".//table[@summary='Rapporten']//li[@class='arrref']").each do |li|
    toezicht = li.content
    datum = Date.strptime(toezicht[/[0-9]{2}-[0-9]{2}-[0-9]{4}/], "%d-%m-%Y")

    ScraperWiki.save_sqlite(["sch_id","arr_id","toezicht","datum"], {
      "sector"=>sector,
      "sch_id"=>sch_id,
      "arr_id"=>arr_id,
      "brinvest"=>brinvest,
      "toezicht"=>toezicht,
      "datum"=>datum
    }, "owinsp_school_toezichthistorie")
  end
  
  # toezichtrapporten
  rapporten = doc.xpath(".//table[@summary='Rapporten']//span[@class='icoon_download']/a").map do |a|
    titel = a.content
    datum = Date.strptime(titel[/[0-9]{2}-[0-9]{2}-[0-9]{4}/], "%d-%m-%Y")
    pdf_id = a["href"][/id=([A-Za-z0-9]+)/,1]

    ScraperWiki.save_sqlite(["sch_id","arr_id","pdf_id"], {
      "sector"=>sector,
      "sch_id"=>sch_id,
      "arr_id"=>arr_id,
      "brinvest"=>brinvest,
      "pdf_id"=>pdf_id,
      "titel"=>titel,
      "datum"=>datum
    }, "owinsp_school_rapporten")
  end
end


# look at each school
ScraperWiki.select("sector, sch_id from owinsp_school_ids").each do |row|
  sector = row["sector"]
  sch_id = row["sch_id"]
  doc = scrape_owinsp("http://toezichtkaart.owinsp.nl/zoekresultaat?sector=#{ sector }&sch_id=#{ sch_id }.22&arr_id=-1")

  if table = doc.at_xpath("//table[@summary='Afdelingen']")
    # meerdere afdelingen
    arr_ids = table.xpath(".//noscript/a").map do |a|
      a["href"][/arr_id=([0-9.]*)/,1]
    end.compact.uniq.each do |arr_id|
      doc_arr = scrape_owinsp("http://toezichtkaart.owinsp.nl/zoekresultaat?sector=#{ sector }&sch_id=#{ sch_id }.22&arr_id=#{ arr_id }")
      process_afdeling(sector, sch_id, doc_arr)
    end
  elsif doc.at_xpath("//div[div[@class='blockopen' and ul/li/noscript/a/strong='Toezichthistorie']]")
    # een enkele afdeling
    process_afdeling(sector, sch_id, doc)
  end
end

