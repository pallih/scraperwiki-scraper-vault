import scraperwiki

#https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=csv&name=oxford_graduate_subjects_by_college&query=select%20*%20from%20%60courses_colleges%60%20join%20courses%20ON%20course_id%3Dcourses.id%20WHERE%20college%3D'Lincoln'

scraperwiki.sqlite.attach("oxford_graduate_subjects_by_college")

print "function get_subjects(college){

print "<select name='college' onselect='javascript:get_subjects(this.value);'>"

for college in scraperwiki.sqlite.select("* from colleges"):
    print "<option value='%(name)s'>%(name)s</option>" % college
 
print "</select>"