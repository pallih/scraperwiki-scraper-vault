import requests 
import scraperwiki
from time import gmtime, strftime
import json 


items_of_interest = {
    "Embelsilk Cloth" : 53010, 
    "Netherweave Cloth" : 21877, 
    "Windwool Cloth" : 72988, 
    "Frostweave Cloth" : 33470, 
    "Cinderboom" : 52983, 
    "FoolsCap" : 79011, 
    "Snow Lily" : 79010, 
    "GreenTeaLeaf" : 72234, 
    "Silkweed" : 72235, 
    "GhostIronOre" : 72092, 
    "GhostIronBar" : 72096, 
    "PyriteOre" : 52183, 
    "ExoticLeather" : 72120, 
    "ShaTouchedLeather" : 72162 
}

item_list = [items_of_interest[i] for i in items_of_interest]

servers = ["Aegwynn","AeriePeak","Agamaggan","Aggramar","Akama","Alexstrasza","Alleria","AltarofStorms","AlteracMountains","Aman'Thul","Andorhal","Anetheron","Antonidas","Anub'arak","Anvilmar","Arathor","Archimonde","Area52","ArgentDawn","Arthas","Arygos","Auchindoun","Azgalor","Azjol-Nerub","Azralon","Azshara","Azuremyst","Baelgun","Balnazzar","Barthilas","BlackDragonflight","Blackhand","Blackrock","BlackwaterRaiders","BlackwingLair","Blade'sEdge","Bladefist","BleedingHollow","BloodFurnace","Bloodhoof","Bloodscalp","Bonechewer","BoreanTundra","Boulderfist","Bronzebeard","BurningBlade","BurningLegion","Caelestrasz","Cairne","CenarionCircle","Cenarius","Cho'gall","Chromaggus","Coilfang","Crushridge","Daggerspine","Dalaran","Dalvengyr","DarkIron","Darkspear","Darrowmere","Dath'Remar","Dawnbringer","Deathwing","DemonSoul","Dentarg","Destromath","Dethecus","Detheroc","Doomhammer","Draenor","Dragonblight","Dragonmaw","Drak'Tharon","Drak'thul","Draka","Drakkari","Dreadmaul","Drenden","Dunemaul","Durotan","Duskwood","EarthenRing","EchoIsles","Eitrigg","Eldre'Thalas","Elune","EmeraldDream","Eonar","Eredar","Executus","Exodar","Farstriders","Feathermoon","Fenris","Firetree","Fizzcrank","Frostmane","Frostmourne","Frostwolf","Galakrond","Gallywix","Garithos","Garona","Garrosh","Ghostlands","Gilneas","Gnomeregan","Goldrinn","Gorefiend","Gorgonnash","Greymane","GrizzlyHills","Gul'dan","Gundrak","Gurubashi","Hakkar","Haomarush","Hellscream","Hydraxis","Hyjal","Icecrown","Illidan","Jaedenar","Jubei'Thos","Kael'thas","Kalecgos","Kargath","Kel'Thuzad","Khadgar","KhazModan","Khaz'goroth","Kil'jaeden","Kilrogg","KirinTor","Korgath","Korialstrasz","KulTiras","LaughingSkull","Lethon","Lightbringer","Lightning'sBlade","Lightninghoof","Llane","Lothar","Madoran","Maelstrom","Magtheridon","Maiev","Mal'Ganis","Malfurion","Malorne","Malygos","Mannoroth","Medivh","Misha","Mok'Nathal","MoonGuard","Moonrunner","Mug'thol","Muradin","Nagrand","Nathrezim","Nazgrel","Nazjatar","Nemesis","Ner'zhul","Nesingwary","Nordrassil","Norgannon","Onyxia","Perenolde","Proudmoore","Quel'dorei","Quel'Thalas","Ragnaros","Ravencrest","Ravenholdt","Rexxar","Rivendare","Runetotem","Sargeras","Saurfang","ScarletCrusade","Scilla","Sen'jin","Sentinels","ShadowCouncil","Shadowmoon","Shadowsong","Shandris","ShatteredHalls","ShatteredHand","Shu'halo","SilverHand","Silvermoon","SistersofElune","Skullcrusher","Skywall","Smolderthorn","Spinebreaker","Spirestone","Staghelm","SteamwheedleCartel","Stonemaul","Stormrage","Stormreaver","Stormscale","Suramar","Tanaris","Terenas","Terokkar","Thaurissan","TheForgottenCoast","TheScryers","TheUnderbog","TheVentureCo","ThoriumBrotherhood","Thrall","Thunderhorn","Thunderlord","Tichondrius","TolBarad","Tortheldrin","Trollbane","Turalyon","TwistingNether","Uldaman","Uldum","Undermine","Ursin","Uther","Vashj","Vek'nilash","Velen","Warsong","Whisperwind","Wildhammer","Windrunner","Winterhoof","WyrmrestAccord","Ysera","Ysondre","Zangarmarsh","Zul'jin","Zuluhed"]

for i in servers: 
    current_server = i
    html_link = "http://us.battle.net/api/wow/auction/data/" + current_server 
    r = requests.get(html_link)
    print r.status_code, i
    if not r.status_code == 404: 
        json_link = json.loads(r.text)['files'][0]['url']
        r_json    = requests.get(json_link)
        if not r_json.status_code == 404: 
            print r_json.text
            for side in ['neutral', 'horde', 'alliance']: 
                json_file = json.loads(r_json.text)[side]['auctions'] 
                for key in json_file: 
                    if(key['item'] in item_list): 
                        data = {'auction_id' : key['auc'], 'time_left' : key['timeLeft'], 'bid' : key['bid'], 'item': key['item'], 'owner' : key['owner'], 'quantity' : key['quantity'], 'server' : current_server, 'side' : side, 'ID_time' :  strftime("%Y-%m-%d %H:%M:%S", gmtime())}
                        scraperwiki.sqlite.save(unique_keys=['ID_time'], data=data)
            import requests 
import scraperwiki
from time import gmtime, strftime
import json 


items_of_interest = {
    "Embelsilk Cloth" : 53010, 
    "Netherweave Cloth" : 21877, 
    "Windwool Cloth" : 72988, 
    "Frostweave Cloth" : 33470, 
    "Cinderboom" : 52983, 
    "FoolsCap" : 79011, 
    "Snow Lily" : 79010, 
    "GreenTeaLeaf" : 72234, 
    "Silkweed" : 72235, 
    "GhostIronOre" : 72092, 
    "GhostIronBar" : 72096, 
    "PyriteOre" : 52183, 
    "ExoticLeather" : 72120, 
    "ShaTouchedLeather" : 72162 
}

item_list = [items_of_interest[i] for i in items_of_interest]

servers = ["Aegwynn","AeriePeak","Agamaggan","Aggramar","Akama","Alexstrasza","Alleria","AltarofStorms","AlteracMountains","Aman'Thul","Andorhal","Anetheron","Antonidas","Anub'arak","Anvilmar","Arathor","Archimonde","Area52","ArgentDawn","Arthas","Arygos","Auchindoun","Azgalor","Azjol-Nerub","Azralon","Azshara","Azuremyst","Baelgun","Balnazzar","Barthilas","BlackDragonflight","Blackhand","Blackrock","BlackwaterRaiders","BlackwingLair","Blade'sEdge","Bladefist","BleedingHollow","BloodFurnace","Bloodhoof","Bloodscalp","Bonechewer","BoreanTundra","Boulderfist","Bronzebeard","BurningBlade","BurningLegion","Caelestrasz","Cairne","CenarionCircle","Cenarius","Cho'gall","Chromaggus","Coilfang","Crushridge","Daggerspine","Dalaran","Dalvengyr","DarkIron","Darkspear","Darrowmere","Dath'Remar","Dawnbringer","Deathwing","DemonSoul","Dentarg","Destromath","Dethecus","Detheroc","Doomhammer","Draenor","Dragonblight","Dragonmaw","Drak'Tharon","Drak'thul","Draka","Drakkari","Dreadmaul","Drenden","Dunemaul","Durotan","Duskwood","EarthenRing","EchoIsles","Eitrigg","Eldre'Thalas","Elune","EmeraldDream","Eonar","Eredar","Executus","Exodar","Farstriders","Feathermoon","Fenris","Firetree","Fizzcrank","Frostmane","Frostmourne","Frostwolf","Galakrond","Gallywix","Garithos","Garona","Garrosh","Ghostlands","Gilneas","Gnomeregan","Goldrinn","Gorefiend","Gorgonnash","Greymane","GrizzlyHills","Gul'dan","Gundrak","Gurubashi","Hakkar","Haomarush","Hellscream","Hydraxis","Hyjal","Icecrown","Illidan","Jaedenar","Jubei'Thos","Kael'thas","Kalecgos","Kargath","Kel'Thuzad","Khadgar","KhazModan","Khaz'goroth","Kil'jaeden","Kilrogg","KirinTor","Korgath","Korialstrasz","KulTiras","LaughingSkull","Lethon","Lightbringer","Lightning'sBlade","Lightninghoof","Llane","Lothar","Madoran","Maelstrom","Magtheridon","Maiev","Mal'Ganis","Malfurion","Malorne","Malygos","Mannoroth","Medivh","Misha","Mok'Nathal","MoonGuard","Moonrunner","Mug'thol","Muradin","Nagrand","Nathrezim","Nazgrel","Nazjatar","Nemesis","Ner'zhul","Nesingwary","Nordrassil","Norgannon","Onyxia","Perenolde","Proudmoore","Quel'dorei","Quel'Thalas","Ragnaros","Ravencrest","Ravenholdt","Rexxar","Rivendare","Runetotem","Sargeras","Saurfang","ScarletCrusade","Scilla","Sen'jin","Sentinels","ShadowCouncil","Shadowmoon","Shadowsong","Shandris","ShatteredHalls","ShatteredHand","Shu'halo","SilverHand","Silvermoon","SistersofElune","Skullcrusher","Skywall","Smolderthorn","Spinebreaker","Spirestone","Staghelm","SteamwheedleCartel","Stonemaul","Stormrage","Stormreaver","Stormscale","Suramar","Tanaris","Terenas","Terokkar","Thaurissan","TheForgottenCoast","TheScryers","TheUnderbog","TheVentureCo","ThoriumBrotherhood","Thrall","Thunderhorn","Thunderlord","Tichondrius","TolBarad","Tortheldrin","Trollbane","Turalyon","TwistingNether","Uldaman","Uldum","Undermine","Ursin","Uther","Vashj","Vek'nilash","Velen","Warsong","Whisperwind","Wildhammer","Windrunner","Winterhoof","WyrmrestAccord","Ysera","Ysondre","Zangarmarsh","Zul'jin","Zuluhed"]

for i in servers: 
    current_server = i
    html_link = "http://us.battle.net/api/wow/auction/data/" + current_server 
    r = requests.get(html_link)
    print r.status_code, i
    if not r.status_code == 404: 
        json_link = json.loads(r.text)['files'][0]['url']
        r_json    = requests.get(json_link)
        if not r_json.status_code == 404: 
            print r_json.text
            for side in ['neutral', 'horde', 'alliance']: 
                json_file = json.loads(r_json.text)[side]['auctions'] 
                for key in json_file: 
                    if(key['item'] in item_list): 
                        data = {'auction_id' : key['auc'], 'time_left' : key['timeLeft'], 'bid' : key['bid'], 'item': key['item'], 'owner' : key['owner'], 'quantity' : key['quantity'], 'server' : current_server, 'side' : side, 'ID_time' :  strftime("%Y-%m-%d %H:%M:%S", gmtime())}
                        scraperwiki.sqlite.save(unique_keys=['ID_time'], data=data)
            