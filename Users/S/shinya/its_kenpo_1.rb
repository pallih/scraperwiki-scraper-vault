require 'rubygems'
require 'mechanize'

def get_months(page)
  select_page = page.frame_with(:name => 'navi').click
  select_page.form_with(:action => './its_w_change_year_month.asp') do |form|
    form.field_with(:name => 'target_date') do |list|
      return list.options
    end
  end
end

def set_month(page, month)
  select_page = page.frame_with(:name => 'navi').click
  select_page.form_with(:action => './its_w_change_year_month.asp') do |form|
    form.field_with(:name => 'target_date') do |list|
      list.value = month
    end
  end.click_button
end

def parse_page(page, ctime)
  vacant_page = page.frame_with(:name => 'main').click
  month = vacant_page.search('//table[position()=2]/tr/td/font/b').text.sub!(/^(\d+)\W+(\d+)\W+/, '\1-\2') 

  vacant_page.search('//table[position()=3]/tr').each do |tr|
    next if tr.has_attribute? ('valign')

    name = ''
    status = []
    tr.search('td').each do |td|
      if td.has_attribute? ('bgcolor') then
        name = td.search('a').text
      else
        t = td.search('font').text
        status << ["\u3000", "\u25CB", "\u25B3", "\uFF0D", "\u2606"].index(t)
      end
    end

    data = {
      name: name,
      month: month,
      status: status.join(','),
      ctime: ctime,
    }
    detect_changes(data, ctime)
    ScraperWiki.save_sqlite([:name, :month], data, 'vacancy')
  end
end

def detect_changes(data, ctime)
  begin
    ScraperWiki.select('status from vacancy where name = ? and month = ? and status != ?', [data[:name], data[:month], data[:status]]).each do |row|
      cr_status = data[:status].split(',')
      pr_status = row['status'].split(',')
      cr_status.each_index do |i|
        next if cr_status[i] == pr_status[i]
        next if cr_status[i] != "1" && cr_status[i] != "2"
        change = {
          name: data[:name],
          date: data[:month] + '-' + sprintf("%02d", i + 1),
          ctime: ctime
        }
        ScraperWiki.save_sqlite([], change, 'changes')
      end
    end
  rescue
    print "error"
    return
  end
end

ctime = Time.now.to_i
a = Mechanize.new
url = 'http://yoyaku.its-kenpo.or.jp/its_rsvestab/vacant/its_w_vacant_top.asp'
a.get(url) do |page|
  get_months(page).each do |month|
    set_month(page, month)
    parse_page(page, ctime)
  end
end

ScraperWiki.sqliteexecute('delete from vacancy where ctime < ?', [ctime]) rescue true
ScraperWiki.sqliteexecute('delete from changes where ctime < ?', [ctime - 60 * 60 * 24 * 3]) rescue true
ScraperWiki.commit()require 'rubygems'
require 'mechanize'

def get_months(page)
  select_page = page.frame_with(:name => 'navi').click
  select_page.form_with(:action => './its_w_change_year_month.asp') do |form|
    form.field_with(:name => 'target_date') do |list|
      return list.options
    end
  end
end

def set_month(page, month)
  select_page = page.frame_with(:name => 'navi').click
  select_page.form_with(:action => './its_w_change_year_month.asp') do |form|
    form.field_with(:name => 'target_date') do |list|
      list.value = month
    end
  end.click_button
end

def parse_page(page, ctime)
  vacant_page = page.frame_with(:name => 'main').click
  month = vacant_page.search('//table[position()=2]/tr/td/font/b').text.sub!(/^(\d+)\W+(\d+)\W+/, '\1-\2') 

  vacant_page.search('//table[position()=3]/tr').each do |tr|
    next if tr.has_attribute? ('valign')

    name = ''
    status = []
    tr.search('td').each do |td|
      if td.has_attribute? ('bgcolor') then
        name = td.search('a').text
      else
        t = td.search('font').text
        status << ["\u3000", "\u25CB", "\u25B3", "\uFF0D", "\u2606"].index(t)
      end
    end

    data = {
      name: name,
      month: month,
      status: status.join(','),
      ctime: ctime,
    }
    detect_changes(data, ctime)
    ScraperWiki.save_sqlite([:name, :month], data, 'vacancy')
  end
end

def detect_changes(data, ctime)
  begin
    ScraperWiki.select('status from vacancy where name = ? and month = ? and status != ?', [data[:name], data[:month], data[:status]]).each do |row|
      cr_status = data[:status].split(',')
      pr_status = row['status'].split(',')
      cr_status.each_index do |i|
        next if cr_status[i] == pr_status[i]
        next if cr_status[i] != "1" && cr_status[i] != "2"
        change = {
          name: data[:name],
          date: data[:month] + '-' + sprintf("%02d", i + 1),
          ctime: ctime
        }
        ScraperWiki.save_sqlite([], change, 'changes')
      end
    end
  rescue
    print "error"
    return
  end
end

ctime = Time.now.to_i
a = Mechanize.new
url = 'http://yoyaku.its-kenpo.or.jp/its_rsvestab/vacant/its_w_vacant_top.asp'
a.get(url) do |page|
  get_months(page).each do |month|
    set_month(page, month)
    parse_page(page, ctime)
  end
end

ScraperWiki.sqliteexecute('delete from vacancy where ctime < ?', [ctime]) rescue true
ScraperWiki.sqliteexecute('delete from changes where ctime < ?', [ctime - 60 * 60 * 24 * 3]) rescue true
ScraperWiki.commit()