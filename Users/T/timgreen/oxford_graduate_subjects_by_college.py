import scraperwiki
import lxml.html
import lxml.etree
import urllib2
import re


#http://www2.admin.ox.ac.uk/progstudy/list_cols.php5?prog=10&keywd=
#http://www2.admin.ox.ac.uk/progstudy/

# First get all the course names and IDs

response = urllib2.urlopen("http://www2.admin.ox.ac.uk/progstudy/")

text = response.read()

id_regex = re.compile("progID\[([0-9]+)\] = (.*?);")
name_regex = re.compile("progName\[([0-9]+)\] = \"(.*?)\";")
degree_regex = re.compile("progDegree\[([0-9]+)\] = \"(.*?)\";")

ids = id_regex.findall(text)
names = name_regex.findall(text)
degrees = degree_regex.findall(text)

courses = {}

for index, id in ids:
  courses[int(index)] = {'id': int(id)}

for index, name in names:
  courses[int(index)]['name'] = name

for index, degree in degrees:
  courses[int(index)]['degree'] = degree

for index, course in courses.items():
    print index, course['id'], course['name']
    course_data = urllib2.urlopen("http://www2.admin.ox.ac.uk/progstudy/list_cols.php5?prog=%d" % course['id'])

    tree = lxml.etree.parse(course_data)

    colleges = [e.text for e in tree.xpath("//colname")]

    scraperwiki.sqlite.save(unique_keys=['id'], data=course, table_name="courses")

    for college in colleges:
        scraperwiki.sqlite.save(unique_keys=['name'], data={'name': college}, table_name="colleges")

        scraperwiki.sqlite.save(unique_keys=['course_id', 'college'], data={'course_id': course['id'], 'college': college}, table_name="courses_colleges")


   
import scraperwiki
import lxml.html
import lxml.etree
import urllib2
import re


#http://www2.admin.ox.ac.uk/progstudy/list_cols.php5?prog=10&keywd=
#http://www2.admin.ox.ac.uk/progstudy/

# First get all the course names and IDs

response = urllib2.urlopen("http://www2.admin.ox.ac.uk/progstudy/")

text = response.read()

id_regex = re.compile("progID\[([0-9]+)\] = (.*?);")
name_regex = re.compile("progName\[([0-9]+)\] = \"(.*?)\";")
degree_regex = re.compile("progDegree\[([0-9]+)\] = \"(.*?)\";")

ids = id_regex.findall(text)
names = name_regex.findall(text)
degrees = degree_regex.findall(text)

courses = {}

for index, id in ids:
  courses[int(index)] = {'id': int(id)}

for index, name in names:
  courses[int(index)]['name'] = name

for index, degree in degrees:
  courses[int(index)]['degree'] = degree

for index, course in courses.items():
    print index, course['id'], course['name']
    course_data = urllib2.urlopen("http://www2.admin.ox.ac.uk/progstudy/list_cols.php5?prog=%d" % course['id'])

    tree = lxml.etree.parse(course_data)

    colleges = [e.text for e in tree.xpath("//colname")]

    scraperwiki.sqlite.save(unique_keys=['id'], data=course, table_name="courses")

    for college in colleges:
        scraperwiki.sqlite.save(unique_keys=['name'], data={'name': college}, table_name="colleges")

        scraperwiki.sqlite.save(unique_keys=['course_id', 'college'], data={'course_id': course['id'], 'college': college}, table_name="courses_colleges")


   
