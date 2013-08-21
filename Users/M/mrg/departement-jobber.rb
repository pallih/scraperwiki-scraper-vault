require 'nokogiri'
require 'open-uri'

def main
  # need to fake user agent :/
  doc = Nokogiri::HTML(open('http://www.jobbnorge.no/employerprofile.aspx?empID=1328', 'User-Agent' => 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:13.0) Gecko/20100101 Firefox/13.0.1').read)
  
  doc.css('#tblJobs tbody tr').each do |el|
    el.at_css('a')['href'] =~ /jobid=(\d+)$/

    if $1 then
      title = el.at_css('td:nth-child(1)').inner_text
      org = el.at_css('td:nth-child(2)').inner_text
      deadline = Date.parse(el.at_css('td:nth-child(4)').inner_text)
      url = "http://www.jobbnorge.no" + el.at_css('a')['href']

      data = ['id' => $1, 'title' => title, 'organization' => org, 'deadline' => deadline, 'url' => url, 'scrapestamputc' => DateTime.now]
      ScraperWiki::save(['id'], data)
    end
  end
end

main