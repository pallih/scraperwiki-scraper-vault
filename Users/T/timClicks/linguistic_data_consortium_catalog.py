import scrapemark
import scraperwiki
project_index_url = "http://www.ldc.upenn.edu/Catalog/project_index.jsp"
catalogue_base_url = "http://www.ldc.upenn.edu/Catalog/CatalogEntry.jsp?catalogId="

PROJECT_INDEX = """{* <a href="CatalogEntry.jsp?catalogId={{ [id] }}></a> *}"""
PROJECT_1 = """
    <td>
      <h3>Introduction</h3>
      {{ intro }}
      <h3>Samples</h3>
      {* <a href="{{ [samples].url|abs }}">{{ [samples].title }}</a> *}
      <h3>Content Copyright</h3>
      {{ copyright }}
    </td>
"""

PROJECT_2 = """
    <td>
      <h3>Introduction</h3>
      {{ intro }}
      <h3>Data</h3>
      <h3>Content Copyright</h3>
      {{ copyright }}
    </td>
"""

PROJECT_3 = PROJECT_1.replace('Content Copyright', 'Copyright')
PROJECT_4 = PROJECT_2.replace('Content Copyright', 'Copyright')

PROJECT_5 = PROJECT_1.replace("""    <h3>Samples</h3>
      {* <a href="{{ [samples].url|abs }}">{{ [samples].title }}</a> *}""", '')
PROJECT_6 = PROJECT_5.replace('Content Copyright', 'Copyright')

PROJECT_7 = '<TD COLSPAN=2>{{ intro }}</TD>'

projects = scrapemark.scrape(pattern=PROJECT_INDEX, url=project_index_url)
print projects

results = []
rejects = []

for project in projects['id']:
    url = catalogue_base_url + project
    page = scraperwiki.scrape(url)
    result = scrapemark.scrape(pattern=PROJECT_1, html=page)
    if result is None:
        result = scrapemark.scrape(pattern=PROJECT_2, html=page)
    if result is None:
        result = scrapemark.scrape(pattern=PROJECT_3, html=page)
    if result is None:
        result = scrapemark.scrape(pattern=PROJECT_4, html=page)
    if result is None:
        result = scrapemark.scrape(pattern=PROJECT_5, html=page)
    if result is None:
        result = scrapemark.scrape(pattern=PROJECT_6, html=page)
    if result is None:
        result = scrapemark.scrape(pattern=PROJECT_7, html=page)
    print 'WIN', url 
    if result is None:
        print 'FIXME: ', url
        scraperwiki.sqlite.save(['ldc_id'], dict(ldc_id=project, url=url), table_name="rejects")
        result = {}
    result['title']= scrapemark.scrape('<font size="+2">{{ title }}</font>', html=page)['title']
    result['url'] = url
    result['ldc_id'] = project
    scraperwiki.sqlite.save(['ldc_id'], result, table_name="datasets")

    

