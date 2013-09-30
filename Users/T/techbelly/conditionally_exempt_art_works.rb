require 'nokogiri'
require 'set'

SCRAPE = 1200 # number of records to scrape
THREADS = 3   # number of threads to use: only one until ruby libs are threadsafe

POSTCODE_REGX = /[A-Z]{1,2}[0-9R][0-9A-Z]?\s*[0-9][ABD-HJLNP-UW-Z]{2}/i

def extract_postcode(text)
  return unless text
  text = text.strip.sub(/\bo(\w\w)$/i,'0\1') # replace o with zero
  postcode = text[POSTCODE_REGX]
  return nil unless postcode
  postcode.gsub(/\s+/,'').insert(-4,' ').upcase 
end
 
def extract_phone(text,phone)
    return unless text
    return phone if (phone and phone != "")
    p_nums = text.scan(/(?:\+44)?[ 0-9\(\)\-]{10,16}/) 
    p_nums.map { |x| x.gsub!(/\D/,'') }
    p_nums.reject! { |x| x.nil? || x.empty? || x.length < 10 }
    p_nums.each do |num|
      num.sub!(/^44/,'')
      num = case num
        when /^02/ 
          num.insert(3,') ').insert(9,' ')
        when /^08/, /^011/, /^01[2-6,9]1/ #
          num.insert(4,') ')
        when /^01697[3,4,7]/ 
          num.insert(6,') ')
        else
          num.insert(5,') ')
      end
      num.insert(0,'(')
    end
end


def scrape_id(id)
    abs_url = "http://www.visitukheritage.gov.uk/servlet/com.eds.ir.cto.servlet.CtoDetailServlet?ID=#{id}"
    regexp = %r{<font face="Arial, Helvetica, sans-serif" size="-1">([^:]*):</font></b></td><td (?:[^<]*)>\s+([^<]*)</td>}mi

    # " <-- Just here to fix the syntax highlighting...
    
    owner_regexp = %r{.*/servlet/com.eds.ir.cto.servlet.CtoOtherLinkedServlet\?Owner=([^&]*).*}mi

    #  /// <-- Just here to fix the syntax highlighting...
    
    begin
      
      html = ScraperWiki.scrape(abs_url)
     

      artwork = {}

      if (match = owner_regexp.match(html))
        artwork['owner_id'] = match[1]
      end

      if (matches = html.scan regexp) 
        matches.each do |m|
          field,value = m[0],m[1]
          clean_field_name = field.downcase.gsub(" ","_")
          artwork[clean_field_name] = value
        end
        if artwork['contact_address']
          artwork['postcode'] = extract_postcode(artwork["contact_address"])
        end
        artwork['telephone_no'] = extract_phone(artwork['contact_address'],artwork['telephone_no'])

      #latlng = ScraperWiki.gb_postcode_to_latlng(artwork['postcode'])
      #if latlng
      #  artwork['lat'] = latlng[0]
      #  artwork['lng'] = latlng[1]
      #end

        if artwork['unique_id']
          ScraperWiki.save(['unique_id'], artwork)
        end
      end
    rescue Timeout::Error => e    
        # not really sure what to do here...
        # should probably requeue, and end the scrape
        # after say 5 timeouts
    end
end


search_url = 'http://www.visitukheritage.gov.uk/servlet/com.eds.ir.cto.servlet.CtoDbQueryServlet?location=All&class1=All&freetext=&Submit=search'
html = ScraperWiki.scrape(search_url)

queue = Queue.new
regexp = /.*HREF='\/servlet\/com.eds.ir.cto.servlet.CtoDetailServlet\?ID=([^']*)'.*/
if (matches = html.scan regexp) 

  match_ids = matches.map { |m| m[0].to_i }
  match_ids = match_ids.sort
  
  max_id = ScraperWiki.get_metadata("scraped_up_to")
  max_id = max_id ? max_id.to_i : 0

  puts "Already scraped up to: #{max_id}"
  
  match_ids.each do |m|
    if m > max_id
      queue.push(m)
      max_id = m
    end
    break if queue.length >= SCRAPE
  end

  if queue.empty? 
    # start the scraping process over again at the next run
    ScraperWiki.save_metadata("scraped_up_to","0")
  end
end

# ruby's array operations aren't guaranteed
# thread-safe AFAIK, so use queue to collect
# successes instead

threads = []
id_queue = Queue.new
THREADS.times do 
  threads << Thread.new do  
    begin
      while id = queue.pop(true) do
        scrape_id(id.to_s)
        id_queue << id
      end 
    rescue ThreadError
      puts "queue empty"
    rescue Exception => e
      puts "#{e}"
      puts e.backtrace
    end
  end
end

threads.each do |t|
  t.join()
end

ids = []
while ! id_queue.empty? do
  ids << id_queue.pop(true)
end 
max_id = ids.max.to_s

ScraperWiki.save_metadata("scraped_up_to",max_id)
puts "Scraped up to: #{max_id}"

require 'nokogiri'
require 'set'

SCRAPE = 1200 # number of records to scrape
THREADS = 3   # number of threads to use: only one until ruby libs are threadsafe

POSTCODE_REGX = /[A-Z]{1,2}[0-9R][0-9A-Z]?\s*[0-9][ABD-HJLNP-UW-Z]{2}/i

def extract_postcode(text)
  return unless text
  text = text.strip.sub(/\bo(\w\w)$/i,'0\1') # replace o with zero
  postcode = text[POSTCODE_REGX]
  return nil unless postcode
  postcode.gsub(/\s+/,'').insert(-4,' ').upcase 
end
 
def extract_phone(text,phone)
    return unless text
    return phone if (phone and phone != "")
    p_nums = text.scan(/(?:\+44)?[ 0-9\(\)\-]{10,16}/) 
    p_nums.map { |x| x.gsub!(/\D/,'') }
    p_nums.reject! { |x| x.nil? || x.empty? || x.length < 10 }
    p_nums.each do |num|
      num.sub!(/^44/,'')
      num = case num
        when /^02/ 
          num.insert(3,') ').insert(9,' ')
        when /^08/, /^011/, /^01[2-6,9]1/ #
          num.insert(4,') ')
        when /^01697[3,4,7]/ 
          num.insert(6,') ')
        else
          num.insert(5,') ')
      end
      num.insert(0,'(')
    end
end


def scrape_id(id)
    abs_url = "http://www.visitukheritage.gov.uk/servlet/com.eds.ir.cto.servlet.CtoDetailServlet?ID=#{id}"
    regexp = %r{<font face="Arial, Helvetica, sans-serif" size="-1">([^:]*):</font></b></td><td (?:[^<]*)>\s+([^<]*)</td>}mi

    # " <-- Just here to fix the syntax highlighting...
    
    owner_regexp = %r{.*/servlet/com.eds.ir.cto.servlet.CtoOtherLinkedServlet\?Owner=([^&]*).*}mi

    #  /// <-- Just here to fix the syntax highlighting...
    
    begin
      
      html = ScraperWiki.scrape(abs_url)
     

      artwork = {}

      if (match = owner_regexp.match(html))
        artwork['owner_id'] = match[1]
      end

      if (matches = html.scan regexp) 
        matches.each do |m|
          field,value = m[0],m[1]
          clean_field_name = field.downcase.gsub(" ","_")
          artwork[clean_field_name] = value
        end
        if artwork['contact_address']
          artwork['postcode'] = extract_postcode(artwork["contact_address"])
        end
        artwork['telephone_no'] = extract_phone(artwork['contact_address'],artwork['telephone_no'])

      #latlng = ScraperWiki.gb_postcode_to_latlng(artwork['postcode'])
      #if latlng
      #  artwork['lat'] = latlng[0]
      #  artwork['lng'] = latlng[1]
      #end

        if artwork['unique_id']
          ScraperWiki.save(['unique_id'], artwork)
        end
      end
    rescue Timeout::Error => e    
        # not really sure what to do here...
        # should probably requeue, and end the scrape
        # after say 5 timeouts
    end
end


search_url = 'http://www.visitukheritage.gov.uk/servlet/com.eds.ir.cto.servlet.CtoDbQueryServlet?location=All&class1=All&freetext=&Submit=search'
html = ScraperWiki.scrape(search_url)

queue = Queue.new
regexp = /.*HREF='\/servlet\/com.eds.ir.cto.servlet.CtoDetailServlet\?ID=([^']*)'.*/
if (matches = html.scan regexp) 

  match_ids = matches.map { |m| m[0].to_i }
  match_ids = match_ids.sort
  
  max_id = ScraperWiki.get_metadata("scraped_up_to")
  max_id = max_id ? max_id.to_i : 0

  puts "Already scraped up to: #{max_id}"
  
  match_ids.each do |m|
    if m > max_id
      queue.push(m)
      max_id = m
    end
    break if queue.length >= SCRAPE
  end

  if queue.empty? 
    # start the scraping process over again at the next run
    ScraperWiki.save_metadata("scraped_up_to","0")
  end
end

# ruby's array operations aren't guaranteed
# thread-safe AFAIK, so use queue to collect
# successes instead

threads = []
id_queue = Queue.new
THREADS.times do 
  threads << Thread.new do  
    begin
      while id = queue.pop(true) do
        scrape_id(id.to_s)
        id_queue << id
      end 
    rescue ThreadError
      puts "queue empty"
    rescue Exception => e
      puts "#{e}"
      puts e.backtrace
    end
  end
end

threads.each do |t|
  t.join()
end

ids = []
while ! id_queue.empty? do
  ids << id_queue.pop(true)
end 
max_id = ids.max.to_s

ScraperWiki.save_metadata("scraped_up_to",max_id)
puts "Scraped up to: #{max_id}"

