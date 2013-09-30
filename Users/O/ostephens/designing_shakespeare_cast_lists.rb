require 'nokogiri'
require 'uri'
require 'open-uri'

class DSPlay
    def initialize(title, uri, nprods)
        @title = title
        @uri = uri
        @nprods = nprods
        @perfs = []
    end
    
    attr_reader :title, :uri, :prods
    attr_accessor :perfs
    
    def getPerfs
      begin
        prodpage = Nokogiri::HTML(open(@uri))
        prodpage.xpath('//div[@class="main01"]/table[1]/tr/td/a').each do |perf|
          performance = perf.inner_text
          path = perf.attributes['href']
          @perfs.push(DSPerfs.new(performance,path))
        end
      rescue
        puts "Error while getting " + @uri
      end
    end
end

class DSPerfs
  def initialize(performance,path)
    @performance = performance
    @path = path
    @cast = []
  end

  attr_reader :performance, :path, :cast

  def getCast(base)
    begin
      prodpage = Nokogiri::HTML(open(base+@path))
      prodpage.xpath('//table').each do |table|
        if table.inner_text.to_s[0,4] == "Cast"
          table.xpath('tr').each do |casting|
            actor = casting.xpath('td[1]').inner_text
            role = casting.xpath('td[2]').inner_text
            @cast.push(DSCast.new(actor,role))
          end
        end
      end
    rescue
      puts "Error while getting " + base + @path
   end
  end

end

class DSCast
  def initialize(actor,role)
    @actor = actor
    @role = role
  end
  
  attr_reader :actor, :role

end

base_url = "http://www.ahds.rhul.ac.uk/ahdscollections/docroot/shakespeare/"
index_page = "playslist.do"
index_doc = Nokogiri::HTML(open(base_url + index_page))
plays = []

index_doc.xpath('//table[1]/tr/td/a').each do |pages|
  play_url = pages.attributes['href']
  title = pages.inner_text.split('(')[0]
  prods = pages.inner_text.split('(')[1].to_s.to_s.chomp("Productions)")
  uri = base_url + play_url
  if title.to_s.length > 0
    plays.push(DSPlay.new(title,uri,prods))
  end
end
 
plays.each do |play|
  play.getPerfs
  play.perfs.each do |perf|
    perf.getCast(base_url)
    perf.cast.each do |castmem|
      data = {
      play: play.title.to_s,
      play_uri: play.uri.to_s,
      performance: perf.performance.to_s,
      performance_uri: base_url+perf.path.to_s,
      actor: castmem.actor.to_s,
      role: castmem.role.to_s
      }
      ScraperWiki::save_sqlite([], data) 
    end
  end
end
#thes_urls.each do |url|
#  html = ScraperWiki.scrape(url)
#  doc = Nokogiri::HTML(html)
#  doc.xpath("//b[not(*)]").each do |terms|
#      term = BMTerm.new(terms.inner_text.downcase)
#      term.getURIfromlabel
#      term.checkFinds
#      begin
#        ScraperWiki.save(unique_keys=['term'], data={'term' => term.label,'uri' => term.uri, 'finds_uri' => term.finds})
#        sleep 1
#      rescue
#        puts "Unable to save record for " + term.label
#      end
#  end
#end

require 'nokogiri'
require 'uri'
require 'open-uri'

class DSPlay
    def initialize(title, uri, nprods)
        @title = title
        @uri = uri
        @nprods = nprods
        @perfs = []
    end
    
    attr_reader :title, :uri, :prods
    attr_accessor :perfs
    
    def getPerfs
      begin
        prodpage = Nokogiri::HTML(open(@uri))
        prodpage.xpath('//div[@class="main01"]/table[1]/tr/td/a').each do |perf|
          performance = perf.inner_text
          path = perf.attributes['href']
          @perfs.push(DSPerfs.new(performance,path))
        end
      rescue
        puts "Error while getting " + @uri
      end
    end
end

class DSPerfs
  def initialize(performance,path)
    @performance = performance
    @path = path
    @cast = []
  end

  attr_reader :performance, :path, :cast

  def getCast(base)
    begin
      prodpage = Nokogiri::HTML(open(base+@path))
      prodpage.xpath('//table').each do |table|
        if table.inner_text.to_s[0,4] == "Cast"
          table.xpath('tr').each do |casting|
            actor = casting.xpath('td[1]').inner_text
            role = casting.xpath('td[2]').inner_text
            @cast.push(DSCast.new(actor,role))
          end
        end
      end
    rescue
      puts "Error while getting " + base + @path
   end
  end

end

class DSCast
  def initialize(actor,role)
    @actor = actor
    @role = role
  end
  
  attr_reader :actor, :role

end

base_url = "http://www.ahds.rhul.ac.uk/ahdscollections/docroot/shakespeare/"
index_page = "playslist.do"
index_doc = Nokogiri::HTML(open(base_url + index_page))
plays = []

index_doc.xpath('//table[1]/tr/td/a').each do |pages|
  play_url = pages.attributes['href']
  title = pages.inner_text.split('(')[0]
  prods = pages.inner_text.split('(')[1].to_s.to_s.chomp("Productions)")
  uri = base_url + play_url
  if title.to_s.length > 0
    plays.push(DSPlay.new(title,uri,prods))
  end
end
 
plays.each do |play|
  play.getPerfs
  play.perfs.each do |perf|
    perf.getCast(base_url)
    perf.cast.each do |castmem|
      data = {
      play: play.title.to_s,
      play_uri: play.uri.to_s,
      performance: perf.performance.to_s,
      performance_uri: base_url+perf.path.to_s,
      actor: castmem.actor.to_s,
      role: castmem.role.to_s
      }
      ScraperWiki::save_sqlite([], data) 
    end
  end
end
#thes_urls.each do |url|
#  html = ScraperWiki.scrape(url)
#  doc = Nokogiri::HTML(html)
#  doc.xpath("//b[not(*)]").each do |terms|
#      term = BMTerm.new(terms.inner_text.downcase)
#      term.getURIfromlabel
#      term.checkFinds
#      begin
#        ScraperWiki.save(unique_keys=['term'], data={'term' => term.label,'uri' => term.uri, 'finds_uri' => term.finds})
#        sleep 1
#      rescue
#        puts "Unable to save record for " + term.label
#      end
#  end
#end

