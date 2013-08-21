import BeautifulSoup
import scraperwiki
from scraperwiki import datastore

url = "http://www.merseyside.police.uk/index.aspx?articleid=1176&area=Mossley%20Hill&areaid=1304"
    
html = scraperwiki.scrape(url)
page = BeautifulSoup.BeautifulSoup(html, fromEncoding="utf-8", convertEntities=BeautifulSoup.BeautifulSoup.HTML_ENTITIES)
data={}
data ["id"] = 1304
data["address"]=page.find(attrs={"class":"sidebar-list"}) .li .a .contents [0]
data["opening times"]= page.find("span",attrs={"id":"openhours"}) .contents [0]
data["image"]= page.find(attrs={"id":"stationwrapper"}) .find ("img") ["src"]
datastore.save(unique_keys=["id"], data=data)

"""
    <img src="./media/station/b/h/allerton1.jpg" alt="" /> 
                                    
                        <span id="stationpointer"></span>

                        <div class="main-header" style="width: 281px; margin-top: -10px;">Your local police station</div>
                        <div class="container leftcol">
                            <ul class="sidebar-list">
                                <li><a href="index.aspx?articleid=2696">
                                    
                                        Rose Lane,
                                    
                                    
                                        Allerton,
                                    
                                    
                                        L18 6JE,
                                    
                                    
                                </a></li>
                            </ul>
                            <span id="openhours">Mon - Sun 8am 11pm</span>

                            <div style="clear: both;"></div>
"""