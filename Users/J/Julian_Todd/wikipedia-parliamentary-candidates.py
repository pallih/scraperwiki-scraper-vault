import scraperwiki
import lxml.etree
import urllib, re, csv

# Work to do: chase down any wikilinks for candidates and follow redirects

# also a 16 constituencies have a nonstandard tabular layout.  seen by
# scraperwiki.sqlite.attach("wikipedia-list-of-constituencies", "s1")
# scraperwiki.sqlite.attach("wikipedia-parliamentary-candidates", "s2")
# print scraperwiki.sqlite.select("wptitle from s1.swdata left join s2.swdata on constituency=wptitle where constituency is null")


qs = "select wptitle, content from constsrc.swdata order by rowid desc limit 1 offset ?"

def Main():
    scraperwiki.sqlite.attach("wikipedia-list-of-constituencies", "constsrc")
    for i in range(0, 7000):
        tdata = scraperwiki.sqlite.execute(qs, i)
        if len(tdata["data"]) == 0:
            break
        cc = tdata["data"][0]
        print i, cc[0]
        text = cc[1]
        templs = ParseTemplates(text)
        ldata = [ ]
        for data in CollateElections(cc[0], templs):
            if data["type"] == "candidate":
                ldata.append(data)
        scraperwiki.sqlite.save(["constituency", "election", "candidate", "party"], ldata)


def CollateElections(title, templs):
    for templ in templs:
        if templ[0] == "Election box begin" or templ[0] == "Election box begin no clear":
            melectionname = re.search("\[\[(.*?)[\|\]]", templ["title"])
            electionname = melectionname and melectionname.group(1) or templ["title"]
            electionname = re.match("(.*?)\s*(\{\{.*|http://.*)?$", electionname).group(1)
            if electionname.startswith("UK "):
                electionname = "United Kingdom " + electionname[3:]
            electionname = re.sub("(United Kingdom general election) (\d\d\d\d)", "\\1, \\2", electionname)
            electionname = re.sub("(United Kingdom general election) (\d\d\d\d)", "\\1, \\2", electionname)
            if electionname == "January 1910 UK general election":
                electionname = "United Kingdom general election, January 1910"
            electionname = re.sub("(Notional 1992 UK General Election Result) : .*", "\\1", electionname)
                
            yield { "type":"election", "name":electionname }

        elif re.match("Election box candidate", templ[0]):
            data = { "type":"candidate", "constituency":title, "election":electionname }
            # get rid of punctuation and references that sometimes gets added to the end
            svotes = re.sub(" \(\?\)$|<br[^\d]*$|<ref[^\d]*$|[,. ]", "", templ["votes"])  
            
            if re.match("\d+$", svotes):
                votes = int(svotes)
            elif svotes in ["Unopposed", "Unoppose", "unopposed", "Elected", "Co-opted", "''N/A''", 
                            "'''unopposed'''", "''unopposed''", "(unopposed)", "''(unopposed)''", 
                            "''uncontested''", 
                            "Returned", "Returnedandseated", "Returnedandunseated", "Unknown"]:
                votes = 1
            elif svotes == "" or svotes == "-":
                votes = None
            elif svotes == "Defeated":
                votes = 0
            else:
                print ("Unparsed votes: " + str(templ) + str([svotes]))
                assert False
                
            if votes != None:
                data["votes"] = votes                
                
            party = re.match("(.*?)\s*(\[?http://.*|{{|<!.*|<ref.*|<sup.*)?$", templ["party"]).group(1)
            mpartycat = re.match("(.*?)\[\[(.+?)[\|\]]", party)
            if mpartycat:
                party = mpartycat.group(1) + mpartycat.group(2)
            party = re.sub(u"\u2013", "-", party)
            party = re.sub(u"\u2019", "-", party)
            assert not re.search("\[|<", party), list(templ["party"])
            data["party"] = party
            
            
            # clean up the candidate field so it contains no stray reference links
            candidate = templ["candidate"]
            mcandidatet = re.match("(?s)(.*?)\s*(<!.*|<ref.*|\[http://.*|\(Ruair.*?\)|\*+|\+|\,|<sup>\d</sup>|<nowiki>\*</nowiki>)$", candidate)
            if mcandidatet:
                candidate = mcandidatet.group(1)
    
            mcandidatet = re.match("(?s)['\"]*(?:Sir |Rt.? |Right |Hon\.? |Rev\.? |Prof\.? |Miss |Mrs\.? |Ms |Maj\.-Gen\. |Lt\.-Col\. |Lt\.-Cmdr\. |Lt-Gen |Maj\.? |Lt |Com |Col |Major |Major-General |Dr\.? |Brig |Gen |Gp |Capt\.? |Count |Captain |Commodore |Admiral |Lord |Lieutenant-Colonel |Commander |[WR]\. |Lieut Col |Lt-Col |Dame |Comm )*(.*?)(?:,? Bt\.?| CMG| KC| RN| [OKMCG]BE| MC| DSO| DFC| TD| KCB| CB| VRD| QC| MB| CSI| CIE| KCMG| GCB| LLD| MD| PhD| GCVO| \[\[Military Cross\|MC\]\]|, \[\[Royal Naval Volunteer Reserve\|RNVR\]\]|{{mnl}}| <sup>1</sup>\s*| \(PPC\)| \(incumbent\))*[\s'\"]*$", candidate)
            if mcandidatet:
                candidate = mcandidatet.group(1)

            # remove the target link in the pattern [[xxx|xxx]]
            mcandidate = re.match("(\[\[[^\]\|]+?)(?:\|[\s\S]+?)?\]\]$", candidate)
            if mcandidate:
                candidate = mcandidate.group(1) + "]]"
            candidate = re.sub(u"\u2019", "'", candidate)
            
            # error in http://en.wikipedia.org/wiki/North_Antrim_(UK_Parliament_constituency)#Elections_in_the_1880s
            if candidate == "[William Pirrie Sinclair":
                candidate = "William Pirrie Sinclair"
            if candidate == "[[John_Hemming_%28politician%29]]":
                candidate = "[[John_Hemming_(politician)]]"
            if candidate == "[[Nikolai Tolstoy]]-Miloslavsky":
                candidate = "[[Nikolai Tolstoy]]"
            if candidate[-27:] == u' ([[SDP\u2013Liberal Alliance]])':
                candidate = candidate[:-27]
            if candidate == u'Donald MacLaren of [[Clan MacLaren|MacLaren]]':
                candidate = u'Donald MacLaren'

            
            data["candidate"] = candidate
            
            
            # there are problems with the ndash in these names where inserting one in this python code causes 
            # an exception and a 0 length file to be saved
            if candidate.startswith("[[Richard Bethell (17"):
                assert title == "Yorkshire (UK Parliament constituency)", templ
            if candidate.startswith("[[Rowland Burdon (18"):
                assert title == "Sedgefield (UK Parliament constituency)", templ
            elif candidate.startswith("[[George Byng"):
                assert title == "Middlesex (UK Parliament constituency)"
            elif candidate == "[[Oliver Baldwin]], [[Viscount Corvedale]]":
                pass
            
            elif candidate and candidate != "[to be confirmed]":
                assert re.match("(\[\[)?[\w\s,.#_\-'\"/\(\)\x80-\xe2\xe9\xed\xfc\xf4]+(\]\])?$", candidate), [candidate, templ, electionname]
            elif candidate == "" and party != "Others":
                assert title in ["Aberavon (UK Parliament constituency)", 
                                 "Wycombe (UK Parliament constituency)", 
                                 "Gower (UK Parliament constituency)", 
                                 "Kettering (UK Parliament constituency)", 
                                 "Manchester Gorton (UK Parliament constituency)", 
                                 "Islington North (UK Parliament constituency)", 
                                 "Hornsey and Wood Green (UK Parliament constituency)", 
                                 "Finchley and Golders Green (UK Parliament constituency)", 
                                 "Epping Forest (UK Parliament constituency)", 
                                 "Bury St Edmunds (UK Parliament constituency)", 
                                 "Harlow (UK Parliament constituency)",
                                 "Bristol East (UK Parliament constituency)",
                                 "Beaconsfield (UK Parliament constituency)",
                                 "Battersea (UK Parliament constituency)",
                                 "Ashton-under-Lyne (UK Parliament constituency)",
                                ], data
                candidate = "unknown"

            else:
                assert party == "Others" or \
                       party == "others" or \
                       party == "non transferable" or \
                       title in ["Croydon North West (UK Parliament constituency)", 
                                 "South Colchester and Maldon (UK Parliament constituency)", 
                                 "Battersea (UK Parliament constituency)", 
                                 "Kettering (UK Parliament constituency)", 
                                 "Harlow (UK Parliament constituency)", 
                                 "Epping Forest (UK Parliament constituency)", 
                                 "North Essex (UK Parliament constituency)", 
                                 "South East Cambridgeshire (UK Parliament constituency)", 
                                 "Rochford and Southend East (UK Parliament constituency)", 
                                 "Finchley and Golders Green (UK Parliament constituency)", 
                                 "Bristol East (UK Parliament constituency)", 
                                 "Glasgow Cathcart (UK Parliament constituency)"] or \
                electionname == "next United Kingdom general election", \
                           [str(templ), electionname, title]
            
            yield data
            
        elif templ[0] == "Election box end":
            electionname = None


        
def ParseTemplates(text):   # pretty obfuscated, isn't it?
    templstack = [ ]
    for tt in re.split("(\{\{\{|\}\}\}|\{\{|\}\}|\[\[|\]\]|\|)", text):
        if tt in ["{{{", "{{", "[["]:
            templstack.append([tt, [ [ ] ] ])
        elif templstack and tt in ["}}}", "}}", "]]"]:
            templstack[-1][1][-1] = "".join(templstack[-1][1][-1])
            templstack[-1].append(tt)
            if len(templstack) == 1:
                if templstack[-1][0] == "{{":
                    res = { }
                    for i, param in enumerate(templstack[-1][1]):
                        k, e, v = re.match("(?s)([^=]*)(=?)(.*)$", param).groups()
                        if e:
                            res[k.strip()] = v.strip()
                        else:
                            res[i] = k.strip()
                    yield res
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


            
Main()
import scraperwiki
import lxml.etree
import urllib, re, csv

# Work to do: chase down any wikilinks for candidates and follow redirects

# also a 16 constituencies have a nonstandard tabular layout.  seen by
# scraperwiki.sqlite.attach("wikipedia-list-of-constituencies", "s1")
# scraperwiki.sqlite.attach("wikipedia-parliamentary-candidates", "s2")
# print scraperwiki.sqlite.select("wptitle from s1.swdata left join s2.swdata on constituency=wptitle where constituency is null")


qs = "select wptitle, content from constsrc.swdata order by rowid desc limit 1 offset ?"

def Main():
    scraperwiki.sqlite.attach("wikipedia-list-of-constituencies", "constsrc")
    for i in range(0, 7000):
        tdata = scraperwiki.sqlite.execute(qs, i)
        if len(tdata["data"]) == 0:
            break
        cc = tdata["data"][0]
        print i, cc[0]
        text = cc[1]
        templs = ParseTemplates(text)
        ldata = [ ]
        for data in CollateElections(cc[0], templs):
            if data["type"] == "candidate":
                ldata.append(data)
        scraperwiki.sqlite.save(["constituency", "election", "candidate", "party"], ldata)


def CollateElections(title, templs):
    for templ in templs:
        if templ[0] == "Election box begin" or templ[0] == "Election box begin no clear":
            melectionname = re.search("\[\[(.*?)[\|\]]", templ["title"])
            electionname = melectionname and melectionname.group(1) or templ["title"]
            electionname = re.match("(.*?)\s*(\{\{.*|http://.*)?$", electionname).group(1)
            if electionname.startswith("UK "):
                electionname = "United Kingdom " + electionname[3:]
            electionname = re.sub("(United Kingdom general election) (\d\d\d\d)", "\\1, \\2", electionname)
            electionname = re.sub("(United Kingdom general election) (\d\d\d\d)", "\\1, \\2", electionname)
            if electionname == "January 1910 UK general election":
                electionname = "United Kingdom general election, January 1910"
            electionname = re.sub("(Notional 1992 UK General Election Result) : .*", "\\1", electionname)
                
            yield { "type":"election", "name":electionname }

        elif re.match("Election box candidate", templ[0]):
            data = { "type":"candidate", "constituency":title, "election":electionname }
            # get rid of punctuation and references that sometimes gets added to the end
            svotes = re.sub(" \(\?\)$|<br[^\d]*$|<ref[^\d]*$|[,. ]", "", templ["votes"])  
            
            if re.match("\d+$", svotes):
                votes = int(svotes)
            elif svotes in ["Unopposed", "Unoppose", "unopposed", "Elected", "Co-opted", "''N/A''", 
                            "'''unopposed'''", "''unopposed''", "(unopposed)", "''(unopposed)''", 
                            "''uncontested''", 
                            "Returned", "Returnedandseated", "Returnedandunseated", "Unknown"]:
                votes = 1
            elif svotes == "" or svotes == "-":
                votes = None
            elif svotes == "Defeated":
                votes = 0
            else:
                print ("Unparsed votes: " + str(templ) + str([svotes]))
                assert False
                
            if votes != None:
                data["votes"] = votes                
                
            party = re.match("(.*?)\s*(\[?http://.*|{{|<!.*|<ref.*|<sup.*)?$", templ["party"]).group(1)
            mpartycat = re.match("(.*?)\[\[(.+?)[\|\]]", party)
            if mpartycat:
                party = mpartycat.group(1) + mpartycat.group(2)
            party = re.sub(u"\u2013", "-", party)
            party = re.sub(u"\u2019", "-", party)
            assert not re.search("\[|<", party), list(templ["party"])
            data["party"] = party
            
            
            # clean up the candidate field so it contains no stray reference links
            candidate = templ["candidate"]
            mcandidatet = re.match("(?s)(.*?)\s*(<!.*|<ref.*|\[http://.*|\(Ruair.*?\)|\*+|\+|\,|<sup>\d</sup>|<nowiki>\*</nowiki>)$", candidate)
            if mcandidatet:
                candidate = mcandidatet.group(1)
    
            mcandidatet = re.match("(?s)['\"]*(?:Sir |Rt.? |Right |Hon\.? |Rev\.? |Prof\.? |Miss |Mrs\.? |Ms |Maj\.-Gen\. |Lt\.-Col\. |Lt\.-Cmdr\. |Lt-Gen |Maj\.? |Lt |Com |Col |Major |Major-General |Dr\.? |Brig |Gen |Gp |Capt\.? |Count |Captain |Commodore |Admiral |Lord |Lieutenant-Colonel |Commander |[WR]\. |Lieut Col |Lt-Col |Dame |Comm )*(.*?)(?:,? Bt\.?| CMG| KC| RN| [OKMCG]BE| MC| DSO| DFC| TD| KCB| CB| VRD| QC| MB| CSI| CIE| KCMG| GCB| LLD| MD| PhD| GCVO| \[\[Military Cross\|MC\]\]|, \[\[Royal Naval Volunteer Reserve\|RNVR\]\]|{{mnl}}| <sup>1</sup>\s*| \(PPC\)| \(incumbent\))*[\s'\"]*$", candidate)
            if mcandidatet:
                candidate = mcandidatet.group(1)

            # remove the target link in the pattern [[xxx|xxx]]
            mcandidate = re.match("(\[\[[^\]\|]+?)(?:\|[\s\S]+?)?\]\]$", candidate)
            if mcandidate:
                candidate = mcandidate.group(1) + "]]"
            candidate = re.sub(u"\u2019", "'", candidate)
            
            # error in http://en.wikipedia.org/wiki/North_Antrim_(UK_Parliament_constituency)#Elections_in_the_1880s
            if candidate == "[William Pirrie Sinclair":
                candidate = "William Pirrie Sinclair"
            if candidate == "[[John_Hemming_%28politician%29]]":
                candidate = "[[John_Hemming_(politician)]]"
            if candidate == "[[Nikolai Tolstoy]]-Miloslavsky":
                candidate = "[[Nikolai Tolstoy]]"
            if candidate[-27:] == u' ([[SDP\u2013Liberal Alliance]])':
                candidate = candidate[:-27]
            if candidate == u'Donald MacLaren of [[Clan MacLaren|MacLaren]]':
                candidate = u'Donald MacLaren'

            
            data["candidate"] = candidate
            
            
            # there are problems with the ndash in these names where inserting one in this python code causes 
            # an exception and a 0 length file to be saved
            if candidate.startswith("[[Richard Bethell (17"):
                assert title == "Yorkshire (UK Parliament constituency)", templ
            if candidate.startswith("[[Rowland Burdon (18"):
                assert title == "Sedgefield (UK Parliament constituency)", templ
            elif candidate.startswith("[[George Byng"):
                assert title == "Middlesex (UK Parliament constituency)"
            elif candidate == "[[Oliver Baldwin]], [[Viscount Corvedale]]":
                pass
            
            elif candidate and candidate != "[to be confirmed]":
                assert re.match("(\[\[)?[\w\s,.#_\-'\"/\(\)\x80-\xe2\xe9\xed\xfc\xf4]+(\]\])?$", candidate), [candidate, templ, electionname]
            elif candidate == "" and party != "Others":
                assert title in ["Aberavon (UK Parliament constituency)", 
                                 "Wycombe (UK Parliament constituency)", 
                                 "Gower (UK Parliament constituency)", 
                                 "Kettering (UK Parliament constituency)", 
                                 "Manchester Gorton (UK Parliament constituency)", 
                                 "Islington North (UK Parliament constituency)", 
                                 "Hornsey and Wood Green (UK Parliament constituency)", 
                                 "Finchley and Golders Green (UK Parliament constituency)", 
                                 "Epping Forest (UK Parliament constituency)", 
                                 "Bury St Edmunds (UK Parliament constituency)", 
                                 "Harlow (UK Parliament constituency)",
                                 "Bristol East (UK Parliament constituency)",
                                 "Beaconsfield (UK Parliament constituency)",
                                 "Battersea (UK Parliament constituency)",
                                 "Ashton-under-Lyne (UK Parliament constituency)",
                                ], data
                candidate = "unknown"

            else:
                assert party == "Others" or \
                       party == "others" or \
                       party == "non transferable" or \
                       title in ["Croydon North West (UK Parliament constituency)", 
                                 "South Colchester and Maldon (UK Parliament constituency)", 
                                 "Battersea (UK Parliament constituency)", 
                                 "Kettering (UK Parliament constituency)", 
                                 "Harlow (UK Parliament constituency)", 
                                 "Epping Forest (UK Parliament constituency)", 
                                 "North Essex (UK Parliament constituency)", 
                                 "South East Cambridgeshire (UK Parliament constituency)", 
                                 "Rochford and Southend East (UK Parliament constituency)", 
                                 "Finchley and Golders Green (UK Parliament constituency)", 
                                 "Bristol East (UK Parliament constituency)", 
                                 "Glasgow Cathcart (UK Parliament constituency)"] or \
                electionname == "next United Kingdom general election", \
                           [str(templ), electionname, title]
            
            yield data
            
        elif templ[0] == "Election box end":
            electionname = None


        
def ParseTemplates(text):   # pretty obfuscated, isn't it?
    templstack = [ ]
    for tt in re.split("(\{\{\{|\}\}\}|\{\{|\}\}|\[\[|\]\]|\|)", text):
        if tt in ["{{{", "{{", "[["]:
            templstack.append([tt, [ [ ] ] ])
        elif templstack and tt in ["}}}", "}}", "]]"]:
            templstack[-1][1][-1] = "".join(templstack[-1][1][-1])
            templstack[-1].append(tt)
            if len(templstack) == 1:
                if templstack[-1][0] == "{{":
                    res = { }
                    for i, param in enumerate(templstack[-1][1]):
                        k, e, v = re.match("(?s)([^=]*)(=?)(.*)$", param).groups()
                        if e:
                            res[k.strip()] = v.strip()
                        else:
                            res[i] = k.strip()
                    yield res
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


            
Main()
import scraperwiki
import lxml.etree
import urllib, re, csv

# Work to do: chase down any wikilinks for candidates and follow redirects

# also a 16 constituencies have a nonstandard tabular layout.  seen by
# scraperwiki.sqlite.attach("wikipedia-list-of-constituencies", "s1")
# scraperwiki.sqlite.attach("wikipedia-parliamentary-candidates", "s2")
# print scraperwiki.sqlite.select("wptitle from s1.swdata left join s2.swdata on constituency=wptitle where constituency is null")


qs = "select wptitle, content from constsrc.swdata order by rowid desc limit 1 offset ?"

def Main():
    scraperwiki.sqlite.attach("wikipedia-list-of-constituencies", "constsrc")
    for i in range(0, 7000):
        tdata = scraperwiki.sqlite.execute(qs, i)
        if len(tdata["data"]) == 0:
            break
        cc = tdata["data"][0]
        print i, cc[0]
        text = cc[1]
        templs = ParseTemplates(text)
        ldata = [ ]
        for data in CollateElections(cc[0], templs):
            if data["type"] == "candidate":
                ldata.append(data)
        scraperwiki.sqlite.save(["constituency", "election", "candidate", "party"], ldata)


def CollateElections(title, templs):
    for templ in templs:
        if templ[0] == "Election box begin" or templ[0] == "Election box begin no clear":
            melectionname = re.search("\[\[(.*?)[\|\]]", templ["title"])
            electionname = melectionname and melectionname.group(1) or templ["title"]
            electionname = re.match("(.*?)\s*(\{\{.*|http://.*)?$", electionname).group(1)
            if electionname.startswith("UK "):
                electionname = "United Kingdom " + electionname[3:]
            electionname = re.sub("(United Kingdom general election) (\d\d\d\d)", "\\1, \\2", electionname)
            electionname = re.sub("(United Kingdom general election) (\d\d\d\d)", "\\1, \\2", electionname)
            if electionname == "January 1910 UK general election":
                electionname = "United Kingdom general election, January 1910"
            electionname = re.sub("(Notional 1992 UK General Election Result) : .*", "\\1", electionname)
                
            yield { "type":"election", "name":electionname }

        elif re.match("Election box candidate", templ[0]):
            data = { "type":"candidate", "constituency":title, "election":electionname }
            # get rid of punctuation and references that sometimes gets added to the end
            svotes = re.sub(" \(\?\)$|<br[^\d]*$|<ref[^\d]*$|[,. ]", "", templ["votes"])  
            
            if re.match("\d+$", svotes):
                votes = int(svotes)
            elif svotes in ["Unopposed", "Unoppose", "unopposed", "Elected", "Co-opted", "''N/A''", 
                            "'''unopposed'''", "''unopposed''", "(unopposed)", "''(unopposed)''", 
                            "''uncontested''", 
                            "Returned", "Returnedandseated", "Returnedandunseated", "Unknown"]:
                votes = 1
            elif svotes == "" or svotes == "-":
                votes = None
            elif svotes == "Defeated":
                votes = 0
            else:
                print ("Unparsed votes: " + str(templ) + str([svotes]))
                assert False
                
            if votes != None:
                data["votes"] = votes                
                
            party = re.match("(.*?)\s*(\[?http://.*|{{|<!.*|<ref.*|<sup.*)?$", templ["party"]).group(1)
            mpartycat = re.match("(.*?)\[\[(.+?)[\|\]]", party)
            if mpartycat:
                party = mpartycat.group(1) + mpartycat.group(2)
            party = re.sub(u"\u2013", "-", party)
            party = re.sub(u"\u2019", "-", party)
            assert not re.search("\[|<", party), list(templ["party"])
            data["party"] = party
            
            
            # clean up the candidate field so it contains no stray reference links
            candidate = templ["candidate"]
            mcandidatet = re.match("(?s)(.*?)\s*(<!.*|<ref.*|\[http://.*|\(Ruair.*?\)|\*+|\+|\,|<sup>\d</sup>|<nowiki>\*</nowiki>)$", candidate)
            if mcandidatet:
                candidate = mcandidatet.group(1)
    
            mcandidatet = re.match("(?s)['\"]*(?:Sir |Rt.? |Right |Hon\.? |Rev\.? |Prof\.? |Miss |Mrs\.? |Ms |Maj\.-Gen\. |Lt\.-Col\. |Lt\.-Cmdr\. |Lt-Gen |Maj\.? |Lt |Com |Col |Major |Major-General |Dr\.? |Brig |Gen |Gp |Capt\.? |Count |Captain |Commodore |Admiral |Lord |Lieutenant-Colonel |Commander |[WR]\. |Lieut Col |Lt-Col |Dame |Comm )*(.*?)(?:,? Bt\.?| CMG| KC| RN| [OKMCG]BE| MC| DSO| DFC| TD| KCB| CB| VRD| QC| MB| CSI| CIE| KCMG| GCB| LLD| MD| PhD| GCVO| \[\[Military Cross\|MC\]\]|, \[\[Royal Naval Volunteer Reserve\|RNVR\]\]|{{mnl}}| <sup>1</sup>\s*| \(PPC\)| \(incumbent\))*[\s'\"]*$", candidate)
            if mcandidatet:
                candidate = mcandidatet.group(1)

            # remove the target link in the pattern [[xxx|xxx]]
            mcandidate = re.match("(\[\[[^\]\|]+?)(?:\|[\s\S]+?)?\]\]$", candidate)
            if mcandidate:
                candidate = mcandidate.group(1) + "]]"
            candidate = re.sub(u"\u2019", "'", candidate)
            
            # error in http://en.wikipedia.org/wiki/North_Antrim_(UK_Parliament_constituency)#Elections_in_the_1880s
            if candidate == "[William Pirrie Sinclair":
                candidate = "William Pirrie Sinclair"
            if candidate == "[[John_Hemming_%28politician%29]]":
                candidate = "[[John_Hemming_(politician)]]"
            if candidate == "[[Nikolai Tolstoy]]-Miloslavsky":
                candidate = "[[Nikolai Tolstoy]]"
            if candidate[-27:] == u' ([[SDP\u2013Liberal Alliance]])':
                candidate = candidate[:-27]
            if candidate == u'Donald MacLaren of [[Clan MacLaren|MacLaren]]':
                candidate = u'Donald MacLaren'

            
            data["candidate"] = candidate
            
            
            # there are problems with the ndash in these names where inserting one in this python code causes 
            # an exception and a 0 length file to be saved
            if candidate.startswith("[[Richard Bethell (17"):
                assert title == "Yorkshire (UK Parliament constituency)", templ
            if candidate.startswith("[[Rowland Burdon (18"):
                assert title == "Sedgefield (UK Parliament constituency)", templ
            elif candidate.startswith("[[George Byng"):
                assert title == "Middlesex (UK Parliament constituency)"
            elif candidate == "[[Oliver Baldwin]], [[Viscount Corvedale]]":
                pass
            
            elif candidate and candidate != "[to be confirmed]":
                assert re.match("(\[\[)?[\w\s,.#_\-'\"/\(\)\x80-\xe2\xe9\xed\xfc\xf4]+(\]\])?$", candidate), [candidate, templ, electionname]
            elif candidate == "" and party != "Others":
                assert title in ["Aberavon (UK Parliament constituency)", 
                                 "Wycombe (UK Parliament constituency)", 
                                 "Gower (UK Parliament constituency)", 
                                 "Kettering (UK Parliament constituency)", 
                                 "Manchester Gorton (UK Parliament constituency)", 
                                 "Islington North (UK Parliament constituency)", 
                                 "Hornsey and Wood Green (UK Parliament constituency)", 
                                 "Finchley and Golders Green (UK Parliament constituency)", 
                                 "Epping Forest (UK Parliament constituency)", 
                                 "Bury St Edmunds (UK Parliament constituency)", 
                                 "Harlow (UK Parliament constituency)",
                                 "Bristol East (UK Parliament constituency)",
                                 "Beaconsfield (UK Parliament constituency)",
                                 "Battersea (UK Parliament constituency)",
                                 "Ashton-under-Lyne (UK Parliament constituency)",
                                ], data
                candidate = "unknown"

            else:
                assert party == "Others" or \
                       party == "others" or \
                       party == "non transferable" or \
                       title in ["Croydon North West (UK Parliament constituency)", 
                                 "South Colchester and Maldon (UK Parliament constituency)", 
                                 "Battersea (UK Parliament constituency)", 
                                 "Kettering (UK Parliament constituency)", 
                                 "Harlow (UK Parliament constituency)", 
                                 "Epping Forest (UK Parliament constituency)", 
                                 "North Essex (UK Parliament constituency)", 
                                 "South East Cambridgeshire (UK Parliament constituency)", 
                                 "Rochford and Southend East (UK Parliament constituency)", 
                                 "Finchley and Golders Green (UK Parliament constituency)", 
                                 "Bristol East (UK Parliament constituency)", 
                                 "Glasgow Cathcart (UK Parliament constituency)"] or \
                electionname == "next United Kingdom general election", \
                           [str(templ), electionname, title]
            
            yield data
            
        elif templ[0] == "Election box end":
            electionname = None


        
def ParseTemplates(text):   # pretty obfuscated, isn't it?
    templstack = [ ]
    for tt in re.split("(\{\{\{|\}\}\}|\{\{|\}\}|\[\[|\]\]|\|)", text):
        if tt in ["{{{", "{{", "[["]:
            templstack.append([tt, [ [ ] ] ])
        elif templstack and tt in ["}}}", "}}", "]]"]:
            templstack[-1][1][-1] = "".join(templstack[-1][1][-1])
            templstack[-1].append(tt)
            if len(templstack) == 1:
                if templstack[-1][0] == "{{":
                    res = { }
                    for i, param in enumerate(templstack[-1][1]):
                        k, e, v = re.match("(?s)([^=]*)(=?)(.*)$", param).groups()
                        if e:
                            res[k.strip()] = v.strip()
                        else:
                            res[i] = k.strip()
                    yield res
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


            
Main()
import scraperwiki
import lxml.etree
import urllib, re, csv

# Work to do: chase down any wikilinks for candidates and follow redirects

# also a 16 constituencies have a nonstandard tabular layout.  seen by
# scraperwiki.sqlite.attach("wikipedia-list-of-constituencies", "s1")
# scraperwiki.sqlite.attach("wikipedia-parliamentary-candidates", "s2")
# print scraperwiki.sqlite.select("wptitle from s1.swdata left join s2.swdata on constituency=wptitle where constituency is null")


qs = "select wptitle, content from constsrc.swdata order by rowid desc limit 1 offset ?"

def Main():
    scraperwiki.sqlite.attach("wikipedia-list-of-constituencies", "constsrc")
    for i in range(0, 7000):
        tdata = scraperwiki.sqlite.execute(qs, i)
        if len(tdata["data"]) == 0:
            break
        cc = tdata["data"][0]
        print i, cc[0]
        text = cc[1]
        templs = ParseTemplates(text)
        ldata = [ ]
        for data in CollateElections(cc[0], templs):
            if data["type"] == "candidate":
                ldata.append(data)
        scraperwiki.sqlite.save(["constituency", "election", "candidate", "party"], ldata)


def CollateElections(title, templs):
    for templ in templs:
        if templ[0] == "Election box begin" or templ[0] == "Election box begin no clear":
            melectionname = re.search("\[\[(.*?)[\|\]]", templ["title"])
            electionname = melectionname and melectionname.group(1) or templ["title"]
            electionname = re.match("(.*?)\s*(\{\{.*|http://.*)?$", electionname).group(1)
            if electionname.startswith("UK "):
                electionname = "United Kingdom " + electionname[3:]
            electionname = re.sub("(United Kingdom general election) (\d\d\d\d)", "\\1, \\2", electionname)
            electionname = re.sub("(United Kingdom general election) (\d\d\d\d)", "\\1, \\2", electionname)
            if electionname == "January 1910 UK general election":
                electionname = "United Kingdom general election, January 1910"
            electionname = re.sub("(Notional 1992 UK General Election Result) : .*", "\\1", electionname)
                
            yield { "type":"election", "name":electionname }

        elif re.match("Election box candidate", templ[0]):
            data = { "type":"candidate", "constituency":title, "election":electionname }
            # get rid of punctuation and references that sometimes gets added to the end
            svotes = re.sub(" \(\?\)$|<br[^\d]*$|<ref[^\d]*$|[,. ]", "", templ["votes"])  
            
            if re.match("\d+$", svotes):
                votes = int(svotes)
            elif svotes in ["Unopposed", "Unoppose", "unopposed", "Elected", "Co-opted", "''N/A''", 
                            "'''unopposed'''", "''unopposed''", "(unopposed)", "''(unopposed)''", 
                            "''uncontested''", 
                            "Returned", "Returnedandseated", "Returnedandunseated", "Unknown"]:
                votes = 1
            elif svotes == "" or svotes == "-":
                votes = None
            elif svotes == "Defeated":
                votes = 0
            else:
                print ("Unparsed votes: " + str(templ) + str([svotes]))
                assert False
                
            if votes != None:
                data["votes"] = votes                
                
            party = re.match("(.*?)\s*(\[?http://.*|{{|<!.*|<ref.*|<sup.*)?$", templ["party"]).group(1)
            mpartycat = re.match("(.*?)\[\[(.+?)[\|\]]", party)
            if mpartycat:
                party = mpartycat.group(1) + mpartycat.group(2)
            party = re.sub(u"\u2013", "-", party)
            party = re.sub(u"\u2019", "-", party)
            assert not re.search("\[|<", party), list(templ["party"])
            data["party"] = party
            
            
            # clean up the candidate field so it contains no stray reference links
            candidate = templ["candidate"]
            mcandidatet = re.match("(?s)(.*?)\s*(<!.*|<ref.*|\[http://.*|\(Ruair.*?\)|\*+|\+|\,|<sup>\d</sup>|<nowiki>\*</nowiki>)$", candidate)
            if mcandidatet:
                candidate = mcandidatet.group(1)
    
            mcandidatet = re.match("(?s)['\"]*(?:Sir |Rt.? |Right |Hon\.? |Rev\.? |Prof\.? |Miss |Mrs\.? |Ms |Maj\.-Gen\. |Lt\.-Col\. |Lt\.-Cmdr\. |Lt-Gen |Maj\.? |Lt |Com |Col |Major |Major-General |Dr\.? |Brig |Gen |Gp |Capt\.? |Count |Captain |Commodore |Admiral |Lord |Lieutenant-Colonel |Commander |[WR]\. |Lieut Col |Lt-Col |Dame |Comm )*(.*?)(?:,? Bt\.?| CMG| KC| RN| [OKMCG]BE| MC| DSO| DFC| TD| KCB| CB| VRD| QC| MB| CSI| CIE| KCMG| GCB| LLD| MD| PhD| GCVO| \[\[Military Cross\|MC\]\]|, \[\[Royal Naval Volunteer Reserve\|RNVR\]\]|{{mnl}}| <sup>1</sup>\s*| \(PPC\)| \(incumbent\))*[\s'\"]*$", candidate)
            if mcandidatet:
                candidate = mcandidatet.group(1)

            # remove the target link in the pattern [[xxx|xxx]]
            mcandidate = re.match("(\[\[[^\]\|]+?)(?:\|[\s\S]+?)?\]\]$", candidate)
            if mcandidate:
                candidate = mcandidate.group(1) + "]]"
            candidate = re.sub(u"\u2019", "'", candidate)
            
            # error in http://en.wikipedia.org/wiki/North_Antrim_(UK_Parliament_constituency)#Elections_in_the_1880s
            if candidate == "[William Pirrie Sinclair":
                candidate = "William Pirrie Sinclair"
            if candidate == "[[John_Hemming_%28politician%29]]":
                candidate = "[[John_Hemming_(politician)]]"
            if candidate == "[[Nikolai Tolstoy]]-Miloslavsky":
                candidate = "[[Nikolai Tolstoy]]"
            if candidate[-27:] == u' ([[SDP\u2013Liberal Alliance]])':
                candidate = candidate[:-27]
            if candidate == u'Donald MacLaren of [[Clan MacLaren|MacLaren]]':
                candidate = u'Donald MacLaren'

            
            data["candidate"] = candidate
            
            
            # there are problems with the ndash in these names where inserting one in this python code causes 
            # an exception and a 0 length file to be saved
            if candidate.startswith("[[Richard Bethell (17"):
                assert title == "Yorkshire (UK Parliament constituency)", templ
            if candidate.startswith("[[Rowland Burdon (18"):
                assert title == "Sedgefield (UK Parliament constituency)", templ
            elif candidate.startswith("[[George Byng"):
                assert title == "Middlesex (UK Parliament constituency)"
            elif candidate == "[[Oliver Baldwin]], [[Viscount Corvedale]]":
                pass
            
            elif candidate and candidate != "[to be confirmed]":
                assert re.match("(\[\[)?[\w\s,.#_\-'\"/\(\)\x80-\xe2\xe9\xed\xfc\xf4]+(\]\])?$", candidate), [candidate, templ, electionname]
            elif candidate == "" and party != "Others":
                assert title in ["Aberavon (UK Parliament constituency)", 
                                 "Wycombe (UK Parliament constituency)", 
                                 "Gower (UK Parliament constituency)", 
                                 "Kettering (UK Parliament constituency)", 
                                 "Manchester Gorton (UK Parliament constituency)", 
                                 "Islington North (UK Parliament constituency)", 
                                 "Hornsey and Wood Green (UK Parliament constituency)", 
                                 "Finchley and Golders Green (UK Parliament constituency)", 
                                 "Epping Forest (UK Parliament constituency)", 
                                 "Bury St Edmunds (UK Parliament constituency)", 
                                 "Harlow (UK Parliament constituency)",
                                 "Bristol East (UK Parliament constituency)",
                                 "Beaconsfield (UK Parliament constituency)",
                                 "Battersea (UK Parliament constituency)",
                                 "Ashton-under-Lyne (UK Parliament constituency)",
                                ], data
                candidate = "unknown"

            else:
                assert party == "Others" or \
                       party == "others" or \
                       party == "non transferable" or \
                       title in ["Croydon North West (UK Parliament constituency)", 
                                 "South Colchester and Maldon (UK Parliament constituency)", 
                                 "Battersea (UK Parliament constituency)", 
                                 "Kettering (UK Parliament constituency)", 
                                 "Harlow (UK Parliament constituency)", 
                                 "Epping Forest (UK Parliament constituency)", 
                                 "North Essex (UK Parliament constituency)", 
                                 "South East Cambridgeshire (UK Parliament constituency)", 
                                 "Rochford and Southend East (UK Parliament constituency)", 
                                 "Finchley and Golders Green (UK Parliament constituency)", 
                                 "Bristol East (UK Parliament constituency)", 
                                 "Glasgow Cathcart (UK Parliament constituency)"] or \
                electionname == "next United Kingdom general election", \
                           [str(templ), electionname, title]
            
            yield data
            
        elif templ[0] == "Election box end":
            electionname = None


        
def ParseTemplates(text):   # pretty obfuscated, isn't it?
    templstack = [ ]
    for tt in re.split("(\{\{\{|\}\}\}|\{\{|\}\}|\[\[|\]\]|\|)", text):
        if tt in ["{{{", "{{", "[["]:
            templstack.append([tt, [ [ ] ] ])
        elif templstack and tt in ["}}}", "}}", "]]"]:
            templstack[-1][1][-1] = "".join(templstack[-1][1][-1])
            templstack[-1].append(tt)
            if len(templstack) == 1:
                if templstack[-1][0] == "{{":
                    res = { }
                    for i, param in enumerate(templstack[-1][1]):
                        k, e, v = re.match("(?s)([^=]*)(=?)(.*)$", param).groups()
                        if e:
                            res[k.strip()] = v.strip()
                        else:
                            res[i] = k.strip()
                    yield res
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


            
Main()
import scraperwiki
import lxml.etree
import urllib, re, csv

# Work to do: chase down any wikilinks for candidates and follow redirects

# also a 16 constituencies have a nonstandard tabular layout.  seen by
# scraperwiki.sqlite.attach("wikipedia-list-of-constituencies", "s1")
# scraperwiki.sqlite.attach("wikipedia-parliamentary-candidates", "s2")
# print scraperwiki.sqlite.select("wptitle from s1.swdata left join s2.swdata on constituency=wptitle where constituency is null")


qs = "select wptitle, content from constsrc.swdata order by rowid desc limit 1 offset ?"

def Main():
    scraperwiki.sqlite.attach("wikipedia-list-of-constituencies", "constsrc")
    for i in range(0, 7000):
        tdata = scraperwiki.sqlite.execute(qs, i)
        if len(tdata["data"]) == 0:
            break
        cc = tdata["data"][0]
        print i, cc[0]
        text = cc[1]
        templs = ParseTemplates(text)
        ldata = [ ]
        for data in CollateElections(cc[0], templs):
            if data["type"] == "candidate":
                ldata.append(data)
        scraperwiki.sqlite.save(["constituency", "election", "candidate", "party"], ldata)


def CollateElections(title, templs):
    for templ in templs:
        if templ[0] == "Election box begin" or templ[0] == "Election box begin no clear":
            melectionname = re.search("\[\[(.*?)[\|\]]", templ["title"])
            electionname = melectionname and melectionname.group(1) or templ["title"]
            electionname = re.match("(.*?)\s*(\{\{.*|http://.*)?$", electionname).group(1)
            if electionname.startswith("UK "):
                electionname = "United Kingdom " + electionname[3:]
            electionname = re.sub("(United Kingdom general election) (\d\d\d\d)", "\\1, \\2", electionname)
            electionname = re.sub("(United Kingdom general election) (\d\d\d\d)", "\\1, \\2", electionname)
            if electionname == "January 1910 UK general election":
                electionname = "United Kingdom general election, January 1910"
            electionname = re.sub("(Notional 1992 UK General Election Result) : .*", "\\1", electionname)
                
            yield { "type":"election", "name":electionname }

        elif re.match("Election box candidate", templ[0]):
            data = { "type":"candidate", "constituency":title, "election":electionname }
            # get rid of punctuation and references that sometimes gets added to the end
            svotes = re.sub(" \(\?\)$|<br[^\d]*$|<ref[^\d]*$|[,. ]", "", templ["votes"])  
            
            if re.match("\d+$", svotes):
                votes = int(svotes)
            elif svotes in ["Unopposed", "Unoppose", "unopposed", "Elected", "Co-opted", "''N/A''", 
                            "'''unopposed'''", "''unopposed''", "(unopposed)", "''(unopposed)''", 
                            "''uncontested''", 
                            "Returned", "Returnedandseated", "Returnedandunseated", "Unknown"]:
                votes = 1
            elif svotes == "" or svotes == "-":
                votes = None
            elif svotes == "Defeated":
                votes = 0
            else:
                print ("Unparsed votes: " + str(templ) + str([svotes]))
                assert False
                
            if votes != None:
                data["votes"] = votes                
                
            party = re.match("(.*?)\s*(\[?http://.*|{{|<!.*|<ref.*|<sup.*)?$", templ["party"]).group(1)
            mpartycat = re.match("(.*?)\[\[(.+?)[\|\]]", party)
            if mpartycat:
                party = mpartycat.group(1) + mpartycat.group(2)
            party = re.sub(u"\u2013", "-", party)
            party = re.sub(u"\u2019", "-", party)
            assert not re.search("\[|<", party), list(templ["party"])
            data["party"] = party
            
            
            # clean up the candidate field so it contains no stray reference links
            candidate = templ["candidate"]
            mcandidatet = re.match("(?s)(.*?)\s*(<!.*|<ref.*|\[http://.*|\(Ruair.*?\)|\*+|\+|\,|<sup>\d</sup>|<nowiki>\*</nowiki>)$", candidate)
            if mcandidatet:
                candidate = mcandidatet.group(1)
    
            mcandidatet = re.match("(?s)['\"]*(?:Sir |Rt.? |Right |Hon\.? |Rev\.? |Prof\.? |Miss |Mrs\.? |Ms |Maj\.-Gen\. |Lt\.-Col\. |Lt\.-Cmdr\. |Lt-Gen |Maj\.? |Lt |Com |Col |Major |Major-General |Dr\.? |Brig |Gen |Gp |Capt\.? |Count |Captain |Commodore |Admiral |Lord |Lieutenant-Colonel |Commander |[WR]\. |Lieut Col |Lt-Col |Dame |Comm )*(.*?)(?:,? Bt\.?| CMG| KC| RN| [OKMCG]BE| MC| DSO| DFC| TD| KCB| CB| VRD| QC| MB| CSI| CIE| KCMG| GCB| LLD| MD| PhD| GCVO| \[\[Military Cross\|MC\]\]|, \[\[Royal Naval Volunteer Reserve\|RNVR\]\]|{{mnl}}| <sup>1</sup>\s*| \(PPC\)| \(incumbent\))*[\s'\"]*$", candidate)
            if mcandidatet:
                candidate = mcandidatet.group(1)

            # remove the target link in the pattern [[xxx|xxx]]
            mcandidate = re.match("(\[\[[^\]\|]+?)(?:\|[\s\S]+?)?\]\]$", candidate)
            if mcandidate:
                candidate = mcandidate.group(1) + "]]"
            candidate = re.sub(u"\u2019", "'", candidate)
            
            # error in http://en.wikipedia.org/wiki/North_Antrim_(UK_Parliament_constituency)#Elections_in_the_1880s
            if candidate == "[William Pirrie Sinclair":
                candidate = "William Pirrie Sinclair"
            if candidate == "[[John_Hemming_%28politician%29]]":
                candidate = "[[John_Hemming_(politician)]]"
            if candidate == "[[Nikolai Tolstoy]]-Miloslavsky":
                candidate = "[[Nikolai Tolstoy]]"
            if candidate[-27:] == u' ([[SDP\u2013Liberal Alliance]])':
                candidate = candidate[:-27]
            if candidate == u'Donald MacLaren of [[Clan MacLaren|MacLaren]]':
                candidate = u'Donald MacLaren'

            
            data["candidate"] = candidate
            
            
            # there are problems with the ndash in these names where inserting one in this python code causes 
            # an exception and a 0 length file to be saved
            if candidate.startswith("[[Richard Bethell (17"):
                assert title == "Yorkshire (UK Parliament constituency)", templ
            if candidate.startswith("[[Rowland Burdon (18"):
                assert title == "Sedgefield (UK Parliament constituency)", templ
            elif candidate.startswith("[[George Byng"):
                assert title == "Middlesex (UK Parliament constituency)"
            elif candidate == "[[Oliver Baldwin]], [[Viscount Corvedale]]":
                pass
            
            elif candidate and candidate != "[to be confirmed]":
                assert re.match("(\[\[)?[\w\s,.#_\-'\"/\(\)\x80-\xe2\xe9\xed\xfc\xf4]+(\]\])?$", candidate), [candidate, templ, electionname]
            elif candidate == "" and party != "Others":
                assert title in ["Aberavon (UK Parliament constituency)", 
                                 "Wycombe (UK Parliament constituency)", 
                                 "Gower (UK Parliament constituency)", 
                                 "Kettering (UK Parliament constituency)", 
                                 "Manchester Gorton (UK Parliament constituency)", 
                                 "Islington North (UK Parliament constituency)", 
                                 "Hornsey and Wood Green (UK Parliament constituency)", 
                                 "Finchley and Golders Green (UK Parliament constituency)", 
                                 "Epping Forest (UK Parliament constituency)", 
                                 "Bury St Edmunds (UK Parliament constituency)", 
                                 "Harlow (UK Parliament constituency)",
                                 "Bristol East (UK Parliament constituency)",
                                 "Beaconsfield (UK Parliament constituency)",
                                 "Battersea (UK Parliament constituency)",
                                 "Ashton-under-Lyne (UK Parliament constituency)",
                                ], data
                candidate = "unknown"

            else:
                assert party == "Others" or \
                       party == "others" or \
                       party == "non transferable" or \
                       title in ["Croydon North West (UK Parliament constituency)", 
                                 "South Colchester and Maldon (UK Parliament constituency)", 
                                 "Battersea (UK Parliament constituency)", 
                                 "Kettering (UK Parliament constituency)", 
                                 "Harlow (UK Parliament constituency)", 
                                 "Epping Forest (UK Parliament constituency)", 
                                 "North Essex (UK Parliament constituency)", 
                                 "South East Cambridgeshire (UK Parliament constituency)", 
                                 "Rochford and Southend East (UK Parliament constituency)", 
                                 "Finchley and Golders Green (UK Parliament constituency)", 
                                 "Bristol East (UK Parliament constituency)", 
                                 "Glasgow Cathcart (UK Parliament constituency)"] or \
                electionname == "next United Kingdom general election", \
                           [str(templ), electionname, title]
            
            yield data
            
        elif templ[0] == "Election box end":
            electionname = None


        
def ParseTemplates(text):   # pretty obfuscated, isn't it?
    templstack = [ ]
    for tt in re.split("(\{\{\{|\}\}\}|\{\{|\}\}|\[\[|\]\]|\|)", text):
        if tt in ["{{{", "{{", "[["]:
            templstack.append([tt, [ [ ] ] ])
        elif templstack and tt in ["}}}", "}}", "]]"]:
            templstack[-1][1][-1] = "".join(templstack[-1][1][-1])
            templstack[-1].append(tt)
            if len(templstack) == 1:
                if templstack[-1][0] == "{{":
                    res = { }
                    for i, param in enumerate(templstack[-1][1]):
                        k, e, v = re.match("(?s)([^=]*)(=?)(.*)$", param).groups()
                        if e:
                            res[k.strip()] = v.strip()
                        else:
                            res[i] = k.strip()
                    yield res
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


            
Main()
import scraperwiki
import lxml.etree
import urllib, re, csv

# Work to do: chase down any wikilinks for candidates and follow redirects

# also a 16 constituencies have a nonstandard tabular layout.  seen by
# scraperwiki.sqlite.attach("wikipedia-list-of-constituencies", "s1")
# scraperwiki.sqlite.attach("wikipedia-parliamentary-candidates", "s2")
# print scraperwiki.sqlite.select("wptitle from s1.swdata left join s2.swdata on constituency=wptitle where constituency is null")


qs = "select wptitle, content from constsrc.swdata order by rowid desc limit 1 offset ?"

def Main():
    scraperwiki.sqlite.attach("wikipedia-list-of-constituencies", "constsrc")
    for i in range(0, 7000):
        tdata = scraperwiki.sqlite.execute(qs, i)
        if len(tdata["data"]) == 0:
            break
        cc = tdata["data"][0]
        print i, cc[0]
        text = cc[1]
        templs = ParseTemplates(text)
        ldata = [ ]
        for data in CollateElections(cc[0], templs):
            if data["type"] == "candidate":
                ldata.append(data)
        scraperwiki.sqlite.save(["constituency", "election", "candidate", "party"], ldata)


def CollateElections(title, templs):
    for templ in templs:
        if templ[0] == "Election box begin" or templ[0] == "Election box begin no clear":
            melectionname = re.search("\[\[(.*?)[\|\]]", templ["title"])
            electionname = melectionname and melectionname.group(1) or templ["title"]
            electionname = re.match("(.*?)\s*(\{\{.*|http://.*)?$", electionname).group(1)
            if electionname.startswith("UK "):
                electionname = "United Kingdom " + electionname[3:]
            electionname = re.sub("(United Kingdom general election) (\d\d\d\d)", "\\1, \\2", electionname)
            electionname = re.sub("(United Kingdom general election) (\d\d\d\d)", "\\1, \\2", electionname)
            if electionname == "January 1910 UK general election":
                electionname = "United Kingdom general election, January 1910"
            electionname = re.sub("(Notional 1992 UK General Election Result) : .*", "\\1", electionname)
                
            yield { "type":"election", "name":electionname }

        elif re.match("Election box candidate", templ[0]):
            data = { "type":"candidate", "constituency":title, "election":electionname }
            # get rid of punctuation and references that sometimes gets added to the end
            svotes = re.sub(" \(\?\)$|<br[^\d]*$|<ref[^\d]*$|[,. ]", "", templ["votes"])  
            
            if re.match("\d+$", svotes):
                votes = int(svotes)
            elif svotes in ["Unopposed", "Unoppose", "unopposed", "Elected", "Co-opted", "''N/A''", 
                            "'''unopposed'''", "''unopposed''", "(unopposed)", "''(unopposed)''", 
                            "''uncontested''", 
                            "Returned", "Returnedandseated", "Returnedandunseated", "Unknown"]:
                votes = 1
            elif svotes == "" or svotes == "-":
                votes = None
            elif svotes == "Defeated":
                votes = 0
            else:
                print ("Unparsed votes: " + str(templ) + str([svotes]))
                assert False
                
            if votes != None:
                data["votes"] = votes                
                
            party = re.match("(.*?)\s*(\[?http://.*|{{|<!.*|<ref.*|<sup.*)?$", templ["party"]).group(1)
            mpartycat = re.match("(.*?)\[\[(.+?)[\|\]]", party)
            if mpartycat:
                party = mpartycat.group(1) + mpartycat.group(2)
            party = re.sub(u"\u2013", "-", party)
            party = re.sub(u"\u2019", "-", party)
            assert not re.search("\[|<", party), list(templ["party"])
            data["party"] = party
            
            
            # clean up the candidate field so it contains no stray reference links
            candidate = templ["candidate"]
            mcandidatet = re.match("(?s)(.*?)\s*(<!.*|<ref.*|\[http://.*|\(Ruair.*?\)|\*+|\+|\,|<sup>\d</sup>|<nowiki>\*</nowiki>)$", candidate)
            if mcandidatet:
                candidate = mcandidatet.group(1)
    
            mcandidatet = re.match("(?s)['\"]*(?:Sir |Rt.? |Right |Hon\.? |Rev\.? |Prof\.? |Miss |Mrs\.? |Ms |Maj\.-Gen\. |Lt\.-Col\. |Lt\.-Cmdr\. |Lt-Gen |Maj\.? |Lt |Com |Col |Major |Major-General |Dr\.? |Brig |Gen |Gp |Capt\.? |Count |Captain |Commodore |Admiral |Lord |Lieutenant-Colonel |Commander |[WR]\. |Lieut Col |Lt-Col |Dame |Comm )*(.*?)(?:,? Bt\.?| CMG| KC| RN| [OKMCG]BE| MC| DSO| DFC| TD| KCB| CB| VRD| QC| MB| CSI| CIE| KCMG| GCB| LLD| MD| PhD| GCVO| \[\[Military Cross\|MC\]\]|, \[\[Royal Naval Volunteer Reserve\|RNVR\]\]|{{mnl}}| <sup>1</sup>\s*| \(PPC\)| \(incumbent\))*[\s'\"]*$", candidate)
            if mcandidatet:
                candidate = mcandidatet.group(1)

            # remove the target link in the pattern [[xxx|xxx]]
            mcandidate = re.match("(\[\[[^\]\|]+?)(?:\|[\s\S]+?)?\]\]$", candidate)
            if mcandidate:
                candidate = mcandidate.group(1) + "]]"
            candidate = re.sub(u"\u2019", "'", candidate)
            
            # error in http://en.wikipedia.org/wiki/North_Antrim_(UK_Parliament_constituency)#Elections_in_the_1880s
            if candidate == "[William Pirrie Sinclair":
                candidate = "William Pirrie Sinclair"
            if candidate == "[[John_Hemming_%28politician%29]]":
                candidate = "[[John_Hemming_(politician)]]"
            if candidate == "[[Nikolai Tolstoy]]-Miloslavsky":
                candidate = "[[Nikolai Tolstoy]]"
            if candidate[-27:] == u' ([[SDP\u2013Liberal Alliance]])':
                candidate = candidate[:-27]
            if candidate == u'Donald MacLaren of [[Clan MacLaren|MacLaren]]':
                candidate = u'Donald MacLaren'

            
            data["candidate"] = candidate
            
            
            # there are problems with the ndash in these names where inserting one in this python code causes 
            # an exception and a 0 length file to be saved
            if candidate.startswith("[[Richard Bethell (17"):
                assert title == "Yorkshire (UK Parliament constituency)", templ
            if candidate.startswith("[[Rowland Burdon (18"):
                assert title == "Sedgefield (UK Parliament constituency)", templ
            elif candidate.startswith("[[George Byng"):
                assert title == "Middlesex (UK Parliament constituency)"
            elif candidate == "[[Oliver Baldwin]], [[Viscount Corvedale]]":
                pass
            
            elif candidate and candidate != "[to be confirmed]":
                assert re.match("(\[\[)?[\w\s,.#_\-'\"/\(\)\x80-\xe2\xe9\xed\xfc\xf4]+(\]\])?$", candidate), [candidate, templ, electionname]
            elif candidate == "" and party != "Others":
                assert title in ["Aberavon (UK Parliament constituency)", 
                                 "Wycombe (UK Parliament constituency)", 
                                 "Gower (UK Parliament constituency)", 
                                 "Kettering (UK Parliament constituency)", 
                                 "Manchester Gorton (UK Parliament constituency)", 
                                 "Islington North (UK Parliament constituency)", 
                                 "Hornsey and Wood Green (UK Parliament constituency)", 
                                 "Finchley and Golders Green (UK Parliament constituency)", 
                                 "Epping Forest (UK Parliament constituency)", 
                                 "Bury St Edmunds (UK Parliament constituency)", 
                                 "Harlow (UK Parliament constituency)",
                                 "Bristol East (UK Parliament constituency)",
                                 "Beaconsfield (UK Parliament constituency)",
                                 "Battersea (UK Parliament constituency)",
                                 "Ashton-under-Lyne (UK Parliament constituency)",
                                ], data
                candidate = "unknown"

            else:
                assert party == "Others" or \
                       party == "others" or \
                       party == "non transferable" or \
                       title in ["Croydon North West (UK Parliament constituency)", 
                                 "South Colchester and Maldon (UK Parliament constituency)", 
                                 "Battersea (UK Parliament constituency)", 
                                 "Kettering (UK Parliament constituency)", 
                                 "Harlow (UK Parliament constituency)", 
                                 "Epping Forest (UK Parliament constituency)", 
                                 "North Essex (UK Parliament constituency)", 
                                 "South East Cambridgeshire (UK Parliament constituency)", 
                                 "Rochford and Southend East (UK Parliament constituency)", 
                                 "Finchley and Golders Green (UK Parliament constituency)", 
                                 "Bristol East (UK Parliament constituency)", 
                                 "Glasgow Cathcart (UK Parliament constituency)"] or \
                electionname == "next United Kingdom general election", \
                           [str(templ), electionname, title]
            
            yield data
            
        elif templ[0] == "Election box end":
            electionname = None


        
def ParseTemplates(text):   # pretty obfuscated, isn't it?
    templstack = [ ]
    for tt in re.split("(\{\{\{|\}\}\}|\{\{|\}\}|\[\[|\]\]|\|)", text):
        if tt in ["{{{", "{{", "[["]:
            templstack.append([tt, [ [ ] ] ])
        elif templstack and tt in ["}}}", "}}", "]]"]:
            templstack[-1][1][-1] = "".join(templstack[-1][1][-1])
            templstack[-1].append(tt)
            if len(templstack) == 1:
                if templstack[-1][0] == "{{":
                    res = { }
                    for i, param in enumerate(templstack[-1][1]):
                        k, e, v = re.match("(?s)([^=]*)(=?)(.*)$", param).groups()
                        if e:
                            res[k.strip()] = v.strip()
                        else:
                            res[i] = k.strip()
                    yield res
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


            
Main()
import scraperwiki
import lxml.etree
import urllib, re, csv

# Work to do: chase down any wikilinks for candidates and follow redirects

# also a 16 constituencies have a nonstandard tabular layout.  seen by
# scraperwiki.sqlite.attach("wikipedia-list-of-constituencies", "s1")
# scraperwiki.sqlite.attach("wikipedia-parliamentary-candidates", "s2")
# print scraperwiki.sqlite.select("wptitle from s1.swdata left join s2.swdata on constituency=wptitle where constituency is null")


qs = "select wptitle, content from constsrc.swdata order by rowid desc limit 1 offset ?"

def Main():
    scraperwiki.sqlite.attach("wikipedia-list-of-constituencies", "constsrc")
    for i in range(0, 7000):
        tdata = scraperwiki.sqlite.execute(qs, i)
        if len(tdata["data"]) == 0:
            break
        cc = tdata["data"][0]
        print i, cc[0]
        text = cc[1]
        templs = ParseTemplates(text)
        ldata = [ ]
        for data in CollateElections(cc[0], templs):
            if data["type"] == "candidate":
                ldata.append(data)
        scraperwiki.sqlite.save(["constituency", "election", "candidate", "party"], ldata)


def CollateElections(title, templs):
    for templ in templs:
        if templ[0] == "Election box begin" or templ[0] == "Election box begin no clear":
            melectionname = re.search("\[\[(.*?)[\|\]]", templ["title"])
            electionname = melectionname and melectionname.group(1) or templ["title"]
            electionname = re.match("(.*?)\s*(\{\{.*|http://.*)?$", electionname).group(1)
            if electionname.startswith("UK "):
                electionname = "United Kingdom " + electionname[3:]
            electionname = re.sub("(United Kingdom general election) (\d\d\d\d)", "\\1, \\2", electionname)
            electionname = re.sub("(United Kingdom general election) (\d\d\d\d)", "\\1, \\2", electionname)
            if electionname == "January 1910 UK general election":
                electionname = "United Kingdom general election, January 1910"
            electionname = re.sub("(Notional 1992 UK General Election Result) : .*", "\\1", electionname)
                
            yield { "type":"election", "name":electionname }

        elif re.match("Election box candidate", templ[0]):
            data = { "type":"candidate", "constituency":title, "election":electionname }
            # get rid of punctuation and references that sometimes gets added to the end
            svotes = re.sub(" \(\?\)$|<br[^\d]*$|<ref[^\d]*$|[,. ]", "", templ["votes"])  
            
            if re.match("\d+$", svotes):
                votes = int(svotes)
            elif svotes in ["Unopposed", "Unoppose", "unopposed", "Elected", "Co-opted", "''N/A''", 
                            "'''unopposed'''", "''unopposed''", "(unopposed)", "''(unopposed)''", 
                            "''uncontested''", 
                            "Returned", "Returnedandseated", "Returnedandunseated", "Unknown"]:
                votes = 1
            elif svotes == "" or svotes == "-":
                votes = None
            elif svotes == "Defeated":
                votes = 0
            else:
                print ("Unparsed votes: " + str(templ) + str([svotes]))
                assert False
                
            if votes != None:
                data["votes"] = votes                
                
            party = re.match("(.*?)\s*(\[?http://.*|{{|<!.*|<ref.*|<sup.*)?$", templ["party"]).group(1)
            mpartycat = re.match("(.*?)\[\[(.+?)[\|\]]", party)
            if mpartycat:
                party = mpartycat.group(1) + mpartycat.group(2)
            party = re.sub(u"\u2013", "-", party)
            party = re.sub(u"\u2019", "-", party)
            assert not re.search("\[|<", party), list(templ["party"])
            data["party"] = party
            
            
            # clean up the candidate field so it contains no stray reference links
            candidate = templ["candidate"]
            mcandidatet = re.match("(?s)(.*?)\s*(<!.*|<ref.*|\[http://.*|\(Ruair.*?\)|\*+|\+|\,|<sup>\d</sup>|<nowiki>\*</nowiki>)$", candidate)
            if mcandidatet:
                candidate = mcandidatet.group(1)
    
            mcandidatet = re.match("(?s)['\"]*(?:Sir |Rt.? |Right |Hon\.? |Rev\.? |Prof\.? |Miss |Mrs\.? |Ms |Maj\.-Gen\. |Lt\.-Col\. |Lt\.-Cmdr\. |Lt-Gen |Maj\.? |Lt |Com |Col |Major |Major-General |Dr\.? |Brig |Gen |Gp |Capt\.? |Count |Captain |Commodore |Admiral |Lord |Lieutenant-Colonel |Commander |[WR]\. |Lieut Col |Lt-Col |Dame |Comm )*(.*?)(?:,? Bt\.?| CMG| KC| RN| [OKMCG]BE| MC| DSO| DFC| TD| KCB| CB| VRD| QC| MB| CSI| CIE| KCMG| GCB| LLD| MD| PhD| GCVO| \[\[Military Cross\|MC\]\]|, \[\[Royal Naval Volunteer Reserve\|RNVR\]\]|{{mnl}}| <sup>1</sup>\s*| \(PPC\)| \(incumbent\))*[\s'\"]*$", candidate)
            if mcandidatet:
                candidate = mcandidatet.group(1)

            # remove the target link in the pattern [[xxx|xxx]]
            mcandidate = re.match("(\[\[[^\]\|]+?)(?:\|[\s\S]+?)?\]\]$", candidate)
            if mcandidate:
                candidate = mcandidate.group(1) + "]]"
            candidate = re.sub(u"\u2019", "'", candidate)
            
            # error in http://en.wikipedia.org/wiki/North_Antrim_(UK_Parliament_constituency)#Elections_in_the_1880s
            if candidate == "[William Pirrie Sinclair":
                candidate = "William Pirrie Sinclair"
            if candidate == "[[John_Hemming_%28politician%29]]":
                candidate = "[[John_Hemming_(politician)]]"
            if candidate == "[[Nikolai Tolstoy]]-Miloslavsky":
                candidate = "[[Nikolai Tolstoy]]"
            if candidate[-27:] == u' ([[SDP\u2013Liberal Alliance]])':
                candidate = candidate[:-27]
            if candidate == u'Donald MacLaren of [[Clan MacLaren|MacLaren]]':
                candidate = u'Donald MacLaren'

            
            data["candidate"] = candidate
            
            
            # there are problems with the ndash in these names where inserting one in this python code causes 
            # an exception and a 0 length file to be saved
            if candidate.startswith("[[Richard Bethell (17"):
                assert title == "Yorkshire (UK Parliament constituency)", templ
            if candidate.startswith("[[Rowland Burdon (18"):
                assert title == "Sedgefield (UK Parliament constituency)", templ
            elif candidate.startswith("[[George Byng"):
                assert title == "Middlesex (UK Parliament constituency)"
            elif candidate == "[[Oliver Baldwin]], [[Viscount Corvedale]]":
                pass
            
            elif candidate and candidate != "[to be confirmed]":
                assert re.match("(\[\[)?[\w\s,.#_\-'\"/\(\)\x80-\xe2\xe9\xed\xfc\xf4]+(\]\])?$", candidate), [candidate, templ, electionname]
            elif candidate == "" and party != "Others":
                assert title in ["Aberavon (UK Parliament constituency)", 
                                 "Wycombe (UK Parliament constituency)", 
                                 "Gower (UK Parliament constituency)", 
                                 "Kettering (UK Parliament constituency)", 
                                 "Manchester Gorton (UK Parliament constituency)", 
                                 "Islington North (UK Parliament constituency)", 
                                 "Hornsey and Wood Green (UK Parliament constituency)", 
                                 "Finchley and Golders Green (UK Parliament constituency)", 
                                 "Epping Forest (UK Parliament constituency)", 
                                 "Bury St Edmunds (UK Parliament constituency)", 
                                 "Harlow (UK Parliament constituency)",
                                 "Bristol East (UK Parliament constituency)",
                                 "Beaconsfield (UK Parliament constituency)",
                                 "Battersea (UK Parliament constituency)",
                                 "Ashton-under-Lyne (UK Parliament constituency)",
                                ], data
                candidate = "unknown"

            else:
                assert party == "Others" or \
                       party == "others" or \
                       party == "non transferable" or \
                       title in ["Croydon North West (UK Parliament constituency)", 
                                 "South Colchester and Maldon (UK Parliament constituency)", 
                                 "Battersea (UK Parliament constituency)", 
                                 "Kettering (UK Parliament constituency)", 
                                 "Harlow (UK Parliament constituency)", 
                                 "Epping Forest (UK Parliament constituency)", 
                                 "North Essex (UK Parliament constituency)", 
                                 "South East Cambridgeshire (UK Parliament constituency)", 
                                 "Rochford and Southend East (UK Parliament constituency)", 
                                 "Finchley and Golders Green (UK Parliament constituency)", 
                                 "Bristol East (UK Parliament constituency)", 
                                 "Glasgow Cathcart (UK Parliament constituency)"] or \
                electionname == "next United Kingdom general election", \
                           [str(templ), electionname, title]
            
            yield data
            
        elif templ[0] == "Election box end":
            electionname = None


        
def ParseTemplates(text):   # pretty obfuscated, isn't it?
    templstack = [ ]
    for tt in re.split("(\{\{\{|\}\}\}|\{\{|\}\}|\[\[|\]\]|\|)", text):
        if tt in ["{{{", "{{", "[["]:
            templstack.append([tt, [ [ ] ] ])
        elif templstack and tt in ["}}}", "}}", "]]"]:
            templstack[-1][1][-1] = "".join(templstack[-1][1][-1])
            templstack[-1].append(tt)
            if len(templstack) == 1:
                if templstack[-1][0] == "{{":
                    res = { }
                    for i, param in enumerate(templstack[-1][1]):
                        k, e, v = re.match("(?s)([^=]*)(=?)(.*)$", param).groups()
                        if e:
                            res[k.strip()] = v.strip()
                        else:
                            res[i] = k.strip()
                    yield res
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


            
Main()
import scraperwiki
import lxml.etree
import urllib, re, csv

# Work to do: chase down any wikilinks for candidates and follow redirects

# also a 16 constituencies have a nonstandard tabular layout.  seen by
# scraperwiki.sqlite.attach("wikipedia-list-of-constituencies", "s1")
# scraperwiki.sqlite.attach("wikipedia-parliamentary-candidates", "s2")
# print scraperwiki.sqlite.select("wptitle from s1.swdata left join s2.swdata on constituency=wptitle where constituency is null")


qs = "select wptitle, content from constsrc.swdata order by rowid desc limit 1 offset ?"

def Main():
    scraperwiki.sqlite.attach("wikipedia-list-of-constituencies", "constsrc")
    for i in range(0, 7000):
        tdata = scraperwiki.sqlite.execute(qs, i)
        if len(tdata["data"]) == 0:
            break
        cc = tdata["data"][0]
        print i, cc[0]
        text = cc[1]
        templs = ParseTemplates(text)
        ldata = [ ]
        for data in CollateElections(cc[0], templs):
            if data["type"] == "candidate":
                ldata.append(data)
        scraperwiki.sqlite.save(["constituency", "election", "candidate", "party"], ldata)


def CollateElections(title, templs):
    for templ in templs:
        if templ[0] == "Election box begin" or templ[0] == "Election box begin no clear":
            melectionname = re.search("\[\[(.*?)[\|\]]", templ["title"])
            electionname = melectionname and melectionname.group(1) or templ["title"]
            electionname = re.match("(.*?)\s*(\{\{.*|http://.*)?$", electionname).group(1)
            if electionname.startswith("UK "):
                electionname = "United Kingdom " + electionname[3:]
            electionname = re.sub("(United Kingdom general election) (\d\d\d\d)", "\\1, \\2", electionname)
            electionname = re.sub("(United Kingdom general election) (\d\d\d\d)", "\\1, \\2", electionname)
            if electionname == "January 1910 UK general election":
                electionname = "United Kingdom general election, January 1910"
            electionname = re.sub("(Notional 1992 UK General Election Result) : .*", "\\1", electionname)
                
            yield { "type":"election", "name":electionname }

        elif re.match("Election box candidate", templ[0]):
            data = { "type":"candidate", "constituency":title, "election":electionname }
            # get rid of punctuation and references that sometimes gets added to the end
            svotes = re.sub(" \(\?\)$|<br[^\d]*$|<ref[^\d]*$|[,. ]", "", templ["votes"])  
            
            if re.match("\d+$", svotes):
                votes = int(svotes)
            elif svotes in ["Unopposed", "Unoppose", "unopposed", "Elected", "Co-opted", "''N/A''", 
                            "'''unopposed'''", "''unopposed''", "(unopposed)", "''(unopposed)''", 
                            "''uncontested''", 
                            "Returned", "Returnedandseated", "Returnedandunseated", "Unknown"]:
                votes = 1
            elif svotes == "" or svotes == "-":
                votes = None
            elif svotes == "Defeated":
                votes = 0
            else:
                print ("Unparsed votes: " + str(templ) + str([svotes]))
                assert False
                
            if votes != None:
                data["votes"] = votes                
                
            party = re.match("(.*?)\s*(\[?http://.*|{{|<!.*|<ref.*|<sup.*)?$", templ["party"]).group(1)
            mpartycat = re.match("(.*?)\[\[(.+?)[\|\]]", party)
            if mpartycat:
                party = mpartycat.group(1) + mpartycat.group(2)
            party = re.sub(u"\u2013", "-", party)
            party = re.sub(u"\u2019", "-", party)
            assert not re.search("\[|<", party), list(templ["party"])
            data["party"] = party
            
            
            # clean up the candidate field so it contains no stray reference links
            candidate = templ["candidate"]
            mcandidatet = re.match("(?s)(.*?)\s*(<!.*|<ref.*|\[http://.*|\(Ruair.*?\)|\*+|\+|\,|<sup>\d</sup>|<nowiki>\*</nowiki>)$", candidate)
            if mcandidatet:
                candidate = mcandidatet.group(1)
    
            mcandidatet = re.match("(?s)['\"]*(?:Sir |Rt.? |Right |Hon\.? |Rev\.? |Prof\.? |Miss |Mrs\.? |Ms |Maj\.-Gen\. |Lt\.-Col\. |Lt\.-Cmdr\. |Lt-Gen |Maj\.? |Lt |Com |Col |Major |Major-General |Dr\.? |Brig |Gen |Gp |Capt\.? |Count |Captain |Commodore |Admiral |Lord |Lieutenant-Colonel |Commander |[WR]\. |Lieut Col |Lt-Col |Dame |Comm )*(.*?)(?:,? Bt\.?| CMG| KC| RN| [OKMCG]BE| MC| DSO| DFC| TD| KCB| CB| VRD| QC| MB| CSI| CIE| KCMG| GCB| LLD| MD| PhD| GCVO| \[\[Military Cross\|MC\]\]|, \[\[Royal Naval Volunteer Reserve\|RNVR\]\]|{{mnl}}| <sup>1</sup>\s*| \(PPC\)| \(incumbent\))*[\s'\"]*$", candidate)
            if mcandidatet:
                candidate = mcandidatet.group(1)

            # remove the target link in the pattern [[xxx|xxx]]
            mcandidate = re.match("(\[\[[^\]\|]+?)(?:\|[\s\S]+?)?\]\]$", candidate)
            if mcandidate:
                candidate = mcandidate.group(1) + "]]"
            candidate = re.sub(u"\u2019", "'", candidate)
            
            # error in http://en.wikipedia.org/wiki/North_Antrim_(UK_Parliament_constituency)#Elections_in_the_1880s
            if candidate == "[William Pirrie Sinclair":
                candidate = "William Pirrie Sinclair"
            if candidate == "[[John_Hemming_%28politician%29]]":
                candidate = "[[John_Hemming_(politician)]]"
            if candidate == "[[Nikolai Tolstoy]]-Miloslavsky":
                candidate = "[[Nikolai Tolstoy]]"
            if candidate[-27:] == u' ([[SDP\u2013Liberal Alliance]])':
                candidate = candidate[:-27]
            if candidate == u'Donald MacLaren of [[Clan MacLaren|MacLaren]]':
                candidate = u'Donald MacLaren'

            
            data["candidate"] = candidate
            
            
            # there are problems with the ndash in these names where inserting one in this python code causes 
            # an exception and a 0 length file to be saved
            if candidate.startswith("[[Richard Bethell (17"):
                assert title == "Yorkshire (UK Parliament constituency)", templ
            if candidate.startswith("[[Rowland Burdon (18"):
                assert title == "Sedgefield (UK Parliament constituency)", templ
            elif candidate.startswith("[[George Byng"):
                assert title == "Middlesex (UK Parliament constituency)"
            elif candidate == "[[Oliver Baldwin]], [[Viscount Corvedale]]":
                pass
            
            elif candidate and candidate != "[to be confirmed]":
                assert re.match("(\[\[)?[\w\s,.#_\-'\"/\(\)\x80-\xe2\xe9\xed\xfc\xf4]+(\]\])?$", candidate), [candidate, templ, electionname]
            elif candidate == "" and party != "Others":
                assert title in ["Aberavon (UK Parliament constituency)", 
                                 "Wycombe (UK Parliament constituency)", 
                                 "Gower (UK Parliament constituency)", 
                                 "Kettering (UK Parliament constituency)", 
                                 "Manchester Gorton (UK Parliament constituency)", 
                                 "Islington North (UK Parliament constituency)", 
                                 "Hornsey and Wood Green (UK Parliament constituency)", 
                                 "Finchley and Golders Green (UK Parliament constituency)", 
                                 "Epping Forest (UK Parliament constituency)", 
                                 "Bury St Edmunds (UK Parliament constituency)", 
                                 "Harlow (UK Parliament constituency)",
                                 "Bristol East (UK Parliament constituency)",
                                 "Beaconsfield (UK Parliament constituency)",
                                 "Battersea (UK Parliament constituency)",
                                 "Ashton-under-Lyne (UK Parliament constituency)",
                                ], data
                candidate = "unknown"

            else:
                assert party == "Others" or \
                       party == "others" or \
                       party == "non transferable" or \
                       title in ["Croydon North West (UK Parliament constituency)", 
                                 "South Colchester and Maldon (UK Parliament constituency)", 
                                 "Battersea (UK Parliament constituency)", 
                                 "Kettering (UK Parliament constituency)", 
                                 "Harlow (UK Parliament constituency)", 
                                 "Epping Forest (UK Parliament constituency)", 
                                 "North Essex (UK Parliament constituency)", 
                                 "South East Cambridgeshire (UK Parliament constituency)", 
                                 "Rochford and Southend East (UK Parliament constituency)", 
                                 "Finchley and Golders Green (UK Parliament constituency)", 
                                 "Bristol East (UK Parliament constituency)", 
                                 "Glasgow Cathcart (UK Parliament constituency)"] or \
                electionname == "next United Kingdom general election", \
                           [str(templ), electionname, title]
            
            yield data
            
        elif templ[0] == "Election box end":
            electionname = None


        
def ParseTemplates(text):   # pretty obfuscated, isn't it?
    templstack = [ ]
    for tt in re.split("(\{\{\{|\}\}\}|\{\{|\}\}|\[\[|\]\]|\|)", text):
        if tt in ["{{{", "{{", "[["]:
            templstack.append([tt, [ [ ] ] ])
        elif templstack and tt in ["}}}", "}}", "]]"]:
            templstack[-1][1][-1] = "".join(templstack[-1][1][-1])
            templstack[-1].append(tt)
            if len(templstack) == 1:
                if templstack[-1][0] == "{{":
                    res = { }
                    for i, param in enumerate(templstack[-1][1]):
                        k, e, v = re.match("(?s)([^=]*)(=?)(.*)$", param).groups()
                        if e:
                            res[k.strip()] = v.strip()
                        else:
                            res[i] = k.strip()
                    yield res
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


            
Main()
import scraperwiki
import lxml.etree
import urllib, re, csv

# Work to do: chase down any wikilinks for candidates and follow redirects

# also a 16 constituencies have a nonstandard tabular layout.  seen by
# scraperwiki.sqlite.attach("wikipedia-list-of-constituencies", "s1")
# scraperwiki.sqlite.attach("wikipedia-parliamentary-candidates", "s2")
# print scraperwiki.sqlite.select("wptitle from s1.swdata left join s2.swdata on constituency=wptitle where constituency is null")


qs = "select wptitle, content from constsrc.swdata order by rowid desc limit 1 offset ?"

def Main():
    scraperwiki.sqlite.attach("wikipedia-list-of-constituencies", "constsrc")
    for i in range(0, 7000):
        tdata = scraperwiki.sqlite.execute(qs, i)
        if len(tdata["data"]) == 0:
            break
        cc = tdata["data"][0]
        print i, cc[0]
        text = cc[1]
        templs = ParseTemplates(text)
        ldata = [ ]
        for data in CollateElections(cc[0], templs):
            if data["type"] == "candidate":
                ldata.append(data)
        scraperwiki.sqlite.save(["constituency", "election", "candidate", "party"], ldata)


def CollateElections(title, templs):
    for templ in templs:
        if templ[0] == "Election box begin" or templ[0] == "Election box begin no clear":
            melectionname = re.search("\[\[(.*?)[\|\]]", templ["title"])
            electionname = melectionname and melectionname.group(1) or templ["title"]
            electionname = re.match("(.*?)\s*(\{\{.*|http://.*)?$", electionname).group(1)
            if electionname.startswith("UK "):
                electionname = "United Kingdom " + electionname[3:]
            electionname = re.sub("(United Kingdom general election) (\d\d\d\d)", "\\1, \\2", electionname)
            electionname = re.sub("(United Kingdom general election) (\d\d\d\d)", "\\1, \\2", electionname)
            if electionname == "January 1910 UK general election":
                electionname = "United Kingdom general election, January 1910"
            electionname = re.sub("(Notional 1992 UK General Election Result) : .*", "\\1", electionname)
                
            yield { "type":"election", "name":electionname }

        elif re.match("Election box candidate", templ[0]):
            data = { "type":"candidate", "constituency":title, "election":electionname }
            # get rid of punctuation and references that sometimes gets added to the end
            svotes = re.sub(" \(\?\)$|<br[^\d]*$|<ref[^\d]*$|[,. ]", "", templ["votes"])  
            
            if re.match("\d+$", svotes):
                votes = int(svotes)
            elif svotes in ["Unopposed", "Unoppose", "unopposed", "Elected", "Co-opted", "''N/A''", 
                            "'''unopposed'''", "''unopposed''", "(unopposed)", "''(unopposed)''", 
                            "''uncontested''", 
                            "Returned", "Returnedandseated", "Returnedandunseated", "Unknown"]:
                votes = 1
            elif svotes == "" or svotes == "-":
                votes = None
            elif svotes == "Defeated":
                votes = 0
            else:
                print ("Unparsed votes: " + str(templ) + str([svotes]))
                assert False
                
            if votes != None:
                data["votes"] = votes                
                
            party = re.match("(.*?)\s*(\[?http://.*|{{|<!.*|<ref.*|<sup.*)?$", templ["party"]).group(1)
            mpartycat = re.match("(.*?)\[\[(.+?)[\|\]]", party)
            if mpartycat:
                party = mpartycat.group(1) + mpartycat.group(2)
            party = re.sub(u"\u2013", "-", party)
            party = re.sub(u"\u2019", "-", party)
            assert not re.search("\[|<", party), list(templ["party"])
            data["party"] = party
            
            
            # clean up the candidate field so it contains no stray reference links
            candidate = templ["candidate"]
            mcandidatet = re.match("(?s)(.*?)\s*(<!.*|<ref.*|\[http://.*|\(Ruair.*?\)|\*+|\+|\,|<sup>\d</sup>|<nowiki>\*</nowiki>)$", candidate)
            if mcandidatet:
                candidate = mcandidatet.group(1)
    
            mcandidatet = re.match("(?s)['\"]*(?:Sir |Rt.? |Right |Hon\.? |Rev\.? |Prof\.? |Miss |Mrs\.? |Ms |Maj\.-Gen\. |Lt\.-Col\. |Lt\.-Cmdr\. |Lt-Gen |Maj\.? |Lt |Com |Col |Major |Major-General |Dr\.? |Brig |Gen |Gp |Capt\.? |Count |Captain |Commodore |Admiral |Lord |Lieutenant-Colonel |Commander |[WR]\. |Lieut Col |Lt-Col |Dame |Comm )*(.*?)(?:,? Bt\.?| CMG| KC| RN| [OKMCG]BE| MC| DSO| DFC| TD| KCB| CB| VRD| QC| MB| CSI| CIE| KCMG| GCB| LLD| MD| PhD| GCVO| \[\[Military Cross\|MC\]\]|, \[\[Royal Naval Volunteer Reserve\|RNVR\]\]|{{mnl}}| <sup>1</sup>\s*| \(PPC\)| \(incumbent\))*[\s'\"]*$", candidate)
            if mcandidatet:
                candidate = mcandidatet.group(1)

            # remove the target link in the pattern [[xxx|xxx]]
            mcandidate = re.match("(\[\[[^\]\|]+?)(?:\|[\s\S]+?)?\]\]$", candidate)
            if mcandidate:
                candidate = mcandidate.group(1) + "]]"
            candidate = re.sub(u"\u2019", "'", candidate)
            
            # error in http://en.wikipedia.org/wiki/North_Antrim_(UK_Parliament_constituency)#Elections_in_the_1880s
            if candidate == "[William Pirrie Sinclair":
                candidate = "William Pirrie Sinclair"
            if candidate == "[[John_Hemming_%28politician%29]]":
                candidate = "[[John_Hemming_(politician)]]"
            if candidate == "[[Nikolai Tolstoy]]-Miloslavsky":
                candidate = "[[Nikolai Tolstoy]]"
            if candidate[-27:] == u' ([[SDP\u2013Liberal Alliance]])':
                candidate = candidate[:-27]
            if candidate == u'Donald MacLaren of [[Clan MacLaren|MacLaren]]':
                candidate = u'Donald MacLaren'

            
            data["candidate"] = candidate
            
            
            # there are problems with the ndash in these names where inserting one in this python code causes 
            # an exception and a 0 length file to be saved
            if candidate.startswith("[[Richard Bethell (17"):
                assert title == "Yorkshire (UK Parliament constituency)", templ
            if candidate.startswith("[[Rowland Burdon (18"):
                assert title == "Sedgefield (UK Parliament constituency)", templ
            elif candidate.startswith("[[George Byng"):
                assert title == "Middlesex (UK Parliament constituency)"
            elif candidate == "[[Oliver Baldwin]], [[Viscount Corvedale]]":
                pass
            
            elif candidate and candidate != "[to be confirmed]":
                assert re.match("(\[\[)?[\w\s,.#_\-'\"/\(\)\x80-\xe2\xe9\xed\xfc\xf4]+(\]\])?$", candidate), [candidate, templ, electionname]
            elif candidate == "" and party != "Others":
                assert title in ["Aberavon (UK Parliament constituency)", 
                                 "Wycombe (UK Parliament constituency)", 
                                 "Gower (UK Parliament constituency)", 
                                 "Kettering (UK Parliament constituency)", 
                                 "Manchester Gorton (UK Parliament constituency)", 
                                 "Islington North (UK Parliament constituency)", 
                                 "Hornsey and Wood Green (UK Parliament constituency)", 
                                 "Finchley and Golders Green (UK Parliament constituency)", 
                                 "Epping Forest (UK Parliament constituency)", 
                                 "Bury St Edmunds (UK Parliament constituency)", 
                                 "Harlow (UK Parliament constituency)",
                                 "Bristol East (UK Parliament constituency)",
                                 "Beaconsfield (UK Parliament constituency)",
                                 "Battersea (UK Parliament constituency)",
                                 "Ashton-under-Lyne (UK Parliament constituency)",
                                ], data
                candidate = "unknown"

            else:
                assert party == "Others" or \
                       party == "others" or \
                       party == "non transferable" or \
                       title in ["Croydon North West (UK Parliament constituency)", 
                                 "South Colchester and Maldon (UK Parliament constituency)", 
                                 "Battersea (UK Parliament constituency)", 
                                 "Kettering (UK Parliament constituency)", 
                                 "Harlow (UK Parliament constituency)", 
                                 "Epping Forest (UK Parliament constituency)", 
                                 "North Essex (UK Parliament constituency)", 
                                 "South East Cambridgeshire (UK Parliament constituency)", 
                                 "Rochford and Southend East (UK Parliament constituency)", 
                                 "Finchley and Golders Green (UK Parliament constituency)", 
                                 "Bristol East (UK Parliament constituency)", 
                                 "Glasgow Cathcart (UK Parliament constituency)"] or \
                electionname == "next United Kingdom general election", \
                           [str(templ), electionname, title]
            
            yield data
            
        elif templ[0] == "Election box end":
            electionname = None


        
def ParseTemplates(text):   # pretty obfuscated, isn't it?
    templstack = [ ]
    for tt in re.split("(\{\{\{|\}\}\}|\{\{|\}\}|\[\[|\]\]|\|)", text):
        if tt in ["{{{", "{{", "[["]:
            templstack.append([tt, [ [ ] ] ])
        elif templstack and tt in ["}}}", "}}", "]]"]:
            templstack[-1][1][-1] = "".join(templstack[-1][1][-1])
            templstack[-1].append(tt)
            if len(templstack) == 1:
                if templstack[-1][0] == "{{":
                    res = { }
                    for i, param in enumerate(templstack[-1][1]):
                        k, e, v = re.match("(?s)([^=]*)(=?)(.*)$", param).groups()
                        if e:
                            res[k.strip()] = v.strip()
                        else:
                            res[i] = k.strip()
                    yield res
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


            
Main()
import scraperwiki
import lxml.etree
import urllib, re, csv

# Work to do: chase down any wikilinks for candidates and follow redirects

# also a 16 constituencies have a nonstandard tabular layout.  seen by
# scraperwiki.sqlite.attach("wikipedia-list-of-constituencies", "s1")
# scraperwiki.sqlite.attach("wikipedia-parliamentary-candidates", "s2")
# print scraperwiki.sqlite.select("wptitle from s1.swdata left join s2.swdata on constituency=wptitle where constituency is null")


qs = "select wptitle, content from constsrc.swdata order by rowid desc limit 1 offset ?"

def Main():
    scraperwiki.sqlite.attach("wikipedia-list-of-constituencies", "constsrc")
    for i in range(0, 7000):
        tdata = scraperwiki.sqlite.execute(qs, i)
        if len(tdata["data"]) == 0:
            break
        cc = tdata["data"][0]
        print i, cc[0]
        text = cc[1]
        templs = ParseTemplates(text)
        ldata = [ ]
        for data in CollateElections(cc[0], templs):
            if data["type"] == "candidate":
                ldata.append(data)
        scraperwiki.sqlite.save(["constituency", "election", "candidate", "party"], ldata)


def CollateElections(title, templs):
    for templ in templs:
        if templ[0] == "Election box begin" or templ[0] == "Election box begin no clear":
            melectionname = re.search("\[\[(.*?)[\|\]]", templ["title"])
            electionname = melectionname and melectionname.group(1) or templ["title"]
            electionname = re.match("(.*?)\s*(\{\{.*|http://.*)?$", electionname).group(1)
            if electionname.startswith("UK "):
                electionname = "United Kingdom " + electionname[3:]
            electionname = re.sub("(United Kingdom general election) (\d\d\d\d)", "\\1, \\2", electionname)
            electionname = re.sub("(United Kingdom general election) (\d\d\d\d)", "\\1, \\2", electionname)
            if electionname == "January 1910 UK general election":
                electionname = "United Kingdom general election, January 1910"
            electionname = re.sub("(Notional 1992 UK General Election Result) : .*", "\\1", electionname)
                
            yield { "type":"election", "name":electionname }

        elif re.match("Election box candidate", templ[0]):
            data = { "type":"candidate", "constituency":title, "election":electionname }
            # get rid of punctuation and references that sometimes gets added to the end
            svotes = re.sub(" \(\?\)$|<br[^\d]*$|<ref[^\d]*$|[,. ]", "", templ["votes"])  
            
            if re.match("\d+$", svotes):
                votes = int(svotes)
            elif svotes in ["Unopposed", "Unoppose", "unopposed", "Elected", "Co-opted", "''N/A''", 
                            "'''unopposed'''", "''unopposed''", "(unopposed)", "''(unopposed)''", 
                            "''uncontested''", 
                            "Returned", "Returnedandseated", "Returnedandunseated", "Unknown"]:
                votes = 1
            elif svotes == "" or svotes == "-":
                votes = None
            elif svotes == "Defeated":
                votes = 0
            else:
                print ("Unparsed votes: " + str(templ) + str([svotes]))
                assert False
                
            if votes != None:
                data["votes"] = votes                
                
            party = re.match("(.*?)\s*(\[?http://.*|{{|<!.*|<ref.*|<sup.*)?$", templ["party"]).group(1)
            mpartycat = re.match("(.*?)\[\[(.+?)[\|\]]", party)
            if mpartycat:
                party = mpartycat.group(1) + mpartycat.group(2)
            party = re.sub(u"\u2013", "-", party)
            party = re.sub(u"\u2019", "-", party)
            assert not re.search("\[|<", party), list(templ["party"])
            data["party"] = party
            
            
            # clean up the candidate field so it contains no stray reference links
            candidate = templ["candidate"]
            mcandidatet = re.match("(?s)(.*?)\s*(<!.*|<ref.*|\[http://.*|\(Ruair.*?\)|\*+|\+|\,|<sup>\d</sup>|<nowiki>\*</nowiki>)$", candidate)
            if mcandidatet:
                candidate = mcandidatet.group(1)
    
            mcandidatet = re.match("(?s)['\"]*(?:Sir |Rt.? |Right |Hon\.? |Rev\.? |Prof\.? |Miss |Mrs\.? |Ms |Maj\.-Gen\. |Lt\.-Col\. |Lt\.-Cmdr\. |Lt-Gen |Maj\.? |Lt |Com |Col |Major |Major-General |Dr\.? |Brig |Gen |Gp |Capt\.? |Count |Captain |Commodore |Admiral |Lord |Lieutenant-Colonel |Commander |[WR]\. |Lieut Col |Lt-Col |Dame |Comm )*(.*?)(?:,? Bt\.?| CMG| KC| RN| [OKMCG]BE| MC| DSO| DFC| TD| KCB| CB| VRD| QC| MB| CSI| CIE| KCMG| GCB| LLD| MD| PhD| GCVO| \[\[Military Cross\|MC\]\]|, \[\[Royal Naval Volunteer Reserve\|RNVR\]\]|{{mnl}}| <sup>1</sup>\s*| \(PPC\)| \(incumbent\))*[\s'\"]*$", candidate)
            if mcandidatet:
                candidate = mcandidatet.group(1)

            # remove the target link in the pattern [[xxx|xxx]]
            mcandidate = re.match("(\[\[[^\]\|]+?)(?:\|[\s\S]+?)?\]\]$", candidate)
            if mcandidate:
                candidate = mcandidate.group(1) + "]]"
            candidate = re.sub(u"\u2019", "'", candidate)
            
            # error in http://en.wikipedia.org/wiki/North_Antrim_(UK_Parliament_constituency)#Elections_in_the_1880s
            if candidate == "[William Pirrie Sinclair":
                candidate = "William Pirrie Sinclair"
            if candidate == "[[John_Hemming_%28politician%29]]":
                candidate = "[[John_Hemming_(politician)]]"
            if candidate == "[[Nikolai Tolstoy]]-Miloslavsky":
                candidate = "[[Nikolai Tolstoy]]"
            if candidate[-27:] == u' ([[SDP\u2013Liberal Alliance]])':
                candidate = candidate[:-27]
            if candidate == u'Donald MacLaren of [[Clan MacLaren|MacLaren]]':
                candidate = u'Donald MacLaren'

            
            data["candidate"] = candidate
            
            
            # there are problems with the ndash in these names where inserting one in this python code causes 
            # an exception and a 0 length file to be saved
            if candidate.startswith("[[Richard Bethell (17"):
                assert title == "Yorkshire (UK Parliament constituency)", templ
            if candidate.startswith("[[Rowland Burdon (18"):
                assert title == "Sedgefield (UK Parliament constituency)", templ
            elif candidate.startswith("[[George Byng"):
                assert title == "Middlesex (UK Parliament constituency)"
            elif candidate == "[[Oliver Baldwin]], [[Viscount Corvedale]]":
                pass
            
            elif candidate and candidate != "[to be confirmed]":
                assert re.match("(\[\[)?[\w\s,.#_\-'\"/\(\)\x80-\xe2\xe9\xed\xfc\xf4]+(\]\])?$", candidate), [candidate, templ, electionname]
            elif candidate == "" and party != "Others":
                assert title in ["Aberavon (UK Parliament constituency)", 
                                 "Wycombe (UK Parliament constituency)", 
                                 "Gower (UK Parliament constituency)", 
                                 "Kettering (UK Parliament constituency)", 
                                 "Manchester Gorton (UK Parliament constituency)", 
                                 "Islington North (UK Parliament constituency)", 
                                 "Hornsey and Wood Green (UK Parliament constituency)", 
                                 "Finchley and Golders Green (UK Parliament constituency)", 
                                 "Epping Forest (UK Parliament constituency)", 
                                 "Bury St Edmunds (UK Parliament constituency)", 
                                 "Harlow (UK Parliament constituency)",
                                 "Bristol East (UK Parliament constituency)",
                                 "Beaconsfield (UK Parliament constituency)",
                                 "Battersea (UK Parliament constituency)",
                                 "Ashton-under-Lyne (UK Parliament constituency)",
                                ], data
                candidate = "unknown"

            else:
                assert party == "Others" or \
                       party == "others" or \
                       party == "non transferable" or \
                       title in ["Croydon North West (UK Parliament constituency)", 
                                 "South Colchester and Maldon (UK Parliament constituency)", 
                                 "Battersea (UK Parliament constituency)", 
                                 "Kettering (UK Parliament constituency)", 
                                 "Harlow (UK Parliament constituency)", 
                                 "Epping Forest (UK Parliament constituency)", 
                                 "North Essex (UK Parliament constituency)", 
                                 "South East Cambridgeshire (UK Parliament constituency)", 
                                 "Rochford and Southend East (UK Parliament constituency)", 
                                 "Finchley and Golders Green (UK Parliament constituency)", 
                                 "Bristol East (UK Parliament constituency)", 
                                 "Glasgow Cathcart (UK Parliament constituency)"] or \
                electionname == "next United Kingdom general election", \
                           [str(templ), electionname, title]
            
            yield data
            
        elif templ[0] == "Election box end":
            electionname = None


        
def ParseTemplates(text):   # pretty obfuscated, isn't it?
    templstack = [ ]
    for tt in re.split("(\{\{\{|\}\}\}|\{\{|\}\}|\[\[|\]\]|\|)", text):
        if tt in ["{{{", "{{", "[["]:
            templstack.append([tt, [ [ ] ] ])
        elif templstack and tt in ["}}}", "}}", "]]"]:
            templstack[-1][1][-1] = "".join(templstack[-1][1][-1])
            templstack[-1].append(tt)
            if len(templstack) == 1:
                if templstack[-1][0] == "{{":
                    res = { }
                    for i, param in enumerate(templstack[-1][1]):
                        k, e, v = re.match("(?s)([^=]*)(=?)(.*)$", param).groups()
                        if e:
                            res[k.strip()] = v.strip()
                        else:
                            res[i] = k.strip()
                    yield res
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


            
Main()
import scraperwiki
import lxml.etree
import urllib, re, csv

# Work to do: chase down any wikilinks for candidates and follow redirects

# also a 16 constituencies have a nonstandard tabular layout.  seen by
# scraperwiki.sqlite.attach("wikipedia-list-of-constituencies", "s1")
# scraperwiki.sqlite.attach("wikipedia-parliamentary-candidates", "s2")
# print scraperwiki.sqlite.select("wptitle from s1.swdata left join s2.swdata on constituency=wptitle where constituency is null")


qs = "select wptitle, content from constsrc.swdata order by rowid desc limit 1 offset ?"

def Main():
    scraperwiki.sqlite.attach("wikipedia-list-of-constituencies", "constsrc")
    for i in range(0, 7000):
        tdata = scraperwiki.sqlite.execute(qs, i)
        if len(tdata["data"]) == 0:
            break
        cc = tdata["data"][0]
        print i, cc[0]
        text = cc[1]
        templs = ParseTemplates(text)
        ldata = [ ]
        for data in CollateElections(cc[0], templs):
            if data["type"] == "candidate":
                ldata.append(data)
        scraperwiki.sqlite.save(["constituency", "election", "candidate", "party"], ldata)


def CollateElections(title, templs):
    for templ in templs:
        if templ[0] == "Election box begin" or templ[0] == "Election box begin no clear":
            melectionname = re.search("\[\[(.*?)[\|\]]", templ["title"])
            electionname = melectionname and melectionname.group(1) or templ["title"]
            electionname = re.match("(.*?)\s*(\{\{.*|http://.*)?$", electionname).group(1)
            if electionname.startswith("UK "):
                electionname = "United Kingdom " + electionname[3:]
            electionname = re.sub("(United Kingdom general election) (\d\d\d\d)", "\\1, \\2", electionname)
            electionname = re.sub("(United Kingdom general election) (\d\d\d\d)", "\\1, \\2", electionname)
            if electionname == "January 1910 UK general election":
                electionname = "United Kingdom general election, January 1910"
            electionname = re.sub("(Notional 1992 UK General Election Result) : .*", "\\1", electionname)
                
            yield { "type":"election", "name":electionname }

        elif re.match("Election box candidate", templ[0]):
            data = { "type":"candidate", "constituency":title, "election":electionname }
            # get rid of punctuation and references that sometimes gets added to the end
            svotes = re.sub(" \(\?\)$|<br[^\d]*$|<ref[^\d]*$|[,. ]", "", templ["votes"])  
            
            if re.match("\d+$", svotes):
                votes = int(svotes)
            elif svotes in ["Unopposed", "Unoppose", "unopposed", "Elected", "Co-opted", "''N/A''", 
                            "'''unopposed'''", "''unopposed''", "(unopposed)", "''(unopposed)''", 
                            "''uncontested''", 
                            "Returned", "Returnedandseated", "Returnedandunseated", "Unknown"]:
                votes = 1
            elif svotes == "" or svotes == "-":
                votes = None
            elif svotes == "Defeated":
                votes = 0
            else:
                print ("Unparsed votes: " + str(templ) + str([svotes]))
                assert False
                
            if votes != None:
                data["votes"] = votes                
                
            party = re.match("(.*?)\s*(\[?http://.*|{{|<!.*|<ref.*|<sup.*)?$", templ["party"]).group(1)
            mpartycat = re.match("(.*?)\[\[(.+?)[\|\]]", party)
            if mpartycat:
                party = mpartycat.group(1) + mpartycat.group(2)
            party = re.sub(u"\u2013", "-", party)
            party = re.sub(u"\u2019", "-", party)
            assert not re.search("\[|<", party), list(templ["party"])
            data["party"] = party
            
            
            # clean up the candidate field so it contains no stray reference links
            candidate = templ["candidate"]
            mcandidatet = re.match("(?s)(.*?)\s*(<!.*|<ref.*|\[http://.*|\(Ruair.*?\)|\*+|\+|\,|<sup>\d</sup>|<nowiki>\*</nowiki>)$", candidate)
            if mcandidatet:
                candidate = mcandidatet.group(1)
    
            mcandidatet = re.match("(?s)['\"]*(?:Sir |Rt.? |Right |Hon\.? |Rev\.? |Prof\.? |Miss |Mrs\.? |Ms |Maj\.-Gen\. |Lt\.-Col\. |Lt\.-Cmdr\. |Lt-Gen |Maj\.? |Lt |Com |Col |Major |Major-General |Dr\.? |Brig |Gen |Gp |Capt\.? |Count |Captain |Commodore |Admiral |Lord |Lieutenant-Colonel |Commander |[WR]\. |Lieut Col |Lt-Col |Dame |Comm )*(.*?)(?:,? Bt\.?| CMG| KC| RN| [OKMCG]BE| MC| DSO| DFC| TD| KCB| CB| VRD| QC| MB| CSI| CIE| KCMG| GCB| LLD| MD| PhD| GCVO| \[\[Military Cross\|MC\]\]|, \[\[Royal Naval Volunteer Reserve\|RNVR\]\]|{{mnl}}| <sup>1</sup>\s*| \(PPC\)| \(incumbent\))*[\s'\"]*$", candidate)
            if mcandidatet:
                candidate = mcandidatet.group(1)

            # remove the target link in the pattern [[xxx|xxx]]
            mcandidate = re.match("(\[\[[^\]\|]+?)(?:\|[\s\S]+?)?\]\]$", candidate)
            if mcandidate:
                candidate = mcandidate.group(1) + "]]"
            candidate = re.sub(u"\u2019", "'", candidate)
            
            # error in http://en.wikipedia.org/wiki/North_Antrim_(UK_Parliament_constituency)#Elections_in_the_1880s
            if candidate == "[William Pirrie Sinclair":
                candidate = "William Pirrie Sinclair"
            if candidate == "[[John_Hemming_%28politician%29]]":
                candidate = "[[John_Hemming_(politician)]]"
            if candidate == "[[Nikolai Tolstoy]]-Miloslavsky":
                candidate = "[[Nikolai Tolstoy]]"
            if candidate[-27:] == u' ([[SDP\u2013Liberal Alliance]])':
                candidate = candidate[:-27]
            if candidate == u'Donald MacLaren of [[Clan MacLaren|MacLaren]]':
                candidate = u'Donald MacLaren'

            
            data["candidate"] = candidate
            
            
            # there are problems with the ndash in these names where inserting one in this python code causes 
            # an exception and a 0 length file to be saved
            if candidate.startswith("[[Richard Bethell (17"):
                assert title == "Yorkshire (UK Parliament constituency)", templ
            if candidate.startswith("[[Rowland Burdon (18"):
                assert title == "Sedgefield (UK Parliament constituency)", templ
            elif candidate.startswith("[[George Byng"):
                assert title == "Middlesex (UK Parliament constituency)"
            elif candidate == "[[Oliver Baldwin]], [[Viscount Corvedale]]":
                pass
            
            elif candidate and candidate != "[to be confirmed]":
                assert re.match("(\[\[)?[\w\s,.#_\-'\"/\(\)\x80-\xe2\xe9\xed\xfc\xf4]+(\]\])?$", candidate), [candidate, templ, electionname]
            elif candidate == "" and party != "Others":
                assert title in ["Aberavon (UK Parliament constituency)", 
                                 "Wycombe (UK Parliament constituency)", 
                                 "Gower (UK Parliament constituency)", 
                                 "Kettering (UK Parliament constituency)", 
                                 "Manchester Gorton (UK Parliament constituency)", 
                                 "Islington North (UK Parliament constituency)", 
                                 "Hornsey and Wood Green (UK Parliament constituency)", 
                                 "Finchley and Golders Green (UK Parliament constituency)", 
                                 "Epping Forest (UK Parliament constituency)", 
                                 "Bury St Edmunds (UK Parliament constituency)", 
                                 "Harlow (UK Parliament constituency)",
                                 "Bristol East (UK Parliament constituency)",
                                 "Beaconsfield (UK Parliament constituency)",
                                 "Battersea (UK Parliament constituency)",
                                 "Ashton-under-Lyne (UK Parliament constituency)",
                                ], data
                candidate = "unknown"

            else:
                assert party == "Others" or \
                       party == "others" or \
                       party == "non transferable" or \
                       title in ["Croydon North West (UK Parliament constituency)", 
                                 "South Colchester and Maldon (UK Parliament constituency)", 
                                 "Battersea (UK Parliament constituency)", 
                                 "Kettering (UK Parliament constituency)", 
                                 "Harlow (UK Parliament constituency)", 
                                 "Epping Forest (UK Parliament constituency)", 
                                 "North Essex (UK Parliament constituency)", 
                                 "South East Cambridgeshire (UK Parliament constituency)", 
                                 "Rochford and Southend East (UK Parliament constituency)", 
                                 "Finchley and Golders Green (UK Parliament constituency)", 
                                 "Bristol East (UK Parliament constituency)", 
                                 "Glasgow Cathcart (UK Parliament constituency)"] or \
                electionname == "next United Kingdom general election", \
                           [str(templ), electionname, title]
            
            yield data
            
        elif templ[0] == "Election box end":
            electionname = None


        
def ParseTemplates(text):   # pretty obfuscated, isn't it?
    templstack = [ ]
    for tt in re.split("(\{\{\{|\}\}\}|\{\{|\}\}|\[\[|\]\]|\|)", text):
        if tt in ["{{{", "{{", "[["]:
            templstack.append([tt, [ [ ] ] ])
        elif templstack and tt in ["}}}", "}}", "]]"]:
            templstack[-1][1][-1] = "".join(templstack[-1][1][-1])
            templstack[-1].append(tt)
            if len(templstack) == 1:
                if templstack[-1][0] == "{{":
                    res = { }
                    for i, param in enumerate(templstack[-1][1]):
                        k, e, v = re.match("(?s)([^=]*)(=?)(.*)$", param).groups()
                        if e:
                            res[k.strip()] = v.strip()
                        else:
                            res[i] = k.strip()
                    yield res
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


            
Main()
import scraperwiki
import lxml.etree
import urllib, re, csv

# Work to do: chase down any wikilinks for candidates and follow redirects

# also a 16 constituencies have a nonstandard tabular layout.  seen by
# scraperwiki.sqlite.attach("wikipedia-list-of-constituencies", "s1")
# scraperwiki.sqlite.attach("wikipedia-parliamentary-candidates", "s2")
# print scraperwiki.sqlite.select("wptitle from s1.swdata left join s2.swdata on constituency=wptitle where constituency is null")


qs = "select wptitle, content from constsrc.swdata order by rowid desc limit 1 offset ?"

def Main():
    scraperwiki.sqlite.attach("wikipedia-list-of-constituencies", "constsrc")
    for i in range(0, 7000):
        tdata = scraperwiki.sqlite.execute(qs, i)
        if len(tdata["data"]) == 0:
            break
        cc = tdata["data"][0]
        print i, cc[0]
        text = cc[1]
        templs = ParseTemplates(text)
        ldata = [ ]
        for data in CollateElections(cc[0], templs):
            if data["type"] == "candidate":
                ldata.append(data)
        scraperwiki.sqlite.save(["constituency", "election", "candidate", "party"], ldata)


def CollateElections(title, templs):
    for templ in templs:
        if templ[0] == "Election box begin" or templ[0] == "Election box begin no clear":
            melectionname = re.search("\[\[(.*?)[\|\]]", templ["title"])
            electionname = melectionname and melectionname.group(1) or templ["title"]
            electionname = re.match("(.*?)\s*(\{\{.*|http://.*)?$", electionname).group(1)
            if electionname.startswith("UK "):
                electionname = "United Kingdom " + electionname[3:]
            electionname = re.sub("(United Kingdom general election) (\d\d\d\d)", "\\1, \\2", electionname)
            electionname = re.sub("(United Kingdom general election) (\d\d\d\d)", "\\1, \\2", electionname)
            if electionname == "January 1910 UK general election":
                electionname = "United Kingdom general election, January 1910"
            electionname = re.sub("(Notional 1992 UK General Election Result) : .*", "\\1", electionname)
                
            yield { "type":"election", "name":electionname }

        elif re.match("Election box candidate", templ[0]):
            data = { "type":"candidate", "constituency":title, "election":electionname }
            # get rid of punctuation and references that sometimes gets added to the end
            svotes = re.sub(" \(\?\)$|<br[^\d]*$|<ref[^\d]*$|[,. ]", "", templ["votes"])  
            
            if re.match("\d+$", svotes):
                votes = int(svotes)
            elif svotes in ["Unopposed", "Unoppose", "unopposed", "Elected", "Co-opted", "''N/A''", 
                            "'''unopposed'''", "''unopposed''", "(unopposed)", "''(unopposed)''", 
                            "''uncontested''", 
                            "Returned", "Returnedandseated", "Returnedandunseated", "Unknown"]:
                votes = 1
            elif svotes == "" or svotes == "-":
                votes = None
            elif svotes == "Defeated":
                votes = 0
            else:
                print ("Unparsed votes: " + str(templ) + str([svotes]))
                assert False
                
            if votes != None:
                data["votes"] = votes                
                
            party = re.match("(.*?)\s*(\[?http://.*|{{|<!.*|<ref.*|<sup.*)?$", templ["party"]).group(1)
            mpartycat = re.match("(.*?)\[\[(.+?)[\|\]]", party)
            if mpartycat:
                party = mpartycat.group(1) + mpartycat.group(2)
            party = re.sub(u"\u2013", "-", party)
            party = re.sub(u"\u2019", "-", party)
            assert not re.search("\[|<", party), list(templ["party"])
            data["party"] = party
            
            
            # clean up the candidate field so it contains no stray reference links
            candidate = templ["candidate"]
            mcandidatet = re.match("(?s)(.*?)\s*(<!.*|<ref.*|\[http://.*|\(Ruair.*?\)|\*+|\+|\,|<sup>\d</sup>|<nowiki>\*</nowiki>)$", candidate)
            if mcandidatet:
                candidate = mcandidatet.group(1)
    
            mcandidatet = re.match("(?s)['\"]*(?:Sir |Rt.? |Right |Hon\.? |Rev\.? |Prof\.? |Miss |Mrs\.? |Ms |Maj\.-Gen\. |Lt\.-Col\. |Lt\.-Cmdr\. |Lt-Gen |Maj\.? |Lt |Com |Col |Major |Major-General |Dr\.? |Brig |Gen |Gp |Capt\.? |Count |Captain |Commodore |Admiral |Lord |Lieutenant-Colonel |Commander |[WR]\. |Lieut Col |Lt-Col |Dame |Comm )*(.*?)(?:,? Bt\.?| CMG| KC| RN| [OKMCG]BE| MC| DSO| DFC| TD| KCB| CB| VRD| QC| MB| CSI| CIE| KCMG| GCB| LLD| MD| PhD| GCVO| \[\[Military Cross\|MC\]\]|, \[\[Royal Naval Volunteer Reserve\|RNVR\]\]|{{mnl}}| <sup>1</sup>\s*| \(PPC\)| \(incumbent\))*[\s'\"]*$", candidate)
            if mcandidatet:
                candidate = mcandidatet.group(1)

            # remove the target link in the pattern [[xxx|xxx]]
            mcandidate = re.match("(\[\[[^\]\|]+?)(?:\|[\s\S]+?)?\]\]$", candidate)
            if mcandidate:
                candidate = mcandidate.group(1) + "]]"
            candidate = re.sub(u"\u2019", "'", candidate)
            
            # error in http://en.wikipedia.org/wiki/North_Antrim_(UK_Parliament_constituency)#Elections_in_the_1880s
            if candidate == "[William Pirrie Sinclair":
                candidate = "William Pirrie Sinclair"
            if candidate == "[[John_Hemming_%28politician%29]]":
                candidate = "[[John_Hemming_(politician)]]"
            if candidate == "[[Nikolai Tolstoy]]-Miloslavsky":
                candidate = "[[Nikolai Tolstoy]]"
            if candidate[-27:] == u' ([[SDP\u2013Liberal Alliance]])':
                candidate = candidate[:-27]
            if candidate == u'Donald MacLaren of [[Clan MacLaren|MacLaren]]':
                candidate = u'Donald MacLaren'

            
            data["candidate"] = candidate
            
            
            # there are problems with the ndash in these names where inserting one in this python code causes 
            # an exception and a 0 length file to be saved
            if candidate.startswith("[[Richard Bethell (17"):
                assert title == "Yorkshire (UK Parliament constituency)", templ
            if candidate.startswith("[[Rowland Burdon (18"):
                assert title == "Sedgefield (UK Parliament constituency)", templ
            elif candidate.startswith("[[George Byng"):
                assert title == "Middlesex (UK Parliament constituency)"
            elif candidate == "[[Oliver Baldwin]], [[Viscount Corvedale]]":
                pass
            
            elif candidate and candidate != "[to be confirmed]":
                assert re.match("(\[\[)?[\w\s,.#_\-'\"/\(\)\x80-\xe2\xe9\xed\xfc\xf4]+(\]\])?$", candidate), [candidate, templ, electionname]
            elif candidate == "" and party != "Others":
                assert title in ["Aberavon (UK Parliament constituency)", 
                                 "Wycombe (UK Parliament constituency)", 
                                 "Gower (UK Parliament constituency)", 
                                 "Kettering (UK Parliament constituency)", 
                                 "Manchester Gorton (UK Parliament constituency)", 
                                 "Islington North (UK Parliament constituency)", 
                                 "Hornsey and Wood Green (UK Parliament constituency)", 
                                 "Finchley and Golders Green (UK Parliament constituency)", 
                                 "Epping Forest (UK Parliament constituency)", 
                                 "Bury St Edmunds (UK Parliament constituency)", 
                                 "Harlow (UK Parliament constituency)",
                                 "Bristol East (UK Parliament constituency)",
                                 "Beaconsfield (UK Parliament constituency)",
                                 "Battersea (UK Parliament constituency)",
                                 "Ashton-under-Lyne (UK Parliament constituency)",
                                ], data
                candidate = "unknown"

            else:
                assert party == "Others" or \
                       party == "others" or \
                       party == "non transferable" or \
                       title in ["Croydon North West (UK Parliament constituency)", 
                                 "South Colchester and Maldon (UK Parliament constituency)", 
                                 "Battersea (UK Parliament constituency)", 
                                 "Kettering (UK Parliament constituency)", 
                                 "Harlow (UK Parliament constituency)", 
                                 "Epping Forest (UK Parliament constituency)", 
                                 "North Essex (UK Parliament constituency)", 
                                 "South East Cambridgeshire (UK Parliament constituency)", 
                                 "Rochford and Southend East (UK Parliament constituency)", 
                                 "Finchley and Golders Green (UK Parliament constituency)", 
                                 "Bristol East (UK Parliament constituency)", 
                                 "Glasgow Cathcart (UK Parliament constituency)"] or \
                electionname == "next United Kingdom general election", \
                           [str(templ), electionname, title]
            
            yield data
            
        elif templ[0] == "Election box end":
            electionname = None


        
def ParseTemplates(text):   # pretty obfuscated, isn't it?
    templstack = [ ]
    for tt in re.split("(\{\{\{|\}\}\}|\{\{|\}\}|\[\[|\]\]|\|)", text):
        if tt in ["{{{", "{{", "[["]:
            templstack.append([tt, [ [ ] ] ])
        elif templstack and tt in ["}}}", "}}", "]]"]:
            templstack[-1][1][-1] = "".join(templstack[-1][1][-1])
            templstack[-1].append(tt)
            if len(templstack) == 1:
                if templstack[-1][0] == "{{":
                    res = { }
                    for i, param in enumerate(templstack[-1][1]):
                        k, e, v = re.match("(?s)([^=]*)(=?)(.*)$", param).groups()
                        if e:
                            res[k.strip()] = v.strip()
                        else:
                            res[i] = k.strip()
                    yield res
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


            
Main()
import scraperwiki
import lxml.etree
import urllib, re, csv

# Work to do: chase down any wikilinks for candidates and follow redirects

# also a 16 constituencies have a nonstandard tabular layout.  seen by
# scraperwiki.sqlite.attach("wikipedia-list-of-constituencies", "s1")
# scraperwiki.sqlite.attach("wikipedia-parliamentary-candidates", "s2")
# print scraperwiki.sqlite.select("wptitle from s1.swdata left join s2.swdata on constituency=wptitle where constituency is null")


qs = "select wptitle, content from constsrc.swdata order by rowid desc limit 1 offset ?"

def Main():
    scraperwiki.sqlite.attach("wikipedia-list-of-constituencies", "constsrc")
    for i in range(0, 7000):
        tdata = scraperwiki.sqlite.execute(qs, i)
        if len(tdata["data"]) == 0:
            break
        cc = tdata["data"][0]
        print i, cc[0]
        text = cc[1]
        templs = ParseTemplates(text)
        ldata = [ ]
        for data in CollateElections(cc[0], templs):
            if data["type"] == "candidate":
                ldata.append(data)
        scraperwiki.sqlite.save(["constituency", "election", "candidate", "party"], ldata)


def CollateElections(title, templs):
    for templ in templs:
        if templ[0] == "Election box begin" or templ[0] == "Election box begin no clear":
            melectionname = re.search("\[\[(.*?)[\|\]]", templ["title"])
            electionname = melectionname and melectionname.group(1) or templ["title"]
            electionname = re.match("(.*?)\s*(\{\{.*|http://.*)?$", electionname).group(1)
            if electionname.startswith("UK "):
                electionname = "United Kingdom " + electionname[3:]
            electionname = re.sub("(United Kingdom general election) (\d\d\d\d)", "\\1, \\2", electionname)
            electionname = re.sub("(United Kingdom general election) (\d\d\d\d)", "\\1, \\2", electionname)
            if electionname == "January 1910 UK general election":
                electionname = "United Kingdom general election, January 1910"
            electionname = re.sub("(Notional 1992 UK General Election Result) : .*", "\\1", electionname)
                
            yield { "type":"election", "name":electionname }

        elif re.match("Election box candidate", templ[0]):
            data = { "type":"candidate", "constituency":title, "election":electionname }
            # get rid of punctuation and references that sometimes gets added to the end
            svotes = re.sub(" \(\?\)$|<br[^\d]*$|<ref[^\d]*$|[,. ]", "", templ["votes"])  
            
            if re.match("\d+$", svotes):
                votes = int(svotes)
            elif svotes in ["Unopposed", "Unoppose", "unopposed", "Elected", "Co-opted", "''N/A''", 
                            "'''unopposed'''", "''unopposed''", "(unopposed)", "''(unopposed)''", 
                            "''uncontested''", 
                            "Returned", "Returnedandseated", "Returnedandunseated", "Unknown"]:
                votes = 1
            elif svotes == "" or svotes == "-":
                votes = None
            elif svotes == "Defeated":
                votes = 0
            else:
                print ("Unparsed votes: " + str(templ) + str([svotes]))
                assert False
                
            if votes != None:
                data["votes"] = votes                
                
            party = re.match("(.*?)\s*(\[?http://.*|{{|<!.*|<ref.*|<sup.*)?$", templ["party"]).group(1)
            mpartycat = re.match("(.*?)\[\[(.+?)[\|\]]", party)
            if mpartycat:
                party = mpartycat.group(1) + mpartycat.group(2)
            party = re.sub(u"\u2013", "-", party)
            party = re.sub(u"\u2019", "-", party)
            assert not re.search("\[|<", party), list(templ["party"])
            data["party"] = party
            
            
            # clean up the candidate field so it contains no stray reference links
            candidate = templ["candidate"]
            mcandidatet = re.match("(?s)(.*?)\s*(<!.*|<ref.*|\[http://.*|\(Ruair.*?\)|\*+|\+|\,|<sup>\d</sup>|<nowiki>\*</nowiki>)$", candidate)
            if mcandidatet:
                candidate = mcandidatet.group(1)
    
            mcandidatet = re.match("(?s)['\"]*(?:Sir |Rt.? |Right |Hon\.? |Rev\.? |Prof\.? |Miss |Mrs\.? |Ms |Maj\.-Gen\. |Lt\.-Col\. |Lt\.-Cmdr\. |Lt-Gen |Maj\.? |Lt |Com |Col |Major |Major-General |Dr\.? |Brig |Gen |Gp |Capt\.? |Count |Captain |Commodore |Admiral |Lord |Lieutenant-Colonel |Commander |[WR]\. |Lieut Col |Lt-Col |Dame |Comm )*(.*?)(?:,? Bt\.?| CMG| KC| RN| [OKMCG]BE| MC| DSO| DFC| TD| KCB| CB| VRD| QC| MB| CSI| CIE| KCMG| GCB| LLD| MD| PhD| GCVO| \[\[Military Cross\|MC\]\]|, \[\[Royal Naval Volunteer Reserve\|RNVR\]\]|{{mnl}}| <sup>1</sup>\s*| \(PPC\)| \(incumbent\))*[\s'\"]*$", candidate)
            if mcandidatet:
                candidate = mcandidatet.group(1)

            # remove the target link in the pattern [[xxx|xxx]]
            mcandidate = re.match("(\[\[[^\]\|]+?)(?:\|[\s\S]+?)?\]\]$", candidate)
            if mcandidate:
                candidate = mcandidate.group(1) + "]]"
            candidate = re.sub(u"\u2019", "'", candidate)
            
            # error in http://en.wikipedia.org/wiki/North_Antrim_(UK_Parliament_constituency)#Elections_in_the_1880s
            if candidate == "[William Pirrie Sinclair":
                candidate = "William Pirrie Sinclair"
            if candidate == "[[John_Hemming_%28politician%29]]":
                candidate = "[[John_Hemming_(politician)]]"
            if candidate == "[[Nikolai Tolstoy]]-Miloslavsky":
                candidate = "[[Nikolai Tolstoy]]"
            if candidate[-27:] == u' ([[SDP\u2013Liberal Alliance]])':
                candidate = candidate[:-27]
            if candidate == u'Donald MacLaren of [[Clan MacLaren|MacLaren]]':
                candidate = u'Donald MacLaren'

            
            data["candidate"] = candidate
            
            
            # there are problems with the ndash in these names where inserting one in this python code causes 
            # an exception and a 0 length file to be saved
            if candidate.startswith("[[Richard Bethell (17"):
                assert title == "Yorkshire (UK Parliament constituency)", templ
            if candidate.startswith("[[Rowland Burdon (18"):
                assert title == "Sedgefield (UK Parliament constituency)", templ
            elif candidate.startswith("[[George Byng"):
                assert title == "Middlesex (UK Parliament constituency)"
            elif candidate == "[[Oliver Baldwin]], [[Viscount Corvedale]]":
                pass
            
            elif candidate and candidate != "[to be confirmed]":
                assert re.match("(\[\[)?[\w\s,.#_\-'\"/\(\)\x80-\xe2\xe9\xed\xfc\xf4]+(\]\])?$", candidate), [candidate, templ, electionname]
            elif candidate == "" and party != "Others":
                assert title in ["Aberavon (UK Parliament constituency)", 
                                 "Wycombe (UK Parliament constituency)", 
                                 "Gower (UK Parliament constituency)", 
                                 "Kettering (UK Parliament constituency)", 
                                 "Manchester Gorton (UK Parliament constituency)", 
                                 "Islington North (UK Parliament constituency)", 
                                 "Hornsey and Wood Green (UK Parliament constituency)", 
                                 "Finchley and Golders Green (UK Parliament constituency)", 
                                 "Epping Forest (UK Parliament constituency)", 
                                 "Bury St Edmunds (UK Parliament constituency)", 
                                 "Harlow (UK Parliament constituency)",
                                 "Bristol East (UK Parliament constituency)",
                                 "Beaconsfield (UK Parliament constituency)",
                                 "Battersea (UK Parliament constituency)",
                                 "Ashton-under-Lyne (UK Parliament constituency)",
                                ], data
                candidate = "unknown"

            else:
                assert party == "Others" or \
                       party == "others" or \
                       party == "non transferable" or \
                       title in ["Croydon North West (UK Parliament constituency)", 
                                 "South Colchester and Maldon (UK Parliament constituency)", 
                                 "Battersea (UK Parliament constituency)", 
                                 "Kettering (UK Parliament constituency)", 
                                 "Harlow (UK Parliament constituency)", 
                                 "Epping Forest (UK Parliament constituency)", 
                                 "North Essex (UK Parliament constituency)", 
                                 "South East Cambridgeshire (UK Parliament constituency)", 
                                 "Rochford and Southend East (UK Parliament constituency)", 
                                 "Finchley and Golders Green (UK Parliament constituency)", 
                                 "Bristol East (UK Parliament constituency)", 
                                 "Glasgow Cathcart (UK Parliament constituency)"] or \
                electionname == "next United Kingdom general election", \
                           [str(templ), electionname, title]
            
            yield data
            
        elif templ[0] == "Election box end":
            electionname = None


        
def ParseTemplates(text):   # pretty obfuscated, isn't it?
    templstack = [ ]
    for tt in re.split("(\{\{\{|\}\}\}|\{\{|\}\}|\[\[|\]\]|\|)", text):
        if tt in ["{{{", "{{", "[["]:
            templstack.append([tt, [ [ ] ] ])
        elif templstack and tt in ["}}}", "}}", "]]"]:
            templstack[-1][1][-1] = "".join(templstack[-1][1][-1])
            templstack[-1].append(tt)
            if len(templstack) == 1:
                if templstack[-1][0] == "{{":
                    res = { }
                    for i, param in enumerate(templstack[-1][1]):
                        k, e, v = re.match("(?s)([^=]*)(=?)(.*)$", param).groups()
                        if e:
                            res[k.strip()] = v.strip()
                        else:
                            res[i] = k.strip()
                    yield res
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


            
Main()
