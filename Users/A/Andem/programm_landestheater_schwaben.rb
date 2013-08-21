# Blank Ruby
# encoding: utf-8

require 'uri'
require 'nokogiri'  
require 'rubygems'
require 'mechanize'

def scrape(scrapurl)
  agent = Mechanize.new
  agent.get(scrapurl)
  doc= agent.page.at('html/body/table/tbody/tr[3]/td[2]')#('html/body/table/tr[3]/td[2]/table[2]')
  cont = doc.at('table[@width="100%"]')
#puts cont

  title='init'
  datum='init'
  link='init'
  uhrzeit='init'
  ort='init'

  for event in cont.search('tr')
    puts event
    datum = event.at('td/span').text
    puts 'datum: '+datum
    link = event.at('a[@class="link_block"]').attributes['href']
    puts 'link: '+'http://www.landestheater-schwaben.de'+link
    elemdesc = event.at('td[2]')
#    @chapters = elemdesc.children.inject([]) do |chapters_hash, child|
#      if child['class'] == 'ueberschrift'   #if child.name == 'span[@class="ueberschrift"]'
#        title = child.inner_text
#        chapters_hash << { :title => title, :contents => ''}
#      end
#       next chapters_hash if chapters_hash.empty? 
#       chapters_hash.last[:contents] << child.to_xhtml
#       chapters_hash
#    end


    elemdesc.inner_html.split(/<br>\s*<br>/).collect do |fragment|
      puts 'fragment'
      puts fragment

      titElement = Nokogiri::HTML(fragment).at('span[@class="ueberschrift"]')
puts '1'
      if titElement == nil
        titElement=Nokogiri::HTML(fragment) #.at('text()')
      end
puts '2'
      title = titElement.text()
      puts 'title: '+title
        uhrzeit=''
        ort=''
      if fragment.strip == ''
      else
        fragment.scan(/\d\d:\d\d Uhr [I\|][^<]*/).collect do |fragfrag|
          #puts 'fragfrag'+fragfrag
          regsplit = /(\d\d:\d\d) Uhr [I\|]([^<]*)/
          uhrzeit = fragfrag[regsplit,1]
          puts 'uhr: '+uhrzeit
          ort = fragfrag[regsplit,2]
          puts 'ort: '+ort
      end

 puts 'vordata'
    data = {
     # 'imgurl' => base+imgurl,
      'name' => title.encode("UTF-8"), 
      'datum' => datum,
      'zeit' => uhrzeit,
      'ort' => ort.encode("UTF-8")#,
    #  'preis' => preis,#zeitpreis.text.split(") "),
    #  'desc' => desc,
#      'url' => 'http://www.landestheater-schwaben.de'+link
    }
    ScraperWiki.save_sqlite(unique_keys=['name'], data=data) 
      end

    end
   
  end
end

scrapebase = 'http://www.landestheater-schwaben.de/index.php?pg=termine/'

begin
  scrape(scrapebase +'termine_sept.php')
rescue
  puts "fehler september"
end
begin
  scrape(scrapebase +'termine_okt.php')
rescue
  puts "fehler oktober"
end
begin
  scrape(scrapebase +'termine_nov.php')
rescue
  puts "fehler november"
end
begin
  scrape(scrapebase +'termine_dez.php')
rescue
  puts "fehler dezember"
end
begin
  scrape(scrapebase +'termine_jan.php')
rescue
  puts "fehler januar"
end
begin
  scrape(scrapebase +'termine_feb.php')
rescue
  puts "fehler februar"
end
begin
  scrape(scrapebase +'termine_mrz.php')
rescue
  puts "fehler maerz" #################warum
end
begin
  scrape(scrapebase +'termine_apr.php')
rescue
  puts "fehler april"
end
begin
  scrape(scrapebase +'termine_mai.php')
rescue
  puts "fehler mai"
end
begin
  scrape(scrapebase +'termine_jun.php')
rescue
  puts "fehler juni"
end
begin
  scrape(scrapebase +'termine_jul.php')
rescue
  puts "fehler juli"
end
begin
  scrape(scrapebase +'termine_aug.php')
rescue
  puts "fehler august"
end