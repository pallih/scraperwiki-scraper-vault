#
# This is an example of scraping multiple URLs.
#

import scraperwiki
import re
http://en.wikipedia.org/wiki/Adamstown_School

# The URLs we're going to scrape:

urls = """


http://en.wikipedia.org/wiki/Alexandra_College
http://en.wikipedia.org/wiki/Ardgillan_Community_College
http://en.wikipedia.org/wiki/Árdscoil_La_Salle
http://en.wikipedia.org/wiki/Ardscoil_Rís
http://en.wikipedia.org/wiki/Assumption_Secondary_School
http://en.wikipedia.org/wiki/Balbriggan_Community_College
http://en.wikipedia.org/wiki/Ballsbridge_College_of_Further_Education
http://en.wikipedia.org/wiki/Ballyfermot_College_of_Further_Education
http://en.wikipedia.org/wiki/Belcamp_College
http://en.wikipedia.org/wiki/Belvedere_College_S.J
http://en.wikipedia.org/wiki/Beneavin_De_La_Salle_College
http://en.wikipedia.org/wiki/Blackrock_College
http://en.wikipedia.org/wiki/Blakestown_Community_School
http://en.wikipedia.org/wiki/C.B.S._James_Street
http://en.wikipedia.org/wiki/C.B.S._Westland_Row
http://en.wikipedia.org/wiki/Cabinteely_Community_School
http://en.wikipedia.org/wiki/Caritas_College
http://en.wikipedia.org/wiki/Castleknock_College
http://en.wikipedia.org/wiki/Castleknock_Community_College
http://en.wikipedia.org/wiki/Catholic_University_School
http://en.wikipedia.org/wiki/Chanel_College
http://en.wikipedia.org/wiki/Christian_Brothers
http://en.wikipedia.org/wiki/Christian_Brothers_College
http://en.wikipedia.org/wiki/Clonkeen_College
http://en.wikipedia.org/wiki/Coláiste_Bríde
http://en.wikipedia.org/wiki/Coláiste_Chilliain
http://en.wikipedia.org/wiki/Coláiste_Choilm
http://en.wikipedia.org/wiki/Coláiste_Cois_Life_
http://en.wikipedia.org/wiki/Coláiste_de_hÍde___
http://en.wikipedia.org/wiki/Coláiste_Dhúlaigh
http://en.wikipedia.org/wiki/Coláiste_Dhúlaigh_College_of_Further_Education
http://en.wikipedia.org/wiki/Colaiste_Eanna,Ballyroan
http://en.wikipedia.org/wiki/Coláiste_Éanna,Cabra
http://en.wikipedia.org/wiki/Coláiste_Eoin
http://en.wikipedia.org/wiki/Coláiste_Eoin
http://en.wikipedia.org/wiki/Colaiste_Ide_College_of_Further_Education
http://en.wikipedia.org/wiki/Coláiste_Íosagáin
http://en.wikipedia.org/wiki/Coláiste_Mhuire
http://en.wikipedia.org/wiki/Coláiste_Phádraig
http://en.wikipedia.org/wiki/College_Of_Further_Education_Dundrum
http://en.wikipedia.org/wiki/Collinstown_Park_Community_College
http://en.wikipedia.org/wiki/Coolmine_Community_School
http://en.wikipedia.org/wiki/Crumlin_College_Of_Further_Education
http://en.wikipedia.org/wiki/Da_La_Salle_College
http://en.wikipedia.org/wiki/Deansrath_Community_College
http://en.wikipedia.org/wiki/Dominican_College,Drumcondra
http://en.wikipedia.org/wiki/Dominican_College,Sion
http://en.wikipedia.org/wiki/Donabate_Community_College
http://en.wikipedia.org/wiki/Dun_Laoghaire_College_of_Further_Education
http://en.wikipedia.org/wiki/Fingal_Community_College
http://en.wikipedia.org/wiki/Firhouse_Community_College
http://en.wikipedia.org/wiki/Gealcholáiste_Reachrann
http://en.wikipedia.org/wiki/Gonzaga_College
http://en.wikipedia.org/wiki/Grange_Community_College
http://en.wikipedia.org/wiki/Greenhills_College
http://en.wikipedia.org/wiki/Hartstown_Community_School
http://en.wikipedia.org/wiki/Holy_Child_Community_School
http://en.wikipedia.org/wiki/Holy_Child_Secondary_School
http://en.wikipedia.org/wiki/Holy_Faith_Secondary_School
http://en.wikipedia.org/wiki/Holy_Family_Community_School
http://en.wikipedia.org/wiki/Inchicore_College_of_Further_Education
http://en.wikipedia.org/wiki/Jobstown_Community_College
http://en.wikipedia.org/wiki/John_Scottus_Secondary_School
http://en.wikipedia.org/wiki/Killester_College_of_Further_Education
http://en.wikipedia.org/wiki/Killinarden_Community_School
http://en.wikipedia.org/wiki/Kylemore_College
http://en.wikipedia.org/wiki/Larkin_Community_College
http://en.wikipedia.org/wiki/Liberties_College
http://en.wikipedia.org/wiki/Loreto_Abbey_Secondary_School
http://en.wikipedia.org/wiki/Loreto_College_Crumlin___
http://en.wikipedia.org/wiki/Loreto_College_Foxrock___
http://en.wikipedia.org/wiki/Loreto_College_Stephens_Green
http://en.wikipedia.org/wiki/Loreto_College_Swords
http://en.wikipedia.org/wiki/Loreto_High_School
http://en.wikipedia.org/wiki/Loreto_Secondary_School
http://en.wikipedia.org/wiki/Lucan_Community_College
http://en.wikipedia.org/wiki/Luttrellstown_Community_College
http://en.wikipedia.org/wiki/Malahide_Community_School
http://en.wikipedia.org/wiki/Manor_House_School
http://en.wikipedia.org/wiki/Margaret_Aylward_Community_College
http://en.wikipedia.org/wiki/Marian_College
http://en.wikipedia.org/wiki/Marino_College
http://en.wikipedia.org/wiki/Maryfield_College
http://en.wikipedia.org/wiki/Mater_Christi
http://en.wikipedia.org/wiki/Meanscoil_Chroimghlinne
http://en.wikipedia.org/wiki/Meanscoil_Iognáid_Rís
http://en.wikipedia.org/wiki/Mercy_College_Coolock
http://en.wikipedia.org/wiki/Mercy_Secondary_School
http://en.wikipedia.org/wiki/Mount_Anville_Secondary_School
http://en.wikipedia.org/wiki/Mount_Carmel_Secondary_School
http://en.wikipedia.org/wiki/Mount_Sackville_Secondary_School
http://en.wikipedia.org/wiki/Mount_Temple_Comprehensive_School
http://en.wikipedia.org/wiki/Moyle_Park_College
http://en.wikipedia.org/wiki/Muckross_Park_College
http://en.wikipedia.org/wiki/Newpark_Comprehensive_School
http://en.wikipedia.org/wiki/Notre_Dame_Secondary_School
http://en.wikipedia.org/wiki/O'Connell_School
http://en.wikipedia.org/wiki/Oatlands_College
http://en.wikipedia.org/wiki/Old_Bawn_Community_School
http://en.wikipedia.org/wiki/Our_Lady_Of_Mercy_College
http://en.wikipedia.org/wiki/Our_Lady_Of_Mercy_Secondary_School
http://en.wikipedia.org/wiki/Our_Ladys_Grove
http://en.wikipedia.org/wiki/Our_Ladys_School
http://en.wikipedia.org/wiki/Patrician_College
http://en.wikipedia.org/wiki/Pearse_College
http://en.wikipedia.org/wiki/Phibblestown_Community_College
http://en.wikipedia.org/wiki/Phobailscoil_Iosolde
http://en.wikipedia.org/wiki/Plunket_College
http://en.wikipedia.org/wiki/Pobalscoil_Neasáin
http://en.wikipedia.org/wiki/Portmarnock_Community_School
http://en.wikipedia.org/wiki/Presentation_College
http://en.wikipedia.org/wiki/Presentation_College
http://en.wikipedia.org/wiki/Rathdown_School
http://en.wikipedia.org/wiki/Rathmines_College
http://en.wikipedia.org/wiki/Riversdale_Community_College
http://en.wikipedia.org/wiki/Rockbrook_Park_School
http://en.wikipedia.org/wiki/Rockford_Manor_Secondary_School
http://en.wikipedia.org/wiki/Rosary_College
http://en.wikipedia.org/wiki/Rosemont_School
http://en.wikipedia.org/wiki/Rosmini_Community_School
http://en.wikipedia.org/wiki/Saint_Dominic's_Secondary_School
http://en.wikipedia.org/wiki/Sallynoggin_College_of_Further_Education
http://en.wikipedia.org/wiki/Sancta_Maria_College
http://en.wikipedia.org/wiki/Sandford_Park_School
http://en.wikipedia.org/wiki/Scoil_Chaitriona
http://en.wikipedia.org/wiki/Scoil_Phobail_Chuil_Mhin
http://en.wikipedia.org/wiki/Senior_College_Dun_laoghaire
http://en.wikipedia.org/wiki/Skerries_Community_College
http://en.wikipedia.org/wiki/St_Aidan's_Community_School
http://en.wikipedia.org/wiki/St_Andrews_College
http://en.wikipedia.org/wiki/St_Benildus_College
http://en.wikipedia.org/wiki/St_Columba's_College
http://en.wikipedia.org/wiki/St_Conleths_College
http://en.wikipedia.org/wiki/St_Declan's_College
http://en.wikipedia.org/wiki/St_Dominic's_High_School
http://en.wikipedia.org/wiki/St_Dominics_College
http://en.wikipedia.org/wiki/St_Finians_Community_College
http://en.wikipedia.org/wiki/St_Johns_College_De_La_Salle
http://en.wikipedia.org/wiki/St_Joseph_Of_Cluny
http://en.wikipedia.org/wiki/St_Joseph's_Secondary_School
http://en.wikipedia.org/wiki/St_Josephs_C.B.S.
http://en.wikipedia.org/wiki/St_Josephs_College
http://en.wikipedia.org/wiki/St_Josephs_Secondary_School,Stanhope
http://en.wikipedia.org/wiki/St_Kevins_College
http://en.wikipedia.org/wiki/St_Kilian's_Deutsche_Schule
http://en.wikipedia.org/wiki/St_Laurence_College
http://en.wikipedia.org/wiki/St_Louis_High_School
http://en.wikipedia.org/wiki/St_Mac_Dara's_Community_College
http://en.wikipedia.org/wiki/St_Marks_Community_School
http://en.wikipedia.org/wiki/St_Mary's_Secondary_School
http://en.wikipedia.org/wiki/St_Marys_College
http://en.wikipedia.org/wiki/St_Marys_Secondary_School,Baldoyle
http://en.wikipedia.org/wiki/St_Marys_Secondary_School,Killester
http://en.wikipedia.org/wiki/St_Michaels_College
http://en.wikipedia.org/wiki/St_Michaels_Secondary_School
http://en.wikipedia.org/wiki/St_Patricks_Cathedral_School
http://en.wikipedia.org/wiki/St_Pauls_C.B.S.
http://en.wikipedia.org/wiki/St_Pauls_College
http://en.wikipedia.org/wiki/St_Pauls_Secondary_School
http://en.wikipedia.org/wiki/St_Raphaela's_Secondary_School
http://en.wikipedia.org/wiki/St_Vincents_C.B.S._Glasnevin
http://en.wikipedia.org/wiki/St._Aidan's_C.B.S.
http://en.wikipedia.org/wiki/St._Colmcille's_Community_School
http://en.wikipedia.org/wiki/St._David's_C.B.S.
http://en.wikipedia.org/wiki/St._Fintan's_High_School
http://en.wikipedia.org/wiki/St._Kevin's_Community_College
http://en.wikipedia.org/wiki/St._Kevins_College
http://en.wikipedia.org/wiki/St._Tiernan's_Community_School
http://en.wikipedia.org/wiki/Stillorgan_College_of_Further_Education
http://en.wikipedia.org/wiki/Stratford_College
http://en.wikipedia.org/wiki/Sutton_Park_School
http://en.wikipedia.org/wiki/Tallaght_Community_School
http://en.wikipedia.org/wiki/Technical_Institute
http://en.wikipedia.org/wiki/Templeogue_College
http://en.wikipedia.org/wiki/Terenure_College
http://en.wikipedia.org/wiki/The_Donahies_Community_School
http://en.wikipedia.org/wiki/The_High_School
http://en.wikipedia.org/wiki/The_Kings_Hospital
http://en.wikipedia.org/wiki/The_Teresian_School
http://en.wikipedia.org/wiki/Trinity_Comprehensive_School
http://en.wikipedia.org/wiki/Wesley_College
http://en.wikipedia.org/wiki/Whitehall_House_Senior_College
http://en.wikipedia.org/wiki/Willow_Park_School

""".strip()

urls = urls.splitlines()


# This is a useful helper function that you might want to steal.
# It cleans up the data a bit.
def gettext(html):
    # Return the text within html, removing any HTML tags it contained.
    cleaned = re.sub('<.*?>', '', html)  # remove tags
    cleaned = ' '.join(cleaned.split())  # collapse whitespace
    return cleaned


for url in urls:
    print "Scraping", url
    page = scraperwiki.scrape(url)
    if page is not None:
        # Store all the h2 headings (matching "<h2>...</h2>")
        headings = re.findall('geo\">(.*?)</span>', page, re.DOTALL)
        # re.DOTALL makes it work across multiple lines as well.

        # Just keep the heading text
        # (Try commenting this out)
        #headings = [gettext(heading) for heading in headings]

        data = {'url': url, 'headings': headings}
        scraperwiki.datastore.save(['url'], data)   # each entry is identified by its url
