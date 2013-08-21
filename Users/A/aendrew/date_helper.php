<?php
# Blank PHP


if (empty($_GET)) exit("Construct query as such: ?from=YEAR&to=YEAR&string=Last day of June");

$to = $_GET['to'];
$from = $_GET['from'];
$str = $_GET['string'];

for ($i=$from; $i <= $to; $i++) {
$date = strtotime($str . ' ' . $i);
$endofweek = date('+2 days', date($date));
echo $endofweek; exit;

if (date('M', $date) != date('M', $endofweek)) {
echo date('M', $date) . ' : '. date('M', $endofweek);
$aweek = 604800;
$date = $date - $aweek;
}

echo $i . ' : ' . date('D, d M Y', $date)  . "<br />";

}
?>
