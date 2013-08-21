<div class="content col left">
<h3>Scraperwiki reference</h3>
<p>ScraperWiki itself offers useful in-built functions for retrieving, geocoding and saving data.</p>

<div class="section">
<h3><span id="scraping"></span>scraperwiki.scrape</h3>
<p>The most basic function. Downloads a web page, and returns you the HTML as a string.</p>
    <h4>Method</h4>
    <table class="api_detail example_table">
    <tr><th width="30%">Method</th><th width="20%">Returned value</th><th>Description</th></tr>
<tr><td><code>scraperwiki.scrape<br/>&nbsp;(url, [params=], )</code></td><td>String</td>
    <td><dl>
    <dt><code>url</code></dt>
        <dd>String. The address of the web page, e.g. <code>http://www.google.co.uk</code>
        </dd>
    <dt><code>params</code> (optional)</dt>
<dd>Dictionary. If present, sends a POST request, with the parameters specified in the dictionary. 
        </dd>
    </dl></td>
    </tr>
    </table>
        <h4>Example</h4>
        <div class="example"><code>
        html = scraperwiki.scrape('http://www.google.co.uk') # GET request.<br/>
        html = scraperwiki.scrape('http://www.google.co.uk', { 'key' : value }) # POST request.
        </code></div>
</div>
        <div class="section">
            <h3><span id="saving"></span>scraperwiki.datastore.save</h3>
            <p>Save your data to the ScraperWiki datastore. You can then download it, 
               or retrieve it later using the API.</p>
                            <h4>Method</h4>
                            <table class="api_detail example_table">
                            <tr><th width="30%">Method</th><th width="20%">Returned value</th><th>Description</th></tr>
                                <tr><td><code>scraperwiki.datastore.save<br/>
                                    &nbsp;(unique_keys, data,<br/>
                                    &nbsp;[date=],<br/>
                                    &nbsp;[latlng=]) </code></td>
                                <td>None</td>
                            <td>
                            <p>Stores a new record in the database, or replaces an existing
                record which has the same unique keys. The data parameter is a
                dictionary containing all the attributes of your record and their
                values.
                </p>
                <dl>
                    <dt><code>unique_keys</code></dt>
                        <dd>Array. Specify the attributes in
                        your record which are together unique, e.g. <code>['dog_id']</code> or
                        <code>['cattery', 'cat_number']</code>. Any existing data with
                        the same values for those attributes as your new data
                        will be overwritten. Must contain at least one element.
                        </dd>
                    <dt><code>data</code></dt>
                        <dd>Dictionary. The data in your record. Values are converted to strings. e.g.
                        in the example given, 
                        the integer <code>9812301</code> will be stored as a string. A null value
                        (e.g. <code>None</code> in Python) is stored as an empty string.
                        As a special case, if you use a key called <code>'date'</code> or <code>'latlng'</code>,
                        then it will be treated as if it were one of the optional arguments described below.
                        </dd>
                    <dt><code>date</code> (optional)</dt>
                        <dd>Special date/time field. You can later retrieve
                        information according to this date using the <a href="{% url api:scraper_getdatabydate %}">getDataByDate</a>
                        function in the external API. You can also store dates
                        in the data field, but you should put the most important one in this field.
                        The date can be formatted as an ISO date in a string (<code>'2009-11-02'</code>), 
                        can include a time (<code>'2015-01-19 03:14:07'</code>) or can be
                        a date/time object from your language (e.g. <code>datetime.datetime.now() - datetime.timedelta(weeks=2)</code>).
                        </dd>
                    <dt><code>latlng</code> (optional)</dt>
                        <dd>Optionally, a location. This is a pair containing
                        latitude and longitude coordinates, e.g. <code>(-2.983333, 53.4)</code>. The coordinates should
                        be in the WGS84 projection. You can later retrieve
                        information according to this location using the <a href="{% url api:scraper_getdatabylocation %}">getDataByLocation</a>.
                        Scrapers for which latitude and longitude coordinates have been added will have a map showing the points displayed
                        on the its page on the site.
                        </dd>
                </dl>
                            </td>
                            </tr>
                            </table>
                                <h4>Example</h4>
                                <div class="example"><code>
                            data = {}<br/>
                            data['name'] = 'Fluffles'<br/>
                            data['breed'] = 'Alsatian'<br/>
                            scraperwiki.datastore.save(['name'], data, date="2009-03-02", latlng=(-2.983333, 53.4))
                                </code></div>
            </div>

        <div class="section">
            <h2><span id="geocoding"></span>Geocoding data</h2>
            <p>ScraperWiki provides three useful geocoding functions: extract the postcode from an address;
            convert postcode to lat/lng; and convert easting/northing to lat/lng. 
            <h4>Method</h4>
            <table class="api_detail example_table">
            <tr><th width="30%">Method</th><th width="20%">Returned value</th><th>Description</th></tr>
                <tr><td><code>scraperwiki.geo.extract_gb_postcode
                      <br/>&nbsp;(string)</code></td><td>String</td>
                    <td><p>Attempts to extract a UK postcode from a given string.</p>
            <dl>
              <dt><code>string</code></dt>
              <dd>String. The string (e.g. an address) that will be searched for a postcode. Returns 
                 <code>False</code> if no postcode can be found. </dd>
            </dl>
            </td>
                    </tr>
                <tr><td><code>scraperwiki.geo.gb_postcode_to_latlng
                              <br/>&nbsp;(postcode)</code></td><td>List</td>
                    <td>
                    <p>Find the lat/lng for a given postcode.</p>
                <dl>
                  <dt><code>postcode</code></dt>
                  <dd>
                    String. The postcode to geocode. 
                    You can supply the returned value as the <code>latlng</code> field in 
                    <a href="#saving">scraperwiki.datastore.save</a>.
                  </dd>
                </dl>
                    </td>
                    </tr>
                <tr><td><code>scraperwiki.geo.os_easting_northing_to_latlng
                              <br/>&nbsp;(easting, northing)</code></td><td>String</td>
                    <td>
                    <p>
              Convert <a href="http://en.wikipedia.org/wiki/British_national_grid_reference_system">OSGB</a>
              easting/northing to lat/lng. 
            </p>
            <dl>
              <dt><code>easting</code></dt>
              <dd>The easting of the point to be converted.</dd>
              <dt><code>northing</code></dt>
              <dd>The northing of the point to be converted.</dd>
            </dl>
                    </td>
                    </tr>       
            </table>
                <h4>Example</h4>
                <div class="example"><code>
                postcode = scraperwiki.geo.gb_postcode_to_latlng("10 Downing Street, London, SW1A 2AA")<br/>
                latlng = scraperwiki.geo.gb_postcode_to_latlng("SW1A 2AA")
                </code></div>
        </div>

        <div class="section">
            <h2><span id="managing"></span>Managing scrapers with metadata</h2> 
            <p>
              Scrapers can store and retrieve metadata that is persisted between
                        runs. This can be used internally by the scraper; to set the order in which 
                        data columns are displayed; or to hide particular columns in the data table.
            </p>
                            <h4>Method</h4>
                            <table class="api_detail example_table">
                            <tr><th width="30%">Method</th><th width="20%">Returned value</th><th>Description</th></tr>
                        <tr><td><code>scraperwiki.metadata.save<br/>&nbsp;(key, value)</code></td><td>String</td>
                            <td>
                         <p>Stores an item of metadata that can later be retrieved using the <code>scraperwiki.metadata.get</code> function.</p>
                            <dl>
                      <dt><code>key</code></dt>
                      <dd>
                        This is a unique identifier for the data being stored. Multiple save requests
                        with the same key will overwrite any existing value associated with the key.
                      </dd>
                      <dt><code>value</code></dt>
                      <dd>The value to be stored.</dd>
                    </dl></td></tr>
                    <tr>
                                <td><code>scraperwiki.metadata.get<br/>&nbsp;(key, [default=])</code></td><td>String</td>
                                 <td>
                                 <p>Retrieves an item of metadata that has previously been stored using the <code>scraperwiki.metadata.save</code> function.</p>
                                <dl>
                      <dt><code>key</code></dt>
                      <dd>The unique identifier that was used when storing the data.</dd>
                      <dt><code>default</code> (optional)</dt>
                      <dd>The value to be returned if no value is found to be associated with this key. Defaults to <code>None</code>.</dd>
                    </dl></td>
                            </tr>
                            </table>

            <h3>Special Keys</h3>
            <p>
              You can store any information in metadata. However, special keys can be used to set
             column ordering in the data table, or hide columns altogether. These include:
            </p>
            <table class='data'>
              <tr><th>Key</th><th>Outcome</th></tr>
              <tr>
                <td>data_columns</td>
                <td>
                  Store a list of column names here to specify the order in which columns are displayed in the ScraperWiki data table.
                </td>
              </tr>
              <tr>
                <td>private_columns</td>
                <td>
                  Store a list of column names here to hide these columns in the ScraperWiki data table from users who do not own the scraper. 
                </td>
              </tr>
            </table>
                        <h4>Example</h4>
                        <div class="example"><code>
                        scraperwiki.metadata.save(data_columns, ['date', 'name', 'breed', 'latlng'])<br/>
                        scraperwiki.metadata.save(private_columns, ['latlng'])
                        </code></div>
        </div>
</div>

<div class="content col right">
<h4>Core ScraperWiki functions</h4>
<h5>Scraping</h4>
<ul>
  <li><a href="#scraping">scraperwiki.scrape</a></li>
</ul>
<h5>Datastore</h4>
<ul>
  <li><a href="#saving">scraperwiki.datastore.save</a></li>
</ul>
<h5>Geo</h4>
<ul>
  <li><a href="#geocoding">scraperwiki.geo.extract_gb_postcode</a></li>
  <li><a href="#geocoding">scraperwiki.geo.gb_postcode_to_latlng</a></li>
  <li><a href="#geocoding">scraperwiki.geo.os_easting_northing_to_latlng</a></li>
</ul>
<h5>Metadata</h4>
<ul>
  <li><a href="#managing">scraperwiki.metadata.save</a></li>
  <li><a href="#managing">scraperwiki.metadata.get</a></li>
</ul> 
</div>









