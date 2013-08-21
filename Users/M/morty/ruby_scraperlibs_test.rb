require "test/unit"

Test::Unit.run=true # Turn off automatic running of the tests

class TestScraperlibs < Test::Unit::TestCase
  def test_scrape
     assert_equal(446, ScraperWiki.scrape("http://scraperwiki.com/hello_world.html").length)
  end

  def test_scrape_with_parameters
    html = ScraperWiki.scrape("http://scraperwiki.com/search/", {"q" => "scraperwiki"})
    assert_not_nil(ScraperWiki.scrape("http://scraperwiki.com/search/", {"q" => "scraperwiki"}).index /\d+ results found/)
  end

  def test_gb_postcode_to_latlng
    assert_equal([51.5035384091066, -0.127695241051564], ScraperWiki.gb_postcode_to_latlng("SW1A 2AA"))
  end

  def test_unicode_truncate_ascii_string
    assert_equal('123', ScraperWiki._unicode_truncate('12345', 3))
  end

  def test_unicode_truncate_unicode_string
    assert_equal('ççç', ScraperWiki._unicode_truncate('çççççç', 3))
  end

  def test_metadata
    key = rand(36**8).to_s(36)
    val = rand(36**8).to_s(36)
    ScraperWiki.save_metadata(key, val)
    assert_equal(val, ScraperWiki.get_metadata(key))
  end

  def test_vars
    key = rand(36**8).to_s(36)
    val = rand(36**8).to_s(36)
    ScraperWiki.save_var(key, val)
    assert_equal(val, ScraperWiki.get_var(key))
  end

  def test_datastore
    random_string = rand(36**8).to_s(36)

    # Save data
    ScraperWiki.save(['random_string'], {'random_string' => random_string})

    # Get data
    assert_equal(['date_scraped', 'random_string'], ScraperWiki.getKeys('ruby_scraperlibs_test'))
    data = Array(ScraperWiki.getData('ruby_scraperlibs_test'))
    assert_not_nil(data.index{|d| d['random_string'] == random_string})
  end
end

# If unit tests fail raise and exception so the scraper will be
# marked as broken and will be displayed in the email alert
raise "Unit Tests Failed" if not Test::Unit::AutoRunner.run
