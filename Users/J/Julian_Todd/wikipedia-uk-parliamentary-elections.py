
def GetInfobox(title, templs):
    for templ in templs:
        if templ[0] == title:
            return templ
    return None


# this parsing will find out if the percentage reported per election agrees with the vote tally
def GetElectionCandidates(templs):
    res = { }
    candidatelist = [ ]
    electionnames = [ ]
    for templ in templs:
        if templ[0] == "Election box begin":
            electionname = re.search("title=\[\[(.*?)[\|\]]", templ["title"]).group(1)
            electionnames.append(electionname)
            candidatelist = [ templ["title"] ]
            res[templ["title"]] = candidatelist
        elif re.match("Election box candidate", templ[0]):
            candidatelist.append(templ)
        elif templ[0] == "Election box end":
            candidatelist = [ ]

    print electionnames


def Parse(reading):
    templs = ParseTemplates(reading.contents())
    for templ in templs:
        if templ[0] == "Election box begin" or templ[0] == "Election box begin no clear":
            melectionname = re.search("\[\[(.*?)[\|\]]", templ["title"])
            electionname = melectionname and melectionname.group(1) or templ["title"]
            electionname = re.match("(.*?)\s*(\{\{.*|http://.*)?$", electionname).group(1)
            if electionname[:3] == "UK ":
                electionname = "United Kingdom " + electionname[3:]
            if electionname[:8] == "next UK ":
                electionname = "next United Kingdom " + electionname[8:]
            if electionname == "Next United Kingdom general election":
                electionname = "next United Kingdom general election"
            if electionname == "United Kingdom general election, 2010":
                electionname = "next United Kingdom general election"
                
            yield { "type":"election", "name":electionname }

        elif re.match("Election box candidate", templ[0]):
            # get rid of punctuation and references that sometimes gets added to the end
            svotes = re.sub(" \(\?\)$|<br[^\d]*$|[,. ]", "", templ["votes"])  
            
            if re.match("\d+$", svotes):
                votes = int(svotes)
            elif svotes in ["Unopposed", "Unoppose", "unopposed", "Elected", "Co-opted", "''N/A''", "''unopposed''", "(unopposed)", "''(unopposed)''", "''uncontested''", "Returned", "Returnedandseated", "Returnedandunseated", "Unknown"]:
                votes = 1
            elif svotes == "":
                votes = 0
            elif svotes == "Defeated":
                votes = 0
            else:
                assert False, "Unparsed votes: " + str(templ) + str([svotes])
                
            party = re.match("(.*?)\s*(\[?http://.*|{{|<!.*|<ref.*|<sup.*)?$", templ["party"]).group(1)
            mpartycat = re.match("(.*?)\[\[(.+?)[\|\]]", party)
            if mpartycat:
                party = mpartycat.group(1) + mpartycat.group(2)
            assert not re.search("\[|<", party), list(templ["party"])
                
            # clean up the candidate field so it contains no stray reference links
            candidate = templ["candidate"]
            mcandidatet = re.match("(.*?)\s*(<!.*|<ref.*|\[http://.*|\(Ruair.*?\)|\*)$", candidate)
            if mcandidatet:
                candidate = mcandidatet.group(1)
    
            mcandidatet = re.match("(?s)['\"]*(?:Sir |Rt |Right |Hon\.? |Rev\.? |Prof\.? |Miss |Mrs\.? |Ms |Maj\.-Gen\. |Lt\.-Col\. |Lt\.-Cmdr\. |Lt-Gen |Maj |Lt |Com |Col |Major |Major-General |Dr\.? |Brig |Gen |Gp |Capt\.? |Count |Captain |Commodore |Admiral |Lord |Lieutenant-Colonel |Commander |[WR]\. |Lieut Col |Lt-Col |Dame |Comm )*(.*?)(?:,? Bt\.?| CMG| KC| RN| [OKMCG]BE| MC| DSO| DFC| TD| KCB| CB| VRD| QC| MB| CSI| CIE| KCMG| GCB| LLD| MD| PhD| GCVO| \[\[Military Cross\|MC\]\]|, \[\[Royal Naval Volunteer Reserve\|RNVR\]\]|{{mnl}}| <sup>1</sup>\s*| \(PPC\)| \(incumbent\))*[\s'\"]*$", candidate)
            if mcandidatet:
                candidate = mcandidatet.group(1)

            # remove the target link in the pattern [[xxx|xxx]]
            mcandidate = re.match("(\[\[[^\]\|]+?)(?:\|[\s\S]+?)?\]\]$", candidate)
            if mcandidate:
                candidate = mcandidate.group(1) + "]]"
            
            # error in http://en.wikipedia.org/wiki/North_Antrim_(UK_Parliament_constituency)#Elections_in_the_1880s
            if candidate == "[William Pirrie Sinclair":
                candidate = "William Pirrie Sinclair"
            if candidate == "[[John_Hemming_%28politician%29]]":
                candidate = "[[John_Hemming_(politician)]]"
            if candidate == "[[Nikolai Tolstoy]]-Miloslavsky":
                candidate = "[[Nikolai Tolstoy]]"

            
            # there are problems with the ndash in these names where inserting one in this python code causes an exception and a 0 length file to be saved
            if candidate[:21] == "[[Richard Bethell (17":
                assert reading.name == "Yorkshire (UK Parliament constituency)", templ
            elif candidate[:13] == "[[George Byng":
                assert reading.name == "Middlesex (UK Parliament constituency)"
            elif candidate == "[[Oliver Baldwin]], [[Viscount Corvedale]]":
                pass
            
            elif candidate and candidate != "[to be confirmed]":
                assert re.match("(\[\[)?[\w\s,.\-'\"/\(\)\x80-\xe2]+(\]\])?$", candidate), [candidate, templ, electionname]
            else:
                assert party == "Others" or \
                       party == "others" or \
                       party == "non transferable" or \
                       reading.name == "Croydon North West (UK Parliament constituency)" or \
                       reading.name == "South Colchester and Maldon (UK Parliament constituency)" or \
                       reading.name == "Battersea (UK Parliament constituency)" or \
                       reading.name == "Kettering (UK Parliament constituency)" or \
                       reading.name == "Harlow (UK Parliament constituency)" or \
                       reading.name == "Epping Forest (UK Parliament constituency)" or \
                       reading.name == "North Essex (UK Parliament constituency)" or \
                       reading.name == "South East Cambridgeshire (UK Parliament constituency)" or \
                       reading.name == "Rochford and Southend East (UK Parliament constituency)" or \
                       reading.name == "Finchley and Golders Green (UK Parliament constituency)" or \
                       reading.name == "Bristol East (UK Parliament constituency)" or \
                       reading.name == "Glasgow Cathcart (UK Parliament constituency)" or \
                electionname == "next United Kingdom general election", \
                           [str(templ), electionname, reading.name]
            
            yield { "type":"candidate", "election":electionname, "constituency":reading.name, "votes":votes, "party":party, "candidate":candidate }
        elif templ[0] == "Election box end":
            electionname = None
    
def Collect():
    DynElection.objects.filter(source="wikipedia").delete()
    scrapermodule = ScraperModule.objects.get(modulename="wpelections")
    i = 0
    for detection in scrapermodule.detection_set.filter(status="parsed"):
        winningcandidate = None
        for kv in detection.contents():
            if kv["type"] == "election":
                if winningcandidate:
                    winningcandidate.winner = True
                    winningcandidate.save()
                winningcandidate = None
            if kv["type"] == "candidate":
                myear = re.search("(\d\d\d\d)", kv["election"])
                year = myear and myear.group(1) or "9999"
                if year > "1940":
                    detection = DynElection(election=kv["election"], year=year, party=kv["party"], votes=kv["votes"] or 0, constituency=kv["constituency"], candidate=kv["candidate"], source="wikipedia")
                    detection.save()
                    if not winningcandidate or winningcandidate.votes < detection.votes:
                        winningcandidate = detection
                    i += 1
                    if (i % 10) == 0:
                        print kv
        if winningcandidate:
            winningcandidate.winner = True
            winningcandidate.save()
                    
def GetInfobox(title, templs):
    for templ in templs:
        if templ[0] == title:
            return templ
    return None


# this parsing will find out if the percentage reported per election agrees with the vote tally
def GetElectionCandidates(templs):
    res = { }
    candidatelist = [ ]
    electionnames = [ ]
    for templ in templs:
        if templ[0] == "Election box begin":
            electionname = re.search("title=\[\[(.*?)[\|\]]", templ["title"]).group(1)
            electionnames.append(electionname)
            candidatelist = [ templ["title"] ]
            res[templ["title"]] = candidatelist
        elif re.match("Election box candidate", templ[0]):
            candidatelist.append(templ)
        elif templ[0] == "Election box end":
            candidatelist = [ ]

    print electionnames


def Parse(reading):
    templs = ParseTemplates(reading.contents())
    for templ in templs:
        if templ[0] == "Election box begin" or templ[0] == "Election box begin no clear":
            melectionname = re.search("\[\[(.*?)[\|\]]", templ["title"])
            electionname = melectionname and melectionname.group(1) or templ["title"]
            electionname = re.match("(.*?)\s*(\{\{.*|http://.*)?$", electionname).group(1)
            if electionname[:3] == "UK ":
                electionname = "United Kingdom " + electionname[3:]
            if electionname[:8] == "next UK ":
                electionname = "next United Kingdom " + electionname[8:]
            if electionname == "Next United Kingdom general election":
                electionname = "next United Kingdom general election"
            if electionname == "United Kingdom general election, 2010":
                electionname = "next United Kingdom general election"
                
            yield { "type":"election", "name":electionname }

        elif re.match("Election box candidate", templ[0]):
            # get rid of punctuation and references that sometimes gets added to the end
            svotes = re.sub(" \(\?\)$|<br[^\d]*$|[,. ]", "", templ["votes"])  
            
            if re.match("\d+$", svotes):
                votes = int(svotes)
            elif svotes in ["Unopposed", "Unoppose", "unopposed", "Elected", "Co-opted", "''N/A''", "''unopposed''", "(unopposed)", "''(unopposed)''", "''uncontested''", "Returned", "Returnedandseated", "Returnedandunseated", "Unknown"]:
                votes = 1
            elif svotes == "":
                votes = 0
            elif svotes == "Defeated":
                votes = 0
            else:
                assert False, "Unparsed votes: " + str(templ) + str([svotes])
                
            party = re.match("(.*?)\s*(\[?http://.*|{{|<!.*|<ref.*|<sup.*)?$", templ["party"]).group(1)
            mpartycat = re.match("(.*?)\[\[(.+?)[\|\]]", party)
            if mpartycat:
                party = mpartycat.group(1) + mpartycat.group(2)
            assert not re.search("\[|<", party), list(templ["party"])
                
            # clean up the candidate field so it contains no stray reference links
            candidate = templ["candidate"]
            mcandidatet = re.match("(.*?)\s*(<!.*|<ref.*|\[http://.*|\(Ruair.*?\)|\*)$", candidate)
            if mcandidatet:
                candidate = mcandidatet.group(1)
    
            mcandidatet = re.match("(?s)['\"]*(?:Sir |Rt |Right |Hon\.? |Rev\.? |Prof\.? |Miss |Mrs\.? |Ms |Maj\.-Gen\. |Lt\.-Col\. |Lt\.-Cmdr\. |Lt-Gen |Maj |Lt |Com |Col |Major |Major-General |Dr\.? |Brig |Gen |Gp |Capt\.? |Count |Captain |Commodore |Admiral |Lord |Lieutenant-Colonel |Commander |[WR]\. |Lieut Col |Lt-Col |Dame |Comm )*(.*?)(?:,? Bt\.?| CMG| KC| RN| [OKMCG]BE| MC| DSO| DFC| TD| KCB| CB| VRD| QC| MB| CSI| CIE| KCMG| GCB| LLD| MD| PhD| GCVO| \[\[Military Cross\|MC\]\]|, \[\[Royal Naval Volunteer Reserve\|RNVR\]\]|{{mnl}}| <sup>1</sup>\s*| \(PPC\)| \(incumbent\))*[\s'\"]*$", candidate)
            if mcandidatet:
                candidate = mcandidatet.group(1)

            # remove the target link in the pattern [[xxx|xxx]]
            mcandidate = re.match("(\[\[[^\]\|]+?)(?:\|[\s\S]+?)?\]\]$", candidate)
            if mcandidate:
                candidate = mcandidate.group(1) + "]]"
            
            # error in http://en.wikipedia.org/wiki/North_Antrim_(UK_Parliament_constituency)#Elections_in_the_1880s
            if candidate == "[William Pirrie Sinclair":
                candidate = "William Pirrie Sinclair"
            if candidate == "[[John_Hemming_%28politician%29]]":
                candidate = "[[John_Hemming_(politician)]]"
            if candidate == "[[Nikolai Tolstoy]]-Miloslavsky":
                candidate = "[[Nikolai Tolstoy]]"

            
            # there are problems with the ndash in these names where inserting one in this python code causes an exception and a 0 length file to be saved
            if candidate[:21] == "[[Richard Bethell (17":
                assert reading.name == "Yorkshire (UK Parliament constituency)", templ
            elif candidate[:13] == "[[George Byng":
                assert reading.name == "Middlesex (UK Parliament constituency)"
            elif candidate == "[[Oliver Baldwin]], [[Viscount Corvedale]]":
                pass
            
            elif candidate and candidate != "[to be confirmed]":
                assert re.match("(\[\[)?[\w\s,.\-'\"/\(\)\x80-\xe2]+(\]\])?$", candidate), [candidate, templ, electionname]
            else:
                assert party == "Others" or \
                       party == "others" or \
                       party == "non transferable" or \
                       reading.name == "Croydon North West (UK Parliament constituency)" or \
                       reading.name == "South Colchester and Maldon (UK Parliament constituency)" or \
                       reading.name == "Battersea (UK Parliament constituency)" or \
                       reading.name == "Kettering (UK Parliament constituency)" or \
                       reading.name == "Harlow (UK Parliament constituency)" or \
                       reading.name == "Epping Forest (UK Parliament constituency)" or \
                       reading.name == "North Essex (UK Parliament constituency)" or \
                       reading.name == "South East Cambridgeshire (UK Parliament constituency)" or \
                       reading.name == "Rochford and Southend East (UK Parliament constituency)" or \
                       reading.name == "Finchley and Golders Green (UK Parliament constituency)" or \
                       reading.name == "Bristol East (UK Parliament constituency)" or \
                       reading.name == "Glasgow Cathcart (UK Parliament constituency)" or \
                electionname == "next United Kingdom general election", \
                           [str(templ), electionname, reading.name]
            
            yield { "type":"candidate", "election":electionname, "constituency":reading.name, "votes":votes, "party":party, "candidate":candidate }
        elif templ[0] == "Election box end":
            electionname = None
    
def Collect():
    DynElection.objects.filter(source="wikipedia").delete()
    scrapermodule = ScraperModule.objects.get(modulename="wpelections")
    i = 0
    for detection in scrapermodule.detection_set.filter(status="parsed"):
        winningcandidate = None
        for kv in detection.contents():
            if kv["type"] == "election":
                if winningcandidate:
                    winningcandidate.winner = True
                    winningcandidate.save()
                winningcandidate = None
            if kv["type"] == "candidate":
                myear = re.search("(\d\d\d\d)", kv["election"])
                year = myear and myear.group(1) or "9999"
                if year > "1940":
                    detection = DynElection(election=kv["election"], year=year, party=kv["party"], votes=kv["votes"] or 0, constituency=kv["constituency"], candidate=kv["candidate"], source="wikipedia")
                    detection.save()
                    if not winningcandidate or winningcandidate.votes < detection.votes:
                        winningcandidate = detection
                    i += 1
                    if (i % 10) == 0:
                        print kv
        if winningcandidate:
            winningcandidate.winner = True
            winningcandidate.save()
                    
def GetInfobox(title, templs):
    for templ in templs:
        if templ[0] == title:
            return templ
    return None


# this parsing will find out if the percentage reported per election agrees with the vote tally
def GetElectionCandidates(templs):
    res = { }
    candidatelist = [ ]
    electionnames = [ ]
    for templ in templs:
        if templ[0] == "Election box begin":
            electionname = re.search("title=\[\[(.*?)[\|\]]", templ["title"]).group(1)
            electionnames.append(electionname)
            candidatelist = [ templ["title"] ]
            res[templ["title"]] = candidatelist
        elif re.match("Election box candidate", templ[0]):
            candidatelist.append(templ)
        elif templ[0] == "Election box end":
            candidatelist = [ ]

    print electionnames


def Parse(reading):
    templs = ParseTemplates(reading.contents())
    for templ in templs:
        if templ[0] == "Election box begin" or templ[0] == "Election box begin no clear":
            melectionname = re.search("\[\[(.*?)[\|\]]", templ["title"])
            electionname = melectionname and melectionname.group(1) or templ["title"]
            electionname = re.match("(.*?)\s*(\{\{.*|http://.*)?$", electionname).group(1)
            if electionname[:3] == "UK ":
                electionname = "United Kingdom " + electionname[3:]
            if electionname[:8] == "next UK ":
                electionname = "next United Kingdom " + electionname[8:]
            if electionname == "Next United Kingdom general election":
                electionname = "next United Kingdom general election"
            if electionname == "United Kingdom general election, 2010":
                electionname = "next United Kingdom general election"
                
            yield { "type":"election", "name":electionname }

        elif re.match("Election box candidate", templ[0]):
            # get rid of punctuation and references that sometimes gets added to the end
            svotes = re.sub(" \(\?\)$|<br[^\d]*$|[,. ]", "", templ["votes"])  
            
            if re.match("\d+$", svotes):
                votes = int(svotes)
            elif svotes in ["Unopposed", "Unoppose", "unopposed", "Elected", "Co-opted", "''N/A''", "''unopposed''", "(unopposed)", "''(unopposed)''", "''uncontested''", "Returned", "Returnedandseated", "Returnedandunseated", "Unknown"]:
                votes = 1
            elif svotes == "":
                votes = 0
            elif svotes == "Defeated":
                votes = 0
            else:
                assert False, "Unparsed votes: " + str(templ) + str([svotes])
                
            party = re.match("(.*?)\s*(\[?http://.*|{{|<!.*|<ref.*|<sup.*)?$", templ["party"]).group(1)
            mpartycat = re.match("(.*?)\[\[(.+?)[\|\]]", party)
            if mpartycat:
                party = mpartycat.group(1) + mpartycat.group(2)
            assert not re.search("\[|<", party), list(templ["party"])
                
            # clean up the candidate field so it contains no stray reference links
            candidate = templ["candidate"]
            mcandidatet = re.match("(.*?)\s*(<!.*|<ref.*|\[http://.*|\(Ruair.*?\)|\*)$", candidate)
            if mcandidatet:
                candidate = mcandidatet.group(1)
    
            mcandidatet = re.match("(?s)['\"]*(?:Sir |Rt |Right |Hon\.? |Rev\.? |Prof\.? |Miss |Mrs\.? |Ms |Maj\.-Gen\. |Lt\.-Col\. |Lt\.-Cmdr\. |Lt-Gen |Maj |Lt |Com |Col |Major |Major-General |Dr\.? |Brig |Gen |Gp |Capt\.? |Count |Captain |Commodore |Admiral |Lord |Lieutenant-Colonel |Commander |[WR]\. |Lieut Col |Lt-Col |Dame |Comm )*(.*?)(?:,? Bt\.?| CMG| KC| RN| [OKMCG]BE| MC| DSO| DFC| TD| KCB| CB| VRD| QC| MB| CSI| CIE| KCMG| GCB| LLD| MD| PhD| GCVO| \[\[Military Cross\|MC\]\]|, \[\[Royal Naval Volunteer Reserve\|RNVR\]\]|{{mnl}}| <sup>1</sup>\s*| \(PPC\)| \(incumbent\))*[\s'\"]*$", candidate)
            if mcandidatet:
                candidate = mcandidatet.group(1)

            # remove the target link in the pattern [[xxx|xxx]]
            mcandidate = re.match("(\[\[[^\]\|]+?)(?:\|[\s\S]+?)?\]\]$", candidate)
            if mcandidate:
                candidate = mcandidate.group(1) + "]]"
            
            # error in http://en.wikipedia.org/wiki/North_Antrim_(UK_Parliament_constituency)#Elections_in_the_1880s
            if candidate == "[William Pirrie Sinclair":
                candidate = "William Pirrie Sinclair"
            if candidate == "[[John_Hemming_%28politician%29]]":
                candidate = "[[John_Hemming_(politician)]]"
            if candidate == "[[Nikolai Tolstoy]]-Miloslavsky":
                candidate = "[[Nikolai Tolstoy]]"

            
            # there are problems with the ndash in these names where inserting one in this python code causes an exception and a 0 length file to be saved
            if candidate[:21] == "[[Richard Bethell (17":
                assert reading.name == "Yorkshire (UK Parliament constituency)", templ
            elif candidate[:13] == "[[George Byng":
                assert reading.name == "Middlesex (UK Parliament constituency)"
            elif candidate == "[[Oliver Baldwin]], [[Viscount Corvedale]]":
                pass
            
            elif candidate and candidate != "[to be confirmed]":
                assert re.match("(\[\[)?[\w\s,.\-'\"/\(\)\x80-\xe2]+(\]\])?$", candidate), [candidate, templ, electionname]
            else:
                assert party == "Others" or \
                       party == "others" or \
                       party == "non transferable" or \
                       reading.name == "Croydon North West (UK Parliament constituency)" or \
                       reading.name == "South Colchester and Maldon (UK Parliament constituency)" or \
                       reading.name == "Battersea (UK Parliament constituency)" or \
                       reading.name == "Kettering (UK Parliament constituency)" or \
                       reading.name == "Harlow (UK Parliament constituency)" or \
                       reading.name == "Epping Forest (UK Parliament constituency)" or \
                       reading.name == "North Essex (UK Parliament constituency)" or \
                       reading.name == "South East Cambridgeshire (UK Parliament constituency)" or \
                       reading.name == "Rochford and Southend East (UK Parliament constituency)" or \
                       reading.name == "Finchley and Golders Green (UK Parliament constituency)" or \
                       reading.name == "Bristol East (UK Parliament constituency)" or \
                       reading.name == "Glasgow Cathcart (UK Parliament constituency)" or \
                electionname == "next United Kingdom general election", \
                           [str(templ), electionname, reading.name]
            
            yield { "type":"candidate", "election":electionname, "constituency":reading.name, "votes":votes, "party":party, "candidate":candidate }
        elif templ[0] == "Election box end":
            electionname = None
    
def Collect():
    DynElection.objects.filter(source="wikipedia").delete()
    scrapermodule = ScraperModule.objects.get(modulename="wpelections")
    i = 0
    for detection in scrapermodule.detection_set.filter(status="parsed"):
        winningcandidate = None
        for kv in detection.contents():
            if kv["type"] == "election":
                if winningcandidate:
                    winningcandidate.winner = True
                    winningcandidate.save()
                winningcandidate = None
            if kv["type"] == "candidate":
                myear = re.search("(\d\d\d\d)", kv["election"])
                year = myear and myear.group(1) or "9999"
                if year > "1940":
                    detection = DynElection(election=kv["election"], year=year, party=kv["party"], votes=kv["votes"] or 0, constituency=kv["constituency"], candidate=kv["candidate"], source="wikipedia")
                    detection.save()
                    if not winningcandidate or winningcandidate.votes < detection.votes:
                        winningcandidate = detection
                    i += 1
                    if (i % 10) == 0:
                        print kv
        if winningcandidate:
            winningcandidate.winner = True
            winningcandidate.save()
                    
def GetInfobox(title, templs):
    for templ in templs:
        if templ[0] == title:
            return templ
    return None


# this parsing will find out if the percentage reported per election agrees with the vote tally
def GetElectionCandidates(templs):
    res = { }
    candidatelist = [ ]
    electionnames = [ ]
    for templ in templs:
        if templ[0] == "Election box begin":
            electionname = re.search("title=\[\[(.*?)[\|\]]", templ["title"]).group(1)
            electionnames.append(electionname)
            candidatelist = [ templ["title"] ]
            res[templ["title"]] = candidatelist
        elif re.match("Election box candidate", templ[0]):
            candidatelist.append(templ)
        elif templ[0] == "Election box end":
            candidatelist = [ ]

    print electionnames


def Parse(reading):
    templs = ParseTemplates(reading.contents())
    for templ in templs:
        if templ[0] == "Election box begin" or templ[0] == "Election box begin no clear":
            melectionname = re.search("\[\[(.*?)[\|\]]", templ["title"])
            electionname = melectionname and melectionname.group(1) or templ["title"]
            electionname = re.match("(.*?)\s*(\{\{.*|http://.*)?$", electionname).group(1)
            if electionname[:3] == "UK ":
                electionname = "United Kingdom " + electionname[3:]
            if electionname[:8] == "next UK ":
                electionname = "next United Kingdom " + electionname[8:]
            if electionname == "Next United Kingdom general election":
                electionname = "next United Kingdom general election"
            if electionname == "United Kingdom general election, 2010":
                electionname = "next United Kingdom general election"
                
            yield { "type":"election", "name":electionname }

        elif re.match("Election box candidate", templ[0]):
            # get rid of punctuation and references that sometimes gets added to the end
            svotes = re.sub(" \(\?\)$|<br[^\d]*$|[,. ]", "", templ["votes"])  
            
            if re.match("\d+$", svotes):
                votes = int(svotes)
            elif svotes in ["Unopposed", "Unoppose", "unopposed", "Elected", "Co-opted", "''N/A''", "''unopposed''", "(unopposed)", "''(unopposed)''", "''uncontested''", "Returned", "Returnedandseated", "Returnedandunseated", "Unknown"]:
                votes = 1
            elif svotes == "":
                votes = 0
            elif svotes == "Defeated":
                votes = 0
            else:
                assert False, "Unparsed votes: " + str(templ) + str([svotes])
                
            party = re.match("(.*?)\s*(\[?http://.*|{{|<!.*|<ref.*|<sup.*)?$", templ["party"]).group(1)
            mpartycat = re.match("(.*?)\[\[(.+?)[\|\]]", party)
            if mpartycat:
                party = mpartycat.group(1) + mpartycat.group(2)
            assert not re.search("\[|<", party), list(templ["party"])
                
            # clean up the candidate field so it contains no stray reference links
            candidate = templ["candidate"]
            mcandidatet = re.match("(.*?)\s*(<!.*|<ref.*|\[http://.*|\(Ruair.*?\)|\*)$", candidate)
            if mcandidatet:
                candidate = mcandidatet.group(1)
    
            mcandidatet = re.match("(?s)['\"]*(?:Sir |Rt |Right |Hon\.? |Rev\.? |Prof\.? |Miss |Mrs\.? |Ms |Maj\.-Gen\. |Lt\.-Col\. |Lt\.-Cmdr\. |Lt-Gen |Maj |Lt |Com |Col |Major |Major-General |Dr\.? |Brig |Gen |Gp |Capt\.? |Count |Captain |Commodore |Admiral |Lord |Lieutenant-Colonel |Commander |[WR]\. |Lieut Col |Lt-Col |Dame |Comm )*(.*?)(?:,? Bt\.?| CMG| KC| RN| [OKMCG]BE| MC| DSO| DFC| TD| KCB| CB| VRD| QC| MB| CSI| CIE| KCMG| GCB| LLD| MD| PhD| GCVO| \[\[Military Cross\|MC\]\]|, \[\[Royal Naval Volunteer Reserve\|RNVR\]\]|{{mnl}}| <sup>1</sup>\s*| \(PPC\)| \(incumbent\))*[\s'\"]*$", candidate)
            if mcandidatet:
                candidate = mcandidatet.group(1)

            # remove the target link in the pattern [[xxx|xxx]]
            mcandidate = re.match("(\[\[[^\]\|]+?)(?:\|[\s\S]+?)?\]\]$", candidate)
            if mcandidate:
                candidate = mcandidate.group(1) + "]]"
            
            # error in http://en.wikipedia.org/wiki/North_Antrim_(UK_Parliament_constituency)#Elections_in_the_1880s
            if candidate == "[William Pirrie Sinclair":
                candidate = "William Pirrie Sinclair"
            if candidate == "[[John_Hemming_%28politician%29]]":
                candidate = "[[John_Hemming_(politician)]]"
            if candidate == "[[Nikolai Tolstoy]]-Miloslavsky":
                candidate = "[[Nikolai Tolstoy]]"

            
            # there are problems with the ndash in these names where inserting one in this python code causes an exception and a 0 length file to be saved
            if candidate[:21] == "[[Richard Bethell (17":
                assert reading.name == "Yorkshire (UK Parliament constituency)", templ
            elif candidate[:13] == "[[George Byng":
                assert reading.name == "Middlesex (UK Parliament constituency)"
            elif candidate == "[[Oliver Baldwin]], [[Viscount Corvedale]]":
                pass
            
            elif candidate and candidate != "[to be confirmed]":
                assert re.match("(\[\[)?[\w\s,.\-'\"/\(\)\x80-\xe2]+(\]\])?$", candidate), [candidate, templ, electionname]
            else:
                assert party == "Others" or \
                       party == "others" or \
                       party == "non transferable" or \
                       reading.name == "Croydon North West (UK Parliament constituency)" or \
                       reading.name == "South Colchester and Maldon (UK Parliament constituency)" or \
                       reading.name == "Battersea (UK Parliament constituency)" or \
                       reading.name == "Kettering (UK Parliament constituency)" or \
                       reading.name == "Harlow (UK Parliament constituency)" or \
                       reading.name == "Epping Forest (UK Parliament constituency)" or \
                       reading.name == "North Essex (UK Parliament constituency)" or \
                       reading.name == "South East Cambridgeshire (UK Parliament constituency)" or \
                       reading.name == "Rochford and Southend East (UK Parliament constituency)" or \
                       reading.name == "Finchley and Golders Green (UK Parliament constituency)" or \
                       reading.name == "Bristol East (UK Parliament constituency)" or \
                       reading.name == "Glasgow Cathcart (UK Parliament constituency)" or \
                electionname == "next United Kingdom general election", \
                           [str(templ), electionname, reading.name]
            
            yield { "type":"candidate", "election":electionname, "constituency":reading.name, "votes":votes, "party":party, "candidate":candidate }
        elif templ[0] == "Election box end":
            electionname = None
    
def Collect():
    DynElection.objects.filter(source="wikipedia").delete()
    scrapermodule = ScraperModule.objects.get(modulename="wpelections")
    i = 0
    for detection in scrapermodule.detection_set.filter(status="parsed"):
        winningcandidate = None
        for kv in detection.contents():
            if kv["type"] == "election":
                if winningcandidate:
                    winningcandidate.winner = True
                    winningcandidate.save()
                winningcandidate = None
            if kv["type"] == "candidate":
                myear = re.search("(\d\d\d\d)", kv["election"])
                year = myear and myear.group(1) or "9999"
                if year > "1940":
                    detection = DynElection(election=kv["election"], year=year, party=kv["party"], votes=kv["votes"] or 0, constituency=kv["constituency"], candidate=kv["candidate"], source="wikipedia")
                    detection.save()
                    if not winningcandidate or winningcandidate.votes < detection.votes:
                        winningcandidate = detection
                    i += 1
                    if (i % 10) == 0:
                        print kv
        if winningcandidate:
            winningcandidate.winner = True
            winningcandidate.save()
                    