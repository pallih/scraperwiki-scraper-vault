# ------------------------------------------------------ #
# Modified from Heiko Braun and Cameron Prebble          #
# https://scraperwiki.com/scrapers/hbraun-zamg/          #
# https://scraperwiki.com/scrapers/olympic_medal_counts/ #
# ------------------------------------------------------ #
# Goal: Scrape award/badge and renown count in an        #
# attempt to back out renown formula using spreadsheet   #
# rref. From assumptions, 68 variables will need 68 data #
# sets.                                                  #
# ------------------------------------------------------ #

require 'nokogiri'    

def farm(url)
puts url
  html = ScraperWiki::scrape(url)
  doc = Nokogiri::HTML html

  doc.search("div[@width='500'] tr").each do |v|
    cells = v.search 'td'
    data = {
      fist: cells[0].inner_html,
    }
    puts data.to_json
  end
end

# def extract(url)
# puts url
#  html = ScraperWiki::scrape(url)
#  doc = Nokogiri::HTML html
#  doc.search("div[@id='contMain'] table").each do |v|
#    cells = v.search 'td'
#    data = {
#      day: File.basename(url),
#      desc: cells[3].content()
#    }
#    puts data
#    data.to_json
#    ScraperWiki::save_sqlite(['day'], data)
#    break
#  end
#end

accounts = ["http://liveweb.archive.org/http://www.wanderlustgame.com/profile-awards.php?username=76561198016008224"]

#accounts = ["http://www.wanderlustgame.com/profile.php?username=76561198016008224",
#        "http://www.wanderlustgame.com/profile-awards.php?username=Mochafox",
#        "http://www.wanderlustgame.com/profile-awards.php?username=Ulanderdennis"]

accounts.each do |url| 
  farm url
end

# ------------------------------------------------------------------------
# ------------------------------------------------------------------------
# ------------------------------------------------------------------------

#require 'rubygems'
#require 'hpricot'

#html = ScraperWiki::scrape("http://m.london2012.com/medals/medal-count/") 
#doc = Hpricot(html)
#doc.search('//*[@id="overall_medals"]/table/tbody/tr').each do |row|
#  country = {
#    :name   => row.search("/td[2]/div/text()").first.to_plain_text,
#    :gold   => row.search(".or-gold").first.inner_html.to_i,
#    :silver => row.search(".or-silver").first.inner_html.to_i,
#    :bronze => row.search(".or-bronze").first.inner_html.to_i,
#    :total  => row.search(".or-total").first.inner_html.to_i
#  }
#  ScraperWiki::save_sqlite(['name'], country)
#end
