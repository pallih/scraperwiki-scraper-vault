<?php

# Type mangling
$s = json_encode( array('id'=>'245456'), JSON_NUMERIC_CHECK );
print $s;

# Non-type mangling
$s = json_encode( array('id'=>'245456') );
print $s;

scraperwiki::save_sqlite(array('id'), array('id'=>'33', 'field'=>'0345345345'));

?>
