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

$handle = fopen('https://docs.google.com/a/thetimes.co.uk/spreadsheet/pub?key=0AiO39oavotZCdGEtQVdlOUZOeEJVNHJwaDZzVjZ5a0E&single=true&gid=0&output=csv', 'r');
$row = 0;
    while (($data = fgetcsv($handle, 1000, ",")) !== FALSE) {
        $meetings[] = $data[0];
        echo $data[0];
        $row++;
    }
    fclose($handle);

foreach ($meetings as $meeting) {
    $meet = make_pairs($meeting);
    foreach ($meet as $ameet) {
        $pairs[] = trim($ameet);
    }
}

#$pairs = array_unique($pairs);
foreach ($pairs as $pair){
    echo "\"$pair\"<br>";
}

?>
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

$handle = fopen('https://docs.google.com/a/thetimes.co.uk/spreadsheet/pub?key=0AiO39oavotZCdGEtQVdlOUZOeEJVNHJwaDZzVjZ5a0E&single=true&gid=0&output=csv', 'r');
$row = 0;
    while (($data = fgetcsv($handle, 1000, ",")) !== FALSE) {
        $meetings[] = $data[0];
        echo $data[0];
        $row++;
    }
    fclose($handle);

foreach ($meetings as $meeting) {
    $meet = make_pairs($meeting);
    foreach ($meet as $ameet) {
        $pairs[] = trim($ameet);
    }
}

#$pairs = array_unique($pairs);
foreach ($pairs as $pair){
    echo "\"$pair\"<br>";
}

?>
