"""
This is an example of scraping multiple URLs.
"""

import scraperwiki
import re

import BeautifulSoup
from datetime import datetime
from scraperwiki import datastore

# The URLs we're going to scrape:

urls = """

http://www.kildarestreet.com/td/caoimhghin_o_caolain/cavan-monaghan
http://www.kildarestreet.com/td/eamon_o_cuiv/galway_west
http://www.kildarestreet.com/td/sean_o_fearghail/kildare_south
http://www.kildarestreet.com/td/aengus_o_snodaigh/dublin_south_central
http://www.kildarestreet.com/td/bertie_ahern/dublin_central
http://www.kildarestreet.com/td/dermot_ahern/louth
http://www.kildarestreet.com/td/michael_ahern/cork_east
http://www.kildarestreet.com/td/noel_ahern/dublin_north_west
http://www.kildarestreet.com/td/bernard_allen/cork_north_central
http://www.kildarestreet.com/td/barry_andrews/dun_laoghaire
http://www.kildarestreet.com/td/chris_andrews/dublin_south_east
http://www.kildarestreet.com/td/sean_ardagh/dublin_south_central
http://www.kildarestreet.com/td/bobby_aylward/carlow-kilkenny
http://www.kildarestreet.com/td/james_bannon/longford-westmeath
http://www.kildarestreet.com/td/sean_barrett/dun_laoghaire
http://www.kildarestreet.com/td/joe_behan/wicklow
http://www.kildarestreet.com/td/niall_blaney/donegal_north_east
http://www.kildarestreet.com/td/aine_brady/kildare_north
http://www.kildarestreet.com/td/cyprian_brady/dublin_central
http://www.kildarestreet.com/td/johnny_brady/meath_west
http://www.kildarestreet.com/td/pat_breen/clare
http://www.kildarestreet.com/td/tommy_broughan/dublin_north_east
http://www.kildarestreet.com/td/john_browne/wexford
http://www.kildarestreet.com/td/richard_bruton/dublin_north_central
http://www.kildarestreet.com/td/ulick_burke/galway_east
http://www.kildarestreet.com/td/joan_burton/dublin_west
http://www.kildarestreet.com/td/catherine_byrne/dublin_south_central
http://www.kildarestreet.com/td/thomas_byrne/meath_east
http://www.kildarestreet.com/td/dara_calleary/mayo
http://www.kildarestreet.com/td/joe_carey/clare
http://www.kildarestreet.com/td/pat_carey/dublin_north_west
http://www.kildarestreet.com/td/deirdre_clune/cork_south_central
http://www.kildarestreet.com/td/niall_collins/limerick_west
http://www.kildarestreet.com/td/margaret_conlon/cavan-monaghan
http://www.kildarestreet.com/td/paul_connaughton/galway_east
http://www.kildarestreet.com/td/sean_connick/wexford
http://www.kildarestreet.com/td/noel_coonan/tipperary_north
http://www.kildarestreet.com/td/joe_costello/dublin_central
http://www.kildarestreet.com/td/mary_coughlan/donegal_south_west
http://www.kildarestreet.com/td/simon_coveney/cork_south_central
http://www.kildarestreet.com/td/brian_cowen/laois-offaly
http://www.kildarestreet.com/td/seymour_crawford/cavan-monaghan
http://www.kildarestreet.com/td/michael_creed/cork_north_west
http://www.kildarestreet.com/td/john_cregan/limerick_west
http://www.kildarestreet.com/td/lucinda_creighton/dublin_south_east
http://www.kildarestreet.com/td/ciaran_cuffe/dun_laoghaire
http://www.kildarestreet.com/td/john_curran/dublin_mid_west
http://www.kildarestreet.com/td/michael_d%27arcy/wexford
http://www.kildarestreet.com/td/john_deasy/waterford
http://www.kildarestreet.com/td/jimmy_deenihan/kerry_north
http://www.kildarestreet.com/td/noel_dempsey/meath_west
http://www.kildarestreet.com/td/jimmy_devins/sligo-north_leitrim
http://www.kildarestreet.com/td/timmy_dooley/clare
http://www.kildarestreet.com/td/andrew_doyle/wicklow
http://www.kildarestreet.com/td/bernard_durkan/kildare_north
http://www.kildarestreet.com/td/damien_english/meath_west
http://www.kildarestreet.com/td/olwyn_enright/laois-offaly
http://www.kildarestreet.com/td/frank_fahey/galway_west
http://www.kildarestreet.com/td/frank_feighan/roscommon-south_leitrim
http://www.kildarestreet.com/td/martin_ferris/kerry_north
http://www.kildarestreet.com/td/michael_finneran/roscommon-south_leitrim
http://www.kildarestreet.com/td/michael_fitzpatrick/kildare_north
http://www.kildarestreet.com/td/charles_flanagan/laois-offaly
http://www.kildarestreet.com/td/terence_flanagan/dublin_north_east
http://www.kildarestreet.com/td/sean_fleming/laois-offaly
http://www.kildarestreet.com/td/beverley_flynn/mayo
http://www.kildarestreet.com/td/eamon_gilmore/dun_laoghaire
http://www.kildarestreet.com/td/paul_gogarty/dublin_mid_west
http://www.kildarestreet.com/td/john_gormley/dublin_south_east
http://www.kildarestreet.com/td/noel_grealish/galway_west
http://www.kildarestreet.com/td/mary_hanafin/dun_laoghaire
http://www.kildarestreet.com/td/mary_harney/dublin_mid_west
http://www.kildarestreet.com/td/sean_haughey/dublin_north_central
http://www.kildarestreet.com/td/brian_hayes/dublin_south_west
http://www.kildarestreet.com/td/tom_hayes/tipperary_south
http://www.kildarestreet.com/td/jackie_healy-rae/kerry_south
http://www.kildarestreet.com/td/michael_d_higgins/galway_west
http://www.kildarestreet.com/td/maire_hoctor/tipperary_north
http://www.kildarestreet.com/td/phil_hogan/carlow-kilkenny
http://www.kildarestreet.com/td/brendan_howlin/wexford
http://www.kildarestreet.com/td/paul_kehoe/wexford
http://www.kildarestreet.com/td/billy_kelleher/cork_north_central
http://www.kildarestreet.com/td/peter_kelly/longford-westmeath
http://www.kildarestreet.com/td/brendan_kenneally/waterford
http://www.kildarestreet.com/td/michael_kennedy/dublin_north
http://www.kildarestreet.com/td/enda_kenny/mayo
http://www.kildarestreet.com/td/tony_killeen/clare
http://www.kildarestreet.com/td/seamus_kirk/louth
http://www.kildarestreet.com/td/michael_kitt/galway_east
http://www.kildarestreet.com/td/tom_kitt/dublin_south
http://www.kildarestreet.com/td/conor_lenihan/dublin_south_west
http://www.kildarestreet.com/td/brian_lenihan_jnr/dublin_west
http://www.kildarestreet.com/td/michael_lowry/tipperary_north
http://www.kildarestreet.com/td/ciaran_lynch/cork_south_central
http://www.kildarestreet.com/td/kathleen_lynch/cork_north_central
http://www.kildarestreet.com/td/martin_mansergh/tipperary_south
http://www.kildarestreet.com/td/micheal_martin/cork_south_central
http://www.kildarestreet.com/td/padraic_mccormack/galway_west
http://www.kildarestreet.com/td/jim_mcdaid/donegal_north_east
http://www.kildarestreet.com/td/tom_mcellistrim/kerry_north
http://www.kildarestreet.com/td/shane_mcentee/meath_east
http://www.kildarestreet.com/td/dinny_mcginley/donegal_south_west
http://www.kildarestreet.com/td/finian_mcgrath/dublin_north_central
http://www.kildarestreet.com/td/mattie_mcgrath/tipperary_south
http://www.kildarestreet.com/td/michael_mcgrath/cork_south_central
http://www.kildarestreet.com/td/john_mcguinness/carlow-kilkenny
http://www.kildarestreet.com/td/joe_mchugh/donegal_north_east
http://www.kildarestreet.com/td/liz_mcmanus/wicklow
http://www.kildarestreet.com/td/olivia_mitchell/dublin_south
http://www.kildarestreet.com/td/john_moloney/laois-offaly
http://www.kildarestreet.com/td/arthur_morgan/louth
http://www.kildarestreet.com/td/michael_moynihan/cork_north_west
http://www.kildarestreet.com/td/michael_mulcahy/dublin_south_central
http://www.kildarestreet.com/td/denis_naughten/roscommon-south_leitrim
http://www.kildarestreet.com/td/dan_neville/limerick_west
http://www.kildarestreet.com/td/m_j_nolan/carlow-kilkenny
http://www.kildarestreet.com/td/michael_noonan/limerick_east
http://www.kildarestreet.com/td/darragh_o%27brien/dublin_north
http://www.kildarestreet.com/td/charlie_o%27connor/dublin_south_west
http://www.kildarestreet.com/td/willie_o%27dea/limerick_east
http://www.kildarestreet.com/td/kieran_o%27donnell/limerick_east
http://www.kildarestreet.com/td/john_o%27donoghue/kerry_south
http://www.kildarestreet.com/td/fergus_o%27dowd/louth
http://www.kildarestreet.com/td/noel_o%27flynn/cork_north_central
http://www.kildarestreet.com/td/rory_o%27hanlon/cavan-monaghan
http://www.kildarestreet.com/td/batt_o%27keeffe/cork_north_west
http://www.kildarestreet.com/td/jim_o%27keeffe/cork_south_west
http://www.kildarestreet.com/td/ned_o%27keeffe/cork_east
http://www.kildarestreet.com/td/john_o%27mahony/mayo
http://www.kildarestreet.com/td/mary_o%27rourke/longford-westmeath
http://www.kildarestreet.com/td/brian_o%27shea/waterford
http://www.kildarestreet.com/td/christy_o%27sullivan/cork_south_west
http://www.kildarestreet.com/td/jan_o%27sullivan/limerick_east
http://www.kildarestreet.com/td/maureen_o%27sullivan/dublin_central
http://www.kildarestreet.com/td/willie_penrose/longford-westmeath
http://www.kildarestreet.com/td/john_perry/sligo-north_leitrim
http://www.kildarestreet.com/td/peter_power/limerick_east
http://www.kildarestreet.com/td/sean_power/kildare_south
http://www.kildarestreet.com/td/ruairi_quinn/dublin_south_east
http://www.kildarestreet.com/td/pat_rabbitte/dublin_south_west
http://www.kildarestreet.com/td/james_reilly/dublin_north
http://www.kildarestreet.com/td/michael_ring/mayo
http://www.kildarestreet.com/td/dick_roche/wicklow
http://www.kildarestreet.com/td/eamon_ryan/dublin_south
http://www.kildarestreet.com/td/trevor_sargent/dublin_north
http://www.kildarestreet.com/td/eamon_scanlon/sligo-north_leitrim
http://www.kildarestreet.com/td/alan_shatter/dublin_south
http://www.kildarestreet.com/td/tom_sheahan/kerry_south
http://www.kildarestreet.com/td/p_j_sheehan/cork_south_west
http://www.kildarestreet.com/td/sean_sherlock/cork_east
http://www.kildarestreet.com/td/roisin_shortall/dublin_north_west
http://www.kildarestreet.com/td/brendan_smith/cavan-monaghan
http://www.kildarestreet.com/td/emmet_stagg/kildare_north
http://www.kildarestreet.com/td/david_stanton/cork_east
http://www.kildarestreet.com/td/billy_timmins/wicklow
http://www.kildarestreet.com/td/noel_treacy/galway_east
http://www.kildarestreet.com/td/joanna_tuffy/dublin_mid_west
http://www.kildarestreet.com/td/mary_upton/dublin_south_central
http://www.kildarestreet.com/td/leo_varadkar/dublin_west
http://www.kildarestreet.com/td/jack_wall/kildare_south
http://www.kildarestreet.com/td/mary_wallace/meath_east
http://www.kildarestreet.com/td/mary_white/carlow-kilkenny
http://www.kildarestreet.com/td/michael_woods/dublin_north_east

""".strip()

urls = urls.splitlines()


# This is a useful helper function that you might want to steal.
# It cleans up the data a bit.
# def gettext(html):
  #  """Return the text within html, removing any HTML tags it contained."""
  #  cleaned = re.sub('<.*?>', '', html)  # remove tags
   # cleaned = ' '.join(cleaned.split())  # collapse whitespace
    # return cleaned

# get all the bill links from http://www.oireachtas.ie/viewdoc.asp?m=&DocID=-1&CatID=59
# http://www.oireachtas.ie/viewdoc.asp?DocID=14885&amp;&amp;CatID=59
# 30 April 2010<br /><a href="viewdoc.asp?DocID=14879&amp;&amp;CatID=59" >Non-Medicinal Psychoactive Substances Bill 2010 (PMB)

for url in urls:
    print "Scraping", url
    page = scraperwiki.scrape(url)
    if page is not None:
        # Store all the h2 headings (matching "<h2>...</h2>")
        title = re.findall("<title>(.*?)</title>", page, re.DOTALL)
        # re.DOTALL makes it work across multiple lines as well.
        
        spoken = re.findall("debates\&amp;pop=1\"><strong>(.*?) debates</strong>", page, re.DOTALL)  
    # enacted = re.findall("Date of Signature: (.*?)<BR>", page, re.DOTALL)  
        wrans = re.findall("wrans\&amp;pop=1\"><strong>(.*?) written questions</strong>", page, re.DOTALL)  

        # Just keep the heading text
        # (Try commenting this out)
        # headings = [gettext(heading) for heading in headings]

#        Has spoken in 0 debates in the last year — well below average among TDs.
# Has received answers to 0 written questions in the last year — well below average among TDs.
# People have made 0 comments on this TD's speeches — average among TDs.
# This TD's speeches, in the printed record, are readable by an average 15–16 year old, going by the Flesch-Kincaid Grade Level score.
# 38 people are tracking whenever this TD speaks — email me whenever Bertie Ahern speaks.
# Has used three-word alliterative phrases (e.g. "she sells seashells") 2139 times in debates — well above average among TDs. (Why is this here?)
 

# <li>Has spoken in <a href="/search/?pid=22&amp;s=section%3Adebates&amp;pop=1"><strong>172 debates</strong></a> in the last year &#8212; well above average among TDs.Has received answers to <li><a href="/search/?pid=74&amp;s=section%3Awrans&amp;pop=1"><strong>353 written questions</strong></a><li>People have made <a href="/comments/recent/?pid=22"><strong>5 comments</strong></a> on this #TD's speeches &#8212; well above average among TDs.<li>This TD's speeches, in the printed record, are readable by an average <strong>17&ndash;18</strong> year old, going by the <a #href="http://en.wikipedia.org/wiki/Flesch-Kincaid_Readability_Test">Flesch-Kincaid Grade Level</a> score.        <li><strong>65</strong> people are tracking whenever this TD speaks &mdash; <a #href="/alert/?only=1&amp;pid=22">email me whenever Dermot Ahern speaks</a>.</li><li>Has used three-word alliterative phrases (e.g. "she sells seashells") <strong>678 times</strong> in debates &#8212; #well above average among TDs. <small>(<a href="/help/#numbers">Why is this here?</a>)</small> 
        
        
        data = {'url': url, 'title': title, 'spoken':spoken, 'wrans':wrans} 
#,  'enacted':enacted}
          #datastore.save(unique_keys=['link'], data=data, date=date_missing)
        scraperwiki.sqlite.save(['url'], data)   # each entry is identified by its url
"""
This is an example of scraping multiple URLs.
"""

import scraperwiki
import re

import BeautifulSoup
from datetime import datetime
from scraperwiki import datastore

# The URLs we're going to scrape:

urls = """

http://www.kildarestreet.com/td/caoimhghin_o_caolain/cavan-monaghan
http://www.kildarestreet.com/td/eamon_o_cuiv/galway_west
http://www.kildarestreet.com/td/sean_o_fearghail/kildare_south
http://www.kildarestreet.com/td/aengus_o_snodaigh/dublin_south_central
http://www.kildarestreet.com/td/bertie_ahern/dublin_central
http://www.kildarestreet.com/td/dermot_ahern/louth
http://www.kildarestreet.com/td/michael_ahern/cork_east
http://www.kildarestreet.com/td/noel_ahern/dublin_north_west
http://www.kildarestreet.com/td/bernard_allen/cork_north_central
http://www.kildarestreet.com/td/barry_andrews/dun_laoghaire
http://www.kildarestreet.com/td/chris_andrews/dublin_south_east
http://www.kildarestreet.com/td/sean_ardagh/dublin_south_central
http://www.kildarestreet.com/td/bobby_aylward/carlow-kilkenny
http://www.kildarestreet.com/td/james_bannon/longford-westmeath
http://www.kildarestreet.com/td/sean_barrett/dun_laoghaire
http://www.kildarestreet.com/td/joe_behan/wicklow
http://www.kildarestreet.com/td/niall_blaney/donegal_north_east
http://www.kildarestreet.com/td/aine_brady/kildare_north
http://www.kildarestreet.com/td/cyprian_brady/dublin_central
http://www.kildarestreet.com/td/johnny_brady/meath_west
http://www.kildarestreet.com/td/pat_breen/clare
http://www.kildarestreet.com/td/tommy_broughan/dublin_north_east
http://www.kildarestreet.com/td/john_browne/wexford
http://www.kildarestreet.com/td/richard_bruton/dublin_north_central
http://www.kildarestreet.com/td/ulick_burke/galway_east
http://www.kildarestreet.com/td/joan_burton/dublin_west
http://www.kildarestreet.com/td/catherine_byrne/dublin_south_central
http://www.kildarestreet.com/td/thomas_byrne/meath_east
http://www.kildarestreet.com/td/dara_calleary/mayo
http://www.kildarestreet.com/td/joe_carey/clare
http://www.kildarestreet.com/td/pat_carey/dublin_north_west
http://www.kildarestreet.com/td/deirdre_clune/cork_south_central
http://www.kildarestreet.com/td/niall_collins/limerick_west
http://www.kildarestreet.com/td/margaret_conlon/cavan-monaghan
http://www.kildarestreet.com/td/paul_connaughton/galway_east
http://www.kildarestreet.com/td/sean_connick/wexford
http://www.kildarestreet.com/td/noel_coonan/tipperary_north
http://www.kildarestreet.com/td/joe_costello/dublin_central
http://www.kildarestreet.com/td/mary_coughlan/donegal_south_west
http://www.kildarestreet.com/td/simon_coveney/cork_south_central
http://www.kildarestreet.com/td/brian_cowen/laois-offaly
http://www.kildarestreet.com/td/seymour_crawford/cavan-monaghan
http://www.kildarestreet.com/td/michael_creed/cork_north_west
http://www.kildarestreet.com/td/john_cregan/limerick_west
http://www.kildarestreet.com/td/lucinda_creighton/dublin_south_east
http://www.kildarestreet.com/td/ciaran_cuffe/dun_laoghaire
http://www.kildarestreet.com/td/john_curran/dublin_mid_west
http://www.kildarestreet.com/td/michael_d%27arcy/wexford
http://www.kildarestreet.com/td/john_deasy/waterford
http://www.kildarestreet.com/td/jimmy_deenihan/kerry_north
http://www.kildarestreet.com/td/noel_dempsey/meath_west
http://www.kildarestreet.com/td/jimmy_devins/sligo-north_leitrim
http://www.kildarestreet.com/td/timmy_dooley/clare
http://www.kildarestreet.com/td/andrew_doyle/wicklow
http://www.kildarestreet.com/td/bernard_durkan/kildare_north
http://www.kildarestreet.com/td/damien_english/meath_west
http://www.kildarestreet.com/td/olwyn_enright/laois-offaly
http://www.kildarestreet.com/td/frank_fahey/galway_west
http://www.kildarestreet.com/td/frank_feighan/roscommon-south_leitrim
http://www.kildarestreet.com/td/martin_ferris/kerry_north
http://www.kildarestreet.com/td/michael_finneran/roscommon-south_leitrim
http://www.kildarestreet.com/td/michael_fitzpatrick/kildare_north
http://www.kildarestreet.com/td/charles_flanagan/laois-offaly
http://www.kildarestreet.com/td/terence_flanagan/dublin_north_east
http://www.kildarestreet.com/td/sean_fleming/laois-offaly
http://www.kildarestreet.com/td/beverley_flynn/mayo
http://www.kildarestreet.com/td/eamon_gilmore/dun_laoghaire
http://www.kildarestreet.com/td/paul_gogarty/dublin_mid_west
http://www.kildarestreet.com/td/john_gormley/dublin_south_east
http://www.kildarestreet.com/td/noel_grealish/galway_west
http://www.kildarestreet.com/td/mary_hanafin/dun_laoghaire
http://www.kildarestreet.com/td/mary_harney/dublin_mid_west
http://www.kildarestreet.com/td/sean_haughey/dublin_north_central
http://www.kildarestreet.com/td/brian_hayes/dublin_south_west
http://www.kildarestreet.com/td/tom_hayes/tipperary_south
http://www.kildarestreet.com/td/jackie_healy-rae/kerry_south
http://www.kildarestreet.com/td/michael_d_higgins/galway_west
http://www.kildarestreet.com/td/maire_hoctor/tipperary_north
http://www.kildarestreet.com/td/phil_hogan/carlow-kilkenny
http://www.kildarestreet.com/td/brendan_howlin/wexford
http://www.kildarestreet.com/td/paul_kehoe/wexford
http://www.kildarestreet.com/td/billy_kelleher/cork_north_central
http://www.kildarestreet.com/td/peter_kelly/longford-westmeath
http://www.kildarestreet.com/td/brendan_kenneally/waterford
http://www.kildarestreet.com/td/michael_kennedy/dublin_north
http://www.kildarestreet.com/td/enda_kenny/mayo
http://www.kildarestreet.com/td/tony_killeen/clare
http://www.kildarestreet.com/td/seamus_kirk/louth
http://www.kildarestreet.com/td/michael_kitt/galway_east
http://www.kildarestreet.com/td/tom_kitt/dublin_south
http://www.kildarestreet.com/td/conor_lenihan/dublin_south_west
http://www.kildarestreet.com/td/brian_lenihan_jnr/dublin_west
http://www.kildarestreet.com/td/michael_lowry/tipperary_north
http://www.kildarestreet.com/td/ciaran_lynch/cork_south_central
http://www.kildarestreet.com/td/kathleen_lynch/cork_north_central
http://www.kildarestreet.com/td/martin_mansergh/tipperary_south
http://www.kildarestreet.com/td/micheal_martin/cork_south_central
http://www.kildarestreet.com/td/padraic_mccormack/galway_west
http://www.kildarestreet.com/td/jim_mcdaid/donegal_north_east
http://www.kildarestreet.com/td/tom_mcellistrim/kerry_north
http://www.kildarestreet.com/td/shane_mcentee/meath_east
http://www.kildarestreet.com/td/dinny_mcginley/donegal_south_west
http://www.kildarestreet.com/td/finian_mcgrath/dublin_north_central
http://www.kildarestreet.com/td/mattie_mcgrath/tipperary_south
http://www.kildarestreet.com/td/michael_mcgrath/cork_south_central
http://www.kildarestreet.com/td/john_mcguinness/carlow-kilkenny
http://www.kildarestreet.com/td/joe_mchugh/donegal_north_east
http://www.kildarestreet.com/td/liz_mcmanus/wicklow
http://www.kildarestreet.com/td/olivia_mitchell/dublin_south
http://www.kildarestreet.com/td/john_moloney/laois-offaly
http://www.kildarestreet.com/td/arthur_morgan/louth
http://www.kildarestreet.com/td/michael_moynihan/cork_north_west
http://www.kildarestreet.com/td/michael_mulcahy/dublin_south_central
http://www.kildarestreet.com/td/denis_naughten/roscommon-south_leitrim
http://www.kildarestreet.com/td/dan_neville/limerick_west
http://www.kildarestreet.com/td/m_j_nolan/carlow-kilkenny
http://www.kildarestreet.com/td/michael_noonan/limerick_east
http://www.kildarestreet.com/td/darragh_o%27brien/dublin_north
http://www.kildarestreet.com/td/charlie_o%27connor/dublin_south_west
http://www.kildarestreet.com/td/willie_o%27dea/limerick_east
http://www.kildarestreet.com/td/kieran_o%27donnell/limerick_east
http://www.kildarestreet.com/td/john_o%27donoghue/kerry_south
http://www.kildarestreet.com/td/fergus_o%27dowd/louth
http://www.kildarestreet.com/td/noel_o%27flynn/cork_north_central
http://www.kildarestreet.com/td/rory_o%27hanlon/cavan-monaghan
http://www.kildarestreet.com/td/batt_o%27keeffe/cork_north_west
http://www.kildarestreet.com/td/jim_o%27keeffe/cork_south_west
http://www.kildarestreet.com/td/ned_o%27keeffe/cork_east
http://www.kildarestreet.com/td/john_o%27mahony/mayo
http://www.kildarestreet.com/td/mary_o%27rourke/longford-westmeath
http://www.kildarestreet.com/td/brian_o%27shea/waterford
http://www.kildarestreet.com/td/christy_o%27sullivan/cork_south_west
http://www.kildarestreet.com/td/jan_o%27sullivan/limerick_east
http://www.kildarestreet.com/td/maureen_o%27sullivan/dublin_central
http://www.kildarestreet.com/td/willie_penrose/longford-westmeath
http://www.kildarestreet.com/td/john_perry/sligo-north_leitrim
http://www.kildarestreet.com/td/peter_power/limerick_east
http://www.kildarestreet.com/td/sean_power/kildare_south
http://www.kildarestreet.com/td/ruairi_quinn/dublin_south_east
http://www.kildarestreet.com/td/pat_rabbitte/dublin_south_west
http://www.kildarestreet.com/td/james_reilly/dublin_north
http://www.kildarestreet.com/td/michael_ring/mayo
http://www.kildarestreet.com/td/dick_roche/wicklow
http://www.kildarestreet.com/td/eamon_ryan/dublin_south
http://www.kildarestreet.com/td/trevor_sargent/dublin_north
http://www.kildarestreet.com/td/eamon_scanlon/sligo-north_leitrim
http://www.kildarestreet.com/td/alan_shatter/dublin_south
http://www.kildarestreet.com/td/tom_sheahan/kerry_south
http://www.kildarestreet.com/td/p_j_sheehan/cork_south_west
http://www.kildarestreet.com/td/sean_sherlock/cork_east
http://www.kildarestreet.com/td/roisin_shortall/dublin_north_west
http://www.kildarestreet.com/td/brendan_smith/cavan-monaghan
http://www.kildarestreet.com/td/emmet_stagg/kildare_north
http://www.kildarestreet.com/td/david_stanton/cork_east
http://www.kildarestreet.com/td/billy_timmins/wicklow
http://www.kildarestreet.com/td/noel_treacy/galway_east
http://www.kildarestreet.com/td/joanna_tuffy/dublin_mid_west
http://www.kildarestreet.com/td/mary_upton/dublin_south_central
http://www.kildarestreet.com/td/leo_varadkar/dublin_west
http://www.kildarestreet.com/td/jack_wall/kildare_south
http://www.kildarestreet.com/td/mary_wallace/meath_east
http://www.kildarestreet.com/td/mary_white/carlow-kilkenny
http://www.kildarestreet.com/td/michael_woods/dublin_north_east

""".strip()

urls = urls.splitlines()


# This is a useful helper function that you might want to steal.
# It cleans up the data a bit.
# def gettext(html):
  #  """Return the text within html, removing any HTML tags it contained."""
  #  cleaned = re.sub('<.*?>', '', html)  # remove tags
   # cleaned = ' '.join(cleaned.split())  # collapse whitespace
    # return cleaned

# get all the bill links from http://www.oireachtas.ie/viewdoc.asp?m=&DocID=-1&CatID=59
# http://www.oireachtas.ie/viewdoc.asp?DocID=14885&amp;&amp;CatID=59
# 30 April 2010<br /><a href="viewdoc.asp?DocID=14879&amp;&amp;CatID=59" >Non-Medicinal Psychoactive Substances Bill 2010 (PMB)

for url in urls:
    print "Scraping", url
    page = scraperwiki.scrape(url)
    if page is not None:
        # Store all the h2 headings (matching "<h2>...</h2>")
        title = re.findall("<title>(.*?)</title>", page, re.DOTALL)
        # re.DOTALL makes it work across multiple lines as well.
        
        spoken = re.findall("debates\&amp;pop=1\"><strong>(.*?) debates</strong>", page, re.DOTALL)  
    # enacted = re.findall("Date of Signature: (.*?)<BR>", page, re.DOTALL)  
        wrans = re.findall("wrans\&amp;pop=1\"><strong>(.*?) written questions</strong>", page, re.DOTALL)  

        # Just keep the heading text
        # (Try commenting this out)
        # headings = [gettext(heading) for heading in headings]

#        Has spoken in 0 debates in the last year — well below average among TDs.
# Has received answers to 0 written questions in the last year — well below average among TDs.
# People have made 0 comments on this TD's speeches — average among TDs.
# This TD's speeches, in the printed record, are readable by an average 15–16 year old, going by the Flesch-Kincaid Grade Level score.
# 38 people are tracking whenever this TD speaks — email me whenever Bertie Ahern speaks.
# Has used three-word alliterative phrases (e.g. "she sells seashells") 2139 times in debates — well above average among TDs. (Why is this here?)
 

# <li>Has spoken in <a href="/search/?pid=22&amp;s=section%3Adebates&amp;pop=1"><strong>172 debates</strong></a> in the last year &#8212; well above average among TDs.Has received answers to <li><a href="/search/?pid=74&amp;s=section%3Awrans&amp;pop=1"><strong>353 written questions</strong></a><li>People have made <a href="/comments/recent/?pid=22"><strong>5 comments</strong></a> on this #TD's speeches &#8212; well above average among TDs.<li>This TD's speeches, in the printed record, are readable by an average <strong>17&ndash;18</strong> year old, going by the <a #href="http://en.wikipedia.org/wiki/Flesch-Kincaid_Readability_Test">Flesch-Kincaid Grade Level</a> score.        <li><strong>65</strong> people are tracking whenever this TD speaks &mdash; <a #href="/alert/?only=1&amp;pid=22">email me whenever Dermot Ahern speaks</a>.</li><li>Has used three-word alliterative phrases (e.g. "she sells seashells") <strong>678 times</strong> in debates &#8212; #well above average among TDs. <small>(<a href="/help/#numbers">Why is this here?</a>)</small> 
        
        
        data = {'url': url, 'title': title, 'spoken':spoken, 'wrans':wrans} 
#,  'enacted':enacted}
          #datastore.save(unique_keys=['link'], data=data, date=date_missing)
        scraperwiki.sqlite.save(['url'], data)   # each entry is identified by its url
"""
This is an example of scraping multiple URLs.
"""

import scraperwiki
import re

import BeautifulSoup
from datetime import datetime
from scraperwiki import datastore

# The URLs we're going to scrape:

urls = """

http://www.kildarestreet.com/td/caoimhghin_o_caolain/cavan-monaghan
http://www.kildarestreet.com/td/eamon_o_cuiv/galway_west
http://www.kildarestreet.com/td/sean_o_fearghail/kildare_south
http://www.kildarestreet.com/td/aengus_o_snodaigh/dublin_south_central
http://www.kildarestreet.com/td/bertie_ahern/dublin_central
http://www.kildarestreet.com/td/dermot_ahern/louth
http://www.kildarestreet.com/td/michael_ahern/cork_east
http://www.kildarestreet.com/td/noel_ahern/dublin_north_west
http://www.kildarestreet.com/td/bernard_allen/cork_north_central
http://www.kildarestreet.com/td/barry_andrews/dun_laoghaire
http://www.kildarestreet.com/td/chris_andrews/dublin_south_east
http://www.kildarestreet.com/td/sean_ardagh/dublin_south_central
http://www.kildarestreet.com/td/bobby_aylward/carlow-kilkenny
http://www.kildarestreet.com/td/james_bannon/longford-westmeath
http://www.kildarestreet.com/td/sean_barrett/dun_laoghaire
http://www.kildarestreet.com/td/joe_behan/wicklow
http://www.kildarestreet.com/td/niall_blaney/donegal_north_east
http://www.kildarestreet.com/td/aine_brady/kildare_north
http://www.kildarestreet.com/td/cyprian_brady/dublin_central
http://www.kildarestreet.com/td/johnny_brady/meath_west
http://www.kildarestreet.com/td/pat_breen/clare
http://www.kildarestreet.com/td/tommy_broughan/dublin_north_east
http://www.kildarestreet.com/td/john_browne/wexford
http://www.kildarestreet.com/td/richard_bruton/dublin_north_central
http://www.kildarestreet.com/td/ulick_burke/galway_east
http://www.kildarestreet.com/td/joan_burton/dublin_west
http://www.kildarestreet.com/td/catherine_byrne/dublin_south_central
http://www.kildarestreet.com/td/thomas_byrne/meath_east
http://www.kildarestreet.com/td/dara_calleary/mayo
http://www.kildarestreet.com/td/joe_carey/clare
http://www.kildarestreet.com/td/pat_carey/dublin_north_west
http://www.kildarestreet.com/td/deirdre_clune/cork_south_central
http://www.kildarestreet.com/td/niall_collins/limerick_west
http://www.kildarestreet.com/td/margaret_conlon/cavan-monaghan
http://www.kildarestreet.com/td/paul_connaughton/galway_east
http://www.kildarestreet.com/td/sean_connick/wexford
http://www.kildarestreet.com/td/noel_coonan/tipperary_north
http://www.kildarestreet.com/td/joe_costello/dublin_central
http://www.kildarestreet.com/td/mary_coughlan/donegal_south_west
http://www.kildarestreet.com/td/simon_coveney/cork_south_central
http://www.kildarestreet.com/td/brian_cowen/laois-offaly
http://www.kildarestreet.com/td/seymour_crawford/cavan-monaghan
http://www.kildarestreet.com/td/michael_creed/cork_north_west
http://www.kildarestreet.com/td/john_cregan/limerick_west
http://www.kildarestreet.com/td/lucinda_creighton/dublin_south_east
http://www.kildarestreet.com/td/ciaran_cuffe/dun_laoghaire
http://www.kildarestreet.com/td/john_curran/dublin_mid_west
http://www.kildarestreet.com/td/michael_d%27arcy/wexford
http://www.kildarestreet.com/td/john_deasy/waterford
http://www.kildarestreet.com/td/jimmy_deenihan/kerry_north
http://www.kildarestreet.com/td/noel_dempsey/meath_west
http://www.kildarestreet.com/td/jimmy_devins/sligo-north_leitrim
http://www.kildarestreet.com/td/timmy_dooley/clare
http://www.kildarestreet.com/td/andrew_doyle/wicklow
http://www.kildarestreet.com/td/bernard_durkan/kildare_north
http://www.kildarestreet.com/td/damien_english/meath_west
http://www.kildarestreet.com/td/olwyn_enright/laois-offaly
http://www.kildarestreet.com/td/frank_fahey/galway_west
http://www.kildarestreet.com/td/frank_feighan/roscommon-south_leitrim
http://www.kildarestreet.com/td/martin_ferris/kerry_north
http://www.kildarestreet.com/td/michael_finneran/roscommon-south_leitrim
http://www.kildarestreet.com/td/michael_fitzpatrick/kildare_north
http://www.kildarestreet.com/td/charles_flanagan/laois-offaly
http://www.kildarestreet.com/td/terence_flanagan/dublin_north_east
http://www.kildarestreet.com/td/sean_fleming/laois-offaly
http://www.kildarestreet.com/td/beverley_flynn/mayo
http://www.kildarestreet.com/td/eamon_gilmore/dun_laoghaire
http://www.kildarestreet.com/td/paul_gogarty/dublin_mid_west
http://www.kildarestreet.com/td/john_gormley/dublin_south_east
http://www.kildarestreet.com/td/noel_grealish/galway_west
http://www.kildarestreet.com/td/mary_hanafin/dun_laoghaire
http://www.kildarestreet.com/td/mary_harney/dublin_mid_west
http://www.kildarestreet.com/td/sean_haughey/dublin_north_central
http://www.kildarestreet.com/td/brian_hayes/dublin_south_west
http://www.kildarestreet.com/td/tom_hayes/tipperary_south
http://www.kildarestreet.com/td/jackie_healy-rae/kerry_south
http://www.kildarestreet.com/td/michael_d_higgins/galway_west
http://www.kildarestreet.com/td/maire_hoctor/tipperary_north
http://www.kildarestreet.com/td/phil_hogan/carlow-kilkenny
http://www.kildarestreet.com/td/brendan_howlin/wexford
http://www.kildarestreet.com/td/paul_kehoe/wexford
http://www.kildarestreet.com/td/billy_kelleher/cork_north_central
http://www.kildarestreet.com/td/peter_kelly/longford-westmeath
http://www.kildarestreet.com/td/brendan_kenneally/waterford
http://www.kildarestreet.com/td/michael_kennedy/dublin_north
http://www.kildarestreet.com/td/enda_kenny/mayo
http://www.kildarestreet.com/td/tony_killeen/clare
http://www.kildarestreet.com/td/seamus_kirk/louth
http://www.kildarestreet.com/td/michael_kitt/galway_east
http://www.kildarestreet.com/td/tom_kitt/dublin_south
http://www.kildarestreet.com/td/conor_lenihan/dublin_south_west
http://www.kildarestreet.com/td/brian_lenihan_jnr/dublin_west
http://www.kildarestreet.com/td/michael_lowry/tipperary_north
http://www.kildarestreet.com/td/ciaran_lynch/cork_south_central
http://www.kildarestreet.com/td/kathleen_lynch/cork_north_central
http://www.kildarestreet.com/td/martin_mansergh/tipperary_south
http://www.kildarestreet.com/td/micheal_martin/cork_south_central
http://www.kildarestreet.com/td/padraic_mccormack/galway_west
http://www.kildarestreet.com/td/jim_mcdaid/donegal_north_east
http://www.kildarestreet.com/td/tom_mcellistrim/kerry_north
http://www.kildarestreet.com/td/shane_mcentee/meath_east
http://www.kildarestreet.com/td/dinny_mcginley/donegal_south_west
http://www.kildarestreet.com/td/finian_mcgrath/dublin_north_central
http://www.kildarestreet.com/td/mattie_mcgrath/tipperary_south
http://www.kildarestreet.com/td/michael_mcgrath/cork_south_central
http://www.kildarestreet.com/td/john_mcguinness/carlow-kilkenny
http://www.kildarestreet.com/td/joe_mchugh/donegal_north_east
http://www.kildarestreet.com/td/liz_mcmanus/wicklow
http://www.kildarestreet.com/td/olivia_mitchell/dublin_south
http://www.kildarestreet.com/td/john_moloney/laois-offaly
http://www.kildarestreet.com/td/arthur_morgan/louth
http://www.kildarestreet.com/td/michael_moynihan/cork_north_west
http://www.kildarestreet.com/td/michael_mulcahy/dublin_south_central
http://www.kildarestreet.com/td/denis_naughten/roscommon-south_leitrim
http://www.kildarestreet.com/td/dan_neville/limerick_west
http://www.kildarestreet.com/td/m_j_nolan/carlow-kilkenny
http://www.kildarestreet.com/td/michael_noonan/limerick_east
http://www.kildarestreet.com/td/darragh_o%27brien/dublin_north
http://www.kildarestreet.com/td/charlie_o%27connor/dublin_south_west
http://www.kildarestreet.com/td/willie_o%27dea/limerick_east
http://www.kildarestreet.com/td/kieran_o%27donnell/limerick_east
http://www.kildarestreet.com/td/john_o%27donoghue/kerry_south
http://www.kildarestreet.com/td/fergus_o%27dowd/louth
http://www.kildarestreet.com/td/noel_o%27flynn/cork_north_central
http://www.kildarestreet.com/td/rory_o%27hanlon/cavan-monaghan
http://www.kildarestreet.com/td/batt_o%27keeffe/cork_north_west
http://www.kildarestreet.com/td/jim_o%27keeffe/cork_south_west
http://www.kildarestreet.com/td/ned_o%27keeffe/cork_east
http://www.kildarestreet.com/td/john_o%27mahony/mayo
http://www.kildarestreet.com/td/mary_o%27rourke/longford-westmeath
http://www.kildarestreet.com/td/brian_o%27shea/waterford
http://www.kildarestreet.com/td/christy_o%27sullivan/cork_south_west
http://www.kildarestreet.com/td/jan_o%27sullivan/limerick_east
http://www.kildarestreet.com/td/maureen_o%27sullivan/dublin_central
http://www.kildarestreet.com/td/willie_penrose/longford-westmeath
http://www.kildarestreet.com/td/john_perry/sligo-north_leitrim
http://www.kildarestreet.com/td/peter_power/limerick_east
http://www.kildarestreet.com/td/sean_power/kildare_south
http://www.kildarestreet.com/td/ruairi_quinn/dublin_south_east
http://www.kildarestreet.com/td/pat_rabbitte/dublin_south_west
http://www.kildarestreet.com/td/james_reilly/dublin_north
http://www.kildarestreet.com/td/michael_ring/mayo
http://www.kildarestreet.com/td/dick_roche/wicklow
http://www.kildarestreet.com/td/eamon_ryan/dublin_south
http://www.kildarestreet.com/td/trevor_sargent/dublin_north
http://www.kildarestreet.com/td/eamon_scanlon/sligo-north_leitrim
http://www.kildarestreet.com/td/alan_shatter/dublin_south
http://www.kildarestreet.com/td/tom_sheahan/kerry_south
http://www.kildarestreet.com/td/p_j_sheehan/cork_south_west
http://www.kildarestreet.com/td/sean_sherlock/cork_east
http://www.kildarestreet.com/td/roisin_shortall/dublin_north_west
http://www.kildarestreet.com/td/brendan_smith/cavan-monaghan
http://www.kildarestreet.com/td/emmet_stagg/kildare_north
http://www.kildarestreet.com/td/david_stanton/cork_east
http://www.kildarestreet.com/td/billy_timmins/wicklow
http://www.kildarestreet.com/td/noel_treacy/galway_east
http://www.kildarestreet.com/td/joanna_tuffy/dublin_mid_west
http://www.kildarestreet.com/td/mary_upton/dublin_south_central
http://www.kildarestreet.com/td/leo_varadkar/dublin_west
http://www.kildarestreet.com/td/jack_wall/kildare_south
http://www.kildarestreet.com/td/mary_wallace/meath_east
http://www.kildarestreet.com/td/mary_white/carlow-kilkenny
http://www.kildarestreet.com/td/michael_woods/dublin_north_east

""".strip()

urls = urls.splitlines()


# This is a useful helper function that you might want to steal.
# It cleans up the data a bit.
# def gettext(html):
  #  """Return the text within html, removing any HTML tags it contained."""
  #  cleaned = re.sub('<.*?>', '', html)  # remove tags
   # cleaned = ' '.join(cleaned.split())  # collapse whitespace
    # return cleaned

# get all the bill links from http://www.oireachtas.ie/viewdoc.asp?m=&DocID=-1&CatID=59
# http://www.oireachtas.ie/viewdoc.asp?DocID=14885&amp;&amp;CatID=59
# 30 April 2010<br /><a href="viewdoc.asp?DocID=14879&amp;&amp;CatID=59" >Non-Medicinal Psychoactive Substances Bill 2010 (PMB)

for url in urls:
    print "Scraping", url
    page = scraperwiki.scrape(url)
    if page is not None:
        # Store all the h2 headings (matching "<h2>...</h2>")
        title = re.findall("<title>(.*?)</title>", page, re.DOTALL)
        # re.DOTALL makes it work across multiple lines as well.
        
        spoken = re.findall("debates\&amp;pop=1\"><strong>(.*?) debates</strong>", page, re.DOTALL)  
    # enacted = re.findall("Date of Signature: (.*?)<BR>", page, re.DOTALL)  
        wrans = re.findall("wrans\&amp;pop=1\"><strong>(.*?) written questions</strong>", page, re.DOTALL)  

        # Just keep the heading text
        # (Try commenting this out)
        # headings = [gettext(heading) for heading in headings]

#        Has spoken in 0 debates in the last year — well below average among TDs.
# Has received answers to 0 written questions in the last year — well below average among TDs.
# People have made 0 comments on this TD's speeches — average among TDs.
# This TD's speeches, in the printed record, are readable by an average 15–16 year old, going by the Flesch-Kincaid Grade Level score.
# 38 people are tracking whenever this TD speaks — email me whenever Bertie Ahern speaks.
# Has used three-word alliterative phrases (e.g. "she sells seashells") 2139 times in debates — well above average among TDs. (Why is this here?)
 

# <li>Has spoken in <a href="/search/?pid=22&amp;s=section%3Adebates&amp;pop=1"><strong>172 debates</strong></a> in the last year &#8212; well above average among TDs.Has received answers to <li><a href="/search/?pid=74&amp;s=section%3Awrans&amp;pop=1"><strong>353 written questions</strong></a><li>People have made <a href="/comments/recent/?pid=22"><strong>5 comments</strong></a> on this #TD's speeches &#8212; well above average among TDs.<li>This TD's speeches, in the printed record, are readable by an average <strong>17&ndash;18</strong> year old, going by the <a #href="http://en.wikipedia.org/wiki/Flesch-Kincaid_Readability_Test">Flesch-Kincaid Grade Level</a> score.        <li><strong>65</strong> people are tracking whenever this TD speaks &mdash; <a #href="/alert/?only=1&amp;pid=22">email me whenever Dermot Ahern speaks</a>.</li><li>Has used three-word alliterative phrases (e.g. "she sells seashells") <strong>678 times</strong> in debates &#8212; #well above average among TDs. <small>(<a href="/help/#numbers">Why is this here?</a>)</small> 
        
        
        data = {'url': url, 'title': title, 'spoken':spoken, 'wrans':wrans} 
#,  'enacted':enacted}
          #datastore.save(unique_keys=['link'], data=data, date=date_missing)
        scraperwiki.sqlite.save(['url'], data)   # each entry is identified by its url
