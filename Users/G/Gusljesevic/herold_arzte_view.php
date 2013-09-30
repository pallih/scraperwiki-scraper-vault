<?php
print "This is a <em>fragment</em> of HTML.";  
scraperwiki::attach("herold_artzte");
$data = scraperwiki::select(
    "* swdata limit 10 "
);
print json_encode($data);
?>
<?php
print "This is a <em>fragment</em> of HTML.";  
scraperwiki::attach("herold_artzte");
$data = scraperwiki::select(
    "* swdata limit 10 "
);
print json_encode($data);
?>
