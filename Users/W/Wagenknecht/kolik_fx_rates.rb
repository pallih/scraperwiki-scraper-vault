# Blank Ruby
require 'nokogiri'           

def doit(direction,currency)

time = Time.new
yr = time.year
mo = time.month
#return


url_template = 'http://kolik.cz/psupp/vypocet_valuta.php?operation=%s&amount=10%%20000&currency=%s'
url = url_template % [ direction, currency ]

html = ScraperWiki::scrape(url)

#p html

doc = Nokogiri::HTML(html, nil, "utf-8")
doc.search("tbody tr").each do |v|
  cells = v.search 'td'
  if cells.count == 7
    fx_s = cells[0].search("a").inner_html
    if fx_s =~ /</
      fx_s[/\ \*.*/] = ""
      fx_s[/<.*?>/] = ""
    end
    day_s = cells[3].inner_html
    dd = day_s[/([0-9]*)\. *[0-9]*\./,1].to_i
    mm = day_s[/[0-9]*\. *([0-9]*)\./,1].to_i
    yy = yr - ((mm > mo) ?  1 : 0)
    data = {
      fx: fx_s,
      dir: direction,
      curr: currency,
      day: "%d-%02d-%02d" % [ yy, mm, dd ],
      rate: cells[2].inner_html,
      net_rate: cells[4].inner_html,
    }
    #puts data.to_json
    ScraperWiki::save_sqlite(['fx','day','curr','dir'], data)
  end
end

end

['buy','sell'].each do |d|
  ['USD','EUR'].each do |c|
    doit(d,c)
  end
end

#p "a=%s&s=%s" % ['a', 'b']
#doit('buy','USD')# Blank Ruby
require 'nokogiri'           

def doit(direction,currency)

time = Time.new
yr = time.year
mo = time.month
#return


url_template = 'http://kolik.cz/psupp/vypocet_valuta.php?operation=%s&amount=10%%20000&currency=%s'
url = url_template % [ direction, currency ]

html = ScraperWiki::scrape(url)

#p html

doc = Nokogiri::HTML(html, nil, "utf-8")
doc.search("tbody tr").each do |v|
  cells = v.search 'td'
  if cells.count == 7
    fx_s = cells[0].search("a").inner_html
    if fx_s =~ /</
      fx_s[/\ \*.*/] = ""
      fx_s[/<.*?>/] = ""
    end
    day_s = cells[3].inner_html
    dd = day_s[/([0-9]*)\. *[0-9]*\./,1].to_i
    mm = day_s[/[0-9]*\. *([0-9]*)\./,1].to_i
    yy = yr - ((mm > mo) ?  1 : 0)
    data = {
      fx: fx_s,
      dir: direction,
      curr: currency,
      day: "%d-%02d-%02d" % [ yy, mm, dd ],
      rate: cells[2].inner_html,
      net_rate: cells[4].inner_html,
    }
    #puts data.to_json
    ScraperWiki::save_sqlite(['fx','day','curr','dir'], data)
  end
end

end

['buy','sell'].each do |d|
  ['USD','EUR'].each do |c|
    doit(d,c)
  end
end

#p "a=%s&s=%s" % ['a', 'b']
#doit('buy','USD')