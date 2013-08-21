require 'mechanize'

agent = Mechanize.new do |a|
  a.verify_mode = OpenSSL::SSL::VERIFY_NONE
  a.foobar
end

p agent.get('https://www.google.com')
