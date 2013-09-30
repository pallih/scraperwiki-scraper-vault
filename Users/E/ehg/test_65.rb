require 'nokogiri'  
require 'thread'

class ThreadPool
  class Worker
    def initialize
      @mutex = Mutex.new
      @thread = Thread.new do
        while true
          sleep 0.001
          block = get_block
          if block
            block.call
            reset_block
          end
        end
      end
    end
    
    def get_block
      @mutex.synchronize {@block}
    end
    
    def set_block(block)
      @mutex.synchronize do
        raise RuntimeError, "Thread already busy." if @block
        @block = block
      end
    end
    
    def reset_block
      @mutex.synchronize {@block = nil}
    end
    
    def busy?
      @mutex.synchronize {!@block.nil?}
    end
  end
  
  attr_accessor :max_size
  attr_reader :workers

  def initialize(max_size = 10)
    @max_size = max_size
    @workers = []
    @mutex = Mutex.new
  end
  
  def size
    @mutex.synchronize {@workers.size}
  end
  
  def busy?
    @mutex.synchronize {@workers.any? {|w| w.busy?}}
  end
  
  def join
    sleep 0.01 while busy?
  end
  
  def process(&block)
        while true
            @mutex.synchronize do
                worker = find_available_worker 
                if worker
                    return worker.set_block(block)
                end
            end
            sleep 0.01
        end
    end

    def find_available_worker
        free_worker || create_worker
    end
  
  def wait_for_worker
    while true
      worker = find_available_worker
      return worker if worker
      sleep 0.01
    end
  end
  
  
  def free_worker
    @workers.each {|w| return w unless w.busy?}; nil
  end
  
  def create_worker
    return nil if @workers.size >= @max_size
    worker = Worker.new
    @workers << worker
    worker
  end
end

def scrape_page(i)
  if scraped_already(i) 
    return
  end
  
  puts "starting on property number #{i}"
  
  retries = 0

  begin 
    return if retries > 3 
    scrape = ScraperWiki.scrape("http://www.valoff.ie/search/details.asp?Pno=#{i}")
  rescue StandardError
    puts "other error, will retry #{i}"
    retries+=1
    retry
  rescue Timeout::Error
    puts "time out, will retry #{i}"
    retry
  end
  
  data = Hash.new
  
  doc = Nokogiri::HTML(scrape)
  for v in doc.search("table[@class='body'] tr")
   
    header_cell = v.search('td div[@class="style26"]').first
    value_cell = v.search('td[@class="bhome"]').first
   
    header = header_cell.content.strip unless header_cell.nil? 
    value = value_cell.content.strip unless value_cell.nil? 
  
    if header
      header = header.gsub(/,*\s+/,'_')
      header = header.downcase
      data[header] = value
    end
  end
  
  puts data.to_json

  ScraperWiki.save_sqlite(unique_keys=['property_number'], data = data)
  ScraperWiki.save_var('last_pno', i)
end

def scraped_already(i)
  if ScraperWiki.select("property_number from swdata where property_number=#{i}").count > 0
    puts "already scraped #{i}"
    return true
  end

  return false
end

start = ScraperWiki.get_var('last_pno') || 1
start -= 50 unless start <= 50

pool = ThreadPool.new(7)

(start..2000000).each do |i|
  pool.process {scrape_page i} 
  
end

pool.join()

require 'nokogiri'  
require 'thread'

class ThreadPool
  class Worker
    def initialize
      @mutex = Mutex.new
      @thread = Thread.new do
        while true
          sleep 0.001
          block = get_block
          if block
            block.call
            reset_block
          end
        end
      end
    end
    
    def get_block
      @mutex.synchronize {@block}
    end
    
    def set_block(block)
      @mutex.synchronize do
        raise RuntimeError, "Thread already busy." if @block
        @block = block
      end
    end
    
    def reset_block
      @mutex.synchronize {@block = nil}
    end
    
    def busy?
      @mutex.synchronize {!@block.nil?}
    end
  end
  
  attr_accessor :max_size
  attr_reader :workers

  def initialize(max_size = 10)
    @max_size = max_size
    @workers = []
    @mutex = Mutex.new
  end
  
  def size
    @mutex.synchronize {@workers.size}
  end
  
  def busy?
    @mutex.synchronize {@workers.any? {|w| w.busy?}}
  end
  
  def join
    sleep 0.01 while busy?
  end
  
  def process(&block)
        while true
            @mutex.synchronize do
                worker = find_available_worker 
                if worker
                    return worker.set_block(block)
                end
            end
            sleep 0.01
        end
    end

    def find_available_worker
        free_worker || create_worker
    end
  
  def wait_for_worker
    while true
      worker = find_available_worker
      return worker if worker
      sleep 0.01
    end
  end
  
  
  def free_worker
    @workers.each {|w| return w unless w.busy?}; nil
  end
  
  def create_worker
    return nil if @workers.size >= @max_size
    worker = Worker.new
    @workers << worker
    worker
  end
end

def scrape_page(i)
  if scraped_already(i) 
    return
  end
  
  puts "starting on property number #{i}"
  
  retries = 0

  begin 
    return if retries > 3 
    scrape = ScraperWiki.scrape("http://www.valoff.ie/search/details.asp?Pno=#{i}")
  rescue StandardError
    puts "other error, will retry #{i}"
    retries+=1
    retry
  rescue Timeout::Error
    puts "time out, will retry #{i}"
    retry
  end
  
  data = Hash.new
  
  doc = Nokogiri::HTML(scrape)
  for v in doc.search("table[@class='body'] tr")
   
    header_cell = v.search('td div[@class="style26"]').first
    value_cell = v.search('td[@class="bhome"]').first
   
    header = header_cell.content.strip unless header_cell.nil? 
    value = value_cell.content.strip unless value_cell.nil? 
  
    if header
      header = header.gsub(/,*\s+/,'_')
      header = header.downcase
      data[header] = value
    end
  end
  
  puts data.to_json

  ScraperWiki.save_sqlite(unique_keys=['property_number'], data = data)
  ScraperWiki.save_var('last_pno', i)
end

def scraped_already(i)
  if ScraperWiki.select("property_number from swdata where property_number=#{i}").count > 0
    puts "already scraped #{i}"
    return true
  end

  return false
end

start = ScraperWiki.get_var('last_pno') || 1
start -= 50 unless start <= 50

pool = ThreadPool.new(7)

(start..2000000).each do |i|
  pool.process {scrape_page i} 
  
end

pool.join()

