require 'nokogiri'

('a'..'z').to_a.each do |letter|
# Search anything in the business name:  
# http://egov.sos.state.or.us/br/pkg_web_name_srch_inq.do_name_srch?p_name=#{letter}&p_regist_nbr=&p_srch=PHASE1&p_print=FALSE&p_entity_status=ACTINA

# Search business names that start with a letter:
  results = ScraperWiki.scrape("http://egov.sos.state.or.us/br/pkg_web_name_srch_inq.do_name_srch?p_name=#{letter}&p_regist_nbr=&p_srch=PHASE1P&p_print=FALSE&p_entity_status=ACTINA")
  doc = Nokogiri::HTML.parse(results)
  table = doc.css('table')[3]
  rows = table.css('tr')
  rows.each do |row|
    next if row.css('td') == nil
    bizdetail = Hash.new
    dtd = nil
    biz_detail_page = nil
    next if row.css('td').length < 3

    oregon_registry_id = row.css('td')[3].text.gsub('&nbsp', '')
    rsn = oregon_registry_id.gsub(/-\d\d/, '')

    if rsn =~ /\d{6}/ then
      url = row.css('td')[3].css('a').attr('href')
      biz_detail_page = "http://egov.sos.state.or.us/br/#{url}"
      details = ScraperWiki.scrape(biz_detail_page)
      details_doc = Nokogiri::HTML.parse(details)
      dtable = details_doc.css('table')[2]
      dtd = dtable.css('tr')[1].css('td')[4].text if dtable.css('tr')[1]
      tables = details_doc.css('table')
      next if tables == nil
      type = nil
      tables.each do |table|
        next if table == nil
        next if table.css('tr')[0] == nil
        next if table.css('tr')[0].css('td')[0] == nil
        thing = table.css('tr')[0].css('td')[0].text
        if thing == 'Type' then
          # parse this for type data
          type = table.css('tr')[0].css('td')[1].text
          bizdetail[type] =  table.css('tr')[0].css('td')[2].text
        elsif thing == 'Addr 1' then
          addr = table.css('tr')[0].css('td')[1].text
          key = type + '_addr1'
          bizdetail[key] =  addr
        elsif thing == 'Addr 2' then
          key = type + '_addr2'
          bizdetail[key] =  table.css('tr')[0].css('td')[1].text
        elsif thing == 'Name' then
          name = table.css('tr')[0].css('td')[1].text + " " + table.css('tr')[0].css('td')[2].text + " " + table.css('tr')[0].css('td')[3].text
          key = type + '_name'
          bizdetail[key] =  name
        elsif thing == 'CSZ' then
          city = table.css('tr')[0].css('td')[1].text
          state = table.css('tr')[0].css('td')[2].text
          zip = table.css('tr')[0].css('td')[3].text
          key = type + '_city'
          bizdetail[key] =  city
          key = type + '_state'
          bizdetail[key] =  state
          key = type + '_zip'
          bizdetail[key] =  zip
        end
      end
    end

    bizdetail['oregon_registry_id'] = row.css('td')[3].text.gsub('&nbsp', '')
    bizdetail['name'] = row.css('td')[5].text.gsub('&nbsp', '')
    bizdetail['registered_date'] = dtd
    bizdetail['source_url'] = biz_detail_page

    ScraperWiki.save(unique_keys=['oregon_registry_id'], data=bizdetail)
  end
end
require 'nokogiri'

('a'..'z').to_a.each do |letter|
# Search anything in the business name:  
# http://egov.sos.state.or.us/br/pkg_web_name_srch_inq.do_name_srch?p_name=#{letter}&p_regist_nbr=&p_srch=PHASE1&p_print=FALSE&p_entity_status=ACTINA

# Search business names that start with a letter:
  results = ScraperWiki.scrape("http://egov.sos.state.or.us/br/pkg_web_name_srch_inq.do_name_srch?p_name=#{letter}&p_regist_nbr=&p_srch=PHASE1P&p_print=FALSE&p_entity_status=ACTINA")
  doc = Nokogiri::HTML.parse(results)
  table = doc.css('table')[3]
  rows = table.css('tr')
  rows.each do |row|
    next if row.css('td') == nil
    bizdetail = Hash.new
    dtd = nil
    biz_detail_page = nil
    next if row.css('td').length < 3

    oregon_registry_id = row.css('td')[3].text.gsub('&nbsp', '')
    rsn = oregon_registry_id.gsub(/-\d\d/, '')

    if rsn =~ /\d{6}/ then
      url = row.css('td')[3].css('a').attr('href')
      biz_detail_page = "http://egov.sos.state.or.us/br/#{url}"
      details = ScraperWiki.scrape(biz_detail_page)
      details_doc = Nokogiri::HTML.parse(details)
      dtable = details_doc.css('table')[2]
      dtd = dtable.css('tr')[1].css('td')[4].text if dtable.css('tr')[1]
      tables = details_doc.css('table')
      next if tables == nil
      type = nil
      tables.each do |table|
        next if table == nil
        next if table.css('tr')[0] == nil
        next if table.css('tr')[0].css('td')[0] == nil
        thing = table.css('tr')[0].css('td')[0].text
        if thing == 'Type' then
          # parse this for type data
          type = table.css('tr')[0].css('td')[1].text
          bizdetail[type] =  table.css('tr')[0].css('td')[2].text
        elsif thing == 'Addr 1' then
          addr = table.css('tr')[0].css('td')[1].text
          key = type + '_addr1'
          bizdetail[key] =  addr
        elsif thing == 'Addr 2' then
          key = type + '_addr2'
          bizdetail[key] =  table.css('tr')[0].css('td')[1].text
        elsif thing == 'Name' then
          name = table.css('tr')[0].css('td')[1].text + " " + table.css('tr')[0].css('td')[2].text + " " + table.css('tr')[0].css('td')[3].text
          key = type + '_name'
          bizdetail[key] =  name
        elsif thing == 'CSZ' then
          city = table.css('tr')[0].css('td')[1].text
          state = table.css('tr')[0].css('td')[2].text
          zip = table.css('tr')[0].css('td')[3].text
          key = type + '_city'
          bizdetail[key] =  city
          key = type + '_state'
          bizdetail[key] =  state
          key = type + '_zip'
          bizdetail[key] =  zip
        end
      end
    end

    bizdetail['oregon_registry_id'] = row.css('td')[3].text.gsub('&nbsp', '')
    bizdetail['name'] = row.css('td')[5].text.gsub('&nbsp', '')
    bizdetail['registered_date'] = dtd
    bizdetail['source_url'] = biz_detail_page

    ScraperWiki.save(unique_keys=['oregon_registry_id'], data=bizdetail)
  end
end
