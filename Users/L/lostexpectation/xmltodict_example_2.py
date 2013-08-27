import xmltodict

doc = xmltodict.parse("""
<mydocument has="an attribute">
  <and>
    <many>elements</many>
    <many>more elements</many>
  </and>
  <plus a="complex">
    element as well
  </plus>
</mydocument>
""")

print doc['mydocument']['@has']
print doc['mydocument']['and']['many']
print doc['mydocument']['plus']['@a']
print doc['mydocument']['plus']['#text']
print docimport xmltodict

doc = xmltodict.parse("""
<mydocument has="an attribute">
  <and>
    <many>elements</many>
    <many>more elements</many>
  </and>
  <plus a="complex">
    element as well
  </plus>
</mydocument>
""")

print doc['mydocument']['@has']
print doc['mydocument']['and']['many']
print doc['mydocument']['plus']['@a']
print doc['mydocument']['plus']['#text']
print docimport xmltodict

doc = xmltodict.parse("""
<mydocument has="an attribute">
  <and>
    <many>elements</many>
    <many>more elements</many>
  </and>
  <plus a="complex">
    element as well
  </plus>
</mydocument>
""")

print doc['mydocument']['@has']
print doc['mydocument']['and']['many']
print doc['mydocument']['plus']['@a']
print doc['mydocument']['plus']['#text']
print doc