import scraperwiki
from bs4 import BeautifulSoup 

# Blank Python
scraperwiki.sqlite.attach("dod-contracts")
links = scraperwiki.sqlite.select("URL from `dod-contracts`.swdata")

counter=0

for link in links:
    url=link["URL"] #to access the value of a dictionary
    #print url

#now run the URL
    html = scraperwiki.scrape(url)
    data = {"html": html, "url": url} #saving the HTML and URL data in a dictionary
    soup = BeautifulSoup(html)
    title = soup.find("div","inner maintext").get_text().strip().replace("\n", "").replace("\t", "").replace("\r","")
    print title

    start= title.find("Reference number:")+18
    end= title.find("Estimated length of contract")
    refno = title[start:end].strip()

    start= title.find("Estimated length of contract")+29
    end= title.find("Awarded value")
    contractLength = title[start:end].strip()
    contractLength.replace("English","")

    start= title.find("Awarded value")+13
    end= title.find("Location where the contract")
    awardedValue = title[start:end].strip()
    awardedValue.replace("English","")

    start= title.find("Location where the contract is to be carried out:")+49
    end= title.find("Name of the buying")
    country = title[start:end].strip()
    country.replace("English","")

    start= title.find("Name of the buying organisation:")+32
    end= len(title)
    buyingOrg = title[start:end].strip()
    buyingOrg = buyingOrg[7:]

    print refno
    print contractLength
    print awardedValue
    print country
    print buyingOrg

    data={"URL": url, "REF": refno, "CON":contractLength, "VAL":awardedValue, "COU":country , "ORG":buyingOrg ,"id": counter}
    scraperwiki.sqlite.save(["id"], data)
    counter +=1


"""
Reference number: MedGS/0102

Estimated length of contract: 16/06/2012 - 15/06/2013

Awarded value£13,832

Location where the contract is to be carried out:
United Kingdom
Name of the buying organisation:
Ministry of Defence
"""
import scraperwiki
from bs4 import BeautifulSoup 

# Blank Python
scraperwiki.sqlite.attach("dod-contracts")
links = scraperwiki.sqlite.select("URL from `dod-contracts`.swdata")

counter=0

for link in links:
    url=link["URL"] #to access the value of a dictionary
    #print url

#now run the URL
    html = scraperwiki.scrape(url)
    data = {"html": html, "url": url} #saving the HTML and URL data in a dictionary
    soup = BeautifulSoup(html)
    title = soup.find("div","inner maintext").get_text().strip().replace("\n", "").replace("\t", "").replace("\r","")
    print title

    start= title.find("Reference number:")+18
    end= title.find("Estimated length of contract")
    refno = title[start:end].strip()

    start= title.find("Estimated length of contract")+29
    end= title.find("Awarded value")
    contractLength = title[start:end].strip()
    contractLength.replace("English","")

    start= title.find("Awarded value")+13
    end= title.find("Location where the contract")
    awardedValue = title[start:end].strip()
    awardedValue.replace("English","")

    start= title.find("Location where the contract is to be carried out:")+49
    end= title.find("Name of the buying")
    country = title[start:end].strip()
    country.replace("English","")

    start= title.find("Name of the buying organisation:")+32
    end= len(title)
    buyingOrg = title[start:end].strip()
    buyingOrg = buyingOrg[7:]

    print refno
    print contractLength
    print awardedValue
    print country
    print buyingOrg

    data={"URL": url, "REF": refno, "CON":contractLength, "VAL":awardedValue, "COU":country , "ORG":buyingOrg ,"id": counter}
    scraperwiki.sqlite.save(["id"], data)
    counter +=1


"""
Reference number: MedGS/0102

Estimated length of contract: 16/06/2012 - 15/06/2013

Awarded value£13,832

Location where the contract is to be carried out:
United Kingdom
Name of the buying organisation:
Ministry of Defence
"""
