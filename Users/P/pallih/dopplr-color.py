# inspired by dopplr's color squares
# http://blog.dopplr.com/2007/10/23/in-rainbows/

from hashlib import md5
from string import Template
import string

def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i+lv/3], 16) for i in range(0, lv, lv/3))

def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb

def getContrastYIQ(hexcolor):
    r = int(hexcolor[:2],16)
    g = int(hexcolor[2:-2],16)
    b = int(hexcolor[-2:],16)

    yiq = ((r*299)+(g*587)+(b*114))/1000
    #return yiq
    if yiq >= 128:
        return 'black'
    else:
        return 'white'
#    return (yiq >= 128)'black':'white';



table = string.maketrans(
    '0123456789abcdef',
    'fedcba9876543210')

print '<html><head><style type="text/css">.place {-moz-border-radius: 12px;-webkit-border-radius: 12px;-khtml-border-radius: 12px;border-radius: 12px;}</style></head><body>'
hood_block = Template("""

    <div class="place" style="background-color:#$bghex; color:$inverthex;font-family:arial;font-size:20px;padding:10px;display:inline-block;margin-bottom:4px;">$place</div>

""")

placelist = [
    "Reykjavíkurborg",
"Reykjavík",
"Kópavogur",
"Hafnarfjörður",
"Akureyri",
"Reykjanesbær",
"Garðabær",
"Mosfellsbær",
"Árborg",
"Akranes",
"Fjarðabyggð",
"Seltjarnarnes",
"Vestmannaeyjar",
"Skagafjörður",
"Ísafjarðarbær",
"Borgarbyggð",
"Fljótsdalshérað",
"Norðurþing",
"Grindavík",
"Álftanes",
"Hveragerði",
"Hornafjörður",
"Fjallabyggð",
"Sveitarfélagið Ölfus",
"Dalvíkurbyggð",
"Rangárþing eystra",
"Sandgerði",
"Snæfellsbær",
"Rangárþing ytra",
"Garður",
"Sveitarfélagið Vogar",
"Húnaþing vestra",
"Stykkishólmur",
"Eyjafjarðarsveit",
"Bolungarvík",
"Þingeyjarsveit",
"Vesturbyggð",
"Bláskógabyggð",
"Grundarfjarðarbær",
"Blönduós",
"Hrunamannahreppur",
"Seyðisfjörður",
"Dalabyggð",
"Vopnafjarðarhreppur",
"Hvalfjarðarsveit",
"Hörgársveit",
"Flóahreppur",
"Langanesbyggð",
"Skagaströnd",
"Skeiða- og Gnúpverjahreppur",
"Mýrdalshreppur",
"Strandabyggð",
"Skaftárhreppur",
"Djúpavogshreppur",
"Húnavatnshreppur",
"Grímsnes- og Grafningshreppur",
"Svalbarðsstrandarhreppur",
"Skútustaðahreppur",
"Grýtubakkahreppur",
"Tálknafjarðarhreppur",
"Reykhólahreppur",
"Breiðdalshreppur",
"Akrahreppur",
"Súðavíkurhreppur",
"Kjósarhreppur",
"Ásahreppur",
"Eyja- og Miklaholtshreppur",
"Borgarfjarðarhreppur",
"Kaldrananeshreppur",
"Svalbarðshreppur",
"Skagabyggð",
"Bæjarhreppur",
"Fljótsdalshreppur",
"Helgafellssveit",
"Skorradalshreppur",
"Tjörneshreppur",
"Árneshreppur",
"1",
"2",
"3",
"4",
"5",
"6",
"7",
"8",
"9",
]



for place in placelist:
    hash = md5(place).hexdigest()
    bghex = hash[:6]
    #rgb = hex_to_rgb(bghex)
    print hood_block.substitute(
        #cityid=place.lower().replace(' ','-'),
        bghex= hash[:6],
        place=place,
        #inverthex = bghex.lower().translate(table).upper()
        inverthex = getContrastYIQ(bghex)
    )
print '</body></html>'
# inspired by dopplr's color squares
# http://blog.dopplr.com/2007/10/23/in-rainbows/

from hashlib import md5
from string import Template
import string

def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i+lv/3], 16) for i in range(0, lv, lv/3))

def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb

def getContrastYIQ(hexcolor):
    r = int(hexcolor[:2],16)
    g = int(hexcolor[2:-2],16)
    b = int(hexcolor[-2:],16)

    yiq = ((r*299)+(g*587)+(b*114))/1000
    #return yiq
    if yiq >= 128:
        return 'black'
    else:
        return 'white'
#    return (yiq >= 128)'black':'white';



table = string.maketrans(
    '0123456789abcdef',
    'fedcba9876543210')

print '<html><head><style type="text/css">.place {-moz-border-radius: 12px;-webkit-border-radius: 12px;-khtml-border-radius: 12px;border-radius: 12px;}</style></head><body>'
hood_block = Template("""

    <div class="place" style="background-color:#$bghex; color:$inverthex;font-family:arial;font-size:20px;padding:10px;display:inline-block;margin-bottom:4px;">$place</div>

""")

placelist = [
    "Reykjavíkurborg",
"Reykjavík",
"Kópavogur",
"Hafnarfjörður",
"Akureyri",
"Reykjanesbær",
"Garðabær",
"Mosfellsbær",
"Árborg",
"Akranes",
"Fjarðabyggð",
"Seltjarnarnes",
"Vestmannaeyjar",
"Skagafjörður",
"Ísafjarðarbær",
"Borgarbyggð",
"Fljótsdalshérað",
"Norðurþing",
"Grindavík",
"Álftanes",
"Hveragerði",
"Hornafjörður",
"Fjallabyggð",
"Sveitarfélagið Ölfus",
"Dalvíkurbyggð",
"Rangárþing eystra",
"Sandgerði",
"Snæfellsbær",
"Rangárþing ytra",
"Garður",
"Sveitarfélagið Vogar",
"Húnaþing vestra",
"Stykkishólmur",
"Eyjafjarðarsveit",
"Bolungarvík",
"Þingeyjarsveit",
"Vesturbyggð",
"Bláskógabyggð",
"Grundarfjarðarbær",
"Blönduós",
"Hrunamannahreppur",
"Seyðisfjörður",
"Dalabyggð",
"Vopnafjarðarhreppur",
"Hvalfjarðarsveit",
"Hörgársveit",
"Flóahreppur",
"Langanesbyggð",
"Skagaströnd",
"Skeiða- og Gnúpverjahreppur",
"Mýrdalshreppur",
"Strandabyggð",
"Skaftárhreppur",
"Djúpavogshreppur",
"Húnavatnshreppur",
"Grímsnes- og Grafningshreppur",
"Svalbarðsstrandarhreppur",
"Skútustaðahreppur",
"Grýtubakkahreppur",
"Tálknafjarðarhreppur",
"Reykhólahreppur",
"Breiðdalshreppur",
"Akrahreppur",
"Súðavíkurhreppur",
"Kjósarhreppur",
"Ásahreppur",
"Eyja- og Miklaholtshreppur",
"Borgarfjarðarhreppur",
"Kaldrananeshreppur",
"Svalbarðshreppur",
"Skagabyggð",
"Bæjarhreppur",
"Fljótsdalshreppur",
"Helgafellssveit",
"Skorradalshreppur",
"Tjörneshreppur",
"Árneshreppur",
"1",
"2",
"3",
"4",
"5",
"6",
"7",
"8",
"9",
]



for place in placelist:
    hash = md5(place).hexdigest()
    bghex = hash[:6]
    #rgb = hex_to_rgb(bghex)
    print hood_block.substitute(
        #cityid=place.lower().replace(' ','-'),
        bghex= hash[:6],
        place=place,
        #inverthex = bghex.lower().translate(table).upper()
        inverthex = getContrastYIQ(bghex)
    )
print '</body></html>'
