#Template/Sample from Friedrich Lindenberg

# Newsfeed available (most recent ?): feed://cmiskp.echr.coe.int/rss/JudDec-123-EN.xml

# http://cmiskp.echr.coe.int/tkp197/search.asp?sessionid=80311369&skin=hudoc-en

# from here we should get a session id
# http://www.echr.coe.int/echr/en/hudoc/
# http://cmiskp.echr.coe.int/tkp197/search.asp?skin=hudoc-en


###############################################################################
# 
# Website: 
# Fields:
#
###############################################################################

import scraperwiki
from BeautifulSoup import BeautifulSoup
import mechanize
import sys
import lxml.html



base_url = 'http://cmiskp.echr.coe.int/tkp197/search.asp?skin=hudoc-en'

# base_url = 'https://www.unternehmensregister.de/ureg/result.html'
# https://www.unternehmensregister.de/ureg/result.html;jsessionid=2F75FB29FC1AF95F5A67809E1A176B5E.www04-1
#http://scraperwikiviews.com/run/python_mechanize_cheat_sheet/

#  Use mechanize to fill the form with a start parameter, the page will  not come up with content. If there is nothing there is an empty table
# So we start with '00' 
# Another reason for meachanize was, in the link the page cannot be adressed directly

br = mechanize.Browser()
br.set_handle_robots(False)
html = br.open(base_url).read()
# print html #deactivated 201106290945

# print response.read() 


# br.select_form("form1")         # works when form has a name 
# br.form = list(br.forms())[0]  # use when form is unnamed
# br.select_form("globalSearchForm")
# br.form = list(br.forms())[0]
br.select_form("frmSearch")


#table class="mainTable"

# print br.form #deactivated 201106290946


# Search Options
#<tbody><tr id="criteriaRow" name="criteriarow" title="Just return the number of potential matches" idcriteria="countonly">
#<tr id="criteriaRow" name="criteriarow" title="The type of document summary" idcriteria="ds_type">
#<tr id="criteriaRow" name="criteriarow" title="Number or Percentage of Sentences to Return for Concept Summary" idcriteria="ds_sentence">
#<tr id="criteriaRow" name="criteriarow" title="Number of Sentences to Return for Concept Summary" idcriteria="ds_num_sentence">
#<tr id="criteriaRow" name="criteriarow" title="Only applies to Concept Summary" idcriteria="ds_percent_sentence">
#<tr id="criteriaRow" name="criteriarow" title="Maximum number of results to be returned by the search" idcriteria="max_search_rows">
# should be 50000
#<tr id="criteriaRow" name="criteriarow" title="Maximum number of items to be displayed on any one page" idcriteria="max_page_rows">
#should be 5000
#<tr id="criteriaRow" name="criteriarow" title="The tags to use for hit highlighting" idcriteria="html_search_tags">
#</tbody>








# <input id="globalSearchForm:extendedResearchCompanyName" type="text" style="width:175px;height:16px;
# font-size:1.1em;" size="30" value="aa" name="globalSearchForm:extendedResearchCompanyName">
# <input id="globalSearchForm:hidden_element_used_for_validation_only" type="text" style="display:none;" value="aaa" name="globalSearchForm:hidden_element_used_for_validation_only">
## br["globalSearchForm:extendedResearchCompanyName"] = "00"

# <input id="pd_metadatalanguage_english" type="checkbox" checked="" onchange="javascript:m_bDirty = true;" name="pd_metadatalanguage_english">
# <span class="textital">English</span>
#br["pd_pd_metadatalanguage_english"] = ""

# <input id="pd_respondent" class="criteriainput" onchange="javascript:m_bDirty = true;" value="" name="pd_respondent">
# <input class="lookupButtons" type="button" onclick="javascript:lookup( 'pd_respondent', lookupLanguages() );" value="...">
br["pd_respondent"] = "GERMANY" 

# <input id="pd_kp_date_from" class="criteriainputdate" onchange="javascript:m_bDirty = true;dateCheck( document.frmSearch.pd_kp_date_from, document.frmSearch.pd_kp_date_to     );" value="" name="pd_kp_date_from">
br["pd_kp_date_from"] = "01/01/2011" 

#<input id="pd_kp_date_to" class="criteriainputdate" value="18/10/2011" onchange="javascript:m_bDirty = true;dateCheck( document.frmSearch.pd_kp_date_from, document.frmSearch.pd_kp_date_to );" name="pd_kp_date_to">
# <span class="textital"> dd/mm/yyyy</span>
br["pd_kp_date_to"] = "01/02/2011" 


html1 = br.submit().read()


# print html1 #deactivated 201106290947
root = lxml.html.fromstring(html1)
# for rec in root.cssselect("div.result_item"): #deactivated 201106290950
for rec in root.cssselect("div.company_result"): #thats where I reduce the data to within the record
    print lxml.html.tostring(rec)
sys.exit(0)
                     
while 1:
    try:
        page = scraperwiki.sqlite.get_var("page", 1)
        starting_url = base_url  # + str(page) + options 

        html = scraperwiki.scrape(starting_url) # thats the selection

#        html = scraperwiki.scrape(starting_url, {'class=company_result'})


# html = scraperwiki.scrape(starting_url, {'page=classement&id_rubrique=1034'})

# <div class="company_result">

    except Exception, e:
        print e

    soup = BeautifulSoup(html)

#    for ldiv in  soup.findAll('table'):
#        if ldiv.find('id').text == 'relevance_header':
#            div = ldiv

#  201106291010 possibly not needed    div =  soup.find('table',{'id':'result_table'}) #selects the element of the  website which includes the table


# This Block not changed - should either be corrected or be removed
# Begin

    susp_rows = div.findAll('b') #the 'bracket around each line'

    print susp_rows

#    urlparse.urljoin()
# End

    recordlist = [ ]
    for susp_row in susp_rows[2:]:## where did this come from? Why?

        company_result = ''
        information_result = ''
        label_result = ''

        cells = susp_row.findAll('td')

#     print susp_row # this helped to see what was coming from the scraper  -> then correction start from Line 2 instead of Line 1.

#Seems to be used when there is content in Line

        def tonum(ss):
            return float(ss.text.strip().replace(".", "").replace(",", "."))

#        NumericVariable = tonum(cells[7])

        company_result = cells[0].text
        information_result  = cells[1].text
        label_result = cells[2].text




# Is this necessary ? Why. Possibly when there are empty lines. It has not been changed.
# Begin
        susp_a = cells[2].find('a')
        if susp_a:
            susp_url = absolutize_url(susp_a['href'])

        reinst_a = cells[3].find('a')
        if reinst_a:
            reinst_url = absolutize_url(reinst_a['href'])
# End


#Seems to be used when there is content in the line
# It seems to be necessary to define every column in the table, otherwise its not working
        record = {
            'company_result' : company_result
            ,'information_result' : information_result
            ,'label_result' : label_result
        }

        print record

        recordlist.append(record)

#        print record

#    scraperwiki.sqlite.save(['Anlagenschluessel'], recordlist) #1st Table

    scraperwiki.sqlite.save_var("page", page+1) #2nd Table
