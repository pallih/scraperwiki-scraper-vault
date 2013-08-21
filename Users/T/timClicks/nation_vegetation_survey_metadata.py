# access guidelines are here http://nvs.landcareresearch.co.nz/html/NVSprotocol.aspx#nvsaccess

# TODO
#  - some irritating nested resources

import datetime
import urllib2
from pprint import pprint

from dateutil import parser as dateparser
import scrapemark
import scraperwiki

urls = ['http://nvs.landcareresearch.co.nz/WebForms/MetadataFrom.aspx?Action=Display&NodeKey=5984&Type=M',
'http://nvs.landcareresearch.co.nz/WebForms/MetadataFrom.aspx?Action=Display&NodeKey=5239&Type=M',
'http://nvs.landcareresearch.co.nz/WebForms/MetadataFrom.aspx?Action=Display&NodeKey=5240&Type=M',
'http://nvs.landcareresearch.co.nz/WebForms/MetadataFrom.aspx?Action=Display&NodeKey=5039&Type=M',
'http://nvs.landcareresearch.co.nz/WebForms/MetadataFrom.aspx?Action=Display&NodeKey=660&Type=M']

pattern="""
<table width="100%" cellpadding="3" cellspacing="0" border="1" style="border-collapse:collapse" class="medium">
  <tr>
    <td>Dataset ID:</td>
    <td>
      <table class="medium">
        <tr>
          <td>{{ id }}</td>
          <td>
            <table>
              <tr>
                <td><b>Last modified:</b></td>
                <td>{{ last_modified }}</td>
              </tr>
            </table>
         </td>
      </tr>
      </table>
    </td>
  </tr>
  <tr>
    <td><h5>Title:</h5></td>
    <td>
      <table class="medium">
        <tr><td>{{ title }}</td></tr>
      </table>
    </td>
  </tr>
  <tr>
    <td><h5>Date(s):</h5></td>
    <td>
      <table class="medium"><tr><td>{{ date_start }}</td><td></td><td>{{ date_end }}</td></tr></table>
    </td>
  </tr>
  <tr>
    <td>
      <h5>Type: </h5>
    </td>
    <td width="100%">
      <table class="medium">
        <tr>
          <td valign="top">{{ dataset_type }}</td>
        </tr>
     </table>
    </td>
  </tr>
  <tr>
    <td>
      <h5>Habitat:</h5>
    </td>
    <td>
      {{ habitat }}
     </td>
  </tr>
  <tr>
    <td><h5> Purpose:</h5></td>
    <td>{{ purpose }}</td>
  </tr>
  <tr>
    <td><h5> Geographic description:</h5></td>
    <td>
      {{ location }}
    </td>
  </tr>
  <tr>
    <td>
      <h5>  Geographic coverage:</h5>
    </td>
    <td>
      {* <tr>{{ [coverage] }}</tr> *}
    </td>
  </tr>
  <tr>
    <td><h5>No. of plots:</h5></td><td><table class="medium">{{ num_plots|int }}</table></td>
  </tr>
  <tr>
    <td>
      <h5>Method description:</h5>
    </td>
    <td>{{ method }}</td>
  </tr>
  <tr>
    <td><h5>Methods used:</h5></td>
    <td>
      <table class="medium">
        {* <tr>{{ [methods] }}</tr> *}
      </table>
    </td>
  </tr>
  <tr>
    <td><h5>  Organisation:</h5></td>
    <td>{{ organisation }}</td>
  </tr>
  <tr>
    <td>
      <h5>  Custodian:</h5>
    </td>
    <td>
      <table>
        <tr>
          <td><b>Name: </b></td>
          <td>{{ custodian.name }}</td>
        </tr>
      </table>
    </td>
  </tr>
  <tr>
    <td><h5>Citations:</h5></td>
    <td>{{ citations }}</td>
  </tr> 
  <tr>
    <td><h5>  Dataset Format:</h5></td>
    <td>{{ dataset_format }}</td>
  </tr>
  <tr>
    <td><h5>Archived material:</h5></td>
    <td>
      <table>
        <tr>
          <td><b>Item:</b></td>
          <td><b>Held as:</b></td>
       </tr>
       {* <tr>
          <td>{{ [archived_material].title }}</td>
          <td>
            <table>
              <tr><td>{{ [archived_material].held_as }}</td></tr>
            </table>
          </td>
       </tr>
       *}
      </table>
    </td>
  </tr>
<tr>
    <td><h5>Associated Resources:</h5></td>
    <td>
      <table>
        <tr>
          <td><b>Resource:</b></td>
          <td><b>Held as:</b></td>
       </tr>
       {* <tr>
          <td>{{ [associated_resources].title }}</td>
          <td>
            <table>
              <tr><td>{{ [associated_resources].held_as }}</td></tr>
            </table>
          </td>
       </tr>
       *}
      </table>
    </td>
  </tr>
  <tr>
    <td><h5>  Linked data sets:</h5></td>
    <td><table>{* <td>{{ [associated_data_sets] }}</td> *}</table>
    </td>
  </tr>
  <tr>
    <td><h5> Access level:</h5></td><td><table><tr><td class="medium"><a target="blank" href="{{ access_level.details|abs }}"><u>{{ access_level.label }}-{{ access_level.num}}</u></a></td></tr></table></td>
  </tr>
  <tr>
    <td><h5>  Available formats:</h5></td>
    <td><table>{* <td>{{ [available_formats] }}</td> *}</table></td>
  </tr>
  <tr>
    <td><h5> Dataset Status:</h5></td>
    <td>
      <table class="medium"><td><b>Dataset State:</b></td><td></td><td>{{ dataset_state }}</td><td></td><td><b>Update frequency:</b></td><td></td><td>{{ update_frequency }}</td></table></td>
  </tr>
  <tr>
    <td><h5>  Accession date:</h5></td><td><table class="medium"><tr><td>{{ accession_date }}</td></tr></table></td>
  </tr>
  <tr>
    <td><h5>Keywords:</h5></td><td><table>{* <tr>{{ [keywords] }}</tr> *}</table></td></tr>
</table>"""

from pprint import pprint


def split_keywords(keyword_lists):
    if len(keyword_lists) == 1:
        li = keyword_lists[0].strip()
        if li.endswith(','): li = li[:-1]
        return li.split(', ')
    else:
        kw = []
        for keyword_list in keyword_lists:
            kw.append(split_keywords(keyword_list)) 
        return kw

def assemble_methods(dataset):
    return [dict(web_id=dataset['web_id'], 
                 id=dataset['id'], 
                 method=m, 
                 date_start=dataset['date_start'], 
                 date_end=dataset['date_end']) for m in dataset['methods']]

def assemble_coverages(dataset):
    return [dict(web_id=dataset['web_id'], id=dataset['id'], title=dataset['title'], coverage=c) for c in dataset['coverage']]

def assemble_keywords(dataset):
    return [dict(web_id=dataset['web_id'], id=dataset['id'], title=dataset['title'], keyword=k) for k in dataset['keywords']]

def assemble_formats(dataset):
    return [dict(web_id=dataset['web_id'], id=dataset['id'], title=dataset['title'], format=f) for f in dataset['available_formats']]

def assemble_associations(dataset):
    return [dict(web_id=dataset['web_id'], id=dataset['id'], title=dataset['title'], association=a) for a in dataset['associated_data_sets']]

def assemble_associated_resources(dataset):
    return [dict(web_id=dataset['web_id'], 
                 resource_held_as=r['held_as'], 
                 id=dataset['id'], 
                 title=dataset['title'], 
                 resource=r['title']) for r in dataset['associated_resources']]

def assemble_archived_material(dataset):
    return [dict(web_id=dataset['web_id'], resource_held_as=r['held_as'], id=dataset['id'], title=dataset['title'], resource=r['title']) for r in dataset['archived_material']]


scraperwiki.sqlite.execute('CREATE TABLE IF NOT EXISTS methods_employed (`web_id` int);')

start = scraperwiki.sqlite.get_var('progress', 1)

for web_id in xrange(start, 7000):
    print web_id
    #retrieval
    url = "http://nvs.landcareresearch.co.nz/WebForms/MetadataFrom.aspx?Action=Display&NodeKey=%s&Type=M" % web_id
    dataset = scrapemark.scrape(pattern, url=url)

    if dataset:
        #prep
        dataset['keywords'] = split_keywords(dataset['keywords'])
        dataset["web_id"] = web_id
    
        #building child resources
        methods  = assemble_methods(dataset)
        coverages = assemble_coverages(dataset)
        keywords = assemble_keywords(dataset)
        formats = assemble_formats(dataset)
        associations = assemble_associations(dataset)
        associated_resources = assemble_associated_resources(dataset)
        archived_material = assemble_archived_material(dataset)
    
        #denormalise/fixup
        dataset['access_level'] = dataset['access_level']['label']
        dataset['associated_data_sets'] = u'\n'.join(dataset['associated_data_sets'])
        dataset['available_formats'] = u'\n'.join(dataset['available_formats'])
        dataset['keywords'] = u'\n'.join(dataset['keywords'])
        dataset['coverages'] = u'\n'.join(dataset['coverage'])
        dataset['custodian'] = dataset['custodian']['name']
        dataset['methods'] = u'\n'.join(dataset['methods'])
        dataset['archived_material'] = u'\n'.join(u"{title} {held_as}".format(title=m['title'], held_as=m['held_as']) for m in dataset['archived_material'])
        dataset['associated_resources'] = u'\n'.join(u"{title} {held_as}".format(title=m['title'], held_as=m['held_as']) for m in dataset['associated_resources'])
        del dataset['coverage']
        for key, value in dataset.items():
            if isinstance(value, basestring) and value.strip().lower() == 'no data':
                dataset[key] = None
        for period in ['date_start', 'date_end', 'last_modified']:
            try:
                new_date = dateparser.parse(dataset[period])
                if datetime.datetime.now() - new_date < datetime.timedelta(days=2): #default behaviour is to use today's date :/
                    raise ValueError
            except ValueError:
                new_date = None
    
            dataset[period] = new_date
    
        #storage
        scraperwiki.sqlite.save(['web_id'], dataset, table_name='datasets')
        scraperwiki.sqlite.save(['web_id', 'association'], associations, table_name='associations')
        scraperwiki.sqlite.save(['web_id', 'format'], formats, table_name='available_formats')
        scraperwiki.sqlite.save(['web_id', 'coverage'], coverages, table_name='coverage')
        scraperwiki.sqlite.save(['web_id', 'keyword'], keywords, table_name='keywords')
        scraperwiki.sqlite.save(['web_id', 'method'], methods, table_name='methods_employed')
        scraperwiki.sqlite.save(['web_id', 'resource'], archived_material, table_name='archived_material')
        scraperwiki.sqlite.save(['web_id', 'resource'], associated_resources, table_name='associated_resources')
    scraperwiki.sqlite.save_var('progress', web_id)




