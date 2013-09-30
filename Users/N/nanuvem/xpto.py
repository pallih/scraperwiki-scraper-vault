import scraperwiki
from BeautifulSoup import BeautifulSoup
from datetime import date
import urllib2

range =[
'%20%20%20Comprimido%20de%20liberta%E7%E3o%20prolongada%20revestido%20por%20pel%EDcula'
, '%20%20%20Comprimido%20gastrorresistente%20de%20liberta%E7%E3o%20prolongada'
, '%20%20%20Emplastro%20para%20teste%20cut%E2neo'
, '%20%20%20Gl%F3bulos'
, '%20%20%20Granulado%20gastrorresistente%20de%20liberta%E7%E3o%20prolongada'
, '%20%20%20Granulado%20para%20solu%E7%E3o%20oral%20ou%20rectal'
, '%20%20%20Granulado%20revestido%20em%20saqueta'
, '%20%20%20Pel%EDcula%20bucal'
, '%20%20%20Pel%EDcula%20orodispers%EDvel'
, '%20%20%20P%F3%20e%20solvente%20para%20solu%E7%E3o%20para%20inala%E7%E3o%20por%20nebuliza%E7%E3o'
, '%20%20%20P%F3%20para%20solu%E7%E3o%20ou%20para%20suspens%E3o%20inject%E1vel'
, '%20%20%20P%F3%20para%20solu%E7%E3o%20vaginal'
, '%20%20%20Solu%E7%E3o%20inject%E1vel%20ou%20para%20perfus%E3o'
, '%20%20%20Solu%E7%E3o%20para%20pulveriza%E7%E3o%20bucal%20ou%20nasal'
, '%20%20%20Solu%E7%E3o%20para%20teste%20cut%E2neo%20em%20picada'
, '%20%20%20Suspens%E3o%20inject%E1vel%20de%20liberta%E7%E3o%20prolongada'
, 'Adesivo%20cut%E2neo'
, 'Aditivo%20para%20banho'
, '%20%20%20Col%EDrio,%20comprimido%20e%20solvente%20para%20solu%E7%E3o'
, 'Champ%F4'
, 'Ch%E1%20medicinal'
, 'Ch%E1%20medicinal%20instant%E2neo'
, 'Col%EDrio%20de%20liberta%E7%E3o%20prolongada'
, 'Col%EDrio,%20solu%E7%E3o'
, 'Col%EDrio,%20suspens%E3o'
, 'Comprimido'
, 'Comprimido%20+%20Suspens%E3o%20Oral'
, 'Comprimido%20bucal'
, 'Comprimido%20bucal%20mucoadesivo'
, 'Comprimido%20de%20liberta%E7%E3o%20modificada'
, 'Comprimido%20de%20liberta%E7%E3o%20prolongada'
, 'Comprimido%20dispers%EDvel'
, 'Comprimido%20dispers%EDvel%20ou%20para%20mastigar'
, 'Comprimido%20efervescente'
, 'Comprimido%20gastrorresistente'
, 'Comprimido%20orodispers%EDvel'
, 'Comprimido%20para%20chupar'
, 'Comprimido%20para%20mastigar'
, 'Comprimido%20para%20suspens%E3o%20rectal'
, 'Comprimido%20revestido'
, 'Comprimido%20revestido%20por%20pel%EDcula'
, 'Comprimido%20sol%FAvel'
, 'Comprimido%20sublingual'
, 'Comprimido%20vaginal'
, 'Concentrado%20para%20solu%E7%E3o%20cut%E2nea'
, 'Concentrado%20para%20solu%E7%E3o%20inject%E1vel'
, 'Concentrado%20para%20solu%E7%E3o%20inject%E1vel%20ou%20para%20perfus%E3o'
, 'Concentrado%20para%20solu%E7%E3o%20oral'
, 'Concentrado%20para%20solu%E7%E3o%20para%20perfus%E3o'
, 'Creme'
, 'Creme%20rectal'
, 'Creme%20vaginal'
, 'Creme%20vaginal%20+%20%D3vulo'
, 'C%E1psula'
, 'C%E1psula%20de%20liberta%E7%E3o%20modificada'
, 'C%E1psula%20de%20liberta%E7%E3o%20prolongada'
, 'C%E1psula%20gastrorresistente'
, 'C%E1psula%20mole'
, 'C%E1psula%20mole%20vaginal'
, 'Dispositivo%20de%20liberta%E7%E3o%20intra-uterino'
, 'Emplastro%20medicamentoso'
, 'Emuls%E3o%20cut%E2nea'
, 'Emuls%E3o%20oral'
, 'Espuma%20cut%E2nea'
, 'Espuma%20rectal'
, 'Espuma%20vaginal'
, 'Gel'
, 'Gel%20bucal'
, 'Gel%20dental'
, 'Gel%20intestinal'
, 'Gel%20nasal'
, 'Gel%20oft%E1lmico'
, 'Gel%20oral'
, 'Gel%20periodontal'
, 'Gel%20rectal'
, 'Gel%20vaginal'
, 'Goma%20para%20mascar%20medicamentosa'
, 'Gotas%20auriculares%20ou%20col%EDrio,%20solu%E7%E3o'
, 'Gotas%20auriculares,%20solu%E7%E3o'
, 'Gotas%20auriculares,%20suspens%E3o'
, 'Gotas%20nasais,%20solu%E7%E3o'
, 'Gotas%20orais,%20emuls%E3o'
, 'Gotas%20orais,%20solu%E7%E3o'
, 'Gotas%20orais,%20suspens%E3o'
, 'Granulado'
, 'Granulado%20de%20liberta%E7%E3o%20modificada'
, 'Granulado%20de%20liberta%E7%E3o%20prolongada'
, 'Granulado%20de%20liberta%E7%E3o%20prolongada%20para%20suspens%E3o%20oral'
, 'Granulado%20efervescente'
, 'Granulado%20gastrorresistente'
, 'Granulado%20gastrorresistente%20para%20suspens%E3o%20oral'
, 'Granulado%20para%20solu%E7%E3o%20oral'
, 'Granulado%20para%20suspens%E3o%20oral'
, 'Implante'
, 'Inserto%20oft%E1lmico'
, 'Liofilizado%20oral'
, 'L%E1pis%20uretral'
, 'L%EDquido%20cut%E2neo'
, 'L%EDquido%20para%20inala%E7%E3o%20por%20vaporiza%E7%E3o'
, 'Pasta%20cut%E2nea'
, 'Pasta%20dent%EDfrica'
, 'Pasta%20oral'
, 'Pastilha'
, 'Pastilha%20mole'
, 'Penso%20impregnado'
, 'Pomada'
, 'Pomada%20nasal'
, 'Pomada%20oft%E1lmica'
, 'Pomada%20rectal'
, 'P%F3%20cut%E2neo'
, 'P%F3%20e%20solu%E7%E3o%20para%20solu%E7%E3o%20inject%E1vel'
, 'P%F3%20e%20solvente%20para%20solu%E7%E3o%20cut%E2nea'
, 'P%F3%20e%20solvente%20para%20solu%E7%E3o%20inject%E1vel'
, 'P%F3%20e%20solvente%20para%20solu%E7%E3o%20oral'
, 'P%F3%20e%20suspens%E3o%20para%20suspens%E3o%20inject%E1vel'
, 'P%F3%20e%20ve%EDculo%20para%20suspens%E3o%20inject%E1vel'
, 'P%F3%20e%20ve%EDculo%20para%20suspens%E3o%20inject%E1vel%20de%20liberta%E7%E3o%20prolongada'
, 'P%F3%20e%20ve%EDculo%20para%20suspens%E3o%20oral'
, 'P%F3%20efervescente'
, 'P%F3%20oral'
, 'P%F3%20para%20concentrado%20para%20solu%E7%E3o%20para%20perfus%E3o'
, 'P%F3%20para%20inala%E7%E3o'
, 'P%F3%20para%20inala%E7%E3o%20em%20recipiente%20unidose'
, 'P%F3%20para%20inala%E7%E3o,%20c%E1psula'
, 'P%F3%20para%20pulveriza%E7%E3o%20cut%E2nea'
, 'P%F3%20para%20solu%E7%E3o%20inject%E1vel'
, 'P%F3%20para%20solu%E7%E3o%20inject%E1vel%20ou%20para%20perfus%E3o'
, 'P%F3%20para%20solu%E7%E3o%20oral'
, 'P%F3%20para%20solu%E7%E3o%20oral%20em%20saqueta'
, 'P%F3%20para%20solu%E7%E3o%20para%20perfus%E3o'
, 'P%F3%20para%20suspens%E3o%20inject%E1vel%20+%20Suspens%E3o%20inject%E1vel'
, 'P%F3%20para%20suspens%E3o%20oral'
, 'P%F3%20para%20suspens%E3o%20oral%20ou%20rectal'
, 'Sistema%20de%20liberta%E7%E3o%20vaginal'
, 'Sistema%20transd%E9rmico'
, 'Solu%E7%E3o%20bucal'
, 'Solu%E7%E3o%20cut%E2nea'
, 'Solu%E7%E3o%20dental'
, 'Solu%E7%E3o%20gengival'
, 'Solu%E7%E3o%20inject%E1vel'
, 'Solu%E7%E3o%20inject%E1vel%20em%20caneta%20pr%E9-cheia'
, 'Solu%E7%E3o%20inject%E1vel%20em%20seringa%20pr%E9-cheia'
, 'Solu%E7%E3o%20oral'
, 'Solu%E7%E3o%20oral%20+%20P%F3%20para%20solu%E7%E3o%20oral'
, 'Solu%E7%E3o%20para%20di%E1lise%20peritoneal'
, 'Solu%E7%E3o%20para%20gargarejar'
, 'Solu%E7%E3o%20para%20inala%E7%E3o%20por%20nebuliza%E7%E3o'
, 'Solu%E7%E3o%20para%20inala%E7%E3o%20por%20vaporiza%E7%E3o'
, 'Solu%E7%E3o%20para%20lavagem%20da%20boca'
, 'Solu%E7%E3o%20para%20lavagem%20oft%E1lmica'
, 'Solu%E7%E3o%20para%20perfus%E3o'
, 'Solu%E7%E3o%20para%20pulveriza%E7%E3o%20bucal'
, 'Solu%E7%E3o%20para%20pulveriza%E7%E3o%20cut%E2nea'
, 'Solu%E7%E3o%20para%20pulveriza%E7%E3o%20nasal'
, 'Solu%E7%E3o%20pressurizada%20para%20inala%E7%E3o'
, 'Solu%E7%E3o%20rectal'
, 'Solu%E7%E3o%20vaginal'
, 'Suposit%F3rio'
, 'Suspens%E3o%20cut%E2nea'
, 'Suspens%E3o%20dental'
, 'Suspens%E3o%20inject%E1vel'
, 'Suspens%E3o%20inject%E1vel%20em%20seringa%20pr%E9-cheia'
, 'Suspens%E3o%20oral'
, 'Suspens%E3o%20para%20inala%E7%E3o%20por%20nebuliza%E7%E3o'
, 'Suspens%E3o%20para%20pulveriza%E7%E3o%20nasal'
, 'Suspens%E3o%20pressurizada%20para%20inala%E7%E3o'
, 'Suspens%E3o%20rectal'
, 'Verniz%20para%20as%20unhas%20medicamentoso'
, 'Xarope'
, '%D3vulo'
]




for ff in range:
    start_url = "http://www.infarmed.pt/genericos/pesquisamg/pesquisaMG.php?page=1&ipp=Todos&firstime=NO&controlo=false&i_dci=&i_MarcaCom=*&i_NumReg=&i_FFarm="
    end_url = "&i_Dosagem=&i_TamanhoEmb="
    url  = start_url + ff + end_url 

    html = scraperwiki.scrape(url)

    soup = BeautifulSoup(html)

    datetime = date.today()
#    print soup
    tipo = soup.findAll("td")[44].text
    tipo2 = urllib2.quote(tipo.encode('utf-16'))
    print tipo2

    #find table class="reports"
    data_table = soup.findAll("table")[6]
        #find each table row <tr>
        #rows = data_table.findAll("tr")
        #for each row, igonring first line, loop through this
    for row in data_table.findAll("tr")[1:]:
        #create a record to hold the data
                record = {}
                #find each cell <td>
                table_cells = row.findAll("td")
                #if there is a cell, record the contents in our dataset, the first cell [0] in 'Name' and so on
                if table_cells:
                    record['DT'] = datetime
                    record['NREG'] = table_cells[0].text
                    record['DCI'] = table_cells[1].text
                    record['NOME'] = table_cells[2].text
                    record['FF'] = table_cells[3].text
                    record['DOSAGEM'] = table_cells[4].text
                    record['TAMANHO'] = table_cells[5].text
                    record['PVPMAX'] = table_cells[6].text
                    record['PVP'] = table_cells[7].text
                    record['PUTENTE'] = table_cells[8].text
                    record['PPENSIO'] = table_cells[9].text
                    record['GEN'] = table_cells[10].text
                    record['COM'] = table_cells[11].text
                # Print out the data we've gathered
                # print record, '------------'
                # Save the record to the datastore - 'Name' is our unique key - 
                scraperwiki.sqlite.save(["DT","NREG"], record)import scraperwiki
from BeautifulSoup import BeautifulSoup
from datetime import date
import urllib2

range =[
'%20%20%20Comprimido%20de%20liberta%E7%E3o%20prolongada%20revestido%20por%20pel%EDcula'
, '%20%20%20Comprimido%20gastrorresistente%20de%20liberta%E7%E3o%20prolongada'
, '%20%20%20Emplastro%20para%20teste%20cut%E2neo'
, '%20%20%20Gl%F3bulos'
, '%20%20%20Granulado%20gastrorresistente%20de%20liberta%E7%E3o%20prolongada'
, '%20%20%20Granulado%20para%20solu%E7%E3o%20oral%20ou%20rectal'
, '%20%20%20Granulado%20revestido%20em%20saqueta'
, '%20%20%20Pel%EDcula%20bucal'
, '%20%20%20Pel%EDcula%20orodispers%EDvel'
, '%20%20%20P%F3%20e%20solvente%20para%20solu%E7%E3o%20para%20inala%E7%E3o%20por%20nebuliza%E7%E3o'
, '%20%20%20P%F3%20para%20solu%E7%E3o%20ou%20para%20suspens%E3o%20inject%E1vel'
, '%20%20%20P%F3%20para%20solu%E7%E3o%20vaginal'
, '%20%20%20Solu%E7%E3o%20inject%E1vel%20ou%20para%20perfus%E3o'
, '%20%20%20Solu%E7%E3o%20para%20pulveriza%E7%E3o%20bucal%20ou%20nasal'
, '%20%20%20Solu%E7%E3o%20para%20teste%20cut%E2neo%20em%20picada'
, '%20%20%20Suspens%E3o%20inject%E1vel%20de%20liberta%E7%E3o%20prolongada'
, 'Adesivo%20cut%E2neo'
, 'Aditivo%20para%20banho'
, '%20%20%20Col%EDrio,%20comprimido%20e%20solvente%20para%20solu%E7%E3o'
, 'Champ%F4'
, 'Ch%E1%20medicinal'
, 'Ch%E1%20medicinal%20instant%E2neo'
, 'Col%EDrio%20de%20liberta%E7%E3o%20prolongada'
, 'Col%EDrio,%20solu%E7%E3o'
, 'Col%EDrio,%20suspens%E3o'
, 'Comprimido'
, 'Comprimido%20+%20Suspens%E3o%20Oral'
, 'Comprimido%20bucal'
, 'Comprimido%20bucal%20mucoadesivo'
, 'Comprimido%20de%20liberta%E7%E3o%20modificada'
, 'Comprimido%20de%20liberta%E7%E3o%20prolongada'
, 'Comprimido%20dispers%EDvel'
, 'Comprimido%20dispers%EDvel%20ou%20para%20mastigar'
, 'Comprimido%20efervescente'
, 'Comprimido%20gastrorresistente'
, 'Comprimido%20orodispers%EDvel'
, 'Comprimido%20para%20chupar'
, 'Comprimido%20para%20mastigar'
, 'Comprimido%20para%20suspens%E3o%20rectal'
, 'Comprimido%20revestido'
, 'Comprimido%20revestido%20por%20pel%EDcula'
, 'Comprimido%20sol%FAvel'
, 'Comprimido%20sublingual'
, 'Comprimido%20vaginal'
, 'Concentrado%20para%20solu%E7%E3o%20cut%E2nea'
, 'Concentrado%20para%20solu%E7%E3o%20inject%E1vel'
, 'Concentrado%20para%20solu%E7%E3o%20inject%E1vel%20ou%20para%20perfus%E3o'
, 'Concentrado%20para%20solu%E7%E3o%20oral'
, 'Concentrado%20para%20solu%E7%E3o%20para%20perfus%E3o'
, 'Creme'
, 'Creme%20rectal'
, 'Creme%20vaginal'
, 'Creme%20vaginal%20+%20%D3vulo'
, 'C%E1psula'
, 'C%E1psula%20de%20liberta%E7%E3o%20modificada'
, 'C%E1psula%20de%20liberta%E7%E3o%20prolongada'
, 'C%E1psula%20gastrorresistente'
, 'C%E1psula%20mole'
, 'C%E1psula%20mole%20vaginal'
, 'Dispositivo%20de%20liberta%E7%E3o%20intra-uterino'
, 'Emplastro%20medicamentoso'
, 'Emuls%E3o%20cut%E2nea'
, 'Emuls%E3o%20oral'
, 'Espuma%20cut%E2nea'
, 'Espuma%20rectal'
, 'Espuma%20vaginal'
, 'Gel'
, 'Gel%20bucal'
, 'Gel%20dental'
, 'Gel%20intestinal'
, 'Gel%20nasal'
, 'Gel%20oft%E1lmico'
, 'Gel%20oral'
, 'Gel%20periodontal'
, 'Gel%20rectal'
, 'Gel%20vaginal'
, 'Goma%20para%20mascar%20medicamentosa'
, 'Gotas%20auriculares%20ou%20col%EDrio,%20solu%E7%E3o'
, 'Gotas%20auriculares,%20solu%E7%E3o'
, 'Gotas%20auriculares,%20suspens%E3o'
, 'Gotas%20nasais,%20solu%E7%E3o'
, 'Gotas%20orais,%20emuls%E3o'
, 'Gotas%20orais,%20solu%E7%E3o'
, 'Gotas%20orais,%20suspens%E3o'
, 'Granulado'
, 'Granulado%20de%20liberta%E7%E3o%20modificada'
, 'Granulado%20de%20liberta%E7%E3o%20prolongada'
, 'Granulado%20de%20liberta%E7%E3o%20prolongada%20para%20suspens%E3o%20oral'
, 'Granulado%20efervescente'
, 'Granulado%20gastrorresistente'
, 'Granulado%20gastrorresistente%20para%20suspens%E3o%20oral'
, 'Granulado%20para%20solu%E7%E3o%20oral'
, 'Granulado%20para%20suspens%E3o%20oral'
, 'Implante'
, 'Inserto%20oft%E1lmico'
, 'Liofilizado%20oral'
, 'L%E1pis%20uretral'
, 'L%EDquido%20cut%E2neo'
, 'L%EDquido%20para%20inala%E7%E3o%20por%20vaporiza%E7%E3o'
, 'Pasta%20cut%E2nea'
, 'Pasta%20dent%EDfrica'
, 'Pasta%20oral'
, 'Pastilha'
, 'Pastilha%20mole'
, 'Penso%20impregnado'
, 'Pomada'
, 'Pomada%20nasal'
, 'Pomada%20oft%E1lmica'
, 'Pomada%20rectal'
, 'P%F3%20cut%E2neo'
, 'P%F3%20e%20solu%E7%E3o%20para%20solu%E7%E3o%20inject%E1vel'
, 'P%F3%20e%20solvente%20para%20solu%E7%E3o%20cut%E2nea'
, 'P%F3%20e%20solvente%20para%20solu%E7%E3o%20inject%E1vel'
, 'P%F3%20e%20solvente%20para%20solu%E7%E3o%20oral'
, 'P%F3%20e%20suspens%E3o%20para%20suspens%E3o%20inject%E1vel'
, 'P%F3%20e%20ve%EDculo%20para%20suspens%E3o%20inject%E1vel'
, 'P%F3%20e%20ve%EDculo%20para%20suspens%E3o%20inject%E1vel%20de%20liberta%E7%E3o%20prolongada'
, 'P%F3%20e%20ve%EDculo%20para%20suspens%E3o%20oral'
, 'P%F3%20efervescente'
, 'P%F3%20oral'
, 'P%F3%20para%20concentrado%20para%20solu%E7%E3o%20para%20perfus%E3o'
, 'P%F3%20para%20inala%E7%E3o'
, 'P%F3%20para%20inala%E7%E3o%20em%20recipiente%20unidose'
, 'P%F3%20para%20inala%E7%E3o,%20c%E1psula'
, 'P%F3%20para%20pulveriza%E7%E3o%20cut%E2nea'
, 'P%F3%20para%20solu%E7%E3o%20inject%E1vel'
, 'P%F3%20para%20solu%E7%E3o%20inject%E1vel%20ou%20para%20perfus%E3o'
, 'P%F3%20para%20solu%E7%E3o%20oral'
, 'P%F3%20para%20solu%E7%E3o%20oral%20em%20saqueta'
, 'P%F3%20para%20solu%E7%E3o%20para%20perfus%E3o'
, 'P%F3%20para%20suspens%E3o%20inject%E1vel%20+%20Suspens%E3o%20inject%E1vel'
, 'P%F3%20para%20suspens%E3o%20oral'
, 'P%F3%20para%20suspens%E3o%20oral%20ou%20rectal'
, 'Sistema%20de%20liberta%E7%E3o%20vaginal'
, 'Sistema%20transd%E9rmico'
, 'Solu%E7%E3o%20bucal'
, 'Solu%E7%E3o%20cut%E2nea'
, 'Solu%E7%E3o%20dental'
, 'Solu%E7%E3o%20gengival'
, 'Solu%E7%E3o%20inject%E1vel'
, 'Solu%E7%E3o%20inject%E1vel%20em%20caneta%20pr%E9-cheia'
, 'Solu%E7%E3o%20inject%E1vel%20em%20seringa%20pr%E9-cheia'
, 'Solu%E7%E3o%20oral'
, 'Solu%E7%E3o%20oral%20+%20P%F3%20para%20solu%E7%E3o%20oral'
, 'Solu%E7%E3o%20para%20di%E1lise%20peritoneal'
, 'Solu%E7%E3o%20para%20gargarejar'
, 'Solu%E7%E3o%20para%20inala%E7%E3o%20por%20nebuliza%E7%E3o'
, 'Solu%E7%E3o%20para%20inala%E7%E3o%20por%20vaporiza%E7%E3o'
, 'Solu%E7%E3o%20para%20lavagem%20da%20boca'
, 'Solu%E7%E3o%20para%20lavagem%20oft%E1lmica'
, 'Solu%E7%E3o%20para%20perfus%E3o'
, 'Solu%E7%E3o%20para%20pulveriza%E7%E3o%20bucal'
, 'Solu%E7%E3o%20para%20pulveriza%E7%E3o%20cut%E2nea'
, 'Solu%E7%E3o%20para%20pulveriza%E7%E3o%20nasal'
, 'Solu%E7%E3o%20pressurizada%20para%20inala%E7%E3o'
, 'Solu%E7%E3o%20rectal'
, 'Solu%E7%E3o%20vaginal'
, 'Suposit%F3rio'
, 'Suspens%E3o%20cut%E2nea'
, 'Suspens%E3o%20dental'
, 'Suspens%E3o%20inject%E1vel'
, 'Suspens%E3o%20inject%E1vel%20em%20seringa%20pr%E9-cheia'
, 'Suspens%E3o%20oral'
, 'Suspens%E3o%20para%20inala%E7%E3o%20por%20nebuliza%E7%E3o'
, 'Suspens%E3o%20para%20pulveriza%E7%E3o%20nasal'
, 'Suspens%E3o%20pressurizada%20para%20inala%E7%E3o'
, 'Suspens%E3o%20rectal'
, 'Verniz%20para%20as%20unhas%20medicamentoso'
, 'Xarope'
, '%D3vulo'
]




for ff in range:
    start_url = "http://www.infarmed.pt/genericos/pesquisamg/pesquisaMG.php?page=1&ipp=Todos&firstime=NO&controlo=false&i_dci=&i_MarcaCom=*&i_NumReg=&i_FFarm="
    end_url = "&i_Dosagem=&i_TamanhoEmb="
    url  = start_url + ff + end_url 

    html = scraperwiki.scrape(url)

    soup = BeautifulSoup(html)

    datetime = date.today()
#    print soup
    tipo = soup.findAll("td")[44].text
    tipo2 = urllib2.quote(tipo.encode('utf-16'))
    print tipo2

    #find table class="reports"
    data_table = soup.findAll("table")[6]
        #find each table row <tr>
        #rows = data_table.findAll("tr")
        #for each row, igonring first line, loop through this
    for row in data_table.findAll("tr")[1:]:
        #create a record to hold the data
                record = {}
                #find each cell <td>
                table_cells = row.findAll("td")
                #if there is a cell, record the contents in our dataset, the first cell [0] in 'Name' and so on
                if table_cells:
                    record['DT'] = datetime
                    record['NREG'] = table_cells[0].text
                    record['DCI'] = table_cells[1].text
                    record['NOME'] = table_cells[2].text
                    record['FF'] = table_cells[3].text
                    record['DOSAGEM'] = table_cells[4].text
                    record['TAMANHO'] = table_cells[5].text
                    record['PVPMAX'] = table_cells[6].text
                    record['PVP'] = table_cells[7].text
                    record['PUTENTE'] = table_cells[8].text
                    record['PPENSIO'] = table_cells[9].text
                    record['GEN'] = table_cells[10].text
                    record['COM'] = table_cells[11].text
                # Print out the data we've gathered
                # print record, '------------'
                # Save the record to the datastore - 'Name' is our unique key - 
                scraperwiki.sqlite.save(["DT","NREG"], record)