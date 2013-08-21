<?php
# Blank PHP
$sourcescraper = 'sr_p3_poddar';
scraperwiki::attach("sr_p3_poddar"); 
$programs = scraperwiki::select( "distinct progId from sr_p3_poddar.swdata" );
print('<?xml version="1.0" encoding="UTF-8"?>');
?>
<opml version="1.1">
    <head>
        <title>Podsändningar i P3</title>
    </head>
    <body>
<?php
foreach($programs as $program){
    print('<outline text="' . $program['progId'] . '">');
    
    $pods = scraperwiki::select( "* from sr_p3_poddar.swdata where progId=" . $program['progId'] . " limit 5" );
    
    foreach($pods as $pod) {
        print('<outline text="' . $pod['description'] . '" URL="' . $pod['url'] . '" type="audio" />');
    }
    print('</outline>');
}
?>
  </body>
</opml>
