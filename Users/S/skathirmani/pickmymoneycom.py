import scraperwiki
import mechanize

br = mechanize.Browser()
br.set_handle_robots(False) # ignore robots
r = br.open('http://pickmymoney.com/login.aspx')
br.select_form(nr=0)
br.form['uname'] = 'stratabiz01'
br.form['password'] = 'stratabiz01'
br.submit()
br.select_form(nr=0)

br.form['amount']=['500']
br.form['fname']='Natasha'
br.form['lname']='Perkins'
br.form['email']='ndperkins23704@yahoo.com'
br.form['address']='605 seventh street  e'
br.form['state']=['RI']
br.form['zip']='2818'
br.form['city']='East greenwich'
br.form['homephn1']='401'
br.form['homephn2']='524'
br.form['homephn3']='8395'
br.submit()
data = {'page':br.response().read(),'page_form':br}
scraperwiki.sqlite.save(unique_keys=['page','page_form'],data=data) 
