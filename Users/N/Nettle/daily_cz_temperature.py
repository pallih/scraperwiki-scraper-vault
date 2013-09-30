import scraperwiki           
import lxml.html
html = scraperwiki.scrape("http://pr-asv.chmi.cz/synopy-map/pocasiin.php?ukazatel=prumtep&pozadi=mapareg&graf=ano")
root = lxml.html.fromstring(html)

data = {
            'date' : root.cssselect("div.vgtext")[0].text,
            'Holesov' : root.cssselect("div.vgtext")[1].text,
            'Brno_Turany' : root.cssselect("div.vgtext")[2].text,
            'Dukovany' : root.cssselect("div.vgtext")[3].text,
            'Kostelni_Myslova' : root.cssselect("div.vgtext")[4].text,
            'Kucharovice' : root.cssselect("div.vgtext")[5].text,
            'Churanov' : root.cssselect("div.vgtext")[6].text,
            'Kocelovice' : root.cssselect("div.vgtext")[7].text,
            'Temelin' : root.cssselect("div.vgtext")[8].text,
            'Ceske_Budejovice' : root.cssselect("div.vgtext")[9].text,
            'Pec_pod_Snezkou' : root.cssselect("div.vgtext")[10].text,
            'Polom' : root.cssselect("div.vgtext")[11].text,
            'Usti_nad_Orlici' : root.cssselect("div.vgtext")[12].text,
                
            #Caslav
            #'Pardubice' : root.cssselect("div.vgtext")[13].text,
            #'Svratouch' : root.cssselect("div.vgtext")[14].text,
            #'Plzen_Mikulka' : root.cssselect("div.vgtext")[15].text,
            #'Primda' : root.cssselect("div.vgtext")[16].text,
            #'Cheb' : root.cssselect("div.vgtext")[17].text,
            #'Karlovy_Vary' : root.cssselect("div.vgtext")[18].text,
            #'Cervena_u_Libave' : root.cssselect("div.vgtext")[19].text,
            #'Lysa_Hora' : root.cssselect("div.vgtext")[20].text,
            #'Ostrava' : root.cssselect("div.vgtext")[21].text,
            #'Serak' : root.cssselect("div.vgtext")[22].text,
            #'Luka' : root.cssselect("div.vgtext")[23].text,
            #'Prerov' : root.cssselect("div.vgtext")[24].text,
            #'Praha_Libus' : root.cssselect("div.vgtext")[25].text,
            #'Praha_Ruzyne' : root.cssselect("div.vgtext")[26].text,
            #'Kosetice' : root.cssselect("div.vgtext")[27].text,
            #'Pribyslav' : root.cssselect("div.vgtext")[28].text,
            #'Doksany' : root.cssselect("div.vgtext")[29].text,
            #'Tusimice' : root.cssselect("div.vgtext")[30].text,
            #'Milesovka' : root.cssselect("div.vgtext")[31].text,
            #'Usti_nad_Labem' : root.cssselect("div.vgtext")[32].text,
            #'Liberec' : root.cssselect("div.vgtext")[33].text

            #Prerov
            #'Caslav' : root.cssselect("div.vgtext")[13].text,
            #'Pardubice' : root.cssselect("div.vgtext")[14].text,
            #'Svratouch' : root.cssselect("div.vgtext")[15].text,
            #'Plzen_Mikulka' : root.cssselect("div.vgtext")[16].text,
            #'Primda' : root.cssselect("div.vgtext")[17].text,
            #'Cheb' : root.cssselect("div.vgtext")[18].text,
            #'Karlovy_Vary' : root.cssselect("div.vgtext")[19].text,
            #'Cervena_u_Libave' : root.cssselect("div.vgtext")[20].text,
            #'Lysa_Hora' : root.cssselect("div.vgtext")[21].text,
            #'Ostrava' : root.cssselect("div.vgtext")[22].text,
            #'Serak' : root.cssselect("div.vgtext")[23].text,
            #'Luka' : root.cssselect("div.vgtext")[24].text,
            #'Praha_Libus' : root.cssselect("div.vgtext")[25].text,
            #'Praha_Ruzyne' : root.cssselect("div.vgtext")[26].text,
            #'Kosetice' : root.cssselect("div.vgtext")[27].text,
            #'Pribyslav' : root.cssselect("div.vgtext")[28].text,
            #'Doksany' : root.cssselect("div.vgtext")[29].text,
            #'Tusimice' : root.cssselect("div.vgtext")[30].text,
            #'Milesovka' : root.cssselect("div.vgtext")[31].text,
            #'Usti_nad_Labem' : root.cssselect("div.vgtext")[32].text,
            #'Liberec' : root.cssselect("div.vgtext")[33].text

            'Caslav' : root.cssselect("div.vgtext")[13].text,
            'Pardubice' : root.cssselect("div.vgtext")[14].text,
            'Svratouch' : root.cssselect("div.vgtext")[15].text,
            'Plzen_Mikulka' : root.cssselect("div.vgtext")[16].text,
            'Primda' : root.cssselect("div.vgtext")[17].text,
            'Cheb' : root.cssselect("div.vgtext")[18].text,
            'Karlovy_Vary' : root.cssselect("div.vgtext")[19].text,
            'Cervena_u_Libave' : root.cssselect("div.vgtext")[20].text,
            'Lysa_Hora' : root.cssselect("div.vgtext")[21].text,
            'Ostrava' : root.cssselect("div.vgtext")[22].text,
            'Serak' : root.cssselect("div.vgtext")[23].text,
            'Luka' : root.cssselect("div.vgtext")[24].text,
            'Prerov' : root.cssselect("div.vgtext")[25].text,
            'Praha_Libus' : root.cssselect("div.vgtext")[26].text,
            'Praha_Ruzyne' : root.cssselect("div.vgtext")[27].text,
            'Kosetice' : root.cssselect("div.vgtext")[28].text,
            'Pribyslav' : root.cssselect("div.vgtext")[29].text,
            'Doksany' : root.cssselect("div.vgtext")[30].text,
            'Tusimice' : root.cssselect("div.vgtext")[31].text,
            'Milesovka' : root.cssselect("div.vgtext")[32].text,
            'Usti_nad_Labem' : root.cssselect("div.vgtext")[33].text,
            'Liberec' : root.cssselect("div.vgtext")[34].text
        }
print data
scraperwiki.sqlite.save(unique_keys=['date'], data=data)      

import scraperwiki           
import lxml.html
html = scraperwiki.scrape("http://pr-asv.chmi.cz/synopy-map/pocasiin.php?ukazatel=prumtep&pozadi=mapareg&graf=ano")
root = lxml.html.fromstring(html)

data = {
            'date' : root.cssselect("div.vgtext")[0].text,
            'Holesov' : root.cssselect("div.vgtext")[1].text,
            'Brno_Turany' : root.cssselect("div.vgtext")[2].text,
            'Dukovany' : root.cssselect("div.vgtext")[3].text,
            'Kostelni_Myslova' : root.cssselect("div.vgtext")[4].text,
            'Kucharovice' : root.cssselect("div.vgtext")[5].text,
            'Churanov' : root.cssselect("div.vgtext")[6].text,
            'Kocelovice' : root.cssselect("div.vgtext")[7].text,
            'Temelin' : root.cssselect("div.vgtext")[8].text,
            'Ceske_Budejovice' : root.cssselect("div.vgtext")[9].text,
            'Pec_pod_Snezkou' : root.cssselect("div.vgtext")[10].text,
            'Polom' : root.cssselect("div.vgtext")[11].text,
            'Usti_nad_Orlici' : root.cssselect("div.vgtext")[12].text,
                
            #Caslav
            #'Pardubice' : root.cssselect("div.vgtext")[13].text,
            #'Svratouch' : root.cssselect("div.vgtext")[14].text,
            #'Plzen_Mikulka' : root.cssselect("div.vgtext")[15].text,
            #'Primda' : root.cssselect("div.vgtext")[16].text,
            #'Cheb' : root.cssselect("div.vgtext")[17].text,
            #'Karlovy_Vary' : root.cssselect("div.vgtext")[18].text,
            #'Cervena_u_Libave' : root.cssselect("div.vgtext")[19].text,
            #'Lysa_Hora' : root.cssselect("div.vgtext")[20].text,
            #'Ostrava' : root.cssselect("div.vgtext")[21].text,
            #'Serak' : root.cssselect("div.vgtext")[22].text,
            #'Luka' : root.cssselect("div.vgtext")[23].text,
            #'Prerov' : root.cssselect("div.vgtext")[24].text,
            #'Praha_Libus' : root.cssselect("div.vgtext")[25].text,
            #'Praha_Ruzyne' : root.cssselect("div.vgtext")[26].text,
            #'Kosetice' : root.cssselect("div.vgtext")[27].text,
            #'Pribyslav' : root.cssselect("div.vgtext")[28].text,
            #'Doksany' : root.cssselect("div.vgtext")[29].text,
            #'Tusimice' : root.cssselect("div.vgtext")[30].text,
            #'Milesovka' : root.cssselect("div.vgtext")[31].text,
            #'Usti_nad_Labem' : root.cssselect("div.vgtext")[32].text,
            #'Liberec' : root.cssselect("div.vgtext")[33].text

            #Prerov
            #'Caslav' : root.cssselect("div.vgtext")[13].text,
            #'Pardubice' : root.cssselect("div.vgtext")[14].text,
            #'Svratouch' : root.cssselect("div.vgtext")[15].text,
            #'Plzen_Mikulka' : root.cssselect("div.vgtext")[16].text,
            #'Primda' : root.cssselect("div.vgtext")[17].text,
            #'Cheb' : root.cssselect("div.vgtext")[18].text,
            #'Karlovy_Vary' : root.cssselect("div.vgtext")[19].text,
            #'Cervena_u_Libave' : root.cssselect("div.vgtext")[20].text,
            #'Lysa_Hora' : root.cssselect("div.vgtext")[21].text,
            #'Ostrava' : root.cssselect("div.vgtext")[22].text,
            #'Serak' : root.cssselect("div.vgtext")[23].text,
            #'Luka' : root.cssselect("div.vgtext")[24].text,
            #'Praha_Libus' : root.cssselect("div.vgtext")[25].text,
            #'Praha_Ruzyne' : root.cssselect("div.vgtext")[26].text,
            #'Kosetice' : root.cssselect("div.vgtext")[27].text,
            #'Pribyslav' : root.cssselect("div.vgtext")[28].text,
            #'Doksany' : root.cssselect("div.vgtext")[29].text,
            #'Tusimice' : root.cssselect("div.vgtext")[30].text,
            #'Milesovka' : root.cssselect("div.vgtext")[31].text,
            #'Usti_nad_Labem' : root.cssselect("div.vgtext")[32].text,
            #'Liberec' : root.cssselect("div.vgtext")[33].text

            'Caslav' : root.cssselect("div.vgtext")[13].text,
            'Pardubice' : root.cssselect("div.vgtext")[14].text,
            'Svratouch' : root.cssselect("div.vgtext")[15].text,
            'Plzen_Mikulka' : root.cssselect("div.vgtext")[16].text,
            'Primda' : root.cssselect("div.vgtext")[17].text,
            'Cheb' : root.cssselect("div.vgtext")[18].text,
            'Karlovy_Vary' : root.cssselect("div.vgtext")[19].text,
            'Cervena_u_Libave' : root.cssselect("div.vgtext")[20].text,
            'Lysa_Hora' : root.cssselect("div.vgtext")[21].text,
            'Ostrava' : root.cssselect("div.vgtext")[22].text,
            'Serak' : root.cssselect("div.vgtext")[23].text,
            'Luka' : root.cssselect("div.vgtext")[24].text,
            'Prerov' : root.cssselect("div.vgtext")[25].text,
            'Praha_Libus' : root.cssselect("div.vgtext")[26].text,
            'Praha_Ruzyne' : root.cssselect("div.vgtext")[27].text,
            'Kosetice' : root.cssselect("div.vgtext")[28].text,
            'Pribyslav' : root.cssselect("div.vgtext")[29].text,
            'Doksany' : root.cssselect("div.vgtext")[30].text,
            'Tusimice' : root.cssselect("div.vgtext")[31].text,
            'Milesovka' : root.cssselect("div.vgtext")[32].text,
            'Usti_nad_Labem' : root.cssselect("div.vgtext")[33].text,
            'Liberec' : root.cssselect("div.vgtext")[34].text
        }
print data
scraperwiki.sqlite.save(unique_keys=['date'], data=data)      

