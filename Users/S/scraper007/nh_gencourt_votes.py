import scraperwiki
from datetime import datetime

lib = scraperwiki.utils.swimport('common-lib')

root_url = "http://www.gencourt.state.nh.us/nhgcrollcalls/"

root = lib.br_load_page(root_url)

last_year = lib.get_var('last_year')

#scraperwiki.sqlite.execute("delete from rep_votes where rep_name = 'Representative'")

for opt in sorted(root.cssselect('select#lbHouseSessionYears option'), key=lambda opt: opt.attrib['value']):
    year = opt.attrib['value']

    if last_year != None and year <= last_year:
        continue

    page = lib.br_submit_form('form1', { 'lbHouseSessionYears' : [ year ], '__EVENTTARGET' : 'btnHouseSearch', '__EVENTARGUMENT' : '' })
    
    last_date = lib.get_var('last_date')
    for opt in sorted(page.cssselect('select#lblSessionDates option'), key=lambda opt: datetime.strptime(opt.attrib['value'], '%m/%d/%Y')):
        date = opt.attrib['value']

        if last_date != None and datetime.strptime(date, '%m/%d/%Y') <= datetime.strptime(last_date, '%m/%d/%Y'):
            continue
    
        page = lib.br_submit_form('form1', { 'lblSessionDates' : [ opt.attrib['value'] ] })
        
        last_link = lib.get_var('last_link')
        for link in sorted(page.xpath('//a[text()="View Votes"]'), key=lambda link: link.attrib['id']):
            link_name = link.attrib['id'].replace('_', '$')

            if last_link != None and link_name <= last_link:
                continue
            
            page = lib.br_submit_form('form1', { '__EVENTTARGET' : link_name, '__EVENTARGUMENT' : '' })
        
            vote_num = lib.get_node_text(page, 'span#lblVoteNo')

            yeas = lib.get_node_text(page, 'span#lblYeas')
            nays = lib.get_node_text(page, 'span#lblNays')

            bill_data = {
                'date_of_vote' : date,
                'vote_num' : vote_num,
                'bill_num' : lib.get_node_text(page, 'span#lblBillNo'),
                'bill_title' : lib.get_node_text(page, 'span#lblBillTitle'),
                'question_or_motion' : lib.get_node_text(page, 'span#lblQuestion_Motion'),
                'yeas' : int(yeas if yeas != '' else 0),
                'nays' : int(nays if nays != '' else 0),
            }

            scraperwiki.sqlite.save(unique_keys=['date_of_vote', 'vote_num'], data=bill_data, table_name="bill_votes")

            rep_data = []        
            for row in page.cssselect('table#dlLegislators tr td table tr')[1:]:        
                tds = row.cssselect('td')
                rep_data.append({
                    'date_of_vote' : date,
                    'vote_num' : vote_num,
                    'rep_name' : tds[0].text_content().strip(),
                    'party' : tds[1].text_content().strip(),
                    'county' : tds[2].text_content().strip(),
                    'district' : tds[3].text_content().strip(),
                    'how_voted' : tds[4].text_content().strip(),
                })
        
            scraperwiki.sqlite.save(unique_keys=['date_of_vote', 'vote_num', 'rep_name'], data=rep_data, table_name="rep_votes")

            lib.save_var('last_link', link_name)        
            lib.br_back()

        lib.save_var('last_date', date)
        lib.save_var('last_link', None)
        lib.br_back()

    if int(year) < datetime.now().year:
        lib.save_var('last_year', year)
        lib.save_var('last_date', None)
    lib.save_var('last_link', None)
    lib.br_back()

print 'DONE'
