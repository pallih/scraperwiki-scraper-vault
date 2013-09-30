# Scrape CLV business license categories and instructions

require 'nokogiri'

base_uri = 'http://www5.lasvegasnevada.gov/LCAT/'

html = ScraperWiki::scrape(base_uri)
page = Nokogiri::HTML html

page.search('#dlLicCategories td').each do |v|

  # Get license name, ID and URI to instructions
  license_url = v.search('a[href]').attr('href').to_s
  license_url.gsub!(/\s/, '%20')
  license_id = license_url.split('=')
  license_id = license_id[1].split('&')
  license_name = v.search('a[href]').inner_html.to_s

  # Retrieve business license instructions page
  morehtml = ScraperWiki::scrape(base_uri + license_url)
  morepage = Nokogiri::HTML morehtml

  # Get license description
  license_desc = morepage.search('#dlInstructionSheet_ctl01_lblInstruction').inner_html.to_s

  # Get license steps
  step01num = morepage.search('#dlInstructionSheet_ctl03_lblInstructionNumber').inner_html.to_s
  step01 = morepage.search('#dlInstructionSheet_ctl03_lblInstruction').inner_html.to_s
  step02num = morepage.search('#dlInstructionSheet_ctl05_lblInstructionNumber').inner_html.to_s
  step02 = morepage.search('#dlInstructionSheet_ctl05_lblInstruction').inner_html.to_s
  step03num = morepage.search('#dlInstructionSheet_ctl07_lblInstructionNumber').inner_html.to_s
  step03 = morepage.search('#dlInstructionSheet_ctl07_lblInstruction').inner_html.to_s
  step04num = morepage.search('#dlInstructionSheet_ctl09_lblInstructionNumber').inner_html.to_s
  step04 = morepage.search('#dlInstructionSheet_ctl09_lblInstruction').inner_html.to_s
  step05num = morepage.search('#dlInstructionSheet_ctl11_lblInstructionNumber').inner_html.to_s
  step05 = morepage.search('#dlInstructionSheet_ctl11_lblInstruction').inner_html.to_s
  step06num = morepage.search('#dlInstructionSheet_ctl13_lblInstructionNumber').inner_html.to_s
  step06 = morepage.search('#dlInstructionSheet_ctl13_lblInstruction').inner_html.to_s
  step07num = morepage.search('#dlInstructionSheet_ctl15_lblInstructionNumber').inner_html.to_s
  step07 = morepage.search('#dlInstructionSheet_ctl15_lblInstruction').inner_html.to_s
  step08num = morepage.search('#dlInstructionSheet_ctl17_lblInstructionNumber').inner_html.to_s
  step08 = morepage.search('#dlInstructionSheet_ctl17_lblInstruction').inner_html.to_s
  step09num = morepage.search('#dlInstructionSheet_ctl19_lblInstructionNumber').inner_html.to_s
  step09 = morepage.search('#dlInstructionSheet_ctl19_lblInstruction').inner_html.to_s
  step10num = morepage.search('#dlInstructionSheet_ctl21_lblInstructionNumber').inner_html.to_s
  step10 = morepage.search('#dlInstructionSheet_ctl21_lblInstruction').inner_html.to_s

  # Assemble data
  data = {
    license_id: license_id[0],
    license_name: license_name,
    license_desc: license_desc,
    step01num: step01num,
    step01dtl: step01,
    step02num: step02num,
    step02dtl: step02,
    step03num: step03num,
    step03dtl: step03,
    step04num: step04num,
    step04dtl: step04,
    step05num: step05num,
    step05dtl: step05,
    step06num: step06num,
    step06dtl: step06,
    step07num: step07num,
    step07dtl: step07,
    step08num: step08num,
    step08dtl: step08,
    step09num: step09num,
    step09dtl: step09,
    step10num: step10num,
    step10dtl: step10
  }

  # Save data
  # puts data.to_json
  ScraperWiki::save_sqlite(['license_id'], data)
end

# Scrape CLV business license categories and instructions

require 'nokogiri'

base_uri = 'http://www5.lasvegasnevada.gov/LCAT/'

html = ScraperWiki::scrape(base_uri)
page = Nokogiri::HTML html

page.search('#dlLicCategories td').each do |v|

  # Get license name, ID and URI to instructions
  license_url = v.search('a[href]').attr('href').to_s
  license_url.gsub!(/\s/, '%20')
  license_id = license_url.split('=')
  license_id = license_id[1].split('&')
  license_name = v.search('a[href]').inner_html.to_s

  # Retrieve business license instructions page
  morehtml = ScraperWiki::scrape(base_uri + license_url)
  morepage = Nokogiri::HTML morehtml

  # Get license description
  license_desc = morepage.search('#dlInstructionSheet_ctl01_lblInstruction').inner_html.to_s

  # Get license steps
  step01num = morepage.search('#dlInstructionSheet_ctl03_lblInstructionNumber').inner_html.to_s
  step01 = morepage.search('#dlInstructionSheet_ctl03_lblInstruction').inner_html.to_s
  step02num = morepage.search('#dlInstructionSheet_ctl05_lblInstructionNumber').inner_html.to_s
  step02 = morepage.search('#dlInstructionSheet_ctl05_lblInstruction').inner_html.to_s
  step03num = morepage.search('#dlInstructionSheet_ctl07_lblInstructionNumber').inner_html.to_s
  step03 = morepage.search('#dlInstructionSheet_ctl07_lblInstruction').inner_html.to_s
  step04num = morepage.search('#dlInstructionSheet_ctl09_lblInstructionNumber').inner_html.to_s
  step04 = morepage.search('#dlInstructionSheet_ctl09_lblInstruction').inner_html.to_s
  step05num = morepage.search('#dlInstructionSheet_ctl11_lblInstructionNumber').inner_html.to_s
  step05 = morepage.search('#dlInstructionSheet_ctl11_lblInstruction').inner_html.to_s
  step06num = morepage.search('#dlInstructionSheet_ctl13_lblInstructionNumber').inner_html.to_s
  step06 = morepage.search('#dlInstructionSheet_ctl13_lblInstruction').inner_html.to_s
  step07num = morepage.search('#dlInstructionSheet_ctl15_lblInstructionNumber').inner_html.to_s
  step07 = morepage.search('#dlInstructionSheet_ctl15_lblInstruction').inner_html.to_s
  step08num = morepage.search('#dlInstructionSheet_ctl17_lblInstructionNumber').inner_html.to_s
  step08 = morepage.search('#dlInstructionSheet_ctl17_lblInstruction').inner_html.to_s
  step09num = morepage.search('#dlInstructionSheet_ctl19_lblInstructionNumber').inner_html.to_s
  step09 = morepage.search('#dlInstructionSheet_ctl19_lblInstruction').inner_html.to_s
  step10num = morepage.search('#dlInstructionSheet_ctl21_lblInstructionNumber').inner_html.to_s
  step10 = morepage.search('#dlInstructionSheet_ctl21_lblInstruction').inner_html.to_s

  # Assemble data
  data = {
    license_id: license_id[0],
    license_name: license_name,
    license_desc: license_desc,
    step01num: step01num,
    step01dtl: step01,
    step02num: step02num,
    step02dtl: step02,
    step03num: step03num,
    step03dtl: step03,
    step04num: step04num,
    step04dtl: step04,
    step05num: step05num,
    step05dtl: step05,
    step06num: step06num,
    step06dtl: step06,
    step07num: step07num,
    step07dtl: step07,
    step08num: step08num,
    step08dtl: step08,
    step09num: step09num,
    step09dtl: step09,
    step10num: step10num,
    step10dtl: step10
  }

  # Save data
  # puts data.to_json
  ScraperWiki::save_sqlite(['license_id'], data)
end

