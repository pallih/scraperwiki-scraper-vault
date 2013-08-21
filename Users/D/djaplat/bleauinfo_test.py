import scraperwiki
import urlparse
import lxml.html
import lxml.etree
from HTMLParser import HTMLParser
import re

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)
        
def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()



#url = "http://bleau.info/longsvaux/7a++25.html"
#html = scraperwiki.scrape(url)
#root = lxml.html.fromstring(html)
#mainsub = root.cssselect("#mainsub1")[0]
#maintable = mainsub.cssselect("table")[0]
#trs = maintable.cssselect("tr")

# list met alle gebieden en daar bij behorende subgebieden in bleau
areas = [
    {"Yvelines, Essonne North": [["maincourt", "Dampierre Maincourt", 26], ["troche", "La Troche", 11], ["orsay", "Orsay", 6]]},
    {"L'Essonne left bank": [["chamarande", "Chamarande", 23], ["fertealais", "La Ferté-Alais", 1], ["pendu", "Le Pendu d'Huison", 4], ["sanglier", "Le Sanglier", 13], ["maisse", "Maisse le Patouillat", 1], ["villeneuve", "Villeneuve sur Auvers", 8]]},
    {"Vall&eacute;e de l'&Eacute;cole": [["beauvaisest", "Beauvais Est", 15], ["guinguette", "Beauvais Guinguette", 5], ["hameau", "Beauvais Hameau", 17], ["beauvais", "Beauvais Nainville", 45], ["telegraphe", "Beauvais Télégraphe", 7], ["valette", "Bois de la Valette", 7], ["charbonniere", "La Charbonnière", 3], ["padole", "La Padôle", 40], ["moigny", "Moigny sur École", 1], ["oncy", "Oncy sur École", 2], ["videlles_abbatoir", "Videlles l'Abattoir", 35], ["videlles", "Videlles les Roches", 32]]},
    {"Coquibus": [["arcades", "Coquibus Arcades", 15], ["auvergne", "Coquibus Auvergne", 32], ["grandesvallees", "Coquibus Grandes Vallées", 11], ["longsvaux", "Coquibus Longs Vaux", 42], ["coquibus", "Coquibus Rumont", 9], ["courances", "Côtes de Courances", 10], ["coquibuswest", "Gorge à Véron", 10], ["guichet", "Le Guichet", 4], ["joncs", "Mare aux Joncs", 11], ["montignotte", "Montignotte", 31], ["montrouget", "Montrouget", 10], ["montrougetouest", "Montrouget Ouest", 7], ["rochequitourne", "Roche qui Tourne", 13], ["ancetres", "Vallée des Ancêtres", 4]]},
    {"Trois Pignons East": [["boisdurocher", "Bois du Rocher", 9], ["rond", "Bois Rond", 38], ["canche", "Canche aux Merciers", 54], ["zinnen", "Drei Zinnen", 56], ["anarchodrome", "L'Anarchodrome", 18], ["beorlots", "Les Béorlots", 49], ["petitereine", "Petite Reine", 17], ["cretenord", "Reine Crête Nord", 6], ["cornebiche", "Rocher de Corne-Biche", 7], ["reine", "Rocher de la Reine", 45], ["valleeronde", "Rocher de la Vallée Ronde", 5], ["milly", "Rocher de Milly", 34], ["mariniers", "Rocher des Mariniers", 4], ["telegraphe2", "Rocher du Télégraphe", 4], ["touche", "Touche aux Mulets", 2], ["valleechaude", "Vallée Chaude", 2]]},
    {"Trois Pignons West": [["91.1", "91.1", 4], ["95.2", "95.2", 48], ["cul", "Cul de Chien", 19], ["chats", "Gorge aux Châts", 58], ["gros", "Gros Sablons", 24], ["jean", "Jean des Vignes", 11], ["chateauveau", "Justice de Chambergeot", 6], ["pivot", "Mont Pivot", 12], ["oiseaux", "Roche aux Oiseaux", 30], ["sabots", "Roche aux Sabots", 72], ["zen", "Roche aux Sabots Sud", 24], ["souris", "Rocher des Souris", 12]]},
    {"Trois Pignons South": [["hautsmilly", "Bois des Hauts de Milly", 12], ["diplodocus", "Diplodocus", 3], ["grandemontagne", "Grande Montagne", 16], ["martin", "J.A. Martin", 48], ["111", "Le 111", 8], ["cailleau", "Rocher Cailleau", 16], ["cathedrale", "Rocher de la Cathédrale", 5], ["general", "Rocher du Général", 9], ["mee", "Rocher du Potala", 46], ["fin", "Rocher Fin", 53], ["guichot", "Rocher Guichot", 18]]},
    {"Cuvier-Châtillon": [["cuvier", "Cuvier", 190], ["cuvierest", "Cuvier Est", 54], ["merveille", "Cuvier Merveille", 18], ["rempart", "Cuvier Rempart", 147], ["cuvierouest", "Cuvier Ouest", 42], ["piat", "La Mare à Piat", 23], ["reconnaissance", "La Reconnaissance", 51], ["montsetmerveilles", "Monts & Merveilles", 2], ["petitrempart", "Petit Rempart", 12]]},
    {"North of Fontainebleau": [["cassepotgrises", "Cassepot Roches Grises", 21], ["cassepotoranges", "Cassepot Roches Oranges", 11], ["cassepotroses", "Cassepot Roches Roses", 10], ["calvaire", "Le Calvaire", 11], ["ussy", "Mont Ussy", 21], ["hercule", "Roche d'Hercule", 15], ["canon", "Rocher Canon", 94], ["canonouest", "Rocher Canon Ouest", 24], ["germain", "Rocher Saint-Germain", 77], ["denecourt", "Tour Dénecourt", 2]]},
    {"Apremont": [["apremont", "Apremont", 96], ["bizons", "Apremont Bizons", 15], ["butteauxpeintres", "Apremont Butte aux Peintres", 13], ["buvette", "Apremont Buvette", 2], ["desert", "Apremont Désert", 11], ["envers", "Apremont Envers", 22], ["apremontouest", "Apremont Ouest", 40], ["apremontsully", "Apremont Vallon de Sully", 12], ["solitude", "Vallon de la Solitude", 14]]},
    {"Franchard": [["carnage", "Cuisinière Carnage", 15], ["cretesud", "Cuisinière Crête Sud", 56], ["bassesplaines", "Franchard Basses Plaines", 11], ["sablons110", "Franchard Carriers", 28], ["cuisiniere", "Franchard Cuisinière", 107], ["ermitage", "Franchard Ermitage", 24], ["plaines", "Franchard Hautes-Plaines", 27], ["isatis", "Franchard Isatis", 129], ["meyer", "Franchard Meyer", 31], ["oiseauxdeproie", "Franchard Oiseaux de Proie", 9], ["franchardpointdevue", "Franchard Point de Vue", 42], ["raymond", "Franchard Raymond", 16], ["sablons", "Franchard Sablons", 29], ["merisiers", "Gorge aux Merisiers", 7], ["houx", "Gorges du Houx", 31], ["aigu", "Mont Aigu - Long Boyau", 16], ["petitparadis", "Petit Paradis", 12]]},
    {"South of Fontainebleau": [["marecorneilles", "Mare aux Corneilles", 30], ["marion", "Marion des Roches", 30], ["recloses", "Recloses", 8], ["restant", "Restant du Long Rocher", 35], ["grottebeatrix", "Restant du Long Rocher Nord", 18], ["longrochergrandesvallees", "Restant du Long Rocher Ouest", 6], ["rocherbrule", "Rocher Brûlé", 27], ["avon", "Rocher d'Avon", 33], ["avonouest", "Rocher d'Avon Ouest", 57], ["bouligny", "Rocher de Bouligny", 28], ["combe", "Rocher de la Combe", 2], ["occidentale", "Rocher de la Salamandre", 18], ["demoiselles", "Rocher des Demoiselles", 59], ["princes", "Rocher des Princes", 16], ["passage", "Rocher du Mauvais Passage", 12], ["montmorillon", "Rocher du Mont Morillon", 12]]},
    {"Nemours": [["chaintreauville", "Chaintreauville", 17], ["fosse", "Fosse aux Loups", 3], ["troglodyte", "Le Troglodyte", 4], ["mammouths", "Les Mammouths", 9], ["olivet", "Mont d'Olivet", 1], ["petit", "Petit Bois", 24], ["puiselet", "Puiselet Le Paradis", 47], ["sarrazin", "Puiselet Mont Sarrasin", 28], ["sablibum", "Puiselet Sablibum", 5], ["greau", "Rocher Gréau", 30], ["cassepot", "Vallée Casse-Pot", 3]]},
    {"Larchant": [["jouanne", "Dame Jouanne", 46], ["elephant", "Éléphant", 51], ["boutdumonde", "Éléphant Bout du Monde", 9], ["elephantnord", "Éléphant Nord", 19], ["ouest", "Éléphant Ouest", 38], ["maunoury", "Maunoury", 48], ["simonet", "Mont Simonet", 14]]},
    {"Malesherbes": [["boigneville", "Boigneville", 26], ["cailles", "Boissy aux Cailles", 21], ["canard", "Buthiers Canard", 26], ["y", "Buthiers Piscine", 36], ["tennis", "Buthiers Tennis", 24], ["marlenval", "Marlanval", 3], ["roisneau", "Moulin de Roisneau", 14], ["champlaid", "Vallée de Champlaid", 3], ["villetard", "Villetard", 4]]}
]


# dictionary met type boulders
existing_types = {1:'wall', 2:'mantle', 3:'high', 4:'slightly overhanging', 5:'slopers', 6:'expo', 7:'crimps', 8:'slab', 9:'monos', 10:'overhang', 
              11:'pillar', 12:'traverse fltr', 13:'traverse frtl', 14:'arete', 15:'pockets', 16:'sitstart', 17:'underclings', 18:'dyno', 19:'traverse',
              20:'bidoigt', 21:'pinches', 22:'prow', 23:'toprope', 24:'belly', 25:'-', 26:'crack', 27:'chimney', 28:'dihedral', 29:'downclimbing', 30:'roof', 31:'loop'}

# save de boulder types in een eigen tabel
type_data = {}
for k,v in existing_types.items():
    type_data['id'] = k
    type_data['type'] = v
    scraperwiki.sqlite.save(unique_keys=['id'], data=type_data, table_name="types")


# dictionary met waarderingen
existing_grades = {1:'5a', 2:'5a+', 3:'5b', 4:'5b+', 5:'5c', 6:'5c+',
                   7:'6a', 8:'6a+', 9:'6b', 10:'6b+', 11:'6c', 12:'6c+',
                   13:'7a', 14:'7a+', 15:'7b', 16:'7b+', 17:'7c', 18:'7c+', 
                   19:'8a', 20:'8a+', 21:'8b', 22:'8b+', 23:'8c', 24:'8c+', 
                   25:'9a'}

# save de grades in een eigen tabel
grade_data = {}
for k,v in existing_grades.items():
    grade_data['id'] = k
    grade_data['grade'] = v
    scraperwiki.sqlite.save(unique_keys=['id'], data=grade_data, table_name="grades")



'''
Haal de naam uit de oneven rows
'''
def get_name(tr_one):
    tr = tr_one.cssselect("td")
    try:
        text = re.sub(r'<[^>]*?>', '', lxml.etree.tostring(tr[0]))
        #text = strip_tags(lxml.etree.tostring(tr[0]))
        boulder_name = re.split(r'[0-9][a-z]\+*', text)
        # TODO: iets fixen voor special characters?
        return boulder_name[0]
    except IndexError:
        return ""

'''
Haal de waarderingen voor de waardering/boulders koppeltabel op
'''
def get_grade_join(pk, tr_one):
    # pk is de primary key van de boulder, deze moet voor elke waardering opgenomen worden in een koppeltabel
    pk = pk

    tr = tr_one.cssselect("td")
    try: 
        text = strip_tags(lxml.etree.tostring(tr[0]))
        
        pattern = re.compile(r'[6-8][a-c]\+*')
        boulder_grade = pattern.findall(text)
                
        grades = []
        for grade in boulder_grade:
            # match de waardering met de existing_grades dictionary
            key = [k for k, v in existing_grades.iteritems() if v == grade][0]
            grades.append(key)
        
        return grades
        
    except:
        return ""

'''
Haal de waarderingen op
'''
def get_grade(tr_one):
    tr = tr_one.cssselect("td")
    try: 
        text = strip_tags(lxml.etree.tostring(tr[0]))
        
        pattern = re.compile(r'[6-8][a-c]\+*')
        boulder_grade = pattern.findall(text)
                
        grades = []
        for grade in boulder_grade:
            grades.append(grade)

        if len(grades) < 2:
            grades = grades[0]
        else:
            grades = grades[0] + " (" + grades[1] + ")"
        
        return grades
        
    except:
        return ""



'''
Haal de description op, gestript van alle ander velden (gps enzo)
'''
def get_description(tr):
    text = lxml.etree.tostring(tr)
    
    description = re.sub(r'<[^>]*?>', '', text)

    # strip GPS shit uit de description
    pattern = re.compile(r'\(GPS:.N[0-9]+\.[0-9]+.E[0-9]+\.[0-9]+\)')
    
    try: 
        description = pattern.sub('', description)
    except TypeError:
        description = description

    # TODO: replace " with &quot;
    wegmetdiequotes = re.compile(r'\"')
    description = wegmetdiequotes.sub('&quot;', description)
    
    return description

'''
Haal de GPS coordinaten uit de even rows en binnen een span tag, split het resultaat in lat/lon values
'''
def get_gps(tr):
    tr = tr.cssselect("span")
    try:
        gps = lxml.etree.tostring(tr[0])
        gps = strip_tags(gps)

        gps = re.split(r"(\d+\.\d+)", gps)
        
        lat = gps[1]
        lon = gps[3]

        latlon = [lat, lon]
        return latlon
    except IndexError:
        return ["", ""]

'''
haal het type boulder uit de oneven rows en de tweede td binnen de row
'''
def get_boulder_type(pk, tr_one):
    tr = tr_one.cssselect("td")
    try:
        boulder_type = strip_tags(lxml.etree.tostring(tr[1]))
        splitter = re.compile(' / ')
        boulder_type = splitter.split(boulder_type)

        foreign_keys = []
        for type in boulder_type:
            key = [k for k, v in existing_types.iteritems() if v == type][0]
            foreign_keys.append(key)
        
        # TODO: hier moet een of ander functie komen die de foreign_keys en de boulder id in de database opnemen
            
        return foreign_keys
    except IndexError:
        pass

'''
haal het aantal sterren op uit de even rows. 1 ster is 2 punten
'''
def get_number_of_stars(tr):
    stars = tr.cssselect("img[alt]")
        
    number_of_stars = 0
    for s in stars:
        if lxml.etree.tostring(s) == '<img src="/images2/navigation/blackstar.png" width="11" height="11" alt="*" hspace="0" vspace="0"/>':
            number_of_stars += 2
        elif lxml.etree.tostring(s) == '<img src="/images2/navigation/blackstar.png" width="11" height="11" alt="*" hspace="1" vspace="0"/>':
            number_of_stars += 2
        elif lxml.etree.tostring(s) == '<img src="/images2/navigation/blackhalfstar.png" width="11" height="11" alt="*" hspace="0" vspace="0"/>':
            number_of_stars +=1
        elif lxml.etree.tostring(s) == '<img src="/images2/navigation/blackhalfstar.png" width="11" height="11" alt="*" hspace="1" vspace="0"/>':
            number_of_stars +=1
        else:
            pass

    return number_of_stars
        
'''
check of er een 'next boulders' link is
'''
def has_next(mainsub):
    string = lxml.html.tostring(mainsub)

    # find the next boulders link (is het tweede element in de string tuple)
    match = re.search(r"<a.*?>next boulders</a>", string)

    # als er een match is, dan zit de link in match.group(0)
    if match:
        # als er een previous link is...
        if re.search(r'<a.*?>previous boulders</a>', match.group(0)) != None:
            # split de previous link van de match
            string = re.split(r'<a.*?>previous boulders</a>', match.group(0))
            # de tweede ,match uit de split willen we hebben, deze doorzoeken naar een next boulders link
            match_two = re.search(r"<a.*?>next boulders</a>", string[1])
            next_link = lxml.html.fromstring(match_two.group(0))
            
        # er is geen previous link, next_link is de eerste group uit de match
        else:
            next_link = lxml.html.fromstring(match.group(0))
        
        next_url = "http://bleau.info%s" % next_link.get('href') 

        return next_url
    else:
        # TODO: geen 'next boulders' link gevonden: ga naar het volgende gebied
        return False



'''
save de boulders in het gebied in de database
'''
def save_area_boulders(area_id, url):
    
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    mainsub = root.cssselect("#mainsub1")[0]
    maintable = mainsub.cssselect("table")[0]
    trs = maintable.cssselect("tr")
    length = len(trs)


    i = 0

    # als de tabel boulders al bestaat, dan is de eerst volgende id de hoogste id uit de tabel + 1
    tables = scraperwiki.sqlite.show_tables()
    if 'boulders' in tables:
        val = scraperwiki.sqlite.select("id FROM boulders ORDER BY id DESC LIMIT 1")        
        # id is van het type [{u'id': 29}], haal het getal uit
        id = val[0]['id'] + 1
    else:
        id = 1

    if 'boulder_type' in tables:
        val = scraperwiki.sqlite.select("id FROM boulder_type ORDER BY id DESC LIMIT 1")
        bt_id = val[0]['id'] + 1
    else:
        bt_id = 1

    if 'boulder_grade' in tables:
        val = scraperwiki.sqlite.select("id FROM boulder_grade ORDER BY id DESC LIMIT 1")
        bg_id = val[0]['id'] + 1
    else:
        bg_id = 1



    while i < length:
        tr_one = trs[i]
        tr = trs[i+1]

        
        data = {
            'id' : id,
            'name' : get_name(tr_one),
            'grade' : get_grade(tr_one),
            'lat' : get_gps(tr)[0],
            'lon' : get_gps(tr)[1],
            'description' : get_description(tr),
            'stars' : get_number_of_stars(tr),
            'area_id' : area_id
        }
        
        # save de data in de scraperwiki database, id is unieke key
        scraperwiki.sqlite.save(unique_keys=['id'], data=data, table_name="boulders")


        # save de boulder types in een koppeltabel boulder_type
        boulder_types = get_boulder_type(id, tr_one)
        for type in boulder_types:

            boulder_type = {
                'id' : bt_id,
                'boulder' : id,
                'type' : type
                }

            scraperwiki.sqlite.save(unique_keys=['id'], data=boulder_type, table_name="boulder_type")
            bt_id += 1

        
        # save de waarderingen in een koppeltabel boulder_grade
        boulder_grades = get_grade_join(id, tr_one)
        for grade in boulder_grades:
            
            boulder_grade = {
                'id' : bg_id,
                'boulder' : id,
                'grade' : grade
            }
            scraperwiki.sqlite.save(unique_keys=['id'], data=boulder_grade, table_name="boulder_grade")
            bg_id += 1


        i += 2
        id += 1


    if not has_next(mainsub) == False:
        next_link = has_next(mainsub)
        # recursion: als de boulder een 'next' link heeft wordt de functie opnieuw uitgevoerd
        return save_area_boulders(area_id, next_link)



area_id = 1
# loop door de bovenstaande array
for area in areas:
    for areaname in area:
        # ga door alle areas heen. Save area + id in area table. Voor elke area; loop door de boulders
        for subarea in area[areaname]:
            #print "The lovely area: %s with url http://bleau.info/%s/7a++.html and about %s boulders 7a or harder" % (subarea[1], subarea[0], subarea[2])

            url = "http://bleau.info/%s/7a++.html" % subarea[0]

            area_data = {
                "id" : area_id,
                "name" : subarea[1]
            }
            scraperwiki.sqlite.save(unique_keys=['id'], data=area_data, table_name="areas")


            save_area_boulders(area_id, url)
            
            area_id += 1

