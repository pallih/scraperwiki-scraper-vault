<?php
# The @ should suppress errors on that line, but doesn't in ScraperWiki.
    # @ is described here: http://www.phpbuilder.com/manual/language.operators.errorcontrol.php

$my_file = @file ('non_existent_file') or
   die ("Failed opening file\n");

?>
