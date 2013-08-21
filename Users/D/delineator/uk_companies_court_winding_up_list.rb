# encoding: utf-8
# Companies Court Winding Up List

require 'date'
require 'open-uri'
require 'nokogiri'
require 'json'
require 'openssl'
OpenSSL::SSL::VERIFY_PEER = OpenSSL::SSL::VERIFY_NONE


module WindingUpList
  extend self

  def load
    html = open('http://www.justice.gov.uk/courts/court-lists/list-companies-winding-up').read
    @doc = Nokogiri::HTML html.gsub('&nbsp;','±')
    self
  end
  
  def date
    find(/^(Monday|Tuesday|Wednesday|Thursday|Friday)/, 'strong').first.inner_text.gsub('±',' ').strip
  end

  def items
    items = find(/^\d+\./)
    items.map! {|x| x.inner_text}
    items.map! {|p| p.squeeze('±').gsub('± ±','±').split('±').map{|x| x.strip} }
    items.map! do |x|
      if x.size == 5
        last = x.pop
        company = x.pop
        x << [company, last].join(' ').squeeze(' ')
      end
      x
    end
    items.map! do |x|
      puts x.inspect
      company = x[3]
      item = {
        'date' => date,
        'court_date' => Date.parse(date),
        'company' => company,
        'opencorporates_uri' => opencorporates_uri(company, date),
        'position' => x[0],
        'number' => x[1],
        'year' => x[2],
        'updated_at_time' => updated_at_time,
        'updated_at_date' => Date.parse(updated_at_date)
      }
      yield item
      item
    end
    items
  end
    
  def updated_at_time
    updated.split.pop
  end

  def updated_at_date
    parts = updated.split
    parts.pop
    parts.join(' ')
  end

  private

  def updated
    @updated ||= find(/^Updated: (.+)/).first.inner_text[/^Updated: ([^(]+)/,1].strip
  end

  def find regexp, tag='p'
    @doc.search(tag).select {|p| p.inner_text.gsub('±',' ').strip[regexp]}
  end

  def opencorporates_uri name, date
    if existing = ScraperWiki::select(%Q|* from db.swdata where date = "#{date}" and company = "#{name.gsub('"','')}"|).first
      if uri = existing['opencorporates_uri']
        return uri
      end
    end

    begin
      sleep 3
      search_name = URI.encode(name)
      api = "http://api.opencorporates.com/v0.2/companies/search?q=#{search_name}&order=score&jurisdiction_code=gb"
      j = JSON.parse open(api).read
      j.delete('api_version')
      
      eval( open('https://raw.github.com/robmckinnon/morph/master/lib/morph.rb').read ) unless defined? Morph

      r = Morph.from_hash j
      puts api
      puts name
      puts j.inspect

      if r = ( find_company(r, name) || find_company(r, name.sub('Ltd','Limited')) || find_company(r, name.sub('Limited','Ltd')) )
        uri = r.company.opencorporates_url
        puts uri
        return uri
      end
    rescue Exception => e
      puts e.to_s
      nil
    end
  end

  def find_company r, name
    company = r.companies.detect {|x| x.company.name.chomp('.') == name.upcase.chomp('.') }

    company = r.companies.detect {|x| x.company.name.chomp('.').tr(' ','') == name.upcase.chomp('.').tr(' ','') } unless company

    company
  end
end

ScraperWiki::attach("uk_companies_court_winding_up_list", "db")

WindingUpList.load.items do |item|
  ScraperWiki::save_sqlite(['date','company'], item)
end
