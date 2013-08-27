# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'csv'
require 'json'
require 'scrapers/cf'

BASE_URL = "http://www.uscounties.org/cffiles_web/counties/"
@br = Mechanize.new { |b|
  b.user_agent_alias = 'Linux Firefox'
  b.read_timeout = 1200
  b.max_history=0
  b.retry_change_requests = true
  b.verify_mode = OpenSSL::SSL::VERIFY_NONE
}

class String
  def pretty
    self.strip
  end
end

class Array
  def pretty
    self.collect{|a| a.strip}
  end
end

def scrape(pg,act,rec)
  data = pg.body
  uri = URI.parse(pg.uri.to_s)

  if act == "counties"
    records = []
    Nokogiri::HTML(data).xpath(".//select[@name='countyid']/option").each{|ele|
      records << {
        "county_link" => BASE_URL + attributes(ele.xpath("."),"value"),
        "county" => s_text(ele.xpath("./text()"))
      }.merge(rec)
    }
    return records
  elsif act == "cities"
    records = []
    Nokogiri::HTML(data).xpath(".//table[@width='90%']/tr[position()>1]").each{|tr|
      td = tr.xpath("td")
      records << {
        "place" => s_text(td[0].xpath("./text()")),
        "mode" => "listed",
        "place_type" => s_text(td[1].xpath("./text()")),
        "city_link" => uri.to_s
      }.merge(rec)
    }
    Nokogiri::HTML(data).xpath(".//table[@width='50%']/tr[position()>1]").each{|tr|
      td = tr.xpath("td")
      a_text(td.first.xpath("./text()")).each{|place|
        records << {
          "place" => place,
          "mode" => "un-listed",
          "city_link" => uri.to_s
        }.merge(rec)
      }
    }
    return records
  end
end

def action(srch)
  counties = scrape(@br.get(BASE_URL + "citiesstatecounty.cfm?STATECODE=#{srch['state_code']}"),"counties",srch)
  counties.each{|county|
    cities = scrape(@br.get(county['county_link']),"cities",county)
    ScraperWiki.save_sqlite(unique_keys=['city_link','place','mode'],cities,table_name='swdata',verbose=2)
  }
end

range = [
{"state_code"=>"AL","state"=>"Alabama"}, {"state_code"=>"AK","state"=>"Alaska"}, {"state_code"=>"AZ","state"=>"Arizona"}, {"state_code"=>"AR","state"=>"Arkansas"}, {"state_code"=>"CA","state"=>"California"}, {"state_code"=>"CO","state"=>"Colorado"}, {"state_code"=>"CT","state"=>"Connecticut"}, {"state_code"=>"DE","state"=>"Delaware"}, {"state_code"=>"DC","state"=>"District of Columbia"}, {"state_code"=>"FL","state"=>"Florida"}, {"state_code"=>"GA","state"=>"Georgia"}, {"state_code"=>"HI","state"=>"Hawaii"}, {"state_code"=>"ID","state"=>"Idaho"}, {"state_code"=>"IL","state"=>"Illinois"}, {"state_code"=>"IN","state"=>"Indiana"}, {"state_code"=>"IA","state"=>"Iowa"}, {"state_code"=>"KS","state"=>"Kansas"}, {"state_code"=>"KY","state"=>"Kentucky"}, {"state_code"=>"LA","state"=>"Louisiana"}, {"state_code"=>"ME","state"=>"Maine"}, {"state_code"=>"MD","state"=>"Maryland"}, {"state_code"=>"MA","state"=>"Massachusetts"}, {"state_code"=>"MI","state"=>"Michigan"}, {"state_code"=>"MN","state"=>"Minnesota"}, {"state_code"=>"MS","state"=>"Mississippi"}, {"state_code"=>"MO","state"=>"Missouri"}, {"state_code"=>"MT","state"=>"Montana"}, {"state_code"=>"NE","state"=>"Nebraska"}, {"state_code"=>"NV","state"=>"Nevada"}, {"state_code"=>"NH","state"=>"New Hampshire"}, {"state_code"=>"NJ","state"=>"New Jersey"}, {"state_code"=>"NM","state"=>"New Mexico"}, {"state_code"=>"NY","state"=>"New York"}, {"state_code"=>"NC","state"=>"North Carolina"}, {"state_code"=>"ND","state"=>"North Dakota"}, {"state_code"=>"OH","state"=>"Ohio"}, {"state_code"=>"OK","state"=>"Oklahoma"}, {"state_code"=>"OR","state"=>"Oregon"}, {"state_code"=>"PA","state"=>"Pennsylvania"}, {"state_code"=>"RI","state"=>"Rhode Island"}, {"state_code"=>"SC","state"=>"South Carolina"}, {"state_code"=>"SD","state"=>"South Dakota"}, {"state_code"=>"TN","state"=>"Tennessee"}, {"state_code"=>"TX","state"=>"Texas"}, {"state_code"=>"UT","state"=>"Utah"}, {"state_code"=>"VT","state"=>"Vermont"}, {"state_code"=>"VA","state"=>"Virginia"}, {"state_code"=>"WA","state"=>"Washington"}, {"state_code"=>"WV","state"=>"West Virginia"}, {"state_code"=>"WI","state"=>"Wisconsin"}, {"state_code"=>"WY","state"=>"Wyoming"}
]
start = get_metadata("start",0)
start = 0 if start >= range.length
range[start..-1].each_with_index{|reg,idx|
  action(reg)
  save_metadata("start",start+idx)

}

#puts scrape(@br.get("http://www.uscounties.org/cffiles_web/counties/citiesstatecounty.cfm?STATECODE=AL").body,"counties",{}).inspect
#puts scrape(@br.get("http://www.uscounties.org/cffiles_web/counties/citiescounty.cfm?countyid=1001").body,"cities",{}).inspect# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'csv'
require 'json'
require 'scrapers/cf'

BASE_URL = "http://www.uscounties.org/cffiles_web/counties/"
@br = Mechanize.new { |b|
  b.user_agent_alias = 'Linux Firefox'
  b.read_timeout = 1200
  b.max_history=0
  b.retry_change_requests = true
  b.verify_mode = OpenSSL::SSL::VERIFY_NONE
}

class String
  def pretty
    self.strip
  end
end

class Array
  def pretty
    self.collect{|a| a.strip}
  end
end

def scrape(pg,act,rec)
  data = pg.body
  uri = URI.parse(pg.uri.to_s)

  if act == "counties"
    records = []
    Nokogiri::HTML(data).xpath(".//select[@name='countyid']/option").each{|ele|
      records << {
        "county_link" => BASE_URL + attributes(ele.xpath("."),"value"),
        "county" => s_text(ele.xpath("./text()"))
      }.merge(rec)
    }
    return records
  elsif act == "cities"
    records = []
    Nokogiri::HTML(data).xpath(".//table[@width='90%']/tr[position()>1]").each{|tr|
      td = tr.xpath("td")
      records << {
        "place" => s_text(td[0].xpath("./text()")),
        "mode" => "listed",
        "place_type" => s_text(td[1].xpath("./text()")),
        "city_link" => uri.to_s
      }.merge(rec)
    }
    Nokogiri::HTML(data).xpath(".//table[@width='50%']/tr[position()>1]").each{|tr|
      td = tr.xpath("td")
      a_text(td.first.xpath("./text()")).each{|place|
        records << {
          "place" => place,
          "mode" => "un-listed",
          "city_link" => uri.to_s
        }.merge(rec)
      }
    }
    return records
  end
end

def action(srch)
  counties = scrape(@br.get(BASE_URL + "citiesstatecounty.cfm?STATECODE=#{srch['state_code']}"),"counties",srch)
  counties.each{|county|
    cities = scrape(@br.get(county['county_link']),"cities",county)
    ScraperWiki.save_sqlite(unique_keys=['city_link','place','mode'],cities,table_name='swdata',verbose=2)
  }
end

range = [
{"state_code"=>"AL","state"=>"Alabama"}, {"state_code"=>"AK","state"=>"Alaska"}, {"state_code"=>"AZ","state"=>"Arizona"}, {"state_code"=>"AR","state"=>"Arkansas"}, {"state_code"=>"CA","state"=>"California"}, {"state_code"=>"CO","state"=>"Colorado"}, {"state_code"=>"CT","state"=>"Connecticut"}, {"state_code"=>"DE","state"=>"Delaware"}, {"state_code"=>"DC","state"=>"District of Columbia"}, {"state_code"=>"FL","state"=>"Florida"}, {"state_code"=>"GA","state"=>"Georgia"}, {"state_code"=>"HI","state"=>"Hawaii"}, {"state_code"=>"ID","state"=>"Idaho"}, {"state_code"=>"IL","state"=>"Illinois"}, {"state_code"=>"IN","state"=>"Indiana"}, {"state_code"=>"IA","state"=>"Iowa"}, {"state_code"=>"KS","state"=>"Kansas"}, {"state_code"=>"KY","state"=>"Kentucky"}, {"state_code"=>"LA","state"=>"Louisiana"}, {"state_code"=>"ME","state"=>"Maine"}, {"state_code"=>"MD","state"=>"Maryland"}, {"state_code"=>"MA","state"=>"Massachusetts"}, {"state_code"=>"MI","state"=>"Michigan"}, {"state_code"=>"MN","state"=>"Minnesota"}, {"state_code"=>"MS","state"=>"Mississippi"}, {"state_code"=>"MO","state"=>"Missouri"}, {"state_code"=>"MT","state"=>"Montana"}, {"state_code"=>"NE","state"=>"Nebraska"}, {"state_code"=>"NV","state"=>"Nevada"}, {"state_code"=>"NH","state"=>"New Hampshire"}, {"state_code"=>"NJ","state"=>"New Jersey"}, {"state_code"=>"NM","state"=>"New Mexico"}, {"state_code"=>"NY","state"=>"New York"}, {"state_code"=>"NC","state"=>"North Carolina"}, {"state_code"=>"ND","state"=>"North Dakota"}, {"state_code"=>"OH","state"=>"Ohio"}, {"state_code"=>"OK","state"=>"Oklahoma"}, {"state_code"=>"OR","state"=>"Oregon"}, {"state_code"=>"PA","state"=>"Pennsylvania"}, {"state_code"=>"RI","state"=>"Rhode Island"}, {"state_code"=>"SC","state"=>"South Carolina"}, {"state_code"=>"SD","state"=>"South Dakota"}, {"state_code"=>"TN","state"=>"Tennessee"}, {"state_code"=>"TX","state"=>"Texas"}, {"state_code"=>"UT","state"=>"Utah"}, {"state_code"=>"VT","state"=>"Vermont"}, {"state_code"=>"VA","state"=>"Virginia"}, {"state_code"=>"WA","state"=>"Washington"}, {"state_code"=>"WV","state"=>"West Virginia"}, {"state_code"=>"WI","state"=>"Wisconsin"}, {"state_code"=>"WY","state"=>"Wyoming"}
]
start = get_metadata("start",0)
start = 0 if start >= range.length
range[start..-1].each_with_index{|reg,idx|
  action(reg)
  save_metadata("start",start+idx)

}

#puts scrape(@br.get("http://www.uscounties.org/cffiles_web/counties/citiesstatecounty.cfm?STATECODE=AL").body,"counties",{}).inspect
#puts scrape(@br.get("http://www.uscounties.org/cffiles_web/counties/citiescounty.cfm?countyid=1001").body,"cities",{}).inspect# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'csv'
require 'json'
require 'scrapers/cf'

BASE_URL = "http://www.uscounties.org/cffiles_web/counties/"
@br = Mechanize.new { |b|
  b.user_agent_alias = 'Linux Firefox'
  b.read_timeout = 1200
  b.max_history=0
  b.retry_change_requests = true
  b.verify_mode = OpenSSL::SSL::VERIFY_NONE
}

class String
  def pretty
    self.strip
  end
end

class Array
  def pretty
    self.collect{|a| a.strip}
  end
end

def scrape(pg,act,rec)
  data = pg.body
  uri = URI.parse(pg.uri.to_s)

  if act == "counties"
    records = []
    Nokogiri::HTML(data).xpath(".//select[@name='countyid']/option").each{|ele|
      records << {
        "county_link" => BASE_URL + attributes(ele.xpath("."),"value"),
        "county" => s_text(ele.xpath("./text()"))
      }.merge(rec)
    }
    return records
  elsif act == "cities"
    records = []
    Nokogiri::HTML(data).xpath(".//table[@width='90%']/tr[position()>1]").each{|tr|
      td = tr.xpath("td")
      records << {
        "place" => s_text(td[0].xpath("./text()")),
        "mode" => "listed",
        "place_type" => s_text(td[1].xpath("./text()")),
        "city_link" => uri.to_s
      }.merge(rec)
    }
    Nokogiri::HTML(data).xpath(".//table[@width='50%']/tr[position()>1]").each{|tr|
      td = tr.xpath("td")
      a_text(td.first.xpath("./text()")).each{|place|
        records << {
          "place" => place,
          "mode" => "un-listed",
          "city_link" => uri.to_s
        }.merge(rec)
      }
    }
    return records
  end
end

def action(srch)
  counties = scrape(@br.get(BASE_URL + "citiesstatecounty.cfm?STATECODE=#{srch['state_code']}"),"counties",srch)
  counties.each{|county|
    cities = scrape(@br.get(county['county_link']),"cities",county)
    ScraperWiki.save_sqlite(unique_keys=['city_link','place','mode'],cities,table_name='swdata',verbose=2)
  }
end

range = [
{"state_code"=>"AL","state"=>"Alabama"}, {"state_code"=>"AK","state"=>"Alaska"}, {"state_code"=>"AZ","state"=>"Arizona"}, {"state_code"=>"AR","state"=>"Arkansas"}, {"state_code"=>"CA","state"=>"California"}, {"state_code"=>"CO","state"=>"Colorado"}, {"state_code"=>"CT","state"=>"Connecticut"}, {"state_code"=>"DE","state"=>"Delaware"}, {"state_code"=>"DC","state"=>"District of Columbia"}, {"state_code"=>"FL","state"=>"Florida"}, {"state_code"=>"GA","state"=>"Georgia"}, {"state_code"=>"HI","state"=>"Hawaii"}, {"state_code"=>"ID","state"=>"Idaho"}, {"state_code"=>"IL","state"=>"Illinois"}, {"state_code"=>"IN","state"=>"Indiana"}, {"state_code"=>"IA","state"=>"Iowa"}, {"state_code"=>"KS","state"=>"Kansas"}, {"state_code"=>"KY","state"=>"Kentucky"}, {"state_code"=>"LA","state"=>"Louisiana"}, {"state_code"=>"ME","state"=>"Maine"}, {"state_code"=>"MD","state"=>"Maryland"}, {"state_code"=>"MA","state"=>"Massachusetts"}, {"state_code"=>"MI","state"=>"Michigan"}, {"state_code"=>"MN","state"=>"Minnesota"}, {"state_code"=>"MS","state"=>"Mississippi"}, {"state_code"=>"MO","state"=>"Missouri"}, {"state_code"=>"MT","state"=>"Montana"}, {"state_code"=>"NE","state"=>"Nebraska"}, {"state_code"=>"NV","state"=>"Nevada"}, {"state_code"=>"NH","state"=>"New Hampshire"}, {"state_code"=>"NJ","state"=>"New Jersey"}, {"state_code"=>"NM","state"=>"New Mexico"}, {"state_code"=>"NY","state"=>"New York"}, {"state_code"=>"NC","state"=>"North Carolina"}, {"state_code"=>"ND","state"=>"North Dakota"}, {"state_code"=>"OH","state"=>"Ohio"}, {"state_code"=>"OK","state"=>"Oklahoma"}, {"state_code"=>"OR","state"=>"Oregon"}, {"state_code"=>"PA","state"=>"Pennsylvania"}, {"state_code"=>"RI","state"=>"Rhode Island"}, {"state_code"=>"SC","state"=>"South Carolina"}, {"state_code"=>"SD","state"=>"South Dakota"}, {"state_code"=>"TN","state"=>"Tennessee"}, {"state_code"=>"TX","state"=>"Texas"}, {"state_code"=>"UT","state"=>"Utah"}, {"state_code"=>"VT","state"=>"Vermont"}, {"state_code"=>"VA","state"=>"Virginia"}, {"state_code"=>"WA","state"=>"Washington"}, {"state_code"=>"WV","state"=>"West Virginia"}, {"state_code"=>"WI","state"=>"Wisconsin"}, {"state_code"=>"WY","state"=>"Wyoming"}
]
start = get_metadata("start",0)
start = 0 if start >= range.length
range[start..-1].each_with_index{|reg,idx|
  action(reg)
  save_metadata("start",start+idx)

}

#puts scrape(@br.get("http://www.uscounties.org/cffiles_web/counties/citiesstatecounty.cfm?STATECODE=AL").body,"counties",{}).inspect
#puts scrape(@br.get("http://www.uscounties.org/cffiles_web/counties/citiescounty.cfm?countyid=1001").body,"cities",{}).inspect