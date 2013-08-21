# Blank Python

from scraperwiki import scrape as GET

def company_url(coy_id):
    return "http://www.business.govt.nz/companies/app/ui/pages/companies/%s/detail" % coy_id

def company_doc_url(coy_id, doc_id):
    return "http://www.business.govt.nz/companies/app/ui/pages/companies/%s/%s/entityFilingRequirement" % (coy_id, doc_id)

def shareholders_url(coy_id):
    return "http://www.business.govt.nz/companies/app/ui/pages/companies/%s/shareholdings" % coy_id

GEO_PATTERN = """<input type="hidden" value="{{ lat }}" id="lat"/> 
<input type="hidden" value="{{ lng }}" id="lng"/> 
<input type="hidden" value="{{ nelat }}" id="nelat"/> 
<input type="hidden" value="{{ nelng }}" id="nelng"/> 
<input type="hidden" value="{{ swlat }}" id="swlat"/> 
<input type="hidden" value="{{ swlng }}" id="swlng"/> 
"""

DIRECTOR_PATTERN = """{*
<td class="director">
  <div class="row"><label>Full legal name:</label>{{ [directors].full_name }}</div>
  <div class="row"><label>Residential Address:</label>{{ [directors].address }}</div>
  <div class="row"><label>Appointment Date:</label>{{ [directors].appointment_date }}</div>
  <div class="row"><label>Consent:</label><a href="{{ [directors].consent_form_link }}"></a></div>
</td>
*}"""

ADDRESSES_PATTERN = """<ul class="tabs"><li>Addresses</li></ul>

{*
<label>{{ [addresses].type }}</label>
<div class="addressLine">{{ [addresses].address }}</div>
*}"""

SHAREHOLDERS_PATTERN = """<div class="panelTabs">
  <ul class="tabs">
    <li id="shareholdingTab"></li>
  </ul>
</div> 

<div class="allocations">
  <div class="row">
    <label>Total Number of Shares:</label><span>{{ total_shares }}</span>
    <label>Extensive Shareholding:</label><span class="noLabel">{{ extensive_shareholding }}</span>
  </div>
{*
  <div class="allocationDetail">
    <div class="row"><label><span class="allocationNumber">{{ [shareholders].number }}</span></label>{{ [shareholders].allocation }}</div>
    <div class="row">{{ [shareholders].name }}</div>
    <div class="row">{{ [shareholders].address }}</div>
  </div>
*}
</div>
"""

DOCUMENTS_PATTERN = """<li id="documentsTab"></li>

<div class="dataList">
{*
  <tr>
    <td>{{ [documents].created_at }}</td>
    <td><a href="{{ [documents].document_id }}">{{ [documents].document_type }}</a></td>
    <td>{{ [documents].size }}</td>  
  </tr>
*}
</div>
"""

INDIVIDUAL_DOCUMENT_PATTERN = """

<div id="documentHeaderDetail">
  <div class="row wideLabel"><label>Registration Date and Time</label>{{ created_at }}</div>
  <div class="row wideLabel"><label>Document Type</label>{{ doc_type }}</div>
  <div class="row wideLabel"><label>Presenter</label>{{ presenter }}</div>

<hr>
<div>
  <div class="panel">
    <a href="{{ doc_link}}" target="self" class="fileName">{{ doc_filename }}</a>
     </div>
     <div class="row wideLabel"><label>Barcode</label>{{ barcode }}</div>
     <hr>
   
</div>


$(document).ready(function() {
   $("#documentHeaderDetail").panel({title:"{{ company_id|int }}&nbsp;&nbsp;{{ company_name }}",notExpandable:true}); 
});

"""

GET(company_url(80000))
