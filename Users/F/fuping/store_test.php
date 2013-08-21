<?php
//scraperwiki::sqliteexecute('create table create_test(a text,b text)');
//$val2="insert into create_test values('$name','$id')";
//scraperwiki::sqliteexecute($val2);
$result=scraperwiki::select('* from tagtable');
//$data=$result[0];
//$data['rank']='2';
print count($result);
?>
