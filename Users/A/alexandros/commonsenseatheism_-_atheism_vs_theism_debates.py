import scraperwiki
import urllib, urlparse
import lxml.etree, lxml.html
import re

url = "http://commonsenseatheism.com/?p=50"

def Main():
    root = lxml.html.parse(url).getroot()

    debtbl = root.find("body/div/div").findall("div")[1].find("div/div").findall("div")[1].find("table/tbody")

    for i,entry in enumerate(debtbl): 
        debate = {}
        debate['id'] = i
        debate["Atheist"] = entry.findall("td")[0].text # column name and value
        debate["Theist"] = entry.findall("td")[1].text # column name and value


        elm = entry.findall("td")[2].findall("a") # column name and value
        debate["Video"] = []
        for item in elm: 
            debate["Video"].append({"type":item.text, "url":item.get('href')})

        elm = entry.findall("td")[3].findall("a") # column name and value
        debate["Audio"] = []
        for item in elm: 
            debate["Audio"].append({"type":item.text, "url":item.get('href')})

        elm = entry.findall("td")[4].findall("a") # column name and value
        debate["Text"] = []
        for item in elm: 
            debate["Text"].append({"type":item.text, "url":item.get('href')})


        debate["Year"] = entry.findall("td")[5].text # column name and value
        debate["Notes"] = entry.findall("td")[6].text

        scraperwiki.sqlite.save(["id"], debate) # save the records one by one
        
Main()

                        

