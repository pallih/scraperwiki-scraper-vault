<?php
# Blank PHP
$source = 'drupal_commerce_modules';
scraperwiki::attach($source);

$data = scraperwiki::select(           
    "* from swdata"
);

foreach($data as $d){
  if ($d['module_pg_type'] == "Sandbox") {
    $msg = " is &lt;reply&gt;".$d['name']." (".strtolower($d['module_pg_type']).") by ".$d['author']." ".$d['url']." (".$d['installs']." Installs / ".$d['downloads']." Downloads)";
    $msg .= " - ".$d['description']."<br />";
    print "drupalcommerce: ".str_replace(" ","_",strtolower($d['name'])).$msg;
    print "drupalcommerce: ".str_replace(" ","_",trim(str_replace("commerce","",strtolower($d['name'])))).$msg;
  } else {
    $msg = " is &lt;reply&gt;".$d['name']." (".strtolower($d['module_pg_type']).") by ".$d['author']." http://dgo.to/".$d['url']." (".$d['installs']." Installs / ".$d['downloads']." Downloads)";
    $msg .= " - ".$d['description']."<br />";
    print "drupalcommerce: ".$d['url'].$msg;
    print "drupalcommerce: ".str_replace(array("commerce_","_commerce"),"",$d['url']).$msg;
  }
}
?>
