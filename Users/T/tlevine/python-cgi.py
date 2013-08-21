import cgi

form = cgi.FieldStorage()
print {name: form[name].value for name in form.keys()}

#q=+