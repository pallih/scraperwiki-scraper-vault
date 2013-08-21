<?php

// set_time_limit(3); // can't find setrlimit, and this is not it

$x = "1.0";
for ($i = 1.0; $i++; $i < 10000000) {
    $x = bcmul($x, $i);
    if (!($i % 1000)) {
        $rlimit = posix_getrlimit();
        print (string)$i . " " . (string)strlen((string)$x) . " " . $rlimit['soft cpu'] . " " . $rlimit['hard cpu']. "\n";
    }
}
