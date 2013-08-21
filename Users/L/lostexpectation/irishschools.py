import scraperwiki

import mechanize
br = mechanize.Browser()
br.open("http://education.ie/en/find-a-school")
br.select_form(nr=0)
print br.formimport scraperwiki

import mechanize
br = mechanize.Browser()
br.open("http://education.ie/en/find-a-school")
br.select_form(nr=0)
print br.form