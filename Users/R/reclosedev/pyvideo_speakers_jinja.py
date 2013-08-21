import scraperwiki
from jinja2 import Template


sourcescraper = 'pyvideos_speakers'
scraperwiki.sqlite.attach(sourcescraper)

template = Template('''
<table border=1>
<tr>
<th>Number of videos</th><th>Speaker</th>
</tr>
{% for pubs, records in data|groupby('pubs')|sort(reverse=True) %}
    <tr>    
    <td>{{ pubs }}</td>
    <td>
    {% for record in records %}
        <a href="http://pyvideo.org{{ record.href }}">{{ record.speaker }}</a>{% if not loop.last %}, {% endif %}
    {% endfor %}    
    </td>
    </tr>
{% endfor %}
</table>
''')

data = scraperwiki.sqlite.select('* from pyvideos_speakers.swdata order by speaker asc')
print template.render(data=data)