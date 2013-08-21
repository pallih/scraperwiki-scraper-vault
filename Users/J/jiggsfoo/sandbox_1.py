# Blank Python
import scraperwiki

scraperwiki.sqlite.attach("15th_philippine_congress_members", "congress")

scraperwiki.sqlite.execute("drop table if exists foo")
scraperwiki.sqlite.execute("CREATE TABLE `foo` (`committee_name` text, `committee_id` text)")
scraperwiki.sqlite.execute("INSERT INTO `foo` (`committee_name`, `committee_id`) SELECT `committee_name`, `committee_id` FROM congress.congcommittees")
scraperwiki.sqlite.commit()