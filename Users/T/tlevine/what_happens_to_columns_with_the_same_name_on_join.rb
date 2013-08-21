require 'scraperwiki'

ScraperWiki.save_sqlite(["id"], {"id" => 1, "answer" => 42}, table_name = "foo")
ScraperWiki.save_sqlite(["id"], {"id" => 1, "answer" => 42}, table_name = "bar")

should_be = {
  "foo.id" => 1,
  "foo.answer" => 42,
  "bar.id" => 1,
  "bar.answer" => 42
}

should_not_be = {
  "id" => 1,
  "answer" => 42
}

should_not_be = ScraperWiki.select('* from foo join bar on foo.id = bar.id')

puts "It should be this."
puts should_be
puts "It is this."
puts should_not_be