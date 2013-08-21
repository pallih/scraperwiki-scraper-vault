$ic = Iconv.new('UTF-8//IGNORE', 'UTF-8')

date = (Date.today + 1).strftime("%Y-%m-%d")
cont = 0
prev_first_row = ScraperWiki.get_var("prev_first_row", nil)
while cont
  html = ScraperWiki.scrape("http://sourcewell.berlios.de/index.php?start=#{ date }&days=1&cnt=#{ cont }&by=Date&SourceWell_Session=1")
  # http://po-ru.com/diary/fixing-invalid-utf-8-in-ruby-revisited/
  html = $ic.iconv(html + ' ')[0..-2]

  announcements = html.scan(/<td width="30%"><b><a href="appbyid\.php\?[^"]+id=([0-9]+)">(.+?)<\/a>.+?<p><b class="small">by <a href="mailto:.+? - [A-Za-z]+day, +([0-9]+\. [A-Za-z]+ [0-9]{4}, [0-9:]+ [^<]+)<\/b><\/p>/m)

  rows = announcements.map do |announcement|
    { "appid"=>announcement[0].strip,
      "version"=>announcement[1].strip,
      "timestamp"=>Time.parse(announcement[2].gsub("CEST", "+02:00").gsub("CET", "+0:00")) }
  end

  ScraperWiki.save_sqlite(["appid","version","timestamp"], rows)
  ScraperWiki.save_var("last_cont", cont)
  
  if cont==0 and not announcements.empty? 
    ScraperWiki.save_var("prev_first_row", rows.first["version"])
  end

  if announcements.empty? or rows.any?{|ann| ann["version"]==prev_first_row }
    cont = nil
  else
    cont += 10
  end
end

