from scraperwiki import swimport
from scraperwiki.sqlite import save
from time import time
dsp=swimport('dsp').dsp
import re
DATE=time()

def main():
  xml=dsp('http://www.finabank.com/rw/locator_kimathi.php',False)
  ps=xml.xpath('//p[@align="center"][strong]')
  d = []
  for p in ps:
    row = parse_p(p)
    row['date_scraped'] = DATE
    d.append(row)
  save([], d)

def parse_p(p):
  name='\n'.join(p.xpath('strong/text()'))
  contact='\n'.join(p.xpath('text()'))
  split_contact = re.split(r'[\n\r]+', contact)
  for nothing in [' ', '']:
    if nothing in split_contact:
      split_contact.remove(nothing)
    if len(split_contact[0]) <= 1:
      split_contact.pop(0)

  if "Tel" in split_contact[1] and len(split_contact) == 4:
    split_contact.pop()

  if "Tel" not in split_contact[1]:
    pobox = split_contact.pop(1)
    split_contact[0]+='\n' + pobox

  if len(split_contact) != 3:
    print split_contact

  street, tel, fax = split_contact[0:3]
  assert "Tel" in tel, split_contact
  assert "Fax" in fax, split_contact
  street = street.strip()
  tel=''.join(i for i in tel if i.isdigit())
  fax=''.join(i for i in fax if i.isdigit())

  return {
    "name": name,
    "town": name.split('Branch')[0].strip(),
    "street-address": street,
    "fax": fax,
    "phone": tel,
  }

main()