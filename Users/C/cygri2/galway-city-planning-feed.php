<?php

scraperwiki::httpresponseheader('Content-Type', 'application/atom+xml');

$url = 'http://scraperwikiviews.com/run/galway-city-planning-feed/';
scraperwiki::attach('latest-galway-city-planning-applications', 'src');

$max_age_days = 28;
$max_entries = 20;
$start = date('Y-m-d', time() - $max_age_days * 24 * 60 * 60);
$query = "appref, date, url, address, applicant, details, lat, lng FROM src.swdata WHERE date >= '$start' ORDER BY date DESC LIMIT $max_entries";
$data = scraperwiki::select($query);

$max_date = $start;
foreach ($data as $app) {
  if ($app['date'] > $max_date) $max_date = $app['date'];
}

echo "<?xml version=\"1.0\"?>\n";

?><feed xmlns="http://www.w3.org/2005/Atom">
  <title>Galway City planning applications</title>
  <subtitle>Recent planning applications submitted to Galway City Council, powered by ScraperWiki</subtitle>
  <link href="http://scraperwikiviews.com/run/map-latest-galway-city-planning-apps"/>
  <link rel="self" href="<?php e($url); ?>"/>
  <updated><?php e($max_date); ?>T06:00:00Z</updated>
  <generator uri="http://scraperwiki.com/views/galway-city-planning-feed/">ScraperWiki</generator>
  <id><?php e($url); ?></id>
<?php foreach ($data as $app) { ?>
  <entry>
    <title><?php e($app['address']); ?> [<?php e($app['appref']); ?>]</title>
    <link href="<?php e($app['url']); ?>"/>
    <id>http://scraperwikiviews.com/run/galway-city-planning-feed#<?php e($app['appref']); ?></id>
    <updated><?php e($app['date']); ?>T06:00:00Z</updated>
    <author><name><?php e($app['applicant']); ?></name></author>
    <content type="xhtml" xml:lang="en">
      <div xmlns="http://www.w3.org/1999/xhtml">
        <p><?php e($app['details']); ?></p>
<?php if (isset($app['lat'])) { ?>
        <p><img src="<?php e('http://maps.google.com/maps/api/staticmap?size=200x200&zoom=16&maptype=hybrid&markers=size:mid|' . $app['lat'] . ',' . $app['lng']. '&sensor=false'); ?>" /></p>
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