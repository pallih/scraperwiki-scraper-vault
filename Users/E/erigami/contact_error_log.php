<?php
# Blank PHP
$sourcescraper = 'communication_log';
scraperwiki::attach("communication_log");

$sql = "* FROM contact WHERE iserror=1";
$data = scraperwiki::select($sql);

foreach ($data as $row) {
?>
    <a href="<?= $row['uri'] ?>"><?= htmlentities($row['uri']) ?> (<?= $row['contact_id'] ?>)</a><br/>
<?php
}
?><?php
# Blank PHP
$sourcescraper = 'communication_log';
scraperwiki::attach("communication_log");

$sql = "* FROM contact WHERE iserror=1";
$data = scraperwiki::select($sql);

foreach ($data as $row) {
?>
    <a href="<?= $row['uri'] ?>"><?= htmlentities($row['uri']) ?> (<?= $row['contact_id'] ?>)</a><br/>
<?php
}
?>