import scraperwiki
import urlparse
from pyquery import PyQuery as pq
import lxml.html
import lxml.etree
from HTMLParser import HTMLParser
import re


seveneightarray=[[["maincourt","Dampierre Maincourt",26],["troche","La Troche",11],["orsay","Orsay",6]],[["chamarande","Chamarande",23],["fertealais","La Ferté-Alais",1],["pendu","Le Pendu d'Huison",4],["sanglier","Le Sanglier",13],["maisse","Maisse le Patouillat",1],["villeneuve","Villeneuve sur Auvers",8]],[["beauvaisest","Beauvais Est",15],["guinguette","Beauvais Guinguette",5],["hameau","Beauvais Hameau",17],["beauvais","Beauvais Nainville",45],["telegraphe","Beauvais Télégraphe",7],["valette","Bois de la Valette",7],["charbonniere","La Charbonnière",3],["padole","La Padôle",40],["moigny","Moigny sur École",1],["oncy","Oncy sur École",2],["videlles_abbatoir","Videlles l'Abattoir",35],["videlles","Videlles les Roches",32]],[["arcades","Coquibus Arcades",15],["auvergne","Coquibus Auvergne",32],["grandesvallees","Coquibus Grandes Vallées",11],["longsvaux","Coquibus Longs Vaux",42],["coquibus","Coquibus Rumont",9],["courances","Côtes de Courances",10],["coquibuswest","Gorge à Véron",10],["guichet","Le Guichet",4],["joncs","Mare aux Joncs",11],["montignotte","Montignotte",31],["montrouget","Montrouget",10],["montrougetouest","Montrouget Ouest",7],["rochequitourne","Roche qui Tourne",13],["ancetres","Vallée des Ancêtres",4]],[["boisdurocher","Bois du Rocher",9],["rond","Bois Rond",38],["canche","Canche aux Merciers",54],["zinnen","Drei Zinnen",56],["anarchodrome","L'Anarchodrome",18],["beorlots","Les Béorlots",49],["petitereine","Petite Reine",17],["cretenord","Reine Crête Nord",6],["cornebiche","Rocher de Corne-Biche",7],["reine","Rocher de la Reine",45],["valleeronde","Rocher de la Vallée Ronde",5],["milly","Rocher de Milly",34],["mariniers","Rocher des Mariniers",4],["telegraphe2","Rocher du Télégraphe",4],["touche","Touche aux Mulets",2],["valleechaude","Vallée Chaude",2]],[["91.1","91.1",4],["95.2","95.2",48],["cul","Cul de Chien",19],["chats","Gorge aux Châts",58],["gros","Gros Sablons",24],["jean","Jean des Vignes",11],["chateauveau","Justice de Chambergeot",6],["pivot","Mont Pivot",12],["oiseaux","Roche aux Oiseaux",30],["sabots","Roche aux Sabots",72],["zen","Roche aux Sabots Sud",24],["souris","Rocher des Souris",12]],[["hautsmilly","Bois des Hauts de Milly",12],["diplodocus","Diplodocus",3],["grandemontagne","Grande Montagne",16],["martin","J.A. Martin",48],["111","Le 111",8],["cailleau","Rocher Cailleau",16],["cathedrale","Rocher de la Cathédrale",5],["general","Rocher du Général",9],["mee","Rocher du Potala",46],["fin","Rocher Fin",53],["guichot","Rocher Guichot",18]],[["cuvier","Cuvier",190],["cuvierest","Cuvier Est",54],["merveille","Cuvier Merveille",18],["rempart","Cuvier Rempart",147],["piat","La Mare à Piat",23],["reconnaissance","La Reconnaissance",51],["montsetmerveilles","Monts & Merveilles",2],["petitrempart","Petit Rempart",12]],[["cassepotgrises","Cassepot Roches Grises",21],["cassepotoranges","Cassepot Roches Oranges",11],["cassepotroses","Cassepot Roches Roses",10],["calvaire","Le Calvaire",11],["ussy","Mont Ussy",21],["hercule","Roche d'Hercule",15],["canon","Rocher Canon",94],["canonouest","Rocher Canon Ouest",24],["germain","Rocher Saint-Germain",77],["denecourt","Tour Dénecourt",2]],[["apremont","Apremont",96],["bizons","Apremont Bizons",15],["butteauxpeintres","Apremont Butte aux Peintres",13],["buvette","Apremont Buvette",2],["desert","Apremont Désert",11],["envers","Apremont Envers",22],["apremontouest","Apremont Ouest",40],["apremontsully","Apremont Vallon de Sully",12],["solitude","Vallon de la Solitude",14]],[["carnage","Cuisinière Carnage",15],["cretesud","Cuisinière Crête Sud",56],["bassesplaines","Franchard Basses Plaines",11],["sablons110","Franchard Carriers",28],["cuisiniere","Franchard Cuisinière",107],["ermitage","Franchard Ermitage",24],["plaines","Franchard Hautes-Plaines",27],["isatis","Franchard Isatis",129],["meyer","Franchard Meyer",31],["oiseauxdeproie","Franchard Oiseaux de Proie",9],["franchardpointdevue","Franchard Point de Vue",42],["raymond","Franchard Raymond",16],["sablons","Franchard Sablons",29],["merisiers","Gorge aux Merisiers",7],["houx","Gorges du Houx",31],["aigu","Mont Aigu - Long Boyau",16],["petitparadis","Petit Paradis",12]],[["marecorneilles","Mare aux Corneilles",30],["marion","Marion des Roches",30],["recloses","Recloses",8],["restant","Restant du Long Rocher",35],["grottebeatrix","Restant du Long Rocher Nord",18],["longrochergrandesvallees","Restant du Long Rocher Ouest",6],["rocherbrule","Rocher Brûlé",27],["avon","Rocher d'Avon",33],["avonouest","Rocher d'Avon Ouest",57],["bouligny","Rocher de Bouligny",28],["combe","Rocher de la Combe",2],["occidentale","Rocher de la Salamandre",18],["demoiselles","Rocher des Demoiselles",59],["princes","Rocher des Princes",16],["passage","Rocher du Mauvais Passage",12],["montmorillon","Rocher du Mont Morillon",12]],[["chaintreauville","Chaintreauville",17],["fosse","Fosse aux Loups",3],["troglodyte","Le Troglodyte",4],["mammouths","Les Mammouths",9],["olivet","Mont d'Olivet",1],["petit","Petit Bois",24],["puiselet","Puiselet Le Paradis",47],["sarrazin","Puiselet Mont Sarrasin",28],["sablibum","Puiselet Sablibum",5],["greau","Rocher Gréau",30],["cassepot","Vallée Casse-Pot",3]],[["jouanne","Dame Jouanne",46],["elephant","Éléphant",51],["boutdumonde","Éléphant Bout du Monde",9],["elephantnord","Éléphant Nord",19],["ouest","Éléphant Ouest",38],["maunoury","Maunoury",48],["simonet","Mont Simonet",14]],[["boigneville","Boigneville",26],["cailles","Boissy aux Cailles",21],["canard","Buthiers Canard",26],["y","Buthiers Piscine",36],["tennis","Buthiers Tennis",24],["marlenval","Marlanval",3],["roisneau","Moulin de Roisneau",14],["champlaid","Vallée de Champlaid",3],["villetard","Villetard",4]]]



d = pq(url='http://bleau.info/maincourt/7a++.html')
table = d("#mainsub1 table tr")

for tr in table:
    tds = pq(tr).find('td').eq(0)
    for td in tds:
        print pq(td)


def get_area_url(area):
    return "http://bleau.info/%s/7a++.html" % area


'''
for region in seveneightarray:
    for area in region:
        print '%s - %s' % (area[0],  area[1])
        print get_area_url(area[0])

'''



