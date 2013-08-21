import re
import scraperwiki
import mechanize
import lxml.html

url = 'http://www.co.multnomah.or.us/dbcs/elections/2011-05/results.shtml'
br = mechanize.Browser()
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
br.set_handle_robots(False)
response = br.open(url)


root = lxml.html.fromstring(response.read())
pres = root.cssselect('pre')
primary_key = 1
positionflag = 1
#position = ''
for pre in pres:
    raw = pre.text_content()
    lines = raw.splitlines()
    data_only = lines[11:]
    for line in data_only:

        # Cleanup
        strippedline = line.lstrip()
        splitline = strippedline.split(' .')

        #if len(splitline) == 1 and re.match('Vote For', splitline[0]):
        #    positionflag = 0
        
        # Was previous line blank? Set position.
        if len(splitline) == 1 and positionflag == 1:
            position = splitline[0]

        # Set blank flag
        if len(splitline) == 1 and splitline[0] == '':
            positionflag = 1
        else:
            positionflag = 0


        # Multiple fields? Data.
        if len(splitline) > 1:
            candidate = splitline[0]
            
            returns = splitline[-1].split()
            #if len(returns) == 2:
            votes = returns[0]
                #percent = float(returns[1])/100
            #else:
            #    votes = returns[0]
                #percent = 0

            data = {
                'primary_key' : primary_key,
                'ballot_item' : position,
                'ballot_choice' : candidate.replace('.',''),
                'number_votes' : int(votes.replace(',','')),
                #'percent' : percent ### NOTE: I think pulling percentage from the page is probably a bad way to do it, can be calculated later if needed.
            }
            scraperwiki.sqlite.save(unique_keys=['primary_key'], data=data)
            primary_key += 1
            #position = ''