import scraperwiki,zipfile,tempfile

data = scraperwiki.scrape("http://www.dairycobreeding.org.uk/uploadeddocuments/conv_and_ext_org_files/64.zip")

t = tempfile.NamedTemporaryFile(suffix=".zip")
t.write(data)
t.seek(0)
z = zipfile.ZipFile(t.name)
for nz in z.namelist():
    data = z.read(nz)

