import requests
import lxml.html

url = 'http://www.lollapalooza.com/tickets/'
changed = False

resp = requests.get(url)
root = lxml.html.fromstring(resp.text)

ticket_choices = [el.text_content().lower() for el in root.cssselect(".ticket-choice")]

if len(ticket_choices) != 3:
    changed = True

for choice in ticket_choices:
    if "souvenir" in choice:
        print choice
        if "soon" not in choice:
            changed = True
        break

print changed
