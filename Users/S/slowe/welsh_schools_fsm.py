import scraperwiki
import re
scraperwiki.sqlite.attach("welsh_school_finder")

ids = scraperwiki.sqlite.select("id,name from welsh_school_finder.swdata LIMIT 10")

scraperwiki.sqlite.attach("welsh_school_data_save")

for id in ids:
    schooldata = {'id' : id["id"]}
    results = scraperwiki.sqlite.select("data,urn from welsh_school_data_save.swdata where urn='"+id["id"]+"'")
    if len(results) > 0:
        print id["name"]+' ('+id["id"]+')'
        #schooldata["id"] = id["id"]
        print results[0]["data"]
        fsm = re.search("Percentage of pupils entitled to free school meals.*?text[\']: [\']([\d\. ]+)",results[0]["data"])
        if fsm:
            fsm = fsm.group(1)
            print '  FSM = '+fsm
            schooldata['fsm'] = fsm
        else:
            print id["name"]+" doesn't seem to have a value for free school meals."
        schooltype = re.search("School type.*?text[\']: [\']([^\']+)\'",results[0]["data"])
        if schooltype:
            print '  Type = '+schooltype.group(1)
            schooldata['schooltype'] = schooltype.group(1)
        ptratio = re.search("Pupil: teacher.*?text[\']: [\']([^\']+)\'",results[0]["data"])
        if ptratio:
            print '  Pupil teacher ratio = '+ptratio.group(1)
            schooldata['ptratio'] = ptratio.group(1)
        classsize = re.search("Average class size.*?text[\']: [\']([^\']+)\'",results[0]["data"])
        if classsize:
            print '  Pupil teacher ratio = '+classsize.group(1)
        excluded = re.search("Number of pupils excluded.*?text[\']: [\']([^\']+)\'",results[0]["data"])
        if excluded:
            print '  Number of pupils excluded in past 12 months = '+excluded.group(1)
        npupils = re.search("At the time of the inspection, there were ([\d]+) pupils on roll",results[0]["data"])
        if npupils:
            print '  Number of pupils = '+npupils.group(1)
    else:
        print id["name"]+" doesn't seem to have a report."
    scraperwiki.sqlite.save(["id"], data=schooldata, table_name="welsh_fsm")

