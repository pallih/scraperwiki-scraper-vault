import scraperwiki
import requests

# Italy's registry of companies

URL = 'http://www.registroimprese.it/dama/comc/navcom'

# For each query, we get no more than 250 results, paged as 10 results per page
# (can be changed to 20). But we also get an overall amount of the number of
# matching items, that can be used as a "progress indicator".
#
# The strategy is very simple. Using a hand-crafted dictionary (perhaps kept in a github
# repo so it's easily updated with suggestions and requests) we pick a random
# word and try to get as many results as we can. The order of results is not random,
# apparently.
#
# In the results page, each company is embedded in a separate form, named "formV1",
# "formV2" and so on. To get to the detail page, it should be enough to POST the
# form. The detail page can be scraped.
#
# IMPORTANT: there is no way to obtain the registration number (partita IVA) from the
# public registry. One has to be registered, and probably also to pay for the service.
# As a consequence, it is not easy to uniquely identify a company. A cautious approach
# will be taken, composing the name, address, phone number and activity.

# Example of POST parameters to the search endpoint
# It is not enough - an error is shown
params = {
    'provenienza': 'home',
    'attivazioneCaptcha': '',
    'azione': 'ricercaXml',
    'base': '/dama/comc/comc/IT/',
    'modalita': '',
    'tipo': 'impresa',
    'cl': 'IT',
    'abbrevNazione': '',
    'exteNazione': '',
    'territorio': '',
    'nazione': '',
    'ricerca': 'gino',
    'numero': '',
    'textfieldcaptcha': '',
    }

r = requests.post(URL, params=params)

print r.text
