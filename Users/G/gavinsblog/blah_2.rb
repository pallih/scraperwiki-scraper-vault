require 'scraperwiki'
require 'mechanize'
require 'open-uri'

ua = Mechanize.new
ua.user_agent_alias = 'Mac Safari'

cookie = Mechanize::Cookie.new('pren_terms_accepted', '1')
cookie.domain = 'http://www.nama.ie'
cookie.path = '/'
ua.cookie_jar.add(URI.parse('http://www.nama.ie/'), cookie)

page = ua.get('http://www.nama.ie/about-our-work/properties-enforced/properties-subject-to-enforcement-action/?display=all&x=1')

page.root.css('.pren-property h2') do |item| 

p item.text

ScraperWiki.save([:data], {data: item.inner_html})

end