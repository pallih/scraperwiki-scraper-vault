<?php

scraperwiki::httpresponseheader('Content-Type', 'application/json');

// Clear datastore
// scraperwiki::sqliteexecute("delete from swdata");
// scraperwiki::sqlitecommit();

if (isset($_POST['data'])) {
  $data=json_decode($_POST['data']);
  $uniques=isset($_POST['uniques']) ? json_decode($_POST['uniques']):array();
  $table_name=isset($_POST['table_name']) ? $_POST['table_name']:'swdata';
  scraperwiki::save($uniques,$data,$table_name);
  echo '{status:"You saved to the datastore."}';
} else {
  echo '{status:"Nothing happened."}';
}
?>
<?php

scraperwiki::httpresponseheader('Content-Type', 'application/json');

// Clear datastore
// scraperwiki::sqliteexecute("delete from swdata");
// scraperwiki::sqlitecommit();

if (isset($_POST['data'])) {
  $data=json_decode($_POST['data']);
  $uniques=isset($_POST['uniques']) ? json_decode($_POST['uniques']):array();
  $table_name=isset($_POST['table_name']) ? $_POST['table_name']:'swdata';
  scraperwiki::save($uniques,$data,$table_name);
  echo '{status:"You saved to the datastore."}';
} else {
  echo '{status:"Nothing happened."}';
}
?>
