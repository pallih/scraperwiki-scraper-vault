import scraperwiki
import scraperwiki html = scraperwiki.scrape('http://webapp.etsi.org/WorkProgram/Frame_WorkItemList.asp?SearchPage=TRUE&butExpertSearch=++Search++&qETSI_STANDARD_TYPE=&qETSI_NUMBER=&qTB_ID=&qINCLUDE_SUB_TB=True&includeNonActiveTB=FALSE&qWKI_REFERENCE=&qTITLE=&qSCOPE=&qCURRENT_STATE_CODE=&qSTOP_FLG=N&qSTART_CURRENT_STATUS_CODE=&qEND_CURRENT_STATUS_CODE=&qFROM_MIL_DAY=&qFROM_MIL_MONTH=&qFROM_MIL_YEAR=&qTO_MIL_DAY=&qTO_MIL_MONTH=&qTO_MIL_YEAR=&qOPERATOR_TS=&qRAPTR_NAME=&qRAPTR_ORGANISATION=&qKEYWORD_BOOLEAN=OR&qKEYWORD=&qPROJECT_BOOLEAN=OR&qPROJECT_CODE=&includeSubProjectCode=FALSE&qSTF_List=&qDIRECTIVE=&qMandate_List=&qSORT=HIGHVERSION&qREPORT_TYPE=SUMMARY&optDisplay=10&titleType=all') 




import lxml.html 
root = lxml.html.fromstring(html)
for tr in root.cssselect("div[align='left'] tr.tcont"): tds = tr.cssselect("td") data = { 'country' : tds[0].text_content(), 'years_in_school' : int(tds[4].text_content()) } 
        scraperwiki.sqlite.save(unique_keys=['country'], data=data)
