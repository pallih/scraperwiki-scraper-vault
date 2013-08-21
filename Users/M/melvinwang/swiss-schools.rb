# swiss schools
# http://www.educa.ch/dyn/79362.asp?action=search

require 'mechanize'
require 'nokogiri'

agent = Mechanize.new

swiss = agent.get("http://www.educa.ch/dyn/79362.asp?action=search")

# get every link that says "Detail" and get the path to the detail page
details = swiss.search("a").find_all { |a|
  a.content.strip == "Detail"
}

details.each do |detail_link|
  result = {}
  # go up to the td level, and back one td
  # get name of school there
  detail_link['onclick'] =~ /(79376\.asp\?id=\d+)/
  url_fragment = $1
  
  name = detail_link.parent.previous_element.content.strip
  if name =~ /(.*)(Homepage)$/
    result['name'] = $1.strip
  else
    # it's a 2-byte space, will this be a problem in ruby 1.9?
    # (i'm guessing an nbsp thing)
    result['name'] = name.chop.chop
  end
  
  # "click" on the link (it's javascript open)
  page = agent.get("http://www.educa.ch/dyn/" + url_fragment)
  divs = page.search("div")
  # find all the leerzeile divs
  leerzeile = []
  other_divs = []
  leerzeile = divs.each do |div|
    div['class'] == "leerzeile" ? leerzeile << div : other_divs << div
  end
  
  other_divs.reverse.each do |div|
    # will we have whitespace issues?
    content = div.content.strip
    href = nil
    link = div.search("a")[0]
    href = link['href'] if link
    # also possible 2-byte space (nbsp) issue
    next if content.chop.chop == ""
    
    if content =~ /^Fax:\s*(.*)/
      result['fax'] = $1.strip
    elsif content =~ /^Tel:\s*(.*)/
      result['tel'] = $1.strip
    elsif href && href =~ /^mailto:(.*)/
      result['email'] = $1.strip
    elsif href
      result['homepage'] = href
    elsif content # content is not empty, must be address line
      if result['address']
        # reminder, we go backwards
        result['address'] = content + ", " + result['address']
      else
        result['address'] = content
      end
    end
  end

  # result.each_pair do |k,v|
    # puts "#{k}|||#{v}"
  # end
  ScraperWiki.save(result.keys, result)
end