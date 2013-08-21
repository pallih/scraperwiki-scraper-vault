require 'scraperwiki'
require 'active_support'
Process.setrlimit(Process::RLIMIT_CPU, 1, 2)
def call_true
  
  x = 2
  while true do
    sleep(2.seconds)
    a = x**x
    p a
  end
end

begin
  call_true
#rescue ScraperWiki.Error => ex
rescue Exception => ex
  p ex 
  if ex.message.match('CPU')
    puts "CPU exception caught"
  else
    puts "Error, unexpected exception"
  end
end