import scraperwiki
import os
import datetime
import re
import urllib
import lxml.etree

urlapi =  "http://en.wikipedia.org/w/api.php"

# needs also to handle redirects and marking up symbols and spaces
def GetWikipediaPage(name):

    "Downloads a single Wikipedia page and its metadata"

    params = { "format":"xml", "action":"query", "prop":"revisions", "rvprop":"timestamp|user|comment|content" }
    params["titles"] = "API|%s" % urllib.quote(name.encode("utf-8"),safe)

    qs = "&".join("%s=%s" % (k, v)  for k, v in params.items())
    url = "%s?%s" % (urlapi, qs)
    tree = lxml.etree.parse(urllib.urlopen(url), safe)
    #print lxml.etree.tostring(tree.getroot())
    normalizedname = name
    normn = tree.xpath('//normalized/n')
    if normn:
        normalizedname = normn[0].attrib["to"]
    revs = tree.xpath('//rev')
    if len(revs) == 1:
        return None
    rev = revs[-1]
    #print lxml.etree.tostring(rev)
    return { "name":normalizedname, "text":rev.text,
             "timestamp":rev.attrib.get("timestamp"),
             "user":rev.attrib.get("user"), "comment":rev.attrib.get("comment") }


def GetWikipediaCategory(categoryname):
    "Downloads all/some names and metadata of pages in given category"
    params = {"action":"query", "format":"xml", "generator":"categorymembers", "prop":"info", "gcmlimit":100 }
    params["gcmtitle"] = "Category:%s" % categoryname.encode("utf-8")
    result = [ ]
    while True:
        url = "%s?%s" % (urlapi, urllib.urlencode(params))
        tree = lxml.etree.parse(urllib.urlopen(url))
        for page in tree.xpath('//page'):
            pdata = dict(page.attrib.items())
            if "redirect" in pdata:   # case of the redirect page having a category, eg Paviland_Cave
                continue
            pdata.pop("new", None)
            assert pdata.keys() == ['lastrevid', 'pageid', 'title', 'counter', 'length', 'touched', 'ns'], (pdata.keys(), pdata)
            pdata['length'] = int(pdata['length'])
            try:
                if pdata["title"][:5] == "File:":
                    continue
                pdata["link"] = "http://en.wikipedia.org/wiki/%s" % (urllib.quote(pdata["title"].replace(" ", "_").replace(u'\u2013'," ").replace(u'\u03b1', "<alpha>").replace(u'\xf0', "<eth>").replace(u'\xdf', "B").replace(u'\u0392', "<Beta>").replace(u'\u03b2', "<beta>").replace(u'\xef', "i").replace(u'\u2032', "'").replace(u'\xe9', "e").replace(u'\u0107', "c").replace(u'\xed', "i").replace(u'\xe8', "e").replace(u'\xe4', "a").replace(u'\xf6', "u").replace(u'\xf8', "o").replace(u'\xc1', "A").replace(u'\u016b', "u").replace(u'\xe1', "a").replace(u'\u014d', "o").replace(u'\xce', "I").replace(u'\xf1', "n").replace(u'\u0161', "s").replace(u'\xfc', "u").replace(u'\xf3', "o").replace(u'\xeb', "e").replace(u'\u2018', "'").replace(u'\xfa', "u").replace(u'\u0391', "A").replace(u'\xe6', "ae").replace(u'\u2014', "-").replace(u'\u0103', "a").replace(u'\u015f', "s").replace(u'\u017e', "z").replace(u'\xe3', "a").replace(u'\xf4', "o").replace(u'\xcd', "I").replace(u'\u0142', "I").replace(u'\xc5', "A").replace(u'\xc9', "E").replace(u'\u0151', "o").replace(u'\u0105', "a").replace(u'\xfd', "y").replace(u'\xe7', "c").replace(u'\u0131', "i").replace(u'\u2212', "-").replace(u'\xb2', "2").replace(u'\u015e', "S").replace(u'\u015e', "S").replace(u'\u015e', "S").replace(u'\u015e', "S").replace(u'\u015e', "S").replace(u'\u015e', "S").replace(u'\u015e', "S").replace(u'\u015e', "S").replace(u'\u015e', "S").replace(u'\u015e', "S").replace(u'\u015e', "S")))
            except:
                pass 
            result.append(pdata)

        cmcontinue = tree.xpath('//query-continue/categorymembers') # attrib.get("gcmcontinue") is fed back in as gmcontinue parameter                     
        if not cmcontinue:
            break
        params["gcmcontinue"] = cmcontinue[0].get("gcmcontinue")
    return result
    url.close()

def GetWikipediaCategoryRecurse(categoryname):
    "Downloads everything in a given category and all the subcategories"
    prestack = [ categoryname ]
    usedcategories = set()
    result = [ ]
    while prestack:
        lcategoryname = prestack.pop() #pops off l(ast)category name from prestack and returns it
        if lcategoryname in usedcategories:
            continue
        for d in GetWikipediaCategory(lcategoryname):
            if d["title"][:9] == "Category:":
                prestack.append(d["title"][9:])
            else:
                result.append(d)
        usedcategories.add(lcategoryname)  # avoids infinite loops
    return result

        
def ParseTemplates(text):
    "Extract all the templates/infoboxes from the text into a list"
    res = { "templates":[ ], "categories":[ ], "images":[ ], "wikilinks":[ ], "flattext":[ ] }
    templstack = [ ]
    for tt in re.split("(\{\{\{|\}\}\}|\{\{|\}\}|\[\[|\]\]|\|)", text):
        if tt in ["{{{", "{{", "[["]:
            templstack.append([tt, [ [ ] ] ])
        elif templstack and tt in ["}}}", "}}", "]]"]:
            templstack[-1][1][-1] = "".join(templstack[-1][1][-1])
            templstack[-1].append(tt)
            if len(templstack) == 1:
                if templstack[-1][0] == "{{":
                    ltempl = [ ]
                    for i, param in enumerate(templstack[-1][1]):
                        k, e, v = param.partition("=")
                        if e:
                            ltempl.append((k.strip(), v.strip()))
                        else:
                            ltempl.append((i, k.strip()))
                    if ltempl:
                        res["templates"].append((ltempl[0][1], dict(ltempl)))
                elif templstack[-1][0] == "[[":
                    llink = templstack[-1][1]
                    if llink:
                        llink0, cllink, cllink1 = llink[0].partition(":")
                        if llink[0][0] == ':':   # eg [[:Category:something]]
                            res["wikilinks"].append(llink[-1])
                            res["flattext"].append(llink[0][1:])  # the [[what you see|actual link]]
                        elif cllink:
                            if llink0 == "Category":
                                res["categories"].append(cllink1.strip())
                            elif llink0 in ["Image", "File"]:
                                res["images"].append(cllink1.strip())
                            elif len(llink0) == 2:
                                pass  # links to other languages
                            else:
                                print "Unrecognized", llink
                        else:
                            res["wikilinks"].append(llink[-1])
                            res["flattext"].append(llink[0])  # the [[what you see|actual link]]
            else:
                templstack[-2][1][-1].append(templstack[-1][0])
                templstack[-2][1][-1].append("|".join(templstack[-1][1]))
                templstack[-2][1][-1].append(templstack[-1][2])
            del templstack[-1]
        elif tt == "|" and templstack:
            templstack[-1][1][-1] = "".join(templstack[-1][1][-1])
            templstack[-1][1].append([ ])
        elif templstack:
            templstack[-1][1][-1].append(tt)
        else:
            res["flattext"].append(tt)
    res["flattext"] = "".join(res["flattext"])
    return res

templist = ['Template:Nucleic acid inhibitors']
templist1 = ['Template:Other respiratory system products','Template:Throat preparations','Template:Respiratory-system-drug-stub','Template:Drugs for obstructive airway diseases','Template:Nasal preparations','Template:Cough and cold preparations','Template:Otologicals','Template:Antiglaucoma preparations and miotics','Template:Mydriatics and cycloplegics','Template:Ocular vascular disorder agents','Template:Ophthalmological anti-infectives','Template:Antiaddictives','Template:Antivertigo preparations','Template:Other nervous system drugs','Template:Nervous-system-drug-stub','Template:Sedative-stub','Template:Anxiolytic-stub','Template:Psychoactive-stub','Template:Hallucinogen-stub','Template:Cannabinoid-stub','Template:Anticonvulsant-stub','Template:Analgesic-stub','Template:Hypnotics and sedatives','Template:Anxiolytics','Template:Antipsychotics','Template:Smoking nav','Template:HolmesNovels','Template:HolmesFilms','Template:Infobox Sherlock Holmes short story','Template:Big five tobacco companies','Template:British American Tobacco','Template:Imperial Tobacco','Template:Psychostimulants, agents used for ADHD and nootropics','Template:Antidepressants','Template:Kava','Template:Anti-dementia drugs','Template:Antiparkinson','Template:Anticonvulsants','Template:Local anesthetics','Template:General anesthetics','Template:Analgesics','Template:Antimigraine preparations','Template:Drugs for treatment of bone diseases','Template:Musculoskeletal-drug-stub','Template:Muscle relaxants','Template:Antigout preparations','Template:Anti-inflammatory products','Template:Antirheumatic products','Template:Glucocorticoids','Template:Ginger ales','Template:Systemic-hormonal-drug-stub','Template:Mineralocorticoids','Template:Gonadotropins and GnRH','Template:Gynecological anti-infectives and antiseptics','Template:Genito-urinary-drug-stub','Template:Urologicals, including antispasmodics','Template:Drugs used in benign prostatic hypertrophy','Template:Drugs for erectile dysfunction and PE','Template:Hormonal contraceptives','Template:Progestogenics','Template:Estrogenics','Template:Estrogens and progestogens','Template:Xenoestrogens','Template:Androgenics','Template:Androgens','Template:Anabolic steroids','Template:Bile and liver therapy','Template:Drugs for functional gastrointestinal disorders','Template:Other alimentary tract and metabolism products','Template:Gastrointestinal-drug-stub','Template:Laxatives','Template:Antiemetics','Template:Antiobesity preparations','Template:Antidiarrheals, intestinal anti-inflammatory/anti-infective agents','Template:Oral hypoglycemics and insulin analogs','Template:Drugs for peptic ulcer and GORD','Template:Antacids','Template:Dermatologic-drug-stub','Template:Preparations for treatment of wounds and ulcers','Template:Emollients and protectives','Template:Antiseptics and disinfectants','Template:Antipsoriatics','Template:Antipruritics','Template:Acne agents','Template:Vasoprotectives','Template:Cardiovascular-drug-stub','Template:Antihypertensive-stub','Template:Peripheral vasodilators','Template:Vasodilators used in cardiac diseases','Template:Cardiac glycosides','Template:Cardiac stimulants excluding cardiac glycosides','Template:Nonsympatholytic vasodilatory antihypertensives','Template:Sympatholytic antihypertensives','Template:Diuretics','Template:Beta blockers','Template:Agents acting on the renin-angiotensin system','Template:Antiarrhythmic agents','Template:B03, B05, B06','Template:Blood-drug-stub','Template:Antithrombotics','Template:Antihemorrhagics','Template:Antineoplastic-drug-stub','Template:Immune sera and immunoglobulins','Template:Engineered antibodies','Template:Monoclonals for bone, musculoskeletal, circulatory, and neurologic systems','Template:Monoclonals for infectious disease and toxins','Template:Monoclonal-antibody-stub','Template:Monoclonals for tumors','Template:Immunosuppressants','Template:Immunostimulants','Template:Extracellular chemotherapeutic agents','Template:Intracellular chemotherapeutic agents','Template:Detoxifying agents for antineoplastic treatment','Template:Antiinfective-drug-stub','Template:Vaccine-stub','Template:Antibiotic-stub','Template:DNA antivirals','Template:RNA antivirals','Template:Antiretroviral drug','Template:Anti-arthropod medications','Template:Agents against amoebozoa','Template:Chromalveolate antiparasitics','Template:Excavata antiparasitics','Template:Anthelmintics','Template:Antifungals','Template:Antimycobacterials','Template:Protein synthesis inhibitor antibiotics','Template:Nucleic acid inhibitors','Template:Cell wall disruptive antibiotics']

#for listurl in templist1:
#    print line
   # print ParseTemplates(listurl)

scrapeddata = GetWikipediaCategoryRecurse("Analgesics")
scraperwiki.sqlite.save(["title"], scrapeddata, 'line')


