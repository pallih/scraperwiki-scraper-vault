import requests

r=requests.get("http://www.elections.ny.gov:8080/plsql_browser/CONTRIBUTORA_COUNTY?ID_in=A19043&date_From=03/12/2011&date_to=09/12/2011&AMOUNT_From=0&AMOUNT_to=100000&ZIP1=10000&ZIP2=15000&ORDERBY_IN=N&CATEGORY_IN=ALL",
    headers={"User-Agent":"User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_5_8) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.77 Safari/535.7"}
)

print r.contentimport requests

r=requests.get("http://www.elections.ny.gov:8080/plsql_browser/CONTRIBUTORA_COUNTY?ID_in=A19043&date_From=03/12/2011&date_to=09/12/2011&AMOUNT_From=0&AMOUNT_to=100000&ZIP1=10000&ZIP2=15000&ORDERBY_IN=N&CATEGORY_IN=ALL",
    headers={"User-Agent":"User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_5_8) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.77 Safari/535.7"}
)

print r.content