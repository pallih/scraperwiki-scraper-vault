# Blank Ruby
# encoding: utf-8

require 'mechanize'
require 'date'
require 'yaml'
require 'json'
require 'digest/md5'

url = 'http://bitly.com/a/sign_in'
perpage = 10
agent = Mechanize.new
agent.user_agent_alias = 'Linux Mozilla'
page = agent.get(url)

auth_form = page.forms.first
auth_form['username'] = 'thisisatest@yopmail.com'
auth_form['password'] = 'thisisatest'
page = auth_form.click_button
xsrf_form = page.forms[1]
xsrftoken = xsrf_form['_xsrf']

data_url = 'http://bitly.com/data/search'
headers = { 'X-Requested-With' => 'XMLHttpRequest', 'Content-Type' => 'application/x-www-form-urlencoded; charset=UTF-8', 'Accept' => 'application/json, text/javascript, */*', 'X-XSRFToken'=> xsrftoken}

for i in (1..10)
  params = {"search_terms" => "","page" => i,"perpage" => perpage}
  page = agent.post(data_url, params, headers)
  data = JSON.parse(page.body)
  
  arguments = ''

  data['data']['results'].each do |result|
    arguments += 'hash='+result['user_hash']+'&'
  end
  page = agent.post("http://bitly.com/data/clicks",arguments[0..-2], headers)
  clicks_data = JSON.parse(page.body)
  click_data = {}
  clicks_data['data']['clicks'].each do |click|
    click_data[click['user_hash']]  = click
  end
  
  
  data['data']['results'].each do |result|
  record = {
     'domain' => result['domain'],
     'keyword' => result['keyword'],
     'title' => result['title'],
     'url' => result['url'],
     'mts'=> result['mts'],
     'ts' => result['ts'],
     'private' => result['private'],
     'global_hash'=> result['global_hash'],
     'user'=> result['user'],
     'media_type' => result['media_type'],
     '_id' => result['_id'],
     'user_hash' => result['user_hash'],
     'global_clicks' => click_data[result['user_hash']]['global_clicks'],
     'user_clicks' => click_data[result['user_hash']]['user_clicks'],
     'key' => Digest::MD5.hexdigest(result['user_hash']+result['global_hash'])
   }
  ScraperWiki.save_sqlite(['key'], record)
  end
  if data['data']['results'].length < perpage
    break
  end
end