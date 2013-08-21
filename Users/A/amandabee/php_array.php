<?php

$winners = array("Amital", "Anika", "Carla");

$students = array("Amital", "Anika", "Carla", "Cesar", "Colin", "Eliza", "Ichi", "Kahliah", "Kathrine", "Lisa", " Madhura", "Martin", "Menglin", "Tom");

$bummed = array();

foreach ($students as $student) {
    if(in_array($student,$winners)) {
        print "Hi five, ".$student."!\n";
    } else {
        print "sorry, ".$student." :(\n";
        $bummed[] = $student;
    }
}

print_r($bummed);

# Documentation:
# http://php.net/manual/en/language.types.array.php
# http://us3.php.net/manual/en/control-structures.foreach.php
# http://us.php.net/in_array
?>
