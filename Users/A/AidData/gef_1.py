import scraperwiki
import urlparse
import lxml.html

for i in range(1,5400): #USER: update range as necessary
    try:
        url = "http://www.thegef.org/gef/project_detail?projID=%s" % i

        html = scraperwiki.scrape(url)
        root = lxml.html.fromstring(html)

        tds = root.cssselect("td") # get all the <td> tags
        pres = root.cssselect("pre") #get all the <pre> tags
        data = {
            'gef_proj_id' : tds[1].text_content(),
            'undp_pmis_id' : tds[3].text_content(),
            'funding_source' : tds[5].text_content(),
            'proj_name' : tds[7].text_content(),
            'country' : tds[9].text_content(),
            'region' : tds[11].text_content(),
            'focal_area' : tds[13].text_content(),
            'operational_program' : tds[15].text_content(), 
            'pipeline_entry_date' : tds[17].text_content(),
            'pdfb_approval_date' : tds[19].text_content(), 
            'approval_date' : tds[21].text_content(),
            'ceo_endorsement_date' : tds[23].text_content(),
            'gef_agency_approval_date' : tds[25].text_content(),
            'project_completion_date' : tds[27].text_content(),
            'project_status' : tds[29].text_content(),
            'gef_agency' : tds[31].text_content(),
            'executing_agency' : tds[33].text_content(),
            'description' : tds[35].text_content(), 
            'pdfb_amount' : pres[0].text_content(), 
            'gef_proj_grant' : pres[1].text_content(),
            'gef_grant' : pres[2].text_content(), 
            'cofinancing_total' : pres[3].text_content(),
            'proj_cost' : pres[4].text_content(), 
            'gef_agency_fees' : pres[5].text_content(),
            'gef_proj_ceo_endo' : pres[6].text_content(),
            'cofinancing_total_ceo_endo' : pres[7].text_content(),
            'proj_cost_ceo_endo' : pres[8].text_content(), 
        }
        scraperwiki.sqlite.save(unique_keys=['gef_proj_id'], data=data)

    except:
       print i
        ## try-except lets us skip URLs that do not exist, and then keep looping
import scraperwiki
import urlparse
import lxml.html

for i in range(1,5400): #USER: update range as necessary
    try:
        url = "http://www.thegef.org/gef/project_detail?projID=%s" % i

        html = scraperwiki.scrape(url)
        root = lxml.html.fromstring(html)

        tds = root.cssselect("td") # get all the <td> tags
        pres = root.cssselect("pre") #get all the <pre> tags
        data = {
            'gef_proj_id' : tds[1].text_content(),
            'undp_pmis_id' : tds[3].text_content(),
            'funding_source' : tds[5].text_content(),
            'proj_name' : tds[7].text_content(),
            'country' : tds[9].text_content(),
            'region' : tds[11].text_content(),
            'focal_area' : tds[13].text_content(),
            'operational_program' : tds[15].text_content(), 
            'pipeline_entry_date' : tds[17].text_content(),
            'pdfb_approval_date' : tds[19].text_content(), 
            'approval_date' : tds[21].text_content(),
            'ceo_endorsement_date' : tds[23].text_content(),
            'gef_agency_approval_date' : tds[25].text_content(),
            'project_completion_date' : tds[27].text_content(),
            'project_status' : tds[29].text_content(),
            'gef_agency' : tds[31].text_content(),
            'executing_agency' : tds[33].text_content(),
            'description' : tds[35].text_content(), 
            'pdfb_amount' : pres[0].text_content(), 
            'gef_proj_grant' : pres[1].text_content(),
            'gef_grant' : pres[2].text_content(), 
            'cofinancing_total' : pres[3].text_content(),
            'proj_cost' : pres[4].text_content(), 
            'gef_agency_fees' : pres[5].text_content(),
            'gef_proj_ceo_endo' : pres[6].text_content(),
            'cofinancing_total_ceo_endo' : pres[7].text_content(),
            'proj_cost_ceo_endo' : pres[8].text_content(), 
        }
        scraperwiki.sqlite.save(unique_keys=['gef_proj_id'], data=data)

    except:
       print i
        ## try-except lets us skip URLs that do not exist, and then keep looping
