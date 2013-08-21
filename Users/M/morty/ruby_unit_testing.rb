require "test/unit"

Test::Unit.run=true # Turn off automatic running of the tests

class TestSimpleNumber < Test::Unit::TestCase
  def test_simple
     assert_equal(2, 1+1)
  end
end

# If unit tests fail raise and exception so the scraper will be
# marked as broken and will be displayed in the email alert
raise "Unit Tests Failed" if not Test::Unit::AutoRunner.run

