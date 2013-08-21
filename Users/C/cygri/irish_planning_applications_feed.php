<?php

$url = 'http://scraperwikiviews.com/run/irish_planning_applications_feed/';
scraperwiki::attach('irish_planning_applications', 'src');

$sites = array(
    'Buncrana' => array(
        'name' => 'Buncrana Town Council',
        'system' => 'ePlan classic plus',
        'url' => "http://www.donegal.ie/buncrana_eplan/internetenquiry/",
        'homepage' => 'rpt_querybysurforrecloc.asp',
    ),
    'Bundoran' => array(
        'name' => 'Bundoran Town Council',
        'system' => 'ePlan classic plus',
        'url' => "http://www.donegal.ie/bundoran_eplan/internetenquiry/",
        'homepage' => 'rpt_querybysurforrecloc.asp',
    ),
    'CorkCity' => array(
        'name' => 'Cork City Council',
        'system' => 'ePlan classic',
        'url' => "http://planning.corkcity.ie/InternetEnquiry/",
        'homepage' => '',
    ),
    'Donegal' => array(
        'name' => 'Donegal County Council',
        'system' => 'ePlan classic plus',
        'url' => "http://www.donegal.ie/DCC/iplaninternet/internetenquiry/",
        'homepage' => 'rpt_querybysurforrecloc.asp',
    ),
    'GalwayCity' => array(
        'name' => 'Galway City Council',
        'system' => 'ePlan classic',
        'url' => "http://gis.galwaycity.ie/ePlan/InternetEnquiry/",
        'homepage' => '',
        'map' => 'http://lab.linkeddata.deri.ie/2010/planning-apps/',
    ),
    'Kerry' => array(
        'name' => 'Kerry County Council',
        'system' => 'ePlan classic plus',
        'url' => "http://atomik.kerrycoco.ie/ePlan/InternetEnquiry/",
        'homepage' => 'rpt_querybysurforrecloc.asp',
    ),
    'Letterkenny' => array(
        'name' => 'Letterkenny Town Council',
        'system' => 'ePlan classic plus',
        'url' => "http://www.donegal.ie/letterkenny_eplan/internetenquiry/",
        'homepage' => 'rpt_querybysurforrecloc.asp',
    ),
    'LimerickCo' => array(
        'name' => 'Limerick County Council',
        'system' => 'ePlan classic',
        'url' => "http://www.lcc.ie/ePlan/InternetEnquiry/",
        'homepage' => '',
        'googlemaps_lowres' => true,
    ),
    'Longford' => array(
        'name' => 'Longford County Council',
        'system' => 'ePlan classic',
        'url' => "http://www.longfordcoco.ie/ePlan/InternetEnquiry/",
        'homepage' => '',
        'googlemaps_lowres' => true,
    ),
    'NTipperary' => array(
        'name' => 'North Tipperary County Council',
        'system' => 'ePlan classic',
        'url' => "http://www.tipperarynorth.ie/iPlan/InternetEnquiry/",
        'homepage' => '',
        'googlemaps_lowres' => true,
    ),
    'Waterford' => array(
        'name' => 'Waterford County Council',
        'system' => 'ePlan classic',
        'url' => "http://www.waterfordcity.ie/ePlan/InternetEnquiry/",
        'homepage' => '',
        'googlemaps_lowres' => true,
    ),
/*
These are broken as of May 15
    'Leitrim' => "http://193.178.1.87/ePlan/InternetEnquiry/",
    'Cavan' => "http://www.cavancoco.ie/ePlan/InternetEnquiry/",
*/
);

$params = array();
parse_str(getenv("URLQUERY"), $params);
if ($params['county'] && isset($sites[$params['county']])) {
    $county = $params['county'];
}

if (empty($county) && $params['county'] != 'all') {
?>
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title>Planning Applications to Local Councils in Ireland</title>
    <style>
th, td { padding: 0.2em 0.4em; }
    </style>
  </head>
  <body>
    <h1>Planning Applications to Local Councils in Ireland</h1>
    <p>This <a href="http://scraperwiki.com/">ScraperWiki</a> view provides Atom feeds
      for the most recent planning applications submitted to various Irish county and
      city councils. It's based on the scraper <a href="http://scraperwiki.com/scrapers/irish_planning_applications/">
      Irish Planning Applications</a>.</p>
    <p>This was made by <a href="http://twitter.com/cygri">@cygri</a> at <a href="http://www.deri.ie/">DERI</a>.</p>
    <p><em>This is work in progress!!!</em></p>
    <table rules="all">      <tr>
        <th>Authority</th>
        <th>Planning inquiry system</th>
        <th>News Feed</th>
        <th>Map of recent applications</th>
      </tr>
<?php foreach ($sites as $code => $site) { ?>
      <tr>
        <td><?php e($site['name']); ?></td>
        <td><a href="<?php e($site['url'] . $site['homepage']); ?>"><?php e($site['system']); ?></a></td>
        <td><a href="http://scraperwikiviews.com/run/irish_planning_applications_feed/?county=<?php e($code); ?>">Atom</a></td>
        <td><?php if (empty($site['map'])) { echo '–'; } else { ?><a href="<?php e($site['map']); ?>">Map</a><?php } ?></td>
      </tr>
<?php } ?>
      <tr>
        <td><strong>All</strong></td>
        <td>–</td>
        <td><a href="http://scraperwikiviews.com/run/irish_planning_applications_feed/?county=all">Atom</a></td>
        <td>–</td>
      </tr>
    </table>
    <p>Do you want to help adding more councils? Then get in touch on the <a href="https://groups.google.com/group/open-data-ireland">Open Data Ireland</a> Google Group mailing list!</p>
  </body>
</html>
<?php
    die();
}

scraperwiki::httpresponseheader('Content-Type', 'application/atom+xml');

$max_age_days = 28;
$max_entries = 50;
$start = date('Y-m-d', time() - $max_age_days * 24 * 60 * 60);
$query = "appref, date, url, address, applicant, details, lat, lng, county FROM src.swdata WHERE date >= '$start' ";
if (!empty($county)) {
    $query .= sprintf("AND county='%s' ", $county);
}
$query .= "ORDER BY date DESC, appref DESC LIMIT $max_entries";
$data = scraperwiki::select($query);

$max_date = $start;
foreach ($data as $app) {
  if ($app['date'] > $max_date) $max_date = $app['date'];
}

echo "<?xml version=\"1.0\"?>\n";

?><feed xmlns="http://www.w3.org/2005/Atom">
  <title>Planning Applications</title>
  <subtitle>Recent planning applications submitted to local councils, powered by ScraperWiki</subtitle>
  <link href="http://scraperwiki.com/scrapers/irish_planning_applications/"/>
  <link rel="self" href="<?php e($url); ?>"/>
  <updated><?php e($max_date); ?>T06:00:00Z</updated>
  <generator uri="http://scraperwiki.com/views/irish_planning_applications_feed/">ScraperWiki</generator>
  <id><?php e($url); ?></id>
<?php foreach ($data as $app) { ?>
  <entry>
    <title><?php e((($county != all) ? ($sites[$app['county']]['name'] . ': ') : '') . str_replace("\n", ", ", $app['address'])); ?> [<?php e($app['appref']); ?>]</title>
    <link href="<?php e($app['url']); ?>"/>
    <id>tag:lab.linkeddata.deri.ie,2011:planning-apps:<?php e($app['county']) . ':' . e($app['appref']); ?></id>
    <updated><?php e($app['date']); ?>T06:00:00Z</updated>
    <author><name><?php e($app['applicant']); ?></name></author>
    <content type="xhtml" xml:lang="en">
      <div xmlns="http://www.w3.org/1999/xhtml">
        <p><?php e($app['details']); ?></p>
<?php if (isset($app['lat'])) { ?>
        <p><img src="<?php e('http://maps.google.com/maps/api/staticmap?size=200x200&zoom=' . ($sites[$app['county']]['googlemaps_lowres'] ? 15 : 16) . '&maptype=hybrid&markers=size:mid|' . $app['lat'] . ',' . $app['lng']. '&sensor=false'); ?>" /></p>
<?php } ?>
      </div>
    </content>
  </entry>
<?php } ?>
</feed>
<!-- ScraperWiki insists on inserting this block, but it's not valid XML, so we put it into a comment
<div id="scraperwikipane"/>
-->
<?php

function e($s) {
  echo htmlspecialchars($s);
}