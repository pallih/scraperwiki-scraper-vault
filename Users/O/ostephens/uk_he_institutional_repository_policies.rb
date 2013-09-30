require 'nokogiri'
require 'open-uri'

url = "http://opendoar.org/api13.php?co=gb&rt=2&show=policy"
xml = ScraperWiki.scrape(url)
doc = Nokogiri::XML(xml)
doc.xpath("//repositories/repository").each do |repo|
  id = repo.attribute("rID")
  name = repo.xpath("rName").inner_text
  url = repo.xpath("rUrl").inner_text
  oai_base = repo.xpath("rOaiBaseUrl").inner_text
  if oai_base.length == 0
    puts name
  end
  mgrade = "No Metadata Policy found"
  mstandard = ""
  dgrade = "No Data Policy found"
  dstandard = ""
  repo.xpath("policies/policy").each do |policy|
    type = policy.xpath("policyType").inner_text
    if type == "Metadata"
      mgrade = policy.xpath("policyGrade").inner_text
      mstandard = policy.xpath("poStandard").inner_text
    end
    if type == "Data"
      dgrade = policy.xpath("policyGrade").inner_text
      dstandard = policy.xpath("poStandard").inner_text
    end
  end
#  oaixml = ScraperWiki.scrape(oai_base.to_s + "?verb=Identify")
#  iddoc = Nokogiri::XML(oaixml)
#  oai_mstandard = iddoc.xpath("//description/metadataPolicy").inner_text
#  oai_dstandard = iddoc.xpath("//description/dataPolicy").inner_text
#  ScraperWiki.save(unique_keys=['Repository ID'], data={'Repository ID' => id, 'Repository Name' => name, 'Repository URL' => url, 'Repository OAI-PMH base' => oai_base, 'Metadata Policy Summary' => mgrade, 'Metadata Policy Detail' => mstandard, 'Data Policy Summary' => dgrade, 'Data Policy Detail' => dstandard, 'Metadata Policy via OAI Identify' => oai_mstandard, 'Data Policy via OAI Identify' => oai_dstandard})
  ScraperWiki.save(unique_keys=['Repository ID'], data={'Repository ID' => id, 'Repository Name' => name, 'Repository URL' => url, 'Repository OAI-PMH base' => oai_base, 'Metadata Policy Summary' => mgrade, 'Metadata Policy Detail' => mstandard, 'Data Policy Summary' => dgrade, 'Data Policy Detail' => dstandard})
end

require 'nokogiri'
require 'open-uri'

url = "http://opendoar.org/api13.php?co=gb&rt=2&show=policy"
xml = ScraperWiki.scrape(url)
doc = Nokogiri::XML(xml)
doc.xpath("//repositories/repository").each do |repo|
  id = repo.attribute("rID")
  name = repo.xpath("rName").inner_text
  url = repo.xpath("rUrl").inner_text
  oai_base = repo.xpath("rOaiBaseUrl").inner_text
  if oai_base.length == 0
    puts name
  end
  mgrade = "No Metadata Policy found"
  mstandard = ""
  dgrade = "No Data Policy found"
  dstandard = ""
  repo.xpath("policies/policy").each do |policy|
    type = policy.xpath("policyType").inner_text
    if type == "Metadata"
      mgrade = policy.xpath("policyGrade").inner_text
      mstandard = policy.xpath("poStandard").inner_text
    end
    if type == "Data"
      dgrade = policy.xpath("policyGrade").inner_text
      dstandard = policy.xpath("poStandard").inner_text
    end
  end
#  oaixml = ScraperWiki.scrape(oai_base.to_s + "?verb=Identify")
#  iddoc = Nokogiri::XML(oaixml)
#  oai_mstandard = iddoc.xpath("//description/metadataPolicy").inner_text
#  oai_dstandard = iddoc.xpath("//description/dataPolicy").inner_text
#  ScraperWiki.save(unique_keys=['Repository ID'], data={'Repository ID' => id, 'Repository Name' => name, 'Repository URL' => url, 'Repository OAI-PMH base' => oai_base, 'Metadata Policy Summary' => mgrade, 'Metadata Policy Detail' => mstandard, 'Data Policy Summary' => dgrade, 'Data Policy Detail' => dstandard, 'Metadata Policy via OAI Identify' => oai_mstandard, 'Data Policy via OAI Identify' => oai_dstandard})
  ScraperWiki.save(unique_keys=['Repository ID'], data={'Repository ID' => id, 'Repository Name' => name, 'Repository URL' => url, 'Repository OAI-PMH base' => oai_base, 'Metadata Policy Summary' => mgrade, 'Metadata Policy Detail' => mstandard, 'Data Policy Summary' => dgrade, 'Data Policy Detail' => dstandard})
end

