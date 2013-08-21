# encoding: utf-8
require 'mechanize'

require 'nokogiri'
# Blank Ruby

#(md5) hash of an (associative-array) hash
def createsig(body)
  Digest::MD5.hexdigest( sigflat body )
end

def sigflat(body)
  if body.class == Hash
    arr = []
    body.each do |key, value|
      arr << "#{sigflat key}=>#{sigflat value}"
    end
    body = arr
  end
  if body.class == Array
    str = ''
    body.map! do |value|
      sigflat value
    end.sort!.each do |value|
      str << value
    end
  end
  if body.class != String
    body = body.to_s << body.class.to_s
  end
  body
end

class OutOfPagesException < Exception
end

def contents_from_body(body)
  # extract the table from a text
  doc = Nokogiri::HTML body
  maintable = doc.search("table[id='ctl00_ContentPlaceHolder3_grwIzvestaji']").first()
  if maintable.nil? 
    raise OutOfPagesException, "Out of Pages"
  end
  rows_on_page = []
  maintable.xpath('tr').each do |tr|
    if tr.attr('class') == 'HeadTitle' then  
      puts "skipping HeadTitle row"
      next
    end
    if tr.attr('class') == 'TableFootSimple left' then  
      puts "skipping TableFood row"
      next
    end
       cells = tr.search('td')
       record = {
        # we have no per-row id, so use random strings as unique identifiers
        # XXX: maybe this should be a hash of the entire row, so we can repeat
        # later and identify/avoid dupes 

        "name_of_buyer" => cells[0].text,
        "company_number" => cells[1].text,
        "company_municipality" => cells[2].text,
        "company_address" => cells[3].text,
        "company_name" => cells[4].text,
        "procurer_number" => cells[5].text,
        "country_of_winner" => cells[6].text,
        "type_of_work" => cells[7].text,
        "goal_of_work" => cells[8].text,
        "contract_description" => cells[9].text,
        "contract_detail" => cells[10].text,
        "contract_value_estimated" => cells[11].text,
        "contract_value_actual_net" => cells[12].text,
        "contract_value_actual_gross" => cells[13].text,
        "contract_award_date" => cells[14].text,
        "number_of_offers" => cells[15].text,
        }

=begin
it'd be nicer to have original labels, but not easy with scraperwiki

        "Назив наручиоца" => cells[0].text,
        "МБ Наручиоца" => cells[1].text,
        "Адреса Наручиоца" => cells[2].text,
        "Општина Наручиоца" => cells[3].text,
        "Назив Понуђача" => cells[4].text,
        "МБ Понуђача" => cells[5].text,
        "Држава Понуђача" => cells[6].text,
        "Врста Поступка" => cells[7].text,
        "Врста Предмета" => cells[8].text,
        "Предмет Набавке" => cells[9].text,
        "Опис предмета" => cells[10].text,
        "Процењена вредност" => cells[11].text,
        "Уговорена вредност" => cells[12].text,
        "Уговорена вредност са ПДВ-ом" => cells[13].text,
        "Датум закључења уговора" => cells[14].text,
        "Број Понуда" => cells[15].text,
=end

      record["hash"] = createsig(record)
      rows_on_page.push(record)
  end
  #doc.search("th[scope='col']").each do |th|
  #  puts th.text
  #end
  puts rows_on_page
  return rows_on_page
end

def scrape
  maxpages = 25
  #ScraperWiki.save_metadata("page", 4)
  puts 'starting'
  baseurl = 'http://portal.ujn.gov.rs/Izvestaji.aspx'
  #argument = 'Page$20000'
  target = 'ctl00$ContentPlaceHolder3$grwIzvestaji'
  agent = Mechanize.new
  #page = agent.get(baseurl)
  puts 'got base'

  current_page = ScraperWiki.get_metadata("page",2)
  max_page = current_page + maxpages

  loop {

  page = agent.get(baseurl)
  
  argument = 'Page$' + current_page.to_s
  puts "argument is " + argument
  if current_page > 1
    form = page.form("aspnetForm")
    form.add_field!('__EVENTARGUMENT', argument)
    form.add_field!('__EVENTTARGET', target)
    page = agent.submit(form)
  end
  begin
    new_records = contents_from_body(page.body)
  rescue OutOfPagesException => e
    puts "out of pages"
    break
  end
  ScraperWiki.save_sqlite(unique_keys=['hash'],new_records)

  current_page += 1
  ScraperWiki.save_metadata("page",current_page)
  puts "on page " + current_page.to_s
  if current_page >= max_page
    break
  end

  }

end

puts scrape()