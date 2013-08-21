import scraperwiki
import lxml.html

html = scraperwiki.scrape("http://code.google.com/p/ci-eye/downloads/list?can=1&colspec=Summary+Filename+ReleaseDate+Size+DownloadCount+Uploaded+UploadedBy+Stars+Project")
root = lxml.html.fromstring(html)

for tr in root.cssselect("#resultstable > tr"):
    summary        = tr.cssselect("td.col_0 a")[0].text_content().strip()
    filename       = tr.cssselect("td.col_1 a")[0].text_content().strip()
    release_date   = tr.cssselect("td.col_2 a")[0].text_content().strip()
    size           = tr.cssselect("td.col_3 a")[0].text_content().strip()
    download_count = tr.cssselect("td.col_4 a")[0].text_content().strip()

    uploaded       = tr.cssselect("td.col_5 a")[0].text_content().strip()
    uploaded_by    = tr.cssselect("td.col_6 a")[0].text_content().strip()
    stars          = tr.cssselect("td.col_7 a")[0].text_content().strip()
    project        = tr.cssselect("td.col_8 a")[0].text_content().strip()

    html_url = "http:" + tr.cssselect("a[title='Download']")[0].attrib['href']
    url = "http://code.google.com/p/" + project +"/downloads/detail?name=" + filename

    detailroot = lxml.html.fromstring(scraperwiki.scrape(url))
    meta_tds = detailroot.cssselect("#issuemeta td")
    release_date = meta_tds[1].text_content().strip()
    
    tags = []
    for a in meta_tds[4].cssselect("a"):
        tags.append(a.text_content().strip())

    data = { 'url' : url,
             'id' : filename,
             'html_url' : html_url,
             'name' : filename,
             'description' : summary,
             'created_at' : release_date,
             'size' : size,
             'download_count' : int(download_count),
             'tags' : tags,
             'uploaded_at' : uploaded,
             'uploaded_by' : uploaded_by,
             'stars' : int(stars),
             'project' : project }

    scraperwiki.sqlite.save(unique_keys=['id'], data=data)

