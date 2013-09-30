#!/usr/bin/env ruby

require 'scraperwiki'
require 'rfgraph'

unique_keys = [ 'InitialFBURL' ]

# Test data set.  Will be loaded in through a custom tool in the future.

# Test data set.  Will be loaded in through a custom tool in the future.
CompanyArray =["https://www.facebook.com/actionwater",
"https://www.facebook.com/AdrenalineRefined",
"https://www.facebook.com/AdvancedMarina",
"https://www.facebook.com/AmericanBoatCenter",
"https://www.facebook.com/AsBoats",
"https://www.facebook.com/barnesboats",
"https://www.facebook.com/BillsOutdoors",
"https://www.facebook.com/bluespringsmarine?filter=2",
"https://www.facebook.com/boatreeds",
"https://www.facebook.com/bretzrvandmarine?ref=stream&hc_location=stream",
"https://www.facebook.com/buckeyebobcaygeon",
"https://www.facebook.com/BuzzsMarine/timeline?filter=1",
"https://www.facebook.com/ccmboats",
"https://www.facebook.com/cecilmarine",
"https://www.facebook.com/crowemarine?ref=stream&hc_location=stream",
"https://www.facebook.com/FaysBoatYard/timeline?filter=1",
"https://www.facebook.com/FishTaleSales",
"https://www.facebook.com/fredricksmarine?rf=144176245618564",
"https://www.facebook.com/idahowatersports",
"https://www.facebook.com/IntermarineBoats",
"https://www.facebook.com/LaceysBoatingCenter?v=wall",
"https://www.facebook.com/lancastercountymarineinc",
"https://www.facebook.com/MagnumBoating",
"https://www.facebook.com/nicholsmarinegrand/timeline?filter=1",
"https://www.facebook.com/oakhillmarina?fref=ts&filter=2",
"https://www.facebook.com/pages/Amity-Harbor-Marine/229856547030305",
"https://www.facebook.com/pages/Barling-Boat-Sales/344289653620?sk=page_map",
"https://www.facebook.com/pages/Barling-Boat-Sales/344289653620?sk=page_map",
"https://www.facebook.com/pages/Boaters-Point/244154331005",
"https://www.facebook.com/pages/Boats-Unlimited-NC/343527748992202",
"https://www.facebook.com/pages/Bosuns-Marine/282719207167",
"https://www.facebook.com/pages/Capri-Marine/112172762143413?rf=152542134787723",
"https://www.facebook.com/pages/Centerville-Marina/414439288603637",
"https://www.facebook.com/pages/Colorado-Boat-Center/182684848323",
"https://www.facebook.com/pages/Dealers-Choice-Marine/190905323323",
"https://www.facebook.com/pages/DRY-DOCK-MARINE-CENTER/38743104028?sk=info",
"https://www.facebook.com/pages/GORDON-MARINE-LTD/422591025283",
"https://www.facebook.com/pages/Jacksonville-Boat-Sales/142513282568307",
"https://www.facebook.com/pages/Jims-Anchorage/126811547343121?hc_location=timeline",
"https://www.facebook.com/pages/Krenzer-Marine/165211693556806",
"https://www.facebook.com/pages/Lakeside-Marina/115838075098256",
"https://www.facebook.com/pages/Longshore-Boats/339148451681",
"https://www.facebook.com/pages/Lookout-Marine-Sales/195198357280507",
"https://www.facebook.com/pages/Main-Marine-Ski-INC/277107908081?sk=wall",
"https://www.facebook.com/pages/Marine-Service-Center-of-Little-River/124095267608156",
"https://www.facebook.com/pages/Master-Marine-Inc/460432310674103",
"https://www.facebook.com/pages/Mattas-Marine-RV/193960773966201?fref=ts",
"https://www.facebook.com/pages/Modern-Marine/375952565765328",
"https://www.facebook.com/pages/Montana-Honda-and-Marine/110086322491729?ref=tn_tnmn",
"https://www.facebook.com/pages/Munson-Ski-Marine/131040552795",
"https://www.facebook.com/pages/OffShore-Marine/104492916346447",
"https://www.facebook.com/pages/OLIVERS-41-MARINE/253368002093",
"https://www.facebook.com/pages/Park-Boat-Company/134137478657",
"https://www.facebook.com/pages/Pilot-Knob-Marina/500563665474",
"https://www.facebook.com/pages/Premier-54-Motor-Sports/113539895382270?rf=138462762891791",
"https://www.facebook.com/pages/Proctor-Marine-Limited/123032104443722",
"https://www.facebook.com/pages/Rainbow-Cycle-Marine/157882547641125?rf=122628947785990",
"https://www.facebook.com/pages/Robbins-Marine/102673833737?ref=stream&hc_location=timeline",
"https://www.facebook.com/pages/Seattle-Waters-Sports/124464967129",
"https://www.facebook.com/pages/Ski-Dock/187048344644083?rf=193548370665864",
"https://www.facebook.com/pages/Strickland-Marine-Center/254792470439",
"https://www.facebook.com/pages/Texas-Marine/107957579496",
"https://www.facebook.com/pages/The-Harbor/135219949870052",
"https://www.facebook.com/pages/Tillys-Marine/117796348299096?ref=ts&fref=ts",
"https://www.facebook.com/pages/Trojan-Landing/186675821353473?sk=page_map",
"https://www.facebook.com/pages/Whites-Cycle-Marine/150395631653891",
"https://www.facebook.com/PerformanceMarine",
"https://www.facebook.com/performanceregina",
"https://www.facebook.com/Pier33Marina/timeline",
"https://www.facebook.com/PlanoMarine",
"https://www.facebook.com/poplarpointemarine",
"https://www.facebook.com/pridemarinegroupinc/page_map",
"https://www.facebook.com/RallyMotorsports",
"https://www.facebook.com/RichardsonsBY",
"https://www.facebook.com/snug.marina",
"https://www.facebook.com/ssmarineutah1",
"https://www.facebook.com/SunCountryMarine",
"https://www.facebook.com/SunriseMarine",
"https://www.facebook.com/theboatrack",
"https://www.facebook.com/ToblerMarina?v=wall&filter=1",
"https://www.facebook.com/WaterfrontMarine",
"https://www.facebook.com/wayzatamarine"]

CompanyArray.each do |companyURL|
    req = RFGraph::Request.new     
    res= req.get_object(companyURL)  #Can get by name, ID, or full URL

    data = { 'InitialFBURL'=>companyURL, 'CompanyName'=>res["name"], 'Website'=>res["website"], 'Likes'=>res["likes"],
        'TalkingAbout'=>res["talking_about_count"], 'WereHere'=>res["were_here_count"],'FacebookURL'=>res["link"],'FacebookID'=>res["id"]}
       
    ScraperWiki.save_sqlite(unique_keys, data)
end


