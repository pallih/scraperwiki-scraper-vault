# lxml is a complete library for parsing xml and html files.  http://codespeak.net/lxml/
# The interface is not totally intuitive, but it is very effective to use, 
# especially with cssselect.

import lxml.etree
import lxml.html

#print help(lxml.html.parse)


# create an example case
samplehtml = """<html><body>
<h1>hi</h1>
<p class="cccc">something <strong>good</strong>
<p>Another paragraph</p>
<ul class="LLL">
  <li class="1">first</li>
  <li class="2">second</li>
  <li class="1" id="nimble">third <b>jjj</b>aaa</li>junk
</ul>
</body></html>"""


root = lxml.html.fromstring(samplehtml)  # an lxml.etree.Element object

# To load directly from a url, use
#root = lxml.html.parse('http://www.google.com')

# Whenever you have an lxml element, you can convert it back to a string like so:
#print lxml.etree.tostring(root)

# Use cssselect to select elements by their css code
print root.cssselect("ul #nimble")   # returns 1 element
print root.cssselect(".LLL li")      # returns 3 elements

# extracting text from a single element 
linimble = root.cssselect("ul #nimble")[0]
help(linimble)                       # prints the documentation for the object
#print lxml.etree.tostring(linimble)  # note how this includes trailing text 'junk'
print linimble.text                  # just the text between the tag
#print linimble.tail                  # the trailing text
#print list(linimble)                 # prints the <b> object


# This recovers all the code inside the object, including any text markups like <b>
#print linimble.text + "".join(map(lxml.etree.tostring, list(linimble)))
# lxml is a complete library for parsing xml and html files.  http://codespeak.net/lxml/
# The interface is not totally intuitive, but it is very effective to use, 
# especially with cssselect.

import lxml.etree
import lxml.html

#print help(lxml.html.parse)


# create an example case
samplehtml = """<html><body>
<h1>hi</h1>
<p class="cccc">something <strong>good</strong>
<p>Another paragraph</p>
<ul class="LLL">
  <li class="1">first</li>
  <li class="2">second</li>
  <li class="1" id="nimble">third <b>jjj</b>aaa</li>junk
</ul>
</body></html>"""


root = lxml.html.fromstring(samplehtml)  # an lxml.etree.Element object

# To load directly from a url, use
#root = lxml.html.parse('http://www.google.com')

# Whenever you have an lxml element, you can convert it back to a string like so:
#print lxml.etree.tostring(root)

# Use cssselect to select elements by their css code
print root.cssselect("ul #nimble")   # returns 1 element
print root.cssselect(".LLL li")      # returns 3 elements

# extracting text from a single element 
linimble = root.cssselect("ul #nimble")[0]
help(linimble)                       # prints the documentation for the object
#print lxml.etree.tostring(linimble)  # note how this includes trailing text 'junk'
print linimble.text                  # just the text between the tag
#print linimble.tail                  # the trailing text
#print list(linimble)                 # prints the <b> object


# This recovers all the code inside the object, including any text markups like <b>
#print linimble.text + "".join(map(lxml.etree.tostring, list(linimble)))
# lxml is a complete library for parsing xml and html files.  http://codespeak.net/lxml/
# The interface is not totally intuitive, but it is very effective to use, 
# especially with cssselect.

import lxml.etree
import lxml.html

#print help(lxml.html.parse)


# create an example case
samplehtml = """<html><body>
<h1>hi</h1>
<p class="cccc">something <strong>good</strong>
<p>Another paragraph</p>
<ul class="LLL">
  <li class="1">first</li>
  <li class="2">second</li>
  <li class="1" id="nimble">third <b>jjj</b>aaa</li>junk
</ul>
</body></html>"""


root = lxml.html.fromstring(samplehtml)  # an lxml.etree.Element object

# To load directly from a url, use
#root = lxml.html.parse('http://www.google.com')

# Whenever you have an lxml element, you can convert it back to a string like so:
#print lxml.etree.tostring(root)

# Use cssselect to select elements by their css code
print root.cssselect("ul #nimble")   # returns 1 element
print root.cssselect(".LLL li")      # returns 3 elements

# extracting text from a single element 
linimble = root.cssselect("ul #nimble")[0]
help(linimble)                       # prints the documentation for the object
#print lxml.etree.tostring(linimble)  # note how this includes trailing text 'junk'
print linimble.text                  # just the text between the tag
#print linimble.tail                  # the trailing text
#print list(linimble)                 # prints the <b> object


# This recovers all the code inside the object, including any text markups like <b>
#print linimble.text + "".join(map(lxml.etree.tostring, list(linimble)))
# lxml is a complete library for parsing xml and html files.  http://codespeak.net/lxml/
# The interface is not totally intuitive, but it is very effective to use, 
# especially with cssselect.

import lxml.etree
import lxml.html

#print help(lxml.html.parse)


# create an example case
samplehtml = """<html><body>
<h1>hi</h1>
<p class="cccc">something <strong>good</strong>
<p>Another paragraph</p>
<ul class="LLL">
  <li class="1">first</li>
  <li class="2">second</li>
  <li class="1" id="nimble">third <b>jjj</b>aaa</li>junk
</ul>
</body></html>"""


root = lxml.html.fromstring(samplehtml)  # an lxml.etree.Element object

# To load directly from a url, use
#root = lxml.html.parse('http://www.google.com')

# Whenever you have an lxml element, you can convert it back to a string like so:
#print lxml.etree.tostring(root)

# Use cssselect to select elements by their css code
print root.cssselect("ul #nimble")   # returns 1 element
print root.cssselect(".LLL li")      # returns 3 elements

# extracting text from a single element 
linimble = root.cssselect("ul #nimble")[0]
help(linimble)                       # prints the documentation for the object
#print lxml.etree.tostring(linimble)  # note how this includes trailing text 'junk'
print linimble.text                  # just the text between the tag
#print linimble.tail                  # the trailing text
#print list(linimble)                 # prints the <b> object


# This recovers all the code inside the object, including any text markups like <b>
#print linimble.text + "".join(map(lxml.etree.tostring, list(linimble)))
# lxml is a complete library for parsing xml and html files.  http://codespeak.net/lxml/
# The interface is not totally intuitive, but it is very effective to use, 
# especially with cssselect.

import lxml.etree
import lxml.html

#print help(lxml.html.parse)


# create an example case
samplehtml = """<html><body>
<h1>hi</h1>
<p class="cccc">something <strong>good</strong>
<p>Another paragraph</p>
<ul class="LLL">
  <li class="1">first</li>
  <li class="2">second</li>
  <li class="1" id="nimble">third <b>jjj</b>aaa</li>junk
</ul>
</body></html>"""


root = lxml.html.fromstring(samplehtml)  # an lxml.etree.Element object

# To load directly from a url, use
#root = lxml.html.parse('http://www.google.com')

# Whenever you have an lxml element, you can convert it back to a string like so:
#print lxml.etree.tostring(root)

# Use cssselect to select elements by their css code
print root.cssselect("ul #nimble")   # returns 1 element
print root.cssselect(".LLL li")      # returns 3 elements

# extracting text from a single element 
linimble = root.cssselect("ul #nimble")[0]
help(linimble)                       # prints the documentation for the object
#print lxml.etree.tostring(linimble)  # note how this includes trailing text 'junk'
print linimble.text                  # just the text between the tag
#print linimble.tail                  # the trailing text
#print list(linimble)                 # prints the <b> object


# This recovers all the code inside the object, including any text markups like <b>
#print linimble.text + "".join(map(lxml.etree.tostring, list(linimble)))
# lxml is a complete library for parsing xml and html files.  http://codespeak.net/lxml/
# The interface is not totally intuitive, but it is very effective to use, 
# especially with cssselect.

import lxml.etree
import lxml.html

#print help(lxml.html.parse)


# create an example case
samplehtml = """<html><body>
<h1>hi</h1>
<p class="cccc">something <strong>good</strong>
<p>Another paragraph</p>
<ul class="LLL">
  <li class="1">first</li>
  <li class="2">second</li>
  <li class="1" id="nimble">third <b>jjj</b>aaa</li>junk
</ul>
</body></html>"""


root = lxml.html.fromstring(samplehtml)  # an lxml.etree.Element object

# To load directly from a url, use
#root = lxml.html.parse('http://www.google.com')

# Whenever you have an lxml element, you can convert it back to a string like so:
#print lxml.etree.tostring(root)

# Use cssselect to select elements by their css code
print root.cssselect("ul #nimble")   # returns 1 element
print root.cssselect(".LLL li")      # returns 3 elements

# extracting text from a single element 
linimble = root.cssselect("ul #nimble")[0]
help(linimble)                       # prints the documentation for the object
#print lxml.etree.tostring(linimble)  # note how this includes trailing text 'junk'
print linimble.text                  # just the text between the tag
#print linimble.tail                  # the trailing text
#print list(linimble)                 # prints the <b> object


# This recovers all the code inside the object, including any text markups like <b>
#print linimble.text + "".join(map(lxml.etree.tostring, list(linimble)))
# lxml is a complete library for parsing xml and html files.  http://codespeak.net/lxml/
# The interface is not totally intuitive, but it is very effective to use, 
# especially with cssselect.

import lxml.etree
import lxml.html

#print help(lxml.html.parse)


# create an example case
samplehtml = """<html><body>
<h1>hi</h1>
<p class="cccc">something <strong>good</strong>
<p>Another paragraph</p>
<ul class="LLL">
  <li class="1">first</li>
  <li class="2">second</li>
  <li class="1" id="nimble">third <b>jjj</b>aaa</li>junk
</ul>
</body></html>"""


root = lxml.html.fromstring(samplehtml)  # an lxml.etree.Element object

# To load directly from a url, use
#root = lxml.html.parse('http://www.google.com')

# Whenever you have an lxml element, you can convert it back to a string like so:
#print lxml.etree.tostring(root)

# Use cssselect to select elements by their css code
print root.cssselect("ul #nimble")   # returns 1 element
print root.cssselect(".LLL li")      # returns 3 elements

# extracting text from a single element 
linimble = root.cssselect("ul #nimble")[0]
help(linimble)                       # prints the documentation for the object
#print lxml.etree.tostring(linimble)  # note how this includes trailing text 'junk'
print linimble.text                  # just the text between the tag
#print linimble.tail                  # the trailing text
#print list(linimble)                 # prints the <b> object


# This recovers all the code inside the object, including any text markups like <b>
#print linimble.text + "".join(map(lxml.etree.tostring, list(linimble)))
# lxml is a complete library for parsing xml and html files.  http://codespeak.net/lxml/
# The interface is not totally intuitive, but it is very effective to use, 
# especially with cssselect.

import lxml.etree
import lxml.html

#print help(lxml.html.parse)


# create an example case
samplehtml = """<html><body>
<h1>hi</h1>
<p class="cccc">something <strong>good</strong>
<p>Another paragraph</p>
<ul class="LLL">
  <li class="1">first</li>
  <li class="2">second</li>
  <li class="1" id="nimble">third <b>jjj</b>aaa</li>junk
</ul>
</body></html>"""


root = lxml.html.fromstring(samplehtml)  # an lxml.etree.Element object

# To load directly from a url, use
#root = lxml.html.parse('http://www.google.com')

# Whenever you have an lxml element, you can convert it back to a string like so:
#print lxml.etree.tostring(root)

# Use cssselect to select elements by their css code
print root.cssselect("ul #nimble")   # returns 1 element
print root.cssselect(".LLL li")      # returns 3 elements

# extracting text from a single element 
linimble = root.cssselect("ul #nimble")[0]
help(linimble)                       # prints the documentation for the object
#print lxml.etree.tostring(linimble)  # note how this includes trailing text 'junk'
print linimble.text                  # just the text between the tag
#print linimble.tail                  # the trailing text
#print list(linimble)                 # prints the <b> object


# This recovers all the code inside the object, including any text markups like <b>
#print linimble.text + "".join(map(lxml.etree.tostring, list(linimble)))
