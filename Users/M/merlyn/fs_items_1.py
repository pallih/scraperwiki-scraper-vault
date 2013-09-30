import scraperwiki, lxml.html, re, urllib2, time

def check_table():
    if len(scraperwiki.sqlite.table_info("swdata")) == 0:
        scraperwiki.sqlite.execute('''
        CREATE TABLE "swdata" (
        "id" integer
        , "Name" text
        , "Rarity" text
        , "Type" text
        , "Level" integer
        , "Attack" integer
        , "Defense" integer
        , "Armor" integer
        , "Damage" integer
        , "HP" integer
        , "XPGain" integer
        , "Stamina" integer
        , "StaminaGain" integer
        , "GoldGain" integer
        , "Banishment" integer
        , "BeastSlayer" integer
        , "Breaker" integer
        , "CriticalHit" integer
        , "Disarm" integer
        , "Dodge" integer
        , "Duelist" integer
        , "EliteHunter" integer
        , "FirstStrike" integer
        , "FuryCaster" integer
        , "GlorySeeker" integer
        , "GreenskinSlayer" integer
        , "Holy" integer
        , "Hypnotize" integer
        , "MasterBlacksmith" integer
        , "MasterCrafter" integer
        , "MasterInventor" integer
        , "MasterThief" integer
        , "Nullify" integer
        , "Oceanic" integer
        , "PiercingStrike" integer
        , "ProtectGold" integer
        , "Protection" integer
        , "ReinforcedArmor" integer
        , "Sustain" integer
        , "Thievery" integer
        , "CraftAttack" integer
        , "CraftDefense" integer
        , "CraftArmor" integer
        , "CraftDamage" integer
        , "CraftHP" integer
        , "CraftXPGain" integer
        , "CraftStamina" integer
        , "CraftGoldGain" integer
        , "SetName" text
        , "SetAttack" integer
        , "SetDefense" integer
        , "SetArmor" integer
        , "SetDamage" integer
        , "SetHP" integer
        , "SetXPGain" integer
        , "SetStamina" integer
        , "SetStaminaGain" integer
        , "SetGoldGain" integer
        )''')
        scraperwiki.sqlite.commit()

def load(url):
    retries = 3
    for i in range(retries):
        try:
            handle = urllib2.urlopen(url)
            return lxml.html.fromstring(handle.read())
        except urllib2.URLError:
            if i + 1 == retries:
                raise
            else:
                print 'IO Error Waiting'
                time.sleep(1)

def get_last():
    root = load(base_url +'&index=0')
    a = root.cssselect('p.small a')
    return int(re.search(r'index=(\d+)&', a[len(a) - 1].attrib.get('href')).group(1))

def get_table(page):
    root = load(base_url +'&index=' + str(page))
    trs = root.cssselect('html>body>table>tr>td>table>tr>td>table>tr')
    index = 1
    for tr in trs:
        if index <> 1 and index <> len(trs) and index % 2 == 1:
            td = tr.cssselect('td')
            a = td[0].cssselect('a')[0]
            id = int(re.search(r'item_id=(\d+)&', a.attrib.get('href')).group(1))
            it = td[2].text
            if it in ('Amulet', 'Armor', 'Boots', 'Gloves', 'Helmet', 'Ring', 'Rune', 'Shield', 'Weapon'):
                get_stats(id)
        index += 1

def get_stats(page):
    root = load(base_url + '&subcmd=view&item_id=' + str(page))
    trs = root.cssselect('html>body>table>tr>td>table>tr>td>table>tr>td>table>tr>td')
    rec = {}
    rec ['id'] = page
    index = 1
    sect = 1
    shd = 'Title'
    tag = ''
    ctd = 0
    for tr in trs:
        hdr = tr.attrib.get('class')
        bar = tr.text_content()
        if len(bar) == 0:
            pass
        elif index == 1:
            SectionHeading = tr.cssselect('b')[0]
            rec ['Name'] = SectionHeading.text.encode('utf-8')
            rec ['Rarity'] = SectionHeading.tail[2:-1]
        elif hdr:
            sect = 1
            shd = bar
        elif shd in ('Title', 'Dropped By', 'Sold At', 'Extra Info'):
            pass
        elif shd == 'Statistics':
            if bar.endswith(':'):
                tag = bar[:-1]
            elif bar.isdigit():
                rec [tag.encode('ascii', 'ignore')] = int(bar)
            else:
                rec [tag.encode('ascii', 'ignore')] = bar
        elif shd == 'Enhancements':
            if bar.endswith(':'):
                tag = bar[:-1]
            elif bar <> '[no enhancements]':
                rec [tag.replace(' ', '')] = int(bar[:-1].replace(' ', ''))
        elif shd == 'Crafting':
            if bar.endswith(':'):
                ctd = 0
                tag = bar[:-1].replace(' ', '')
            else:
                ctd += 1
                if ctd == 3:
                    rec ['Craft' + tag] = int(bar)
        elif shd == 'Set Bonuses':
            sect += 1
            if bar == '[none]':
                pass
            elif sect == 2:
                foo = tr.cssselect('td>a>b')
                if foo[0].text is not None:
                    rec ['SetName'] = foo[0].text.encode('utf-8')
            elif bar.endswith(':'):
                tag = bar[:-1]
            else:
                rec ['Set' + tag.encode('ascii', 'ignore')] = int(bar)
        else:
            sect += 1
            print 'default', '---', index, '---', sect, '---', shd, '---', bar, '---', len(bar)
        index += 1
#    print rec
    scraperwiki.sqlite.save(unique_keys = ['id'], data = rec, table_name = "swdata", verbose = 0)

scraperwiki.sqlite.save_var('StartTime', time.asctime( time.localtime(time.time()) ))

base_url = 'http://guide.fallensword.com/index.php?cmd=items'

check_table()

j = scraperwiki.sqlite.get_var('LastIndex', 0)
last = get_last()
if j >= last - 30:
    j = 0

print 'Last Page =', last, 'NextIndex =', j

for i in range(j, last):
#for i in range(j, j + 1):
#    print 'NextIndex =', i
    get_table(i)
    scraperwiki.sqlite.save_var('LastIndex', i + 1)
    scraperwiki.sqlite.save_var('LastTime', time.asctime( time.localtime(time.time()) ))import scraperwiki, lxml.html, re, urllib2, time

def check_table():
    if len(scraperwiki.sqlite.table_info("swdata")) == 0:
        scraperwiki.sqlite.execute('''
        CREATE TABLE "swdata" (
        "id" integer
        , "Name" text
        , "Rarity" text
        , "Type" text
        , "Level" integer
        , "Attack" integer
        , "Defense" integer
        , "Armor" integer
        , "Damage" integer
        , "HP" integer
        , "XPGain" integer
        , "Stamina" integer
        , "StaminaGain" integer
        , "GoldGain" integer
        , "Banishment" integer
        , "BeastSlayer" integer
        , "Breaker" integer
        , "CriticalHit" integer
        , "Disarm" integer
        , "Dodge" integer
        , "Duelist" integer
        , "EliteHunter" integer
        , "FirstStrike" integer
        , "FuryCaster" integer
        , "GlorySeeker" integer
        , "GreenskinSlayer" integer
        , "Holy" integer
        , "Hypnotize" integer
        , "MasterBlacksmith" integer
        , "MasterCrafter" integer
        , "MasterInventor" integer
        , "MasterThief" integer
        , "Nullify" integer
        , "Oceanic" integer
        , "PiercingStrike" integer
        , "ProtectGold" integer
        , "Protection" integer
        , "ReinforcedArmor" integer
        , "Sustain" integer
        , "Thievery" integer
        , "CraftAttack" integer
        , "CraftDefense" integer
        , "CraftArmor" integer
        , "CraftDamage" integer
        , "CraftHP" integer
        , "CraftXPGain" integer
        , "CraftStamina" integer
        , "CraftGoldGain" integer
        , "SetName" text
        , "SetAttack" integer
        , "SetDefense" integer
        , "SetArmor" integer
        , "SetDamage" integer
        , "SetHP" integer
        , "SetXPGain" integer
        , "SetStamina" integer
        , "SetStaminaGain" integer
        , "SetGoldGain" integer
        )''')
        scraperwiki.sqlite.commit()

def load(url):
    retries = 3
    for i in range(retries):
        try:
            handle = urllib2.urlopen(url)
            return lxml.html.fromstring(handle.read())
        except urllib2.URLError:
            if i + 1 == retries:
                raise
            else:
                print 'IO Error Waiting'
                time.sleep(1)

def get_last():
    root = load(base_url +'&index=0')
    a = root.cssselect('p.small a')
    return int(re.search(r'index=(\d+)&', a[len(a) - 1].attrib.get('href')).group(1))

def get_table(page):
    root = load(base_url +'&index=' + str(page))
    trs = root.cssselect('html>body>table>tr>td>table>tr>td>table>tr')
    index = 1
    for tr in trs:
        if index <> 1 and index <> len(trs) and index % 2 == 1:
            td = tr.cssselect('td')
            a = td[0].cssselect('a')[0]
            id = int(re.search(r'item_id=(\d+)&', a.attrib.get('href')).group(1))
            it = td[2].text
            if it in ('Amulet', 'Armor', 'Boots', 'Gloves', 'Helmet', 'Ring', 'Rune', 'Shield', 'Weapon'):
                get_stats(id)
        index += 1

def get_stats(page):
    root = load(base_url + '&subcmd=view&item_id=' + str(page))
    trs = root.cssselect('html>body>table>tr>td>table>tr>td>table>tr>td>table>tr>td')
    rec = {}
    rec ['id'] = page
    index = 1
    sect = 1
    shd = 'Title'
    tag = ''
    ctd = 0
    for tr in trs:
        hdr = tr.attrib.get('class')
        bar = tr.text_content()
        if len(bar) == 0:
            pass
        elif index == 1:
            SectionHeading = tr.cssselect('b')[0]
            rec ['Name'] = SectionHeading.text.encode('utf-8')
            rec ['Rarity'] = SectionHeading.tail[2:-1]
        elif hdr:
            sect = 1
            shd = bar
        elif shd in ('Title', 'Dropped By', 'Sold At', 'Extra Info', 'Created by Recipe', 'Used In Recipes'):
            pass
        elif shd == 'Statistics':
            if bar.endswith(':'):
                tag = bar[:-1]
            elif bar.isdigit():
                rec [tag.encode('ascii', 'ignore')] = int(bar)
            else:
                rec [tag.encode('ascii', 'ignore')] = bar
        elif shd == 'Enhancements':
            if bar.endswith(':'):
                tag = bar[:-1]
            elif bar <> '[no enhancements]':
                rec [tag.replace(' ', '')] = int(bar[:-1].replace(' ', ''))
        elif shd == 'Crafting':
            if bar.endswith(':'):
                ctd = 0
                tag = bar[:-1].replace(' ', '')
            else:
                ctd += 1
                if ctd == 3:
                    rec ['Craft' + tag] = int(bar)
        elif shd == 'Set Bonuses':
            sect += 1
            if bar == '[none]':
                pass
            elif sect == 2:
                foo = tr.cssselect('td>a>b')
                if foo[0].text is not None:
                    rec ['SetName'] = foo[0].text.encode('utf-8')
            elif bar.endswith(':'):
                tag = bar[:-1]
            else:
                rec ['Set' + tag.encode('ascii', 'ignore')] = int(bar)
        else:
            sect += 1
            print 'default', '---', index, '---', sect, '---', shd, '---', bar, '---', len(bar)
        index += 1
#    print rec
    scraperwiki.sqlite.save(unique_keys = ['id'], data = rec, table_name = "swdata", verbose = 0)

scraperwiki.sqlite.save_var('StartTime', time.asctime( time.localtime(time.time()) ))

base_url = 'http://guide.fallensword.com/index.php?cmd=items'

check_table()

j = scraperwiki.sqlite.get_var('LastIndex', 0)
last = get_last()
if j >= last - 30:
    j = 0

print 'Last Page =', last, 'NextIndex =', j

for i in range(j, last):
#for i in range(j, j + 1):
#    print 'NextIndex =', i
    get_table(i)
    scraperwiki.sqlite.save_var('LastIndex', i + 1)
    scraperwiki.sqlite.save_var('LastTime', time.asctime( time.localtime(time.time()) ))