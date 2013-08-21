<?php
# A temporary view, much worse than the original site!

scraperwiki::attach("un_test_2"); 

$data = scraperwiki::select(           
    "* from un_test_2.swdata"
);
foreach ($data as $img) {
    print "<img src=\"" . $img["url"] . "\"><br>";
}

?>
