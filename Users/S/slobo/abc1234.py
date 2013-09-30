import json,urllib
data = urllib.urlopen("http://pipes.yahoo.com/pipes/pipe.run?_id=8511da59eb00dce51878dde76f66bf77&_render=json").read()
d = json.loads(data)
print "<html><body><table border='1'>"
print "<tr><th>Addresse</th><th>Bezeichnung</th><th>Beschreibung</th><th>gesamtkosten</th><th>flaeche</th></tr>"
t = ""
for counter in [0,1,2,3]:
    try:
        for x in d["value"]["items"][counter]["wohnung"]:
                print "<tr>"
                try:
                    print "<td>", t.join(x["adresse"]),"</td>"
                except KeyError:
                    print ''
                except TypeError:
                    print ''
                try:
                    print "<td>", t.join(x["bezeichnung"]), "</td>"
                except KeyError:
                    print ''
                except TypeError:
                    print ''
                try:
                    print "<td>", t.join(x["beschreibung"]), "</td>"
                except KeyError:
                    print ''
                except TypeError:
                    print ''
                try:
                    print "<td>", t.join(x["gesamtkosten"]), "</td>"
                except KeyError:
                    print ''
                except TypeError:
                    print ''
                try:
                    print "<td>", t.join(x["flaeche"]), "</td>"
                except KeyError:
                    print ''
                except TypeError:
                    print ''
                print "</tr>"
    except IndexError:
        print "Warning: not all sources loaded <br>"
print "</body></html>"




import json,urllib
data = urllib.urlopen("http://pipes.yahoo.com/pipes/pipe.run?_id=8511da59eb00dce51878dde76f66bf77&_render=json").read()
d = json.loads(data)
print "<html><body><table border='1'>"
print "<tr><th>Addresse</th><th>Bezeichnung</th><th>Beschreibung</th><th>gesamtkosten</th><th>flaeche</th></tr>"
t = ""
for counter in [0,1,2,3]:
    try:
        for x in d["value"]["items"][counter]["wohnung"]:
                print "<tr>"
                try:
                    print "<td>", t.join(x["adresse"]),"</td>"
                except KeyError:
                    print ''
                except TypeError:
                    print ''
                try:
                    print "<td>", t.join(x["bezeichnung"]), "</td>"
                except KeyError:
                    print ''
                except TypeError:
                    print ''
                try:
                    print "<td>", t.join(x["beschreibung"]), "</td>"
                except KeyError:
                    print ''
                except TypeError:
                    print ''
                try:
                    print "<td>", t.join(x["gesamtkosten"]), "</td>"
                except KeyError:
                    print ''
                except TypeError:
                    print ''
                try:
                    print "<td>", t.join(x["flaeche"]), "</td>"
                except KeyError:
                    print ''
                except TypeError:
                    print ''
                print "</tr>"
    except IndexError:
        print "Warning: not all sources loaded <br>"
print "</body></html>"




