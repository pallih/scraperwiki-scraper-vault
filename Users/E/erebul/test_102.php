<?php
scraperwiki::sqliteexecute("CREATE TABLE IF NOT EXISTS `links` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `url` varchar(250) NOT NULL,
  `status` tinyint(1) NOT NULL DEFAULT '0',
  `title` varchar(350) NOT NULL,
  `description` varchar(350) NOT NULL,
  `keywords` varchar(350) NOT NULL,
  `kcount` int(5) NOT NULL DEFAULT '0',
  `density` text NOT NULL,
  `headers` text NOT NULL,
  `ip` varchar(250) NOT NULL,
  `dns` varchar(250) NOT NULL,
  `records` text NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `url` (`url`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 AUTO_INCREMENT=1;");
