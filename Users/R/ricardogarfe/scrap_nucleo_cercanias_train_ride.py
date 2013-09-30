'''Copyright [2012] [Ricardo García Fernández]

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

'''

import scraperwiki
from lxml.html import fromstring, tostring, parse, submit_form
import mechanize

params = { "ciudad":"valencia", "nucleo":"40"}

base_url = "http://renfe.mobi/renfev2/hora_ga_cercanias.do?ss=DE7041DE00BB11DECBEF1BBBEA591BD6&ciudad=murciaalicante&nucleo=41"

output_url = "http://renfe.mobi/renfev2/resultado_cercanias.do"

'''
html = scraperwiki.scrape(base_url, params)

root = fromstring(html)

print tostring(root)

for form in root.forms:
    print type(form), form.action, form.inputs, form.fields['o'], type(form.fields['o'])
'''

# Mechanize
br = mechanize.Browser()

response = br.open(base_url)

for form in br.forms():
    print form.name

print response

# form.action = 'http://horarios.renfe.com/cer/hjcer300.jsp'
'''form.fields['o'] = '67211'
form.fields['d'] = '65207'

result = parse(submit_form(form)).getroot()

print tostring(result)
'''
# <class 'lxml.html.FormElement'> /cer/hjcer310.jsp <InputGetter for form f1> ['i', 'cp', 'nucleo', 'd', 'o']
# nucleo=40&i=s&cp=NO&o=67211&d=65207&df=20121219&ho=00&hd=26&TXTInfo=
'''Copyright [2012] [Ricardo García Fernández]

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

'''

import scraperwiki
from lxml.html import fromstring, tostring, parse, submit_form
import mechanize

params = { "ciudad":"valencia", "nucleo":"40"}

base_url = "http://renfe.mobi/renfev2/hora_ga_cercanias.do?ss=DE7041DE00BB11DECBEF1BBBEA591BD6&ciudad=murciaalicante&nucleo=41"

output_url = "http://renfe.mobi/renfev2/resultado_cercanias.do"

'''
html = scraperwiki.scrape(base_url, params)

root = fromstring(html)

print tostring(root)

for form in root.forms:
    print type(form), form.action, form.inputs, form.fields['o'], type(form.fields['o'])
'''

# Mechanize
br = mechanize.Browser()

response = br.open(base_url)

for form in br.forms():
    print form.name

print response

# form.action = 'http://horarios.renfe.com/cer/hjcer300.jsp'
'''form.fields['o'] = '67211'
form.fields['d'] = '65207'

result = parse(submit_form(form)).getroot()

print tostring(result)
'''
# <class 'lxml.html.FormElement'> /cer/hjcer310.jsp <InputGetter for form f1> ['i', 'cp', 'nucleo', 'd', 'o']
# nucleo=40&i=s&cp=NO&o=67211&d=65207&df=20121219&ho=00&hd=26&TXTInfo=
