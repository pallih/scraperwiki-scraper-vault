require 'nokogiri'

cats = ScraperWiki.scrape('http://www2.co.multnomah.or.us/AnimalWeb/Default.aspx?ListBox1=2')

doc = Nokogiri::HTML(cats)
doc.search('#dgAdoptables').children.each do |tr|  
  cat = {}
  photo = tr.search('img')
  photo_url = photo[3].attr('src').split('file=')[1].downcase if photo.length > 0
  cat['photo'] = "http://www2.co.multnomah.or.us/AnimalWeb/#{photo_url}" if photo_url
  info = tr.content.each_line.map(&:strip).delete_if {|l| l.strip == ""}
  %w(name-0 gender-3 breed-4 age-5 weight-6).each do |attr|
    d = attr.split('-')
    if info[d[1].to_i]
      if info[d[1].to_i] =~ /:/
        cat[d[0]] = info[d[1].to_i].split(':')[1].strip.downcase
      else
        cat[d[0]] = info[d[1].to_i].strip.downcase
      end
    end
  end
  ScraperWiki.save(unique_keys=cat.keys.map(&:to_s), data=cat)
end
