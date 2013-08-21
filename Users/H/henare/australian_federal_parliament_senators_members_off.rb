require 'mechanize'

def save_results_from_page(page, house)
  page.at('.search-filter-results').search(:li).each do |i|
    electorate, party, contact_page, email, facebook, twitter = nil, nil, nil, nil, nil, nil

    aph_id = i.at('.title').at(:a).attr(:href).match(/MPID\=(.*)/)[1]

    i.at(:dl).search(:dt).each do |dt|
      case dt.inner_text
      when 'Member for', 'Senator for'
        electorate = dt.next_element.inner_text
      when 'Party'
        party = dt.next_element.inner_text
      end
    end

    email = i.search('.social.mail').at(:a).attr(:href).gsub('mailto:', '') unless i.search('.social.mail').empty? 
    facebook = i.search('.social.facebook').at(:a).attr(:href) unless i.search('.social.facebook').empty? 
    twitter = i.search('.social.twitter').at(:a).attr(:href) unless i.search('.social.twitter').empty? 

    profile_page_url = "http://www.aph.gov.au#{i.at('.title').at(:a).attr(:href)}"
    profile_page = @agent.get profile_page_url
    website = profile_page.link_with(text: 'Personal website').href if profile_page.link_with(text: 'Personal website')

    record = {
      house: house,
      aph_id: aph_id,
      full_name: i.at('.title').inner_text,
      electorate: electorate,
      party: party,
      profile_page: profile_page_url,
      # Some members don't list this page on their profile (WTF?!) but generating this URL works fine
      contact_page: "http://www.aph.gov.au/Senators_and_Members/Contact_Senator_or_Member?MPID=#{aph_id}",
      photo_url: i.at('.thumbnail').at(:img).attr(:src),
      email: email,
      facebook: facebook,
      twitter: twitter,
      website: website
    }

    ScraperWiki::save_sqlite [:aph_id], record
  end
end

@agent = Mechanize.new
search_url = 'http://www.aph.gov.au/Senators_and_Members/Parliamentarian_Search_Results'

page = @agent.get "#{search_url}?mem=1&q="

while page.link_with(:text => 'Next')
  save_results_from_page(page, :representatives)
  page = @agent.get search_url + page.link_with(:text => 'Next').href
end

page = @agent.get "#{search_url}?sen=1&q="

while page.link_with(:text => 'Next')
  save_results_from_page(page, :senate)
  page = @agent.get search_url + page.link_with(:text => 'Next').href
end
require 'mechanize'

def save_results_from_page(page, house)
  page.at('.search-filter-results').search(:li).each do |i|
    electorate, party, contact_page, email, facebook, twitter = nil, nil, nil, nil, nil, nil

    aph_id = i.at('.title').at(:a).attr(:href).match(/MPID\=(.*)/)[1]

    i.at(:dl).search(:dt).each do |dt|
      case dt.inner_text
      when 'Member for', 'Senator for'
        electorate = dt.next_element.inner_text
      when 'Party'
        party = dt.next_element.inner_text
      end
    end

    email = i.search('.social.mail').at(:a).attr(:href).gsub('mailto:', '') unless i.search('.social.mail').empty? 
    facebook = i.search('.social.facebook').at(:a).attr(:href) unless i.search('.social.facebook').empty? 
    twitter = i.search('.social.twitter').at(:a).attr(:href) unless i.search('.social.twitter').empty? 

    profile_page_url = "http://www.aph.gov.au#{i.at('.title').at(:a).attr(:href)}"
    profile_page = @agent.get profile_page_url
    website = profile_page.link_with(text: 'Personal website').href if profile_page.link_with(text: 'Personal website')

    record = {
      house: house,
      aph_id: aph_id,
      full_name: i.at('.title').inner_text,
      electorate: electorate,
      party: party,
      profile_page: profile_page_url,
      # Some members don't list this page on their profile (WTF?!) but generating this URL works fine
      contact_page: "http://www.aph.gov.au/Senators_and_Members/Contact_Senator_or_Member?MPID=#{aph_id}",
      photo_url: i.at('.thumbnail').at(:img).attr(:src),
      email: email,
      facebook: facebook,
      twitter: twitter,
      website: website
    }

    ScraperWiki::save_sqlite [:aph_id], record
  end
end

@agent = Mechanize.new
search_url = 'http://www.aph.gov.au/Senators_and_Members/Parliamentarian_Search_Results'

page = @agent.get "#{search_url}?mem=1&q="

while page.link_with(:text => 'Next')
  save_results_from_page(page, :representatives)
  page = @agent.get search_url + page.link_with(:text => 'Next').href
end

page = @agent.get "#{search_url}?sen=1&q="

while page.link_with(:text => 'Next')
  save_results_from_page(page, :senate)
  page = @agent.get search_url + page.link_with(:text => 'Next').href
end
