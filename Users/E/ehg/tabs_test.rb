20.times { |i| ScraperWiki.save_sqlite ['id'], { 'id' => i }, "table_#{i}" }

