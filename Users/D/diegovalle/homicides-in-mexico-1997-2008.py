###########################################################################################
# Scrape the CIEISP pdf forms from the Mexican Police Website
# which contain the number of homicides from Jan 1997 to Sep 2010
###########################################################################################
import scraperwiki
import json
from BeautifulSoup import BeautifulSoup


def scrape_cieisp(year, text):
    if (year == 2010):
        pdfurl = "http://www.secretariadoejecutivosnsp.gob.mx/work/models/SecretariadoEjecutivo/Resource/131/1/images/INCIDENCIA_DELICTIVA_2010_030211.pdf"
    else:
        pdfurl = "http://www.secretariadoejecutivosnsp.gob.mx/work/models/SecretariadoEjecutivo/Resource/131/1/images/CIEISP" + `year` + ".pdf"
    a = scraperwiki.scrape(pdfurl)
    s = BeautifulSoup(scraperwiki.pdftoxml(a))

    dolosos_position = []
    i = 0
    for t in s.findAll('text'):
        if t.text == "DOLOSOS":
            if text == "POR ARMA DE FUEGO":
                dolosos_position.append(i+14)
            else:
                dolosos_position.append(i)
        i += 1

    all_text = s.findAll('text')
    #print all_text
    
    if (year <= 2008) :
        if (year >=2006):
            states_names = states3
        else:
            states_names = states2
    else:
        states_names = states

    for i in range(0,33):
        for j in range(1,14):
            record = {'State' : states_names[i], 'Year' : year, 'Month' : months[j-1], 'Homicides' : all_text[dolosos_position[i]+j].text, 'Crimetype' : text}
            scraperwiki.datastore.save(["State", "Year", "Month"], record)
    return


months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Tot']
states = ['National', 'Aguascalientes', 'Baja California', 'Baja California Sur', 'Campeche',
'Chiapas', 'Chihuahua', 'Coahuila', 'Colima', 'Distrito Federal', 'Durango', 'Guanajuato',
'Guerrero', 'Hidalgo', 'Jalisco', 'Mexico', 'Michoacan', 'Morelos', 'Nayarit', 'Nuevo Leon',
'Oaxaca', 'Puebla', 'Queretaro', 'Quintana Roo', 'San Luis Potosi', 'Sinaloa', 'Sonora',
'Tamaulipas', 'Tabasco', 'Tlaxcala', 'Veracruz', 'Yucatan', 'Zacatecas']

#2006-2008 with tabasco and tamaulipas in the correct order
states3 = ['National', 'Aguascalientes', 'Baja California', 'Baja California Sur', 'Campeche',
 'Coahuila', 'Colima','Chiapas', 'Chihuahua', 'Distrito Federal', 'Durango', 'Guanajuato',
'Guerrero', 'Hidalgo', 'Jalisco', 'Mexico', 'Michoacan', 'Morelos', 'Nayarit', 'Nuevo Leon',
'Oaxaca', 'Puebla', 'Queretaro', 'Quintana Roo', 'San Luis Potosi', 'Sinaloa', 'Sonora',
 'Tabasco', 'Tamaulipas', 'Tlaxcala', 'Veracruz', 'Yucatan', 'Zacatecas']

#Before 2009 the states are not in alphabethical order
states2 = ['National', 'Aguascalientes', 'Baja California', 'Baja California Sur', 'Campeche',
 'Coahuila', 'Colima','Chiapas', 'Chihuahua', 'Distrito Federal', 'Durango', 'Guanajuato',
'Guerrero', 'Hidalgo', 'Jalisco', 'Mexico', 'Michoacan', 'Morelos', 'Nayarit', 'Nuevo Leon',
'Oaxaca', 'Puebla', 'Queretaro', 'Quintana Roo', 'San Luis Potosi', 'Sinaloa', 'Sonora',
'Tamaulipas' , 'Tabasco', 'Tlaxcala', 'Veracruz', 'Yucatan', 'Zacatecas']
# column headings
record = {'State' : 'State', 'Year' : 'Year', 'Month' : 'Month', 'Homicides' :'Homicides', 'Crimetype' : 'Crimetype'}
scraperwiki.datastore.save(["State", "Year", "Month"], record)

#for year in range(1997,2011):
#    scrape_cieisp(year, "POR ARMA DE FUEGO")
for year in range(1997,2011):
    scrape_cieisp(year, "DOLOSOS")

#scrape_cieisp(1997, "POR ARMA DE FUEGO")
scrape_cieisp(1997, "DOLOSOS")

