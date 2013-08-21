import mechanize

# Author: Felipe Oliveira
# Dec 21st 2010

# List of States
states = ["AL", "Alabama", "AK", "Alaska", "AZ", "Arizona", "AR", "Arkansas", "CA", "California", "CO", "Colorado", "CT", "Connecticut", "DE", "Delaware", "DC", "District Of Columbia", "FL", "Florida", "GA", "Georgia", "HI", "Hawaii", "ID", "Idaho", "IL", "Illinois", "IN", "Indiana", "IA", "Iowa", "KS", "Kansas", "KY", "Kentucky", "LA", "Louisiana", "ME", "Maine", "MD", "Maryland", "MA", "Massachusetts", "MI", "Michigan", "MN", "Minnesota", "MS", "Mississippi", "MO", "Missouri", "MT", "Montana", "NE", "Nebraska", "NV", "Nevada", "NH", "New Hampshire", "NJ", "New Jersey", "NM", "New Mexico", "NY", "New York", "NC", "North Carolina", "ND", "North Dakota", "OH", "Ohio", "OK", "Oklahoma", "OR", "Oregon", "PA", "Pennsylvania", "RI", "Rhode Island", "SC", "South Carolina", "SD", "South Dakota", "TN", "Tennessee", "TX", "Texas", "UT", "Utah", "VT", "Vermont", "VA", "Virginia", "WA", "Washington", "WV", "West Virginia", "WI", "Wisconsin", "WY", "Wyoming"]

# Debug Mode?
debug = True

# Loop on each state
for state in states:
    # Just define url on states with two characters - I copied and pasted from somewhere else and got lazy to remove it :)
    if state and len(state) == 2:
        url = "http://realestate.smarteragent.com/SA/BasicSearchPage.action?state=%s" % state

    # Log Debug
    if debug:
        print "\n"
        print "\n"
        print "Url: %s" % url
        br = mechanize.Browser()
        br.open(url)
        
    # Define list that will hold list of cities
    cities = []

    # Get forms from state page
    allforms = list(br.forms())

    # Log Debug
    if debug:
            print "There are %d forms" % len(allforms)
        
    # Loop on the forms and their fields to get the list of cities
    for i, form in enumerate(allforms):
          br.form = allforms[i]  #  br.select_form(name=form.name) works only if name is not None
          for control in br.form.controls:        
                if control.name and control.name == "city":
                        for item in control.items:
                            if item and item.name:
                               cities.append(item.attrs['value'])

    # Log Debug
    if debug: 
        print "Cities for State %s" % state
        print cities
        
    # Loop on each city to get list of communities
    for city in cities:
        # Halt if string is invalid
        if not city:
           continue

        # Define City Page Url
        url = "http://realestate.smarteragent.com/SA/BasicSearchPage.action?state=%s&city=%s" % (state, city.replace(' ', '+'))
        
        # Log Debug
        if debug:
            print url
            br = mechanize.Browser()
            br.open(url)
        
            if not br:
                continue
        
            try:
                hoods = []
                allforms = list(br.forms())
                if not allforms:
                    continue
                #print "There are %d forms" % len(allforms)
                
                for i, form in enumerate(allforms):
                    #print "--------------------"
                    #print form
                    #print "br.forms()[%d] br.select_form(name='%s')" % (i, form.name)
                    br.form = allforms[i]  #  br.select_form(name=form.name) works only if name is not None
                    
                    # loop through the controls in the form
                    for control in br.form.controls:
                        # (could group the controls by type)
                        #r = [ ]
                        #r.append("  -  type=%s, name=%s, value=%s, disabled=%s, readonly=%s" %  (control.type,  control.name, br[control.name], control.disabled,  control.readonly))
                
                        if control.name and control.name == "neighborhood":
                                for item in control.items:
                                    if item and item.name:
                                       hoods.append(item.attrs['value'])
                if item.attrs['value']:
                    item.attrs['value'] = item.attrs['value'].replace('"',"")
                    line = '"%s","%s","%s"\n' % (state, city, item.attrs['value'])
                    if debug:
                        print line
                           #file.write(line)
            except:
                pass
        
            #print city
            #print hoods

    
        

