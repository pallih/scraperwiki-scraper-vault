# -*- coding: utf-8 -*-

require 'rubygems'
require 'open-uri'
require 'nokogiri'


if RUBY_VERSION < '1.9.0'
  $KCODE = 'UTF8'
end

# Module and classes
module KazWebHelper
  def parse_get_parameters(uri)
    parsed_parameters = {}
    parsed_uri = URI.parse(uri)
    parsed_uri.query.split("&").each { |item|
      array = item.split("=").to_a
      parsed_parameters.store(array[0], array[1])
    }
    return parsed_parameters
  end
  module_function :parse_get_parameters
end

# Classes

class RidersPageParser

  def initialize(list_url)
    @list_url = list_url
  end

  def parse_riders_page()
    doc = Nokogiri::HTML.parse(open(@list_url),  'UTF-8')

    current_result = parse_riders_table(@list_url, doc)


    next_url = get_url_of_next_page(@list_url, doc)
    if(next_url)

      return current_result
      #return current_result + parse_riders_list(next_url)
    else
      return current_result
    end
  end


  def parse_riders_table(url, doc)
    riders_table = doc.xpath('id("container00")/table/tr[2]/td/table/tr/td/table[2]/tr/td/table')[0]
    profile = []
    detailed_profile = []
    stats = {'carrer' => [], 'this_year' => [], 'last_year' => []}
    advanced_stats = {'this_year' => [], 'last_year' => []}

    if(riders_table)
      riders_table.xpath('tr[position() > 1]').each do |tr|
        tds = tr.xpath('td')

        detailed_url = URI::join(url, tds[1].xpath('b/a').attribute("href").to_s).to_s
        
        basic_profile = get_basic_profile(tds)
        
        detailed_url_params = KazWebHelper.parse_get_parameters(detailed_url)
        # p detailed_url_params['k_riderLicenseNo']
        basic_profile.store('id', detailed_url_params['k_riderLicenseNo'])
        profile << basic_profile
        
        detailed_profile_item, stats_item, advanced_stats_item = get_rider_detail(Nokogiri::HTML.parse(open(detailed_url), 'UTF-8'))
        detailed_profile << detailed_profile_item
        stats['carrer'] << stats_item['carrer']
        stats['this_year'] << stats_item['this_year']
        stats['last_year'] << stats_item['last_year']
        advanced_stats['this_year'] << advanced_stats_item['this_year']
        advanced_stats['last_year'] << advanced_stats_item['last_year']
        
      end

      for i in 1..profile.length do
        profile[i-1].merge!(detailed_profile[i-1])
        
        stats['carrer'][i-1].store("id", profile[i-1]['id'])
        stats['carrer'][i-1].store("profile_id", profile[i-1]['id'])
        stats['this_year'][i-1].store("id", profile[i-1]['id'])
        stats['this_year'][i-1].store("profile_id", profile[i-1]['id'])
        stats['last_year'][i-1].store("id", profile[i-1]['id'])
        stats['last_year'][i-1].store("profile_id", profile[i-1]['id'])
        
        advanced_stats['this_year'][i-1].store("id", profile[i-1]['id'])
        advanced_stats['this_year'][i-1].store("profile_id", profile[i-1]['id'])
        advanced_stats['last_year'][i-1].store("id", profile[i-1]['id'])
        advanced_stats['last_year'][i-1].store("profile_id", profile[i-1]['id'])
      end

      return profile, stats, advanced_stats
    end
  end
  private :parse_riders_table


  def get_basic_profile(tds)
    # id = tds[0].children.to_s
    name = tds[1].xpath('b/a').children.to_s.split("　").join
    stable = tds[2].children.to_s
    organization = tds[3].children.to_s

    return {
      # 'id'           => id,
      'name'         => name,
      'stable'       => stable,
      'organization' => organization
    }
  end
  private :get_basic_profile


  def get_rider_detail(doc)
    detailed_profile_item = {}
    stats_item = {}
    advanced_stats_item = {}
    
    detailed_profile_item = get_detailed_profile_item(doc)
    stats_item = get_stats_item(doc)
    advanced_stats_item = get_advanced_stats_item(doc)

    return detailed_profile_item, stats_item, advanced_stats_item
  end
  private :get_rider_detail


  def get_detailed_profile_item(doc)
    profile_items_1 = doc.xpath('id("container00")/table/tr[2]/td/table/tr/td/table[1]/tbody/tr/td/table/tbody/tr[2]/td')
    profile_items_2 = doc.xpath('id("container00")/table/tr[2]/td/table/tr/td/table[1]/tbody/tr/td/table/tbody/tr[3]/td')
    # p profile_items_1.to_s
    # p profile_items_2.to_s

    yomigana = profile_items_1[1].children.to_s
    sex = profile_items_1[3].children.to_s
    date_of_first_riding = profile_items_1[5].children.to_s

    date_of_birth = profile_items_2[2].children.to_s
    # p date_of_birth
    date_of_first_winning = profile_items_2[4].children.to_s
    # p date_of_first_winning

    return {
      'yomigana' => yomigana,
      'sex' => sex,
      'date_of_birth' => date_of_birth,
      'date_of_first_riding' => date_of_first_riding,
      'date_of_first_winning' => date_of_first_winning
    }
  end
  private :get_detailed_profile_item

  def get_stats_item(doc)
    basic_stats_table = doc.xpath('id("container00")/table/tr[2]/td/table/tr/td/table[2]/tbody/tr/td/table')
    # p basic_stats_table.to_s
    carrer_stats_item = get_chakujun(basic_stats_table.xpath('tbody/tr[3]'))
    this_year_stats_item = get_chakujun(basic_stats_table.xpath('tbody/tr[4]'))
    last_year_stats_item = get_chakujun(basic_stats_table.xpath('tbody/tr[5]'))

    return {
      'carrer' => carrer_stats_item,
      'this_year' => this_year_stats_item,
      'last_year' => last_year_stats_item
    }
  end
  private :get_stats_item

  def get_chakujun(tr)
    #for i in 2..8
    return {
      'first' => tr.xpath('td[2]').children.to_s.to_i,
      'second' => tr.xpath('td[3]').children.to_s.to_i,
      'third' => tr.xpath('td[4]').children.to_s.to_i,
      'fourth' => tr.xpath('td[5]').children.to_s.to_i,
      'fifth' => tr.xpath('td[6]').children.to_s.to_i,
      'etc.' => tr.xpath('td[7]').children.to_s.to_i,
      # 'total' => t_row.xpath('td[8]').children.to_s.to_i
    }
  end
  private :get_chakujun


  def get_advanced_stats_item(doc)
    advanced_stats_table_this_year = doc.xpath('id("container00")/table/tr[2]/td/table/tr/td/table[3]/tbody/tr/td/table')
    advanced_stats_table_last_year = doc.xpath('id("container00")/table/tr[2]/td/table/tr/td/table[4]/tbody/tr/td/table')
    # p basic_stats_table.to_s
    first_uchiwake = get_ninki_uchiwake(advanced_stats_table_this_year.xpath('tbody/tr[3]'))
    second_uchiwake = get_ninki_uchiwake(advanced_stats_table_this_year.xpath('tbody/tr[4]'))
    third_uchiwake = get_ninki_uchiwake(advanced_stats_table_this_year.xpath('tbody/tr[5]'))
    chakugai_uchiwake = get_ninki_uchiwake(advanced_stats_table_this_year.xpath('tbody/tr[6]'))

    advanced_stats_this_year_item =  {
      'first_uchiwake' => first_uchiwake,
      'second_uchiwake' => second_uchiwake,
      'third_uchiwake' => third_uchiwake,
      'chakugai_uchiwake' => chakugai_uchiwake
    }

    first_uchiwake = get_ninki_uchiwake(advanced_stats_table_last_year.xpath('tbody/tr[3]'))
    second_uchiwake = get_ninki_uchiwake(advanced_stats_table_last_year.xpath('tbody/tr[4]'))
    third_uchiwake = get_ninki_uchiwake(advanced_stats_table_last_year.xpath('tbody/tr[5]'))
    chakugai_uchiwake = get_ninki_uchiwake(advanced_stats_table_last_year.xpath('tbody/tr[6]'))

    advanced_stats_last_year_item =  {
      'first_uchiwake' => first_uchiwake,
      'second_uchiwake' => second_uchiwake,
      'third_uchiwake' => third_uchiwake,
      'chakugai_uchiwake' => chakugai_uchiwake
    }
    
    advanced_stats_item = {'this_year' => advanced_stats_this_year_item, 'last_year' => advanced_stats_last_year_item}

    return advanced_stats_item

  end
  private :get_advanced_stats_item

  def get_ninki_uchiwake(tr)
    #for i in 2..8
    return {
      '1ban_ninki' => tr.xpath('td[2]').children.to_s.to_i,
      '2ban_ninki' => tr.xpath('td[3]').children.to_s.to_i,
      '3ban_ninki' => tr.xpath('td[4]').children.to_s.to_i,
      '4ban_ninki' => tr.xpath('td[5]').children.to_s.to_i,
      '5ban_ninki' => tr.xpath('td[6]').children.to_s.to_i,
      'etc.' => tr.xpath('td[7]').children.to_s.to_i,
      # 'total' => t_row.xpath('td[8]').children.to_s.to_i
    }
  end
  private :get_ninki_uchiwake

  def get_url_of_next_page(url, doc)
    anchors = doc.xpath('id("container00")/table/tr[2]/td/table/tr/td/table[1]/tr/td[2]/a').each do |anchor|
      a_text = anchor.children.to_s

      unless (a_text.scan(/^次/).eql?([]))
        abs_url = URI::join(url, anchor.attribute("href").to_s).to_s
        # p abs_url
        return abs_url
      end
    end
    return nil
  end
  private :get_url_of_next_page

end










=begin
def parse_doc(doc)
  result = []

  table = doc.xpath('/html/body/table[2]//table')[0]

  # Note tr[1] is actually a table header
  table.xpath('tr[position() > 1]').each do |tr|
    fields = tr.xpath('td').map do |td|
      field = td.text
      field.gsub!(/(?:\s|\xe3\x80\x80)+/, ' ') # Shrink spaces (\xe3... == full-width space)
      field.gsub!(/\s?$/, '')                  # Chop off trailing space
      field
    end
    name, furigana, party, district, _ = fields

    name.gsub!(/.$/, '') # Chop off "-kun"

    result << {
      'name'     => name,
      'furigana' => furigana,
      'party'    => party,
      'district' => district
    }
  end

  result
end
=end





=begin
module DB_Wrapper
  def createDB
  end
  def store_data(table_name, id_list, data)
  end
end
=end

class ScraperWiki_Wrapper
  def self.create_db
    ScraperWiki.sqliteexecute("PRAGMA foreign_keys=ON;")
    
    ScraperWiki.sqliteexecute("drop table if exists profile")
    ScraperWiki.sqliteexecute("drop table if exists carrer_stats")
    ScraperWiki.sqliteexecute("drop table if exists this_year_stats")
    ScraperWiki.sqliteexecute("drop table if exists last_year_stats")
    
    ScraperWiki.sqliteexecute("create table 'profile' ('id' int PRIMARY KEY, 'name' string not null, 'yomigana' string not null, 'sex' string not null, 'organization' string not null, 'stable' string, date_of_birth string not null ,date_of_first_riding string, date_of_first_winning string)")
    
    ScraperWiki.sqliteexecute("create table 'carrer_stats' ('id' int PRIMARY KEY, 'profile_id' int not null, 'first' int not null, 'second' int not null, 'third' int not null, 'fourth' int not null, 'fifth' int not null, 'etc.' int not null, FOREIGN KEY(profile_id) REFERENCES profile(id))")

    ScraperWiki.sqliteexecute("create table 'this_year_stats' ('id' int PRIMARY KEY, 'profile_id' int not null, 'first' int not null, 'second' int not null, 'third' int not null, 'fourth' int not null, 'fifth' int not null, 'etc.' int not null, FOREIGN KEY(profile_id) REFERENCES profile(id))")

    ScraperWiki.sqliteexecute("create table 'last_year_stats' ('id' int PRIMARY KEY, 'profile_id' int not null, 'first' int not null, 'second' int not null, 'third' int not null, 'fourth' int not null, 'fifth' int not null, 'etc.' int not null, FOREIGN KEY(profile_id) REFERENCES profile(id))")
    # ScraperWiki.sqliteexecute("create table 'stats' ('id' int PRIMARY KEY, 'ttt_id' int not null, FOREIGN KEY(ttt_id) REFERENCES ttt(id))")
  end

  def self.store_profile(profile)
    # ScraperWiki.save(id, data)

    # 2 is a mazic number (for detail, see doc on scraperwiki.com)
    ScraperWiki.sqliteexecute("PRAGMA foreign_keys=ON;")
    ScraperWiki.save_sqlite(["id"], profile, "profile", 2)
=begin
    ScraperWiki.sqliteexecute("insert into ttt values (?,?)", [1, 'hello'])
    ScraperWiki.sqliteexecute("insert into ttt values (?,?)", [2, 'ohayo'])
    ScraperWiki.sqliteexecute("insert into tt2 values (?,?)", [1, 1])
    ScraperWiki.sqliteexecute("insert into tt2 values (?,?)", [2, 3])
    ScraperWiki.commit()
=end
  end

  def self.store_stats(stats)
    # 2 is a mazic number (for detail, see doc on scraperwiki.com)
p :hoge
    ScraperWiki.sqliteexecute("PRAGMA foreign_keys=ON;")
    ScraperWiki.save_sqlite(["id"], stats['carrer'], "carrer_stats", 2)
p :ishige
    #ScraperWiki.save_sqlite(["id"], stats['this_year'], "this_year_stats", 2)
    #ScraperWiki.save_sqlite(["id"], stats['last_year'], "last_year_stats", 2)
  end
  
  def self.store_advanced_stats_this_year(profile, advanced_stats_this_year)
  end
  def self.store_advanced_stats_last_year(profile, advanced_stats_last_year)
  end

end

=begin
class LocalDB_Wrapper
  def self.create_db
    db = SQLite3::Database.new("../db/riders.db")
    db.execute("PRAGMA foreign_keys=ON;")
    
    db.execute("drop table if exists profile")
    db.execute("drop table if exists carrer_stats")
    db.execute("drop table if exists this_year_stats")
    db.execute("drop table if exists last_year_stats")
    
    db.execute("create table 'profile' ('id' int PRIMARY KEY, 'name' string not null, 'yomigana' string not null, 'sex' string not null, 'organization' string not null, 'stable' string, date_of_birth string not null ,date_of_first_riding string, date_of_first_winning string)")
    
    db.execute("create table 'carrer_stats' ('id' int PRIMARY KEY, 'profile_id' int not null, 'first' int not null, 'second' int not null, 'third' int not null, 'fourth' int not null, 'fifth' int not null, 'etc.' int not null, FOREIGN KEY(profile_id) REFERENCES profile(id))")

    db.execute("create table 'this_year_stats' ('id' int PRIMARY KEY, 'profile_id' int not null, 'first' int not null, 'second' int not null, 'third' int not null, 'fourth' int not null, 'fifth' int not null, 'etc.' int not null, FOREIGN KEY(profile_id) REFERENCES profile(id))")

    db.execute("create table 'last_year_stats' ('id' int PRIMARY KEY, 'profile_id' int not null, 'first' int not null, 'second' int not null, 'third' int not null, 'fourth' int not null, 'fifth' int not null, 'etc.' int not null, FOREIGN KEY(profile_id) REFERENCES profile(id))")
    # db.execute("create table 'stats' ('id' int PRIMARY KEY, 'ttt_id' int not null, FOREIGN KEY(ttt_id) REFERENCES ttt(id))")
  end

  def self.store_profile(profile)
    db = SQLite3::Database.new("../db/riders.db")
    db.transaction do 
      db.execute("PRAGMA foreign_keys=ON;")
      db.execute("insert into profile values (?,?,?,?,?,?,?,?,?)", [6, "赤嶺亮", "アカミネ　リヨウ", "男", "大井", "赤嶺本", "1986年8月13日", "2005年10月30日", "2005年10月30日"])
    end
  end

  def self.store_stats(stats)
    db = SQLite3::Database.new("../db/riders.db")
    db.transaction do
      db.execute("PRAGMA foreign_keys=ON;")
      db.execute("insert into carrer_stats values (?,?,?,?,?,?,?,?)", [6, 6, 1, 2, 3, 4, 5, 6])
    end
  end
  
  def self.store_advanced_stats_this_year(profile, advanced_stats_this_year)
  end
  def self.store_advanced_stats_last_year(profile, advanced_stats_last_year)
  end

end
=end

# main logic
first_page_of_riders_list = "http://www2.keiba.go.jp/KeibaWeb/DataRoom/RiderList?k_flag=1&k_pageNum=0&k_name=&k_genneki_flag=1&k_syozoku=&k_sei="

profile, stats, advanced_stats_this_year, advanced_stats_last_year = RidersPageParser.new(first_page_of_riders_list).parse_riders_page

=begin
for n in 1..profile.length do
  #p profile[i-1]
  # p stats['last_year'][i-1]
  p stats['carrer'][n-1]
  # p advanced_stats_this_year[i-1]
  # advanced_stats_last_year[i-1]
end
=end

ScraperWiki_Wrapper.create_db
ScraperWiki_Wrapper.store_profile(profile)
ScraperWiki_Wrapper.store_stats(stats)

# require 'sqlite3'
# LocalDB_Wrapper.create_db
# LocalDB_Wrapper.store_profile(nil)
