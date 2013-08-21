# Scraper All RIS
require 'rubygems'
require 'nokogiri'
require 'mechanize'

# a_ris = ["ba-charlottenburg-wilmersdorf","ba-friedrichshain-kreuzberg","ba-lichtenberg","ba-marzahn-hellersdorf","ba-mitte","ba-neukoelln","ba-pankow","ba-reinickendorf","ba-spandau","ba-steglitz-zehlendorf","ba-tempelhof-schoeneberg","ba-treptow-koepenick"]
a_ris = {
          'celle' => 'http://celle.allris-online.de/bi/pa021.asp',
          'bvv-friedrichshain-kreuzberg' => 'http://www.berlin.de/ba-friedrichshain-kreuzberg/bvv-online/pa021.asp'
        }

# init mechnaize
agent = Mechanize.new
agent.user_agent_alias = 'Linux Mozilla'

a_ris.each do |ris_name, ris_url|

  # get page and look for form nodes
  page = agent.get(ris_url)
  page.forms_with(:action => /kp020.asp/).each do |form|

    # cells with personal data
    nl_cells = form.form_node.search('./ancestor::tr[1]//td')

    # submit form, select content container from response
    page_kp = form.submit()
    n_kp = page_kp.search("table[@class='mainwork']")[0]

    # look for committee nodes and save them
    nl_committees = n_kp.search(".//tr[td/form[contains(@action,'au020.asp')]]")
    nl_committees.each do |committee|
      data = {
        'url' => page_kp.uri.to_s+"?"+form.request_data(),
        'committee' => committee.search("td[2]").text(),
        'function' => committee.search("td[3]").text(),
        'member_since' => committee.search("td[4]").text()
      }
      ScraperWiki.save_sqlite(unique_keys=[], data, table_name='test-'+ris_name+'-committees')
    end

    # save personal data
    data = {
      'url' => page_kp.uri.to_s+"?"+form.request_data(),
      'name' => nl_cells[2].text(),
      'function' => nl_cells[3].text(),
      'party' => nl_cells[4].text(),
      'member_since' => nl_cells[5].text(),
      'salutation' => n_kp.search(".//tr[td/img/@width=150]/td[@class='text4']").text(),
      'url_portrait' => n_kp.search(".//tr/td/img[@width=150][1]/@src").text(),
      'email' => n_kp.search("//tr[td/img[contains(@src,'email.gif')]]/td/a").to_a().join('|'),
      'phone' => n_kp.search(".//tr[td/img[contains(@src,'telefon.gif')]]/td/span[text()]").to_a().join('|'),
      'fax' => n_kp.search(".//tr[td/img[contains(@src,'fax.gif')]]/td/span[text()]").to_a().join('|')
    }
    ScraperWiki.save_sqlite(unique_keys=['url'], data, table_name='test-'+ris_name)

  end
end