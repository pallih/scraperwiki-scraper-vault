import scraperwiki
import lxml.html as lh
import requests

u"""
名前の取得先：
http://www.socialsecurity.gov/cgi-bin/popularnames.cgi
1879-2011 のアメリカの男女上位1000の名前が得られる。
postリクエストで渡すべき変数：
"year"      : 1880 - 2011
"top"       : 1000
"number"    : "p"

"""

URL = "http://www.socialsecurity.gov/cgi-bin/popularnames.cgi"

def get_html(year):
    params = {\
    "year"   : year,
    "top"    : 1000,
    "number" : "p",
    }

    r = requests.post(URL,data=params)
    s = r.text
    r.close()
    return s

def main():
    years = range(1880,2013)
    
    for y in years:
        element = lh.fromstring(get_html(y))
        
        for subelem in element.findall('.//tr[@align="right"]'):
            number,male_name,male_ratio,female_name,female_ratio = [e.text for e in list(subelem)]

            male_data = {\
            "year"   : y,
            "rank"   : number,
            "name"   : male_name,
            "percent": male_ratio,
            "sex"    : "male",
            }

            female_data = {\
            "year"   : y,
            "rank"   : number,
            "name"   : female_name,
            "percent": female_ratio,
            "sex"    : "female",
            }

            for data in [male_data,female_data]:
                scraperwiki.sqlite.save(unique_keys=["year","rank","sex"],data=data)


main()