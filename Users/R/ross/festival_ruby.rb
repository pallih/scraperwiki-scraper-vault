require 'rubygems'
require 'mechanize'

a = Mechanize.new { |agent|
  agent.user_agent_alias = 'Mac Safari'
}

a.get('http://www.festivalsearcher.com/festivallists.aspx?region=uk') do |page|

  p page.at('body')
endrequire 'rubygems'
require 'mechanize'

a = Mechanize.new { |agent|
  agent.user_agent_alias = 'Mac Safari'
}

a.get('http://www.festivalsearcher.com/festivallists.aspx?region=uk') do |page|

  p page.at('body')
endrequire 'rubygems'
require 'mechanize'

a = Mechanize.new { |agent|
  agent.user_agent_alias = 'Mac Safari'
}

a.get('http://www.festivalsearcher.com/festivallists.aspx?region=uk') do |page|

  p page.at('body')
endrequire 'rubygems'
require 'mechanize'

a = Mechanize.new { |agent|
  agent.user_agent_alias = 'Mac Safari'
}

a.get('http://www.festivalsearcher.com/festivallists.aspx?region=uk') do |page|

  p page.at('body')
end