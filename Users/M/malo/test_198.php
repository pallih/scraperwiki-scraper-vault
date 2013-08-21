<?php
require 'http://www.wipo.int/amc/en/domains/search/text.jsp?case=D2013-0001'; $html_content = scraperwiki::scrape("http://www.wipo.int/amc/en/domains/search/text.jsp?case=D2013-0001"); $html = str_get_html($html_content);


?>
