import scraperwiki
import lxml.html

def my_containsAll(str, set):
    """
    Check for all characters in a string. 
    http://code.activestate.com/recipes/65441-checking-whether-a-string-contains-a-set-of-chars/
    """
    for c in set:
        if c not in str: return 0;
    return 1;

def my_containsAny(string, substrings):
    """
    Check for the existence of ANY substrings.
    """
    for ss in substrings:
        if string.find(ss) > -1: 
            return True;
    return False;

url = "http://www.techstars.org/nyc/"

root = lxml.html.parse(url).getroot()
#print lxml.html.tostring(root)

mentors = root.cssselect("div.mpop")

print "There are %d New York mentors." % len(mentors)

# mentors table
mentor_fields = ["mentor_id INTEGER PRIMARY KEY", "first TEXT", "last TEXT", "roles TEXT", "primary_company TEXT", "investor INT"]
scraperwiki.sqlite.execute("create table if not exists mentors (%s)" % ",".join(mentor_fields))
# roles table
role_fields = ["role_name TEXT", "company_name TEXT", "mentor_id INTEGER", "FOREIGN KEY(mentor_id) REFERENCES mentors(mentor_id)"]
scraperwiki.sqlite.execute("create table if not exists roles (%s)" % ",".join(role_fields))

for mid, m in enumerate(mentors):
    mid += 1 # start the IDs at 1, not 0

    # Get the wrapping list item so we can get links to individual mentor pages. 
    li = m.getparent().tag
    
    # Get the mentor's name. 
    mname = m.cssselect("div.mentor")[0]
    # Get the mentor's roles at his or her companies, cleaning up carriage returns and ampersands. 
    roles_str = lxml.html.tostring(mname).replace("&amp;", "&").replace("&#13;", '').split("</div>")[-1]
    
    investor = my_containsAny(roles_str.lower(), ['investor', 'capital', 'ventures'])
    name = mname.text_content().rsplit(' ')

    # Save the mentor 
    primary_company = roles_str.rsplit(',', 1)[-1].strip()
    mdata = {'mentor_id': mid, 'first':name[0], 'last':name[1], 'roles':roles_str, 'primary_company':primary_company, 'investor':investor}
    scraperwiki.sqlite.save(unique_keys=['mentor_id', 'first', 'last'], data=mdata, table_name="mentors")

    for rpair in roles_str.split(';'): 
        rind = rpair.rsplit(',', 1)
        role = rind[0].strip()
        company = None
        try: 
            company = rind[1].strip()
        except IndexError: 
            print "No company for role %s." % role

        scraperwiki.sqlite.execute("INSERT into 'roles' values(?,?,?)", (role, company, mid))
        scraperwiki.sqlite.commit()

    #print (m.tag, m.attrib.get("id"), mname.text_content(), roles)

results = scraperwiki.sqlite.select("m.first, m.last, r.company_name from mentors m, roles r "\
    "where investor=1 and m.mentor_id = r.mentor_id")
print results
