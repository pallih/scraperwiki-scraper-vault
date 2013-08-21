<?php
function make_pairs($str) {
  $pairs = array();
  $chars = explode(',', $str);
  for ($i = 0; $i <= count($chars); $i++) {
    $f = array_shift($chars);
    foreach ($chars as $char) {
      $pairs[] = "$f,$char\n";
    }
  }
    return $pairs;
}

$handle = fopen('https://docs.google.com/spreadsheet/pub?key=0Aqqh1cRUSxC-dG1GdnU2YzFTTjVrT2hneng0R1JYWHc&single=true&gid=4&output=csv', 'r');
$row = 0;
    while (($data = fgetcsv($handle, 1000, ",")) !== FALSE) {
        $meetings[] = $data[0];
        $row++;
    }
    fclose($handle);
foreach ($meetings as $meeting) {
    $meet = make_pairs($meeting);
    foreach ($meet as $ameet) {
        $pairs[] = trim($ameet);
    }
}

$pairs = array_unique($pairs);
foreach ($pairs as $pair){
    $pair = preg_replace('/[[:^print:]]/', '', $pair); //weird non-printing characters with Patrick O'Flynn
    $pair = preg_replace('/D"ancona/', 'D\'Ancona', $pair); //weird behaviour with Matthew D'Ancona.
    echo "\"$pair\"<br>";
}

?>
