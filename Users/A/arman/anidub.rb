# Blank Ruby
require 'nokogiri'
require 'typhoeus'

home_url = 'http://online.anidub.com'

def get_html_doc(url)
  html = Typhoeus::Request.get url
  Nokogiri::HTML html.body
end

def get_anime_list(doc)
  doc.css('.title a').map {|a| a.attr('href')}
end

def get_player_links(doc)
  doc.css('select#sel option').map{|opt| opt.attr('value')}.to_json
end
def get_video_links(id, doc)
  doc.css('select#sel option').map do |opt|
    raw_link = opt.attr('value').split('|')
    #ScraperWiki::save_sqlite(
    #  [:episode, :anime_id], {:id => raw_link[1], :link => raw_link[0], :anime_id => id }, 'videos'
    #)
    {:episode => raw_link[1], :link => raw_link[0], :anime_id => id }
  end
end
def get_anime_data(url, doc)
  if doc.css('.r_col > noindex .info').empty? 
    data = {
      :id => url[/\d+(?=-)/].to_i,
      :url => url,
      :title => (doc.css('.titlfull').text if doc.css('.titlfull').any?),
      :description => (doc.css('.maincont div')[2].text if doc.css('.maincont div')[2].any?),
      :poster => (doc.css('div.maincont div.poster_img img').attr('src').value\
                 if doc.css('div.maincont div.poster_img img').any?),
      :year => (doc.css('div.maincont ul.reset li')[0].css('span a').text\
               if doc.css('div.maincont ul.reset li')[0].css('span a').any?),
      :genre => (doc.css('div.maincont ul.reset li')[1].css('span a').map{|genre| genre.text}.join(',')\
                if doc.css('div.maincont ul.reset li')[1].css('span a').any?),
      :country => (doc.css('div.maincont ul.reset li')[2].css('span').text\
                  if doc.css('div.maincont ul.reset li')[2].css('span').any?),
      :release_date => (doc.css('div.maincont ul.reset li')[4].css('span').text\
                      if doc.css('div.maincont ul.reset li')[4].css('span').any?),
      :director => (doc.css('div.maincont ul.reset li')[5].css('span a').text\
                  if doc.css('div.maincont ul.reset li')[5].css('span a').any?),
      :author => (doc.css('div.maincont ul.reset li')[6].css('span a').text\
                if doc.css('div.maincont ul.reset li')[6].css('span a').any?),
      :voice => (doc.css('div.maincont ul.reset li')[7].css('span a').map{|voice| voice.text}.join(',')\
                if doc.css('div.maincont ul.reset li')[7].css('span a').any?),
      :trabslated_by => (doc.css('div.maincont ul.reset li')[8].css('span a').map{|tr|tr.text}.join(',')\
                        if doc.css('div.maincont ul.reset li')[8].css('span a').any?),
      :studio => (doc.css('div.maincont div.video_info a img').attr('alt').value\
                 if doc.css('div.maincont div.video_info a img').any?),
      :updated_at => DateTime.now.to_date.to_s
    }
  end
  data
end


doc = get_html_doc(home_url)

years_links = doc.css('.submenu ul.reset li').select do |li|
  li.css('a').attr('href').value =~ /\/\d/
end.map!{|li| li.css('a').attr('href').value}


anime_list = []


years_links.each do |year|
  y_url = home_url + year
  doc = get_html_doc y_url
  get_anime_list(doc).each do |anime_url|
    doc = get_html_doc(anime_url) 
    anime_data = get_anime_data(anime_url, doc)
    ScraperWiki::save_sqlite([:id], anime_data, 'anidub.anime')
    anime_video_links = get_video_links(anime_data[:id], doc)
    ScraperWiki::save_sqlite([:episode, :anime_id], anime_video_links, 'anidub.videos')
  end
  p anime_list = anime_list + get_anime_list(doc)
  pages_count = doc.css('span.navigation a').last.text.to_i

  2.upto pages_count do |page|
    url = y_url + 'page/' + page.to_s
    
    doc = get_html_doc(url)
    p anime_list = anime_list + get_anime_list(doc)

    get_anime_list(doc).each do |anime_url|
      doc = get_html_doc(anime_url)
      anime_data = get_anime_data(anime_url, doc)
      ScraperWiki::save_sqlite([:id], anime_data, 'anidub.anime')
      anime_video_links = get_video_links(anime_data[:id], doc)
      ScraperWiki::save_sqlite([:episode, :anime_id], anime_video_links, 'anidub.videos')
    end

  end

end
p anime_list.count












#html = Typhoeus::Request.get 'http://online.anidub.com/anime_tv/8378-skazka-o-hvoste-fei-fairy-tail.html'
#doc = Nokogiri::HTML html.body

#urls = doc.css('select#sel option').map do |opt|
#  raw_link = opt.attr('value').split('|')
#  {raw_link[1].to_sym => raw_link[0]}
#end


#[/.+(?=\|)/]}
#p urls.to_json
#videos = []
#urls.each do |url|
#  videos.push Nokogiri::HTML Typhoeus::Request.get(url).body
#end
#videos.each do |video|
#  player = video.css('#flash_video_obj')
#  p CGI::parse(player.attr('flashvars').value).select{|k,v| k=~/url\d/}.to_json unless player.nil? 
#end

# Blank Ruby
require 'nokogiri'
require 'typhoeus'

home_url = 'http://online.anidub.com'

def get_html_doc(url)
  html = Typhoeus::Request.get url
  Nokogiri::HTML html.body
end

def get_anime_list(doc)
  doc.css('.title a').map {|a| a.attr('href')}
end

def get_player_links(doc)
  doc.css('select#sel option').map{|opt| opt.attr('value')}.to_json
end
def get_video_links(id, doc)
  doc.css('select#sel option').map do |opt|
    raw_link = opt.attr('value').split('|')
    #ScraperWiki::save_sqlite(
    #  [:episode, :anime_id], {:id => raw_link[1], :link => raw_link[0], :anime_id => id }, 'videos'
    #)
    {:episode => raw_link[1], :link => raw_link[0], :anime_id => id }
  end
end
def get_anime_data(url, doc)
  if doc.css('.r_col > noindex .info').empty? 
    data = {
      :id => url[/\d+(?=-)/].to_i,
      :url => url,
      :title => (doc.css('.titlfull').text if doc.css('.titlfull').any?),
      :description => (doc.css('.maincont div')[2].text if doc.css('.maincont div')[2].any?),
      :poster => (doc.css('div.maincont div.poster_img img').attr('src').value\
                 if doc.css('div.maincont div.poster_img img').any?),
      :year => (doc.css('div.maincont ul.reset li')[0].css('span a').text\
               if doc.css('div.maincont ul.reset li')[0].css('span a').any?),
      :genre => (doc.css('div.maincont ul.reset li')[1].css('span a').map{|genre| genre.text}.join(',')\
                if doc.css('div.maincont ul.reset li')[1].css('span a').any?),
      :country => (doc.css('div.maincont ul.reset li')[2].css('span').text\
                  if doc.css('div.maincont ul.reset li')[2].css('span').any?),
      :release_date => (doc.css('div.maincont ul.reset li')[4].css('span').text\
                      if doc.css('div.maincont ul.reset li')[4].css('span').any?),
      :director => (doc.css('div.maincont ul.reset li')[5].css('span a').text\
                  if doc.css('div.maincont ul.reset li')[5].css('span a').any?),
      :author => (doc.css('div.maincont ul.reset li')[6].css('span a').text\
                if doc.css('div.maincont ul.reset li')[6].css('span a').any?),
      :voice => (doc.css('div.maincont ul.reset li')[7].css('span a').map{|voice| voice.text}.join(',')\
                if doc.css('div.maincont ul.reset li')[7].css('span a').any?),
      :trabslated_by => (doc.css('div.maincont ul.reset li')[8].css('span a').map{|tr|tr.text}.join(',')\
                        if doc.css('div.maincont ul.reset li')[8].css('span a').any?),
      :studio => (doc.css('div.maincont div.video_info a img').attr('alt').value\
                 if doc.css('div.maincont div.video_info a img').any?),
      :updated_at => DateTime.now.to_date.to_s
    }
  end
  data
end


doc = get_html_doc(home_url)

years_links = doc.css('.submenu ul.reset li').select do |li|
  li.css('a').attr('href').value =~ /\/\d/
end.map!{|li| li.css('a').attr('href').value}


anime_list = []


years_links.each do |year|
  y_url = home_url + year
  doc = get_html_doc y_url
  get_anime_list(doc).each do |anime_url|
    doc = get_html_doc(anime_url) 
    anime_data = get_anime_data(anime_url, doc)
    ScraperWiki::save_sqlite([:id], anime_data, 'anidub.anime')
    anime_video_links = get_video_links(anime_data[:id], doc)
    ScraperWiki::save_sqlite([:episode, :anime_id], anime_video_links, 'anidub.videos')
  end
  p anime_list = anime_list + get_anime_list(doc)
  pages_count = doc.css('span.navigation a').last.text.to_i

  2.upto pages_count do |page|
    url = y_url + 'page/' + page.to_s
    
    doc = get_html_doc(url)
    p anime_list = anime_list + get_anime_list(doc)

    get_anime_list(doc).each do |anime_url|
      doc = get_html_doc(anime_url)
      anime_data = get_anime_data(anime_url, doc)
      ScraperWiki::save_sqlite([:id], anime_data, 'anidub.anime')
      anime_video_links = get_video_links(anime_data[:id], doc)
      ScraperWiki::save_sqlite([:episode, :anime_id], anime_video_links, 'anidub.videos')
    end

  end

end
p anime_list.count












#html = Typhoeus::Request.get 'http://online.anidub.com/anime_tv/8378-skazka-o-hvoste-fei-fairy-tail.html'
#doc = Nokogiri::HTML html.body

#urls = doc.css('select#sel option').map do |opt|
#  raw_link = opt.attr('value').split('|')
#  {raw_link[1].to_sym => raw_link[0]}
#end


#[/.+(?=\|)/]}
#p urls.to_json
#videos = []
#urls.each do |url|
#  videos.push Nokogiri::HTML Typhoeus::Request.get(url).body
#end
#videos.each do |video|
#  player = video.css('#flash_video_obj')
#  p CGI::parse(player.attr('flashvars').value).select{|k,v| k=~/url\d/}.to_json unless player.nil? 
#end

require 'mechanize'

@agent = Mechanize.new
@@logged_in = false
home_url = 'http://online.anidub.com'

def get_html_doc(url)
  unless @@logged_in
    login_form = @agent.get(url).form
    login_form.login_name = 'reignmaker'
    login_form.login_password = '7u8aa8aq84f'
    doc = @agent.submit(login_form, login_form.buttons.first)
    @@logged_in  = true
    p doc.search('#userlogin a strong').text
    return doc
  end
  @agent.get(url)
  rescue
  @agent.get(url)
end

def get_anime_list(doc)
  doc.search('.title a').map {|a| a.attr('href')}
end

def get_player_links(doc)
  doc.search('select#sel option').map{|opt| opt.attr('value')}.to_json
end

def get_video_links(id, doc)
  doc.search('select#sel option').map do |opt|
    raw_link = opt.attr('value').split('|')
    {:episode => raw_link[1], :link => raw_link[0], :anime_id => id }
  end
end

def get_anime_data(url, doc)
  if doc.search('.r_col > noindex .info').empty? 
    data = {}
      data[:id] = url[/\d+(?=-)/].to_i
      data[:url] = url
      data[:title] = doc.search('.titlfull').any? ? doc.search('.titlfull').text : ''
      data[:description] = doc.search('div[itemprop="description"]').any? ? \
          doc.search('div[itemprop="description"]').text : ''
      data[:poster] = doc.search('div.maincont div.poster_img img').any? ? \
          doc.search('div.maincont div.poster_img img').attr('src').value : ''
      data[:year] = doc.search('div.maincont ul.reset li')[0].search('span a').any? ? \
          doc.search('div.maincont ul.reset li')[0].search('span a').text : ''
      data[:genre] = doc.search('div.maincont ul.reset li')[1].search('span a').any? ? \
          doc.search('div.maincont ul.reset li')[1].search('span a').map{|genre| genre.text}.join(',') :''
      data[:country] = doc.search('div.maincont ul.reset li')[2].search('span').any? ? \
          doc.search('div.maincont ul.reset li')[2].search('span').text : ''
      data[:release_date] = doc.search('div.maincont ul.reset li')[4].search('span').any? ? \
          doc.search('div.maincont ul.reset li')[4].search('span').text : ''
      data[:director] = doc.search('div.maincont ul.reset li')[5].search('span a').any? ? \
          doc.search('div.maincont ul.reset li')[5].search('span a').text : ''
      data[:author] = doc.search('div.maincont ul.reset li')[6].search('span a').any? ? \
          doc.search('div.maincont ul.reset li')[6].search('span a').text : ''
      data[:voice] = doc.search('div.maincont ul.reset li')[7].search('span a').any? ? \
          doc.search('div.maincont ul.reset li')[7].search('span a').map{|voice| voice.text}.join(',') : ''
      data[:trabslated_by] = doc.search('div.maincont ul.reset li')[8].search('span a').any? ? \
          doc.search('div.maincont ul.reset li')[8].search('span a').map{|tr|tr.text}.join(',') : ''
      data[:studio] = doc.search('div.maincont div.video_info a img').any? ? \
          doc.search('div.maincont div.video_info a img').attr('alt').value : ''
      data[:updated_at] = DateTime.now.to_date.to_s
  end
  data
end


doc = get_html_doc(home_url)

years_links = doc.search('.submenu ul.reset li').select do |li|
  li.search('a').attr('href').value =~ /\/\d/
end.map!{|li| li.search('a').attr('href').value}


anime_list = []


years_links.each do |year|
  y_url = home_url + year
  doc = get_html_doc y_url
  get_anime_list(doc).each do |anime_url|
    doc = get_html_doc(anime_url)
    anime_data = get_anime_data(anime_url, doc)
    ScraperWiki::save_sqlite([:id], anime_data, 'anidub.anime')
    anime_video_links = get_video_links(anime_data[:id], doc)
    ScraperWiki::save_sqlite([:episode, :anime_id], anime_video_links, 'anidub.videos')
  end
  pages_count = doc.search('span.navigation a').last.text.to_i

  2.upto pages_count do |page|
    url = y_url + 'page/' + page.to_s
    
    doc = get_html_doc(url)

    get_anime_list(doc).each do |anime_url|
      doc = get_html_doc(anime_url)
      anime_data = get_anime_data(anime_url, doc)
      ScraperWiki::save_sqlite([:id], anime_data, 'anidub.anime')
      anime_video_links = get_video_links(anime_data[:id], doc)
      ScraperWiki::save_sqlite([:episode, :anime_id], anime_video_links, 'anidub.videos')
    end

  end

end












#html = Typhoeus::Request.get 'http://online.anidub.com/anime_tv/8378-skazka-o-hvoste-fei-fairy-tail.html'
#doc = Nokogiri::HTML html.body

#urls = doc.search('select#sel option').map do |opt|
#  raw_link = opt.attr('value').split('|')
#  {raw_link[1].to_sym => raw_link[0]}
#end


#[/.+(?=\|)/]}
#p urls.to_json
#videos = []
#urls.each do |url|
#  videos.push Nokogiri::HTML Typhoeus::Request.get(url).body
#end
#videos.each do |video|
#  player = video.search('#flash_video_obj')
#  p CGI::parse(player.attr('flashvars').value).select{|k,v| k=~/url\d/}.to_json unless player.nil?
#end

require 'mechanize'

@agent = Mechanize.new
@@logged_in = false
home_url = 'http://online.anidub.com'
ANIME_TYPES = %w( /anime_tv/ /anime_movie/ /anime_ova/ )

def get_html_doc(url)
  unless @@logged_in
    login_form = @agent.get(url).form
    login_form.login_name = 'reignmaker'
    login_form.login_password = '7u8aa8aq84f'
    doc = @agent.submit(login_form, login_form.buttons.first)
    @@logged_in  = true
    p doc.search('#userlogin a strong').text
    return doc
  end
  @agent.get(url)
  rescue
  @agent.get(url)
end

def get_anime_list(doc)
  doc.search('.title a').map {|a| a.attr('href')}
end

def get_player_links(doc)
  doc.search('select#sel option').map{|opt| opt.attr('value')}.to_json
end

def get_video_links(id, doc)
  if (links = doc.search('select#sel option')) && links.length > 0
    links.map do |opt|
      raw_link = opt.attr('value').split('|')
      { :episode => raw_link[1], :link => raw_link[0], :anime_id => id }
    end
  elsif (link = doc.search('.vk_onefilm iframe')) && link.length > 0
    p link
    { :episode => 0, :link => link.attr('src').value, :anime_id => id }
  end
end

def get_anime_data(url, doc)
  if doc.search('.r_col > noindex .info').empty? 
    data = {}
      data[:id] = url[/\d+(?=-)/].to_i
      data[:url] = url
      data[:title] = doc.search('.titlfull').any? ? doc.search('.titlfull').text : ''
      data[:description] = doc.search('div[itemprop="description"]').any? ? \
          doc.search('div[itemprop="description"]').text : ''
      data[:poster] = doc.search('div.maincont div.poster_img img').any? ? \
          doc.search('div.maincont div.poster_img img').attr('src').value : ''
      data[:year] = doc.search('div.maincont ul.reset li')[0].search('span a').any? ? \
          doc.search('div.maincont ul.reset li')[0].search('span a').text : ''
      data[:genre] = doc.search('div.maincont ul.reset li')[1].search('span a').any? ? \
          doc.search('div.maincont ul.reset li')[1].search('span a').map{|genre| genre.text}.join(',') :''
      data[:country] = doc.search('div.maincont ul.reset li')[2].search('span').any? ? \
          doc.search('div.maincont ul.reset li')[2].search('span').text : ''
      data[:release_date] = doc.search('div.maincont ul.reset li')[4].search('span').any? ? \
          doc.search('div.maincont ul.reset li')[4].search('span').text : ''
      data[:director] = doc.search('div.maincont ul.reset li')[5].search('span a').any? ? \
          doc.search('div.maincont ul.reset li')[5].search('span a').text : ''
      data[:author] = doc.search('div.maincont ul.reset li')[6].search('span a').any? ? \
          doc.search('div.maincont ul.reset li')[6].search('span a').text : ''
      data[:voice] = doc.search('div.maincont ul.reset li')[7].search('span a').any? ? \
          doc.search('div.maincont ul.reset li')[7].search('span a').map{|voice| voice.text}.join(',') : ''
      data[:trabslated_by] = doc.search('div.maincont ul.reset li')[8].any? ? \
          doc.search('div.maincont ul.reset li')[8].search('span a').map{|tr|tr.text}.join(',') : ''
      data[:studio] = doc.search('div.maincont div.video_info a img').any? ? \
          doc.search('div.maincont div.video_info a img').attr('alt').value : ''
      data[:votes] = doc.search('[id*="vote-num"]').text
      data[:updated_at] = DateTime.now.to_date.to_s
  end
  data
end


ANIME_TYPES.each do |anime_type|
  anime_type_url = home_url + anime_type
  doc = get_html_doc(anime_type_url)
  get_anime_list(doc).each do |anime_url|
p 'anime url: '+ anime_url
    doc = get_html_doc(anime_url)
    anime_data = get_anime_data(anime_url, doc)
    ScraperWiki::save_sqlite([:id], anime_data, 'anidub.anime')
    anime_video_links = get_video_links(anime_data[:id], doc)
    ScraperWiki::save_sqlite([:episode, :anime_id], anime_video_links, 'anidub.videos')
  end
  pages_count = doc.search('span.navigation a').last.text.to_i

  2.upto pages_count do |page|
    url = anime_type_url + 'page/' + page.to_s + '/'
    p url
    doc = get_html_doc(url)

    get_anime_list(doc).each do |anime_url|
      doc = get_html_doc(anime_url)
      anime_data = get_anime_data(anime_url, doc)
      ScraperWiki::save_sqlite([:id], anime_data, 'anidub.anime')
      anime_video_links = get_video_links(anime_data[:id], doc)
      ScraperWiki::save_sqlite([:episode, :anime_id], anime_video_links, 'anidub.videos')
    end

  end

end
