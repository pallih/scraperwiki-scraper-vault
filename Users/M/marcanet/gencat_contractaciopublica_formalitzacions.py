import requests   
  
r = requests.get('https://contractaciopublica.gencat.cat/ecofin_pscp/AppJava/search.pscp?reqCode=searchDcan&pagingPage=1&advancedSearch=false&lawType=2', verify=False)
html = r.text
print html                                                                                              

