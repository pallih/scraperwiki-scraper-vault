<?php
// From this bug: http://sourceforge.net/tracker/index.php?func=detail&aid=3399037&group_id=218559&atid=1044037

require_once("scraperwiki/simple_html_dom.php");

$html = str_get_html('
<table>
<thead>
<tr>
<th>THIS IS THE WRONG ONE</th>
</tr>
</thead>
<tbody>
<tr>
<td>THIS ONE IS CORRECT</td>
</tr>
</tbody>
</table>
');

echo $html->find('table tbody tr', 0)->innertext;
?><?php
// From this bug: http://sourceforge.net/tracker/index.php?func=detail&aid=3399037&group_id=218559&atid=1044037

require_once("scraperwiki/simple_html_dom.php");

$html = str_get_html('
<table>
<thead>
<tr>
<th>THIS IS THE WRONG ONE</th>
</tr>
</thead>
<tbody>
<tr>
<td>THIS ONE IS CORRECT</td>
</tr>
</tbody>
</table>
');

echo $html->find('table tbody tr', 0)->innertext;
?>