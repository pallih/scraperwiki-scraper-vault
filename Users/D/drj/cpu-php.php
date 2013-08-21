<?php

echo "php started\n";
set_time_limit(1);
$x=2;
try {
    while(true) {
        $a = $x*$x;
    }
} catch (Exception $e) {
    echo $e . " was caught";
}
?>
