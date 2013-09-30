import urllib2

  # This reads in a list of urls & emails, comma separated.
  # It checks each url for a specific phrase in its HTML 
  # and writes the url and email to a log file.
  # The status print lines are for fun, to watch it scroll. 


#  lines = open("biglist.txt",'r').readlines()
#  for l in lines:
#   line = l.strip()
#   try:
#     (blog,email) = line.split(",")
#   except ValueError:
#     continue

try:
     blog = "http://bookmaniac.org/learning-python-by-writing-a-screen-scraper"
     f = urllib2.urlopen(blog)
     h= ''.join(f.readlines())
     if 'NEW BIT OF CODE' in h:
        filename = "gotnewcode.txt"
        status = "New! "
        if 'OLD BIT OF CODE' in h:
          filename = "gotbothcodes.txt" # replaces filename!
          status = "Mixed up codes: "
     elif 'OLD BIT OF CODE' in h:
        filename= "gotoldcode.txt"
        status = "Old code: "
     else:
        filename = "gotnocode.txt"
        status = "No code here: "
#     msg = blog + "," + email + "\n"
     msg = blog + "\n"
     outfile = open(filename,'a')
     outfile.writelines(msg)
     print  status + msg
  # check for 404 or other not found error
except (urllib2.HTTPError, urllib2.URLError) :
     msg = blog + "," + email + "\n"
     outfile = open("gotsitedown.txt",'a')
     outfile.writelines(msg)
     status = "Site down: "
     print status + msg
