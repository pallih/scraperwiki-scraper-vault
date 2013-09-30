require 'mechanize'

agent = Mechanize.new
page = agent.get('https://secure.indiedb.com/members/login')

login_form = page.form('memberform')

login_form.username = 'StauntonLick2'
login_form.password = 'stauntonlick2'

page = agent.submit(login_form, login_form.buttons.first)

pp pagerequire 'mechanize'

agent = Mechanize.new
page = agent.get('https://secure.indiedb.com/members/login')

login_form = page.form('memberform')

login_form.username = 'StauntonLick2'
login_form.password = 'stauntonlick2'

page = agent.submit(login_form, login_form.buttons.first)

pp page