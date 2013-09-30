require 'rubygems'
require 'mechanize'

agent = Mechanize.new
page = agent.get('http://schools.nyc.gov/Common/Templates/MainTemplate/CommonMainTemplate.aspx?NRMODE=Published&NRNODEGUID=%7bE4428845-1159-45A0-AFFA-A69E0BBDDAC1%7d&NRORIGINALURL=%2fAboutUs%2ffunding%2fschoolbudgets%2fGalaxyAllocationFY2012%2ehtm&NRCACHEHINT=Guest')

form = page.form('StandardMain')
form['doecontrol_middlecentercontainer_a_budgetgallexy$SCH_INPUT'] = 'm015'
page = agent.submit(form)

puts page.body


require 'rubygems'
require 'mechanize'

agent = Mechanize.new
page = agent.get('http://schools.nyc.gov/Common/Templates/MainTemplate/CommonMainTemplate.aspx?NRMODE=Published&NRNODEGUID=%7bE4428845-1159-45A0-AFFA-A69E0BBDDAC1%7d&NRORIGINALURL=%2fAboutUs%2ffunding%2fschoolbudgets%2fGalaxyAllocationFY2012%2ehtm&NRCACHEHINT=Guest')

form = page.form('StandardMain')
form['doecontrol_middlecentercontainer_a_budgetgallexy$SCH_INPUT'] = 'm015'
page = agent.submit(form)

puts page.body


