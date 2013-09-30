<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN"
   "http://www.w3.org/TR/html4/strict.dtd">
<HTML>
  <HEAD>
   <STYLE type="text/css">
a { font-weight: bold; color: #ffa; text-decoration: none; }
div { margin-bottom: 10px; }
body { background: #441300; }
   </STYLE>
  </HEAD>
  <BODY>

<?php
# Blank PHP
$sourcescraper = 'cooperative_directories';

scraperwiki::attach($sourcescraper);
 $data = scraperwiki::select(           
    "* from cooperative_directories.swdata order by 'Name of directory'"
);

# Leave some space for scraperwiki's banner - any way to predict its height?
print "<br />\n";
print "<br />\n";
foreach($data as $d){
  print "<div><a href='" . $d['Link to directory'] . "'>" . $d['Name of directory'] . "</a></div>\n";
}

?>

  </BODY>
</HTML>
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN"
   "http://www.w3.org/TR/html4/strict.dtd">
<HTML>
  <HEAD>
   <STYLE type="text/css">
a { font-weight: bold; color: #ffa; text-decoration: none; }
div { margin-bottom: 10px; }
body { background: #441300; }
   </STYLE>
  </HEAD>
  <BODY>

<?php
# Blank PHP
$sourcescraper = 'cooperative_directories';

scraperwiki::attach($sourcescraper);
 $data = scraperwiki::select(           
    "* from cooperative_directories.swdata order by 'Name of directory'"
);

# Leave some space for scraperwiki's banner - any way to predict its height?
print "<br />\n";
print "<br />\n";
foreach($data as $d){
  print "<div><a href='" . $d['Link to directory'] . "'>" . $d['Name of directory'] . "</a></div>\n";
}

?>

  </BODY>
</HTML>
