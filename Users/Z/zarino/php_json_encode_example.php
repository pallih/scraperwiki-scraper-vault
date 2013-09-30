<?php

$a = array('fb'=>array('foo', 'bar'), 'xyz'=>'abc', '123');

echo 'STANDARD USAGE: ' . json_encode($a);

$b = json_encode($a);

echo "\n";
echo "$b";
echo "\n";

echo 'JSON_FORCE_OBJECT: ' . json_encode($a, JSON_FORCE_OBJECT);

?>
<?php

$a = array('fb'=>array('foo', 'bar'), 'xyz'=>'abc', '123');

echo 'STANDARD USAGE: ' . json_encode($a);

$b = json_encode($a);

echo "\n";
echo "$b";
echo "\n";

echo 'JSON_FORCE_OBJECT: ' . json_encode($a, JSON_FORCE_OBJECT);

?>
