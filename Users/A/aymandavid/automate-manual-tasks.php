<?php
$diary_entries = array('121799','121899','121999','122199','122099','122399','122299',
'122699','122499','122799','122899','123099','122999','010800','123199','010100',
'010200','010500','010300','010700','010600','010900','011000','012100','011400',
'070700','012200','021500','071400','070800','071200','071300','073000','072000',
'072900','072800','073100','021801','021901','122802','122902','030301','030401',
'042701');
sort($diary_entries);
$as_timestamps = array();
$i = 0;
foreach ($diary_entries as $s) {
  $month = substr($s, 0, 2);
  $day = substr($s, 2, 2);
  $year = substr($s, 4, 2);
  $unix_timestamp = mktime(0,0,0, $month, $day, $year);
  print("$s = $unix_timestamp<br>");
  $as_timestamps[$i] = $unix_timestamp;
  $i++;
}
sort($as_timestamps);
print("<br>Now sorted by timestamp, oldest to newest<br>");
foreach ($as_timestamps as $s) {
  $diary_entry = date("mdy", $s);
  print("$s = $diary_entry<br>");
}

$last_diary = $as_timestamps[$i-2];
$diary_entry = date("mdy", $last_diary);
print("<br>Most recent diary entry is: <b>$diary_entry</b>");
?>
