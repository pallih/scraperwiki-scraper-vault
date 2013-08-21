require 'kconv'

def main()
  source_scraper = 'findnico2'
  ScraperWiki.attach(source_scraper)
  data = ScraperWiki.select("* from #{source_scraper}.swdata limit 500")
  puts '<table>'
  data.each do |d|
    puts td(d['image_url'], d['page_url'], d['page_title'], d['description'])
  end
  puts '</table>'
end

def td(image_url, page_url, page_title, description)
  return <<EOS
<tr>
  <td valign="top">
    <a href="#{image_url}">
      <img src="#{image_url}" width="200" />
    </a>
  </td>
  <td valign="top" width="500">
    <a href="#{page_url}">#{page_title}</a>
    <br />
    <p>
      #{description}
    </p>
  </td>
</tr>
EOS
end

main
