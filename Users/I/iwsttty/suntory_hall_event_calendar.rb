# Blank Ruby

require 'nokogiri'

$KCODE = 'u'
$now = Time.now

def main

  today = Date.today

  [0, 1, 2].each do |n|
    mon = today >> n
    p mon.strftime("%y%m")
  end

end

main
