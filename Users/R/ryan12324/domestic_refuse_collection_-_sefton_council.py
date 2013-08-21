import scraperwiki
import mechanize
import twill
from bs4 import BeautifulSoup
from twill.commands import *
form = "aspnetForm";

go("http://www.sefton.gov.uk/default.aspx?page=4247");

formclear(form);
fv(form,"Template$ctl38$ctl00$TxtBoxPostCode","pr8 5ej");

submit(8);

soup = BeautifulSoup(show());
table = soup.find_all('table');



for record in soup.table.find_all("tr"):
    record = record;
    for cell in soup.record.find_all("td"):
        print(soup.cell.contents)
