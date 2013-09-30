<?php
// You can't get_var before you've (ever) used save_var...
scraperwiki::save(array('id'), array('id'=>7));
// So this generates an error:
scraperwiki::get_var('last_postcode','00000');
?>
<?php
// You can't get_var before you've (ever) used save_var...
scraperwiki::save(array('id'), array('id'=>7));
// So this generates an error:
scraperwiki::get_var('last_postcode','00000');
?>
