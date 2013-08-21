# Scrape CLV business license categories and instructions

# individual business page - TEST

require 'nokogiri'

base_uri = 'http://www5.lasvegasnevada.gov/LCAT/Bus_Lic_Instructions.aspx?Category=A32&CategoryName=Adult%20Book%20Store'

html = ScraperWiki::scrape(base_uri)
page = Nokogiri::HTML html

license_id = 'A32'
license_desc = page.search('#dlInstructionSheet_ctl01_lblInstruction').inner_html.to_s

step01num = page.search('#dlInstructionSheet_ctl03_lblInstructionNumber').inner_html.to_s
step01 = page.search('#dlInstructionSheet_ctl03_lblInstruction').inner_html.to_s
step02num = page.search('#dlInstructionSheet_ctl05_lblInstructionNumber').inner_html.to_s
step02 = page.search('#dlInstructionSheet_ctl05_lblInstruction').inner_html.to_s
step03num = page.search('#dlInstructionSheet_ctl07_lblInstructionNumber').inner_html.to_s
step03 = page.search('#dlInstructionSheet_ctl03_lblInstruction').inner_html.to_s
step04num = page.search('#dlInstructionSheet_ctl07_lblInstructionNumber').inner_html.to_s
step04 = page.search('#dlInstructionSheet_ctl03_lblInstruction').inner_html.to_s
step05num = page.search('#dlInstructionSheet_ctl09_lblInstructionNumber').inner_html.to_s
step05 = page.search('#dlInstructionSheet_ctl09_lblInstruction').inner_html.to_s
step06num = page.search('#dlInstructionSheet_ctl11_lblInstructionNumber').inner_html.to_s
step06 = page.search('#dlInstructionSheet_ctl11_lblInstruction').inner_html.to_s
step07num = page.search('#dlInstructionSheet_ctl13_lblInstructionNumber').inner_html.to_s
step07 = page.search('#dlInstructionSheet_ctl13_lblInstruction').inner_html.to_s
step08num = page.search('#dlInstructionSheet_ctl15_lblInstructionNumber').inner_html.to_s
step08 = page.search('#dlInstructionSheet_ctl15_lblInstruction').inner_html.to_s
step09num = page.search('#dlInstructionSheet_ctl17_lblInstructionNumber').inner_html.to_s
step09 = page.search('#dlInstructionSheet_ctl17_lblInstruction').inner_html.to_s
step10num = page.search('#dlInstructionSheet_ctl19_lblInstructionNumber').inner_html.to_s
step10 = page.search('#dlInstructionSheet_ctl19_lblInstruction').inner_html.to_s

# Assemble data
data = {
  license_id: license_id,
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

