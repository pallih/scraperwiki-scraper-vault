import scraperwiki
from BeautifulSoup import BeautifulSoup
from time import sleep
from random import randint

start_id = 116
end_id = 117
sleep_time = randint (1,2)

for url_id in range (start_id ,end_id):
#http://open.dapper.net/RunDapp?dappName=PortaldaSaude&v=1&applyToUrl=   
    base_url  = "http://www.min-saude.pt/Portal/servicos/prestadoresV2/?providerid="
    url  = base_url + str(url_id)
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup(html, fromEncoding='utf-8')     

#print soup

#status = soup.find('status').text

#if status == "OK":

people = soup.findAll("div", {"class":"right_l"})[2]
rows = people.findAll("span")

for row in range (1, len(rows)/2):
   
        record= {}
#        record['Type']            = 'People'
        record['ID_INST']         = url_id
        record['ID_LINK']         = row
        record['Nome_Link']       = people.findAll('span')[2 * row - 2].text
        record['Cargo_Ind']       = people.findAll('span')[2 * row - 1].text
        
        scraperwiki.sqlite.save(["ID_INST","ID_LINK"], record, table_name="people")
    
institution = soup.findAll("div", {"class":"right_l"})[16]
rows_inst = institution .findAll("span")
for row_inst in range (1, len(rows_inst)):  
        record= {}
#        record['Type']            = 'Institution'
        record['ID_INST']         = url_id
        record['ID_LINK']         = institution.findAll('a', href=True)[row_inst-1]['href']
        record['Nome_Link']       = institution.findAll('span')[row_inst - 1].text
        
        scraperwiki.sqlite.save(["ID_INST","ID_LINK"], record, table_name="institution")

