require 'mechanize'
require 'date'
require 'digest'

def save_details_from_search_results(page)
  form = page.form_with(name: 'frmSearchResults')

  page.at('#dgSearchResults').search(:tr).each do |r|
    next if r.at(:a).nil? || r.at(:a).attr(:id).nil? 
    event_target = r.at(:a).attr(:id).gsub('_', '$')
    form['__EVENTTARGET'] = event_target

    detail_page = form.submit

    defendant = detail_page.at('#lblDefendant').inner_text.strip
    date = Date.strptime(detail_page.at('#lblDateCourt').inner_text.strip, '%d/%m/%Y')

    # Create a record ID so we can refer to it
    record_id = Digest::SHA1.new.hexdigest(date.to_s + defendant)

    number_of_prosecutions = detail_page.at('#dgProsecution').search(:tr).count - 1

    case_record = {
      id:                     record_id,
      defendant:              defendant,
      court:                  detail_page.at('#lblCourt').inner_text.strip,
      date:                   date,
      result:                 detail_page.at('#lblResult').inner_text.strip,
      number_of_prosecutions: number_of_prosecutions
    }

    ScraperWiki::save_sqlite [:id], case_record, 'cases'

    element_id = 3
    number_of_prosecutions.times do |n|
      prosecution_record = {
        id:            "#{record_id}-#{n + 1}",
        case_id:       record_id,
        court_number:  detail_page.at("#dgProsecution_ctl0#{element_id}_lblgrCourtNo").inner_text.strip,
        abn:           detail_page.at("#dgProsecution_ctl0#{element_id}_lblgrABN").inner_text.strip,
        act:           detail_page.at("#dgProsecution_ctl0#{element_id}_lblgrAct").inner_text.strip,
        section:       detail_page.at("#dgProsecution_ctl0#{element_id}_lblgrSection").inner_text.strip,
        description:   detail_page.at("#dgProsecution_ctl0#{element_id}_lblDescription").inner_text.strip,
        amount:        detail_page.at("#dgProsecution_ctl0#{element_id}_lblgrAmount").inner_text.strip,
        other_penalty: detail_page.at("#dgProsecution_ctl0#{element_id}_lblgrOther").inner_text.strip
      }

      ScraperWiki::save_sqlite [:id], prosecution_record, 'prosecutions'

      element_id += 1
    end
  end
end

agent = Mechanize.new
agent.keep_alive = false # HACK: to avoid a "Net::HTTP::Persistent::Error:too many connection resets" condition
                     # https://github.com/tenderlove/mechanize/issues/123#issuecomment-6432074
url = 'http://www.environment.nsw.gov.au/casesapp/Searchresultprosecution.aspx'

page = agent.get url
form = page.form_with(name: 'frmSearchScreen')
page = form.submit(form.button_with(value: 'Search'))

while page
  puts "Getting details from page #{page.at('#lblPageCountCurrent').inner_text}"
  save_details_from_search_results(page)

  pagination = page.at('#dgSearchResults').search(:tr).last

  break if pagination.at(:span).next.nil? 

  next_page_link = pagination.at(:span).next.next.attr(:href)
  event_target = next_page_link.match(/\'(.*)\',/)[1]

  form = page.form_with(name: 'frmSearchResults')
  form['__EVENTTARGET'] = event_target
  page = form.submit
end
require 'mechanize'
require 'date'
require 'digest'

def save_details_from_search_results(page)
  form = page.form_with(name: 'frmSearchResults')

  page.at('#dgSearchResults').search(:tr).each do |r|
    next if r.at(:a).nil? || r.at(:a).attr(:id).nil? 
    event_target = r.at(:a).attr(:id).gsub('_', '$')
    form['__EVENTTARGET'] = event_target

    detail_page = form.submit

    defendant = detail_page.at('#lblDefendant').inner_text.strip
    date = Date.strptime(detail_page.at('#lblDateCourt').inner_text.strip, '%d/%m/%Y')

    # Create a record ID so we can refer to it
    record_id = Digest::SHA1.new.hexdigest(date.to_s + defendant)

    number_of_prosecutions = detail_page.at('#dgProsecution').search(:tr).count - 1

    case_record = {
      id:                     record_id,
      defendant:              defendant,
      court:                  detail_page.at('#lblCourt').inner_text.strip,
      date:                   date,
      result:                 detail_page.at('#lblResult').inner_text.strip,
      number_of_prosecutions: number_of_prosecutions
    }

    ScraperWiki::save_sqlite [:id], case_record, 'cases'

    element_id = 3
    number_of_prosecutions.times do |n|
      prosecution_record = {
        id:            "#{record_id}-#{n + 1}",
        case_id:       record_id,
        court_number:  detail_page.at("#dgProsecution_ctl0#{element_id}_lblgrCourtNo").inner_text.strip,
        abn:           detail_page.at("#dgProsecution_ctl0#{element_id}_lblgrABN").inner_text.strip,
        act:           detail_page.at("#dgProsecution_ctl0#{element_id}_lblgrAct").inner_text.strip,
        section:       detail_page.at("#dgProsecution_ctl0#{element_id}_lblgrSection").inner_text.strip,
        description:   detail_page.at("#dgProsecution_ctl0#{element_id}_lblDescription").inner_text.strip,
        amount:        detail_page.at("#dgProsecution_ctl0#{element_id}_lblgrAmount").inner_text.strip,
        other_penalty: detail_page.at("#dgProsecution_ctl0#{element_id}_lblgrOther").inner_text.strip
      }

      ScraperWiki::save_sqlite [:id], prosecution_record, 'prosecutions'

      element_id += 1
    end
  end
end

agent = Mechanize.new
agent.keep_alive = false # HACK: to avoid a "Net::HTTP::Persistent::Error:too many connection resets" condition
                     # https://github.com/tenderlove/mechanize/issues/123#issuecomment-6432074
url = 'http://www.environment.nsw.gov.au/casesapp/Searchresultprosecution.aspx'

page = agent.get url
form = page.form_with(name: 'frmSearchScreen')
page = form.submit(form.button_with(value: 'Search'))

while page
  puts "Getting details from page #{page.at('#lblPageCountCurrent').inner_text}"
  save_details_from_search_results(page)

  pagination = page.at('#dgSearchResults').search(:tr).last

  break if pagination.at(:span).next.nil? 

  next_page_link = pagination.at(:span).next.next.attr(:href)
  event_target = next_page_link.match(/\'(.*)\',/)[1]

  form = page.form_with(name: 'frmSearchResults')
  form['__EVENTTARGET'] = event_target
  page = form.submit
end
require 'mechanize'
require 'date'
require 'digest'

def save_details_from_search_results(page)
  form = page.form_with(name: 'frmSearchResults')

  page.at('#dgSearchResults').search(:tr).each do |r|
    next if r.at(:a).nil? || r.at(:a).attr(:id).nil? 
    event_target = r.at(:a).attr(:id).gsub('_', '$')
    form['__EVENTTARGET'] = event_target

    detail_page = form.submit

    defendant = detail_page.at('#lblDefendant').inner_text.strip
    date = Date.strptime(detail_page.at('#lblDateCourt').inner_text.strip, '%d/%m/%Y')

    # Create a record ID so we can refer to it
    record_id = Digest::SHA1.new.hexdigest(date.to_s + defendant)

    number_of_prosecutions = detail_page.at('#dgProsecution').search(:tr).count - 1

    case_record = {
      id:                     record_id,
      defendant:              defendant,
      court:                  detail_page.at('#lblCourt').inner_text.strip,
      date:                   date,
      result:                 detail_page.at('#lblResult').inner_text.strip,
      number_of_prosecutions: number_of_prosecutions
    }

    ScraperWiki::save_sqlite [:id], case_record, 'cases'

    element_id = 3
    number_of_prosecutions.times do |n|
      prosecution_record = {
        id:            "#{record_id}-#{n + 1}",
        case_id:       record_id,
        court_number:  detail_page.at("#dgProsecution_ctl0#{element_id}_lblgrCourtNo").inner_text.strip,
        abn:           detail_page.at("#dgProsecution_ctl0#{element_id}_lblgrABN").inner_text.strip,
        act:           detail_page.at("#dgProsecution_ctl0#{element_id}_lblgrAct").inner_text.strip,
        section:       detail_page.at("#dgProsecution_ctl0#{element_id}_lblgrSection").inner_text.strip,
        description:   detail_page.at("#dgProsecution_ctl0#{element_id}_lblDescription").inner_text.strip,
        amount:        detail_page.at("#dgProsecution_ctl0#{element_id}_lblgrAmount").inner_text.strip,
        other_penalty: detail_page.at("#dgProsecution_ctl0#{element_id}_lblgrOther").inner_text.strip
      }

      ScraperWiki::save_sqlite [:id], prosecution_record, 'prosecutions'

      element_id += 1
    end
  end
end

agent = Mechanize.new
agent.keep_alive = false # HACK: to avoid a "Net::HTTP::Persistent::Error:too many connection resets" condition
                     # https://github.com/tenderlove/mechanize/issues/123#issuecomment-6432074
url = 'http://www.environment.nsw.gov.au/casesapp/Searchresultprosecution.aspx'

page = agent.get url
form = page.form_with(name: 'frmSearchScreen')
page = form.submit(form.button_with(value: 'Search'))

while page
  puts "Getting details from page #{page.at('#lblPageCountCurrent').inner_text}"
  save_details_from_search_results(page)

  pagination = page.at('#dgSearchResults').search(:tr).last

  break if pagination.at(:span).next.nil? 

  next_page_link = pagination.at(:span).next.next.attr(:href)
  event_target = next_page_link.match(/\'(.*)\',/)[1]

  form = page.form_with(name: 'frmSearchResults')
  form['__EVENTTARGET'] = event_target
  page = form.submit
end
