<?php
scraperwiki::attach("communication_log");

$mode = $_SERVER['URLQUERY'];

$sql = "behalf, count(behalf) AS c FROM contact GROUP BY behalf ORDER by behalf";
if ($mode == 'count') {
    $sql = "behalf, count(behalf) AS c FROM contact GROUP BY behalf ORDER by c DESC";
?>Order by <a href="?alpha">name</a>/count<br/><?php
} else {
?>Order by name/<a href="?count">count</a><br/><?php
}

$data = scraperwiki::select($sql);
foreach ($data as $row) {
?>
    <a href="../communication_log_lobbier/?<?= urlencode($row['behalf']) ?>"><?= htmlentities($row['behalf']) ?> (<?= $row['c'] ?>)</a><br/>
<?php
}
?>
