# coding: utf-8
# @see https://scraperwiki.com/scrapers/seao/

require 'json'
require 'open-uri'
require 'time'
require 'nokogiri'

unless ScraperWiki.select('name FROM sqlite_master WHERE type="table" AND name="swdata"').empty? 
  ScraperWiki.sqliteexecute 'DELETE FROM swdata'
end

class String
  # @see https://github.com/rails/rails/blob/master/activesupport/lib/active_support/inflector/methods.rb#L75
  def underscore
    word = self.dup
    word.gsub!('::', '/')
    #word.gsub!(/(?:([A-Za-z\d])|^)(#{inflections.acronym_regex})(?=\b|[^a-z])/) { "#{$1}#{$1 && '_'}#{$2.downcase}" }
    word.gsub!(/([A-Z\d]+)([A-Z][a-z])/,'\1_\2')
    word.gsub!(/([a-z\d])([A-Z])/,'\1_\2')
    word.tr!("-", "_")
    word.downcase!
    word
  end
end

class DetailPageParser
  attr_reader :parser, :attributes

  def initialize(uri)
    @parser = Nokogiri::HTML(open(uri), nil, 'utf-8')
    @attributes = {}
  end

  def add_raw(id, attribute = nil)
    add_key id, attribute
  end

  def add(id, attribute = nil)
    add_key id, attribute, ->(node) {text(node)}
  end

  def add_float(id, attribute = nil)
    add_key id, attribute, ->(node) {node.text.strip.sub(',', '.').sub(/[^\d.]/, '').to_f}
  end

  def add_row(id, attribute = nil)
    add_key id, attribute, ->(node) {text(node.parent.next_element)}
  end

private

  def add_key(id, attribute = nil, lambda = nil)
    node = @parser.at_css "##{id}"
    if node
      value = if lambda
        lambda.call(node)
      else
        node.children.to_s
      end
      unless value == 'N/A' || value.to_s.empty? 
        attribute ||= id.sub(/\AMainUserControl_lbl?/, '').sub(/Text(text|value)\z/, '').underscore.to_sym
        @attributes[attribute] = value
      end
    end
  end

  def text(node)
    # Convert <br> to newline.
    node.search('br').each do |br|
      br.replace Nokogiri::XML::Text.new("\n", node.document)
    end
    node.text.strip
  end
end

# @return [Integer] the offset at which to start the scraping run
def start
  ScraperWiki.get_var('offset', 0).to_i
end

ScraperWiki.attach 'seao'
count = ScraperWiki.select('COUNT(*) count FROM seao.swdata')[0]['count']

STEP = 1000
(start..count).step(STEP).each do |offset|
  puts "Scraping #{STEP} records at offset #{offset}"
  ScraperWiki.select("* FROM seao.swdata LIMIT #{offset},#{STEP}").each_with_index do |record,i|
    puts "Scraping #{record['uri']}"
    parser = DetailPageParser.new record['uri']
    extra = {}

    # Already have:
    # * No (no)
    # * No. Ref. (id)
    # * Statut (statut)
    # * Titre / Titre de l'avis (titre)
    # * Date de publication (publication)
    # * Type de l'avis (type)
    # * Date limite de réception des offres (fermeture)
    # * Organisation (organisation)
    #
    # Can scrape category number, if necessary.

    # Délai pour la réception des offres
    parser.add 'MainUserControl_lblReceptionDelay', :delai_pour_la_reception_des_offres # "X jours et Y heures"
    # Nature du contrat
    parser.add 'MainUserControl_lbContractType', :nature_du_contrat
    # Région(s) de livraison
    parser.add 'MainUserControl_lbDeliveryArea', :regions_de_livraison
    # Type d'adjudicataire
    parser.add 'MainUserControl_lblTendererType', :type_d_adjudicataire
    # Accord(s) applicable(s)
    parser.add 'MainUserControl_lbAccordType', :accords_applicables
    # Valeur estimée
    parser.add 'ContractValueTextvalue', :valeur_estimee
    # Montant estimé de la dépense
    parser.add_float 'MainUserControl_lblEstAmount', :montant_estime
    # Montant total estimé de la dépense incluant les options de renouvellement
    parser.add_float 'MainUserControl_lblRenewalAmount', :montant_total_estime

    # Adresse
    parser.add 'OrganizationAddressTextvalue', :organisation_adresse
    # Site Web
    parser.add_row 'WebSiteUrlTexttext', :organisation_uri
    # Responsable(s)
    # @todo extract name, tel, fax, email separately
    # Can be multiple, e.g. http://seao.ca/OpportunityPublication/avisconsultes.aspx?ItemId=5c30c588-314b-48cb-9ab7-f06d7032ce91&COpp=Search&SubCategoryCode=&callingPage=3
    parser.add_row 'MainUserControl_lbResponsable', :organisation_responsable

    # Description UNSPSC
    node = parser.parser.at_css('#MainUserControl_dgUNSPSC')
    if node
      extra[:unspsc] = []
      node.css('tr:gt(1)').each do |tr|
        extra[:unspsc] << {
          numero: tr.at_css('td:eq(1)').text.strip,
          description: tr.at_css('td:eq(2)').text.strip,
        }
      end
      if extra[:unspsc].empty? 
        extra.delete :unspsc
      else
        extra[:unspsc] = extra[:unspsc].to_json
      end
    end

    # Description
    parser.add_raw 'MainUserControl_lbDescription'

    # Fournisseur
    node = parser.parser.at_css('#MainUserControl_dgFournisseurs')
    if node
      extra[:fournisseurs] = []
      headers = node.at_css('tr:eq(1)').css('td:gt(1)').map{|x| x.text.strip.squeeze ' '}
      node.css('tr:gt(1)').each do |tr|
        hash = {
          adjudicataire_du_contrat: !!tr.at_css('td:eq(1) img'),
        }
        headers.each_with_index do |header,j|
          td = tr.at_css("td:eq(#{j + 2})")
          case header
          when 'Organisation'
            hash[:nom] = td.at_css('.titreAvis').text.strip
            value = td.at_css('a')[:href]
            hash[:uri] = value if value
            value = td.children.reject{|child|
              ['span', 'a'].include?(child.name) || child.text.strip.empty? 
            }.map{|child|
              child.text.strip
            }.join("\n")
            hash[:adresse] = value unless value.empty? 
          when 'Contact'
            value = td.text.gsub(/[[:space:]]+/, ' ').strip
            hash[:contact] = value unless value.empty? 
          when 'Conformité'
            value = td.text.gsub(/[[:space:]]+/, ' ').strip
            hash[:conformite] = value unless value.empty? 
          when 'Montant soumis',
               'Prix soumis'
            value = td.text.strip
            hash[:prix_soumis] = value.sub(',', '.').sub(/[^\d.]/, '').to_f unless value.empty? 
          when 'Montant du contrat',
               'Prix du contrat'
            value = td.text.strip
            hash[:prix_du_contrat] = value.sub(',', '.').sub(/[^\d.]/, '').to_f unless value.empty? 
          when 'Montant total de la dépense incluant les options de renouvellement',
               'Montant total de la dépense prévue incluant les options de renouvellement'
            value = td.text.gsub(/[[:space:]]+/, ' ').strip
            hash[:montant_total] = value.sub(',', '.').sub(/[^\d.]/, '').to_f unless value.empty? 
          else
            raise "Unknown fournisseur column #{header}"
          end
        end
        extra[:fournisseurs] << hash
      end
      extra[:fournisseurs] = extra[:fournisseurs].to_json
    end

    # Documents
    node = parser.parser.at_css('#MainUserControl_headerDocuments')
    if node
      node = node.next_element until node.name == 'table'
      last = {}
      extra[:documents] = []
      node.css('tr:gt(1)').each do |tr|
        size = tr.css('td').size
        next if size.zero? 
        # There will be partial rows if the table lists English and French documents separately.
        partial = size == 3
        index = partial ? 0 : 2

        unless partial
          last = {
            titre: tr.at_css('td:eq(1)').text.strip,
            description: tr.at_css('td:eq(2)').text.strip,
          }
        end

        extra[:documents] << last.merge({
          langue: tr.at_css("td:eq(#{index + 1})").text.strip,
          dimension: tr.at_css("td:eq(#{index + 2})").text.strip,
          nombre: tr.at_css("td:eq(#{index + 3})").text[/\d+/].to_i,
        })
      end
      extra[:documents] = extra[:documents].to_json
    end

    # Addenda
    node = parser.parser.at_css('#MainUserControl_headerAddendas')
    if node
      node = node.next_element until node.name == 'table'
      last = {}
      extra[:addenda] = []
      node.css('tr:gt(1)').each do |tr|
        size = tr.css('td').size
        next if size.zero? 
        # There will be partial rows if the table lists English and French addenda separately.
        partial = size == 4
        index = partial ? 0 : 2

        unless partial
          last = {
            titre: tr.at_css('td:eq(1)').text.strip,
            description: tr.at_css('td:eq(2)').text.strip,
          }
        end

        extra[:addenda] << last.merge({
          langue: tr.at_css("td:eq(#{index + 1})").text.strip,
          dimension: tr.at_css("td:eq(#{index + 2})").text.strip,
          nombre: tr.at_css("td:eq(#{index + 3})").text[/\d+/].to_i,
          publication: Time.parse(tr.at_css("td:eq(#{index + 4})").text.strip),
        })
      end
      if extra[:addenda].empty? 
        extra.delete :addenda
      else
        extra[:addenda] = extra[:addenda].to_json
      end
    end
    
    # @todo Disposition de la loi ou du règlement
    # e.g. http://seao.ca/OpportunityPublication/avisconsultes.aspx?ItemId=e76198bd-f83b-4f7b-a68f-ded0592290ae&COpp=Search&SubCategoryCode=&callingPage=3

    # @todo Conditions et critères d'admissibilité
    # Can be complex, e.g. http://seao.ca/OpportunityPublication/avisconsultes.aspx?ItemId=6e536680-8303-45dd-8163-393cab0f7318&COpp=Search&SubCategoryCode=&callingPage=3

    ScraperWiki.save_sqlite([:id], record.merge(extra).merge(parser.attributes).merge({
      updated_at: Time.now,
    }))
    ScraperWiki.save_var('offset', offset + i)
  end
end
# coding: utf-8
# @see https://scraperwiki.com/scrapers/seao/

require 'json'
require 'open-uri'
require 'time'
require 'nokogiri'

unless ScraperWiki.select('name FROM sqlite_master WHERE type="table" AND name="swdata"').empty? 
  ScraperWiki.sqliteexecute 'DELETE FROM swdata'
end

class String
  # @see https://github.com/rails/rails/blob/master/activesupport/lib/active_support/inflector/methods.rb#L75
  def underscore
    word = self.dup
    word.gsub!('::', '/')
    #word.gsub!(/(?:([A-Za-z\d])|^)(#{inflections.acronym_regex})(?=\b|[^a-z])/) { "#{$1}#{$1 && '_'}#{$2.downcase}" }
    word.gsub!(/([A-Z\d]+)([A-Z][a-z])/,'\1_\2')
    word.gsub!(/([a-z\d])([A-Z])/,'\1_\2')
    word.tr!("-", "_")
    word.downcase!
    word
  end
end

class DetailPageParser
  attr_reader :parser, :attributes

  def initialize(uri)
    @parser = Nokogiri::HTML(open(uri), nil, 'utf-8')
    @attributes = {}
  end

  def add_raw(id, attribute = nil)
    add_key id, attribute
  end

  def add(id, attribute = nil)
    add_key id, attribute, ->(node) {text(node)}
  end

  def add_float(id, attribute = nil)
    add_key id, attribute, ->(node) {node.text.strip.sub(',', '.').sub(/[^\d.]/, '').to_f}
  end

  def add_row(id, attribute = nil)
    add_key id, attribute, ->(node) {text(node.parent.next_element)}
  end

private

  def add_key(id, attribute = nil, lambda = nil)
    node = @parser.at_css "##{id}"
    if node
      value = if lambda
        lambda.call(node)
      else
        node.children.to_s
      end
      unless value == 'N/A' || value.to_s.empty? 
        attribute ||= id.sub(/\AMainUserControl_lbl?/, '').sub(/Text(text|value)\z/, '').underscore.to_sym
        @attributes[attribute] = value
      end
    end
  end

  def text(node)
    # Convert <br> to newline.
    node.search('br').each do |br|
      br.replace Nokogiri::XML::Text.new("\n", node.document)
    end
    node.text.strip
  end
end

# @return [Integer] the offset at which to start the scraping run
def start
  ScraperWiki.get_var('offset', 0).to_i
end

ScraperWiki.attach 'seao'
count = ScraperWiki.select('COUNT(*) count FROM seao.swdata')[0]['count']

STEP = 1000
(start..count).step(STEP).each do |offset|
  puts "Scraping #{STEP} records at offset #{offset}"
  ScraperWiki.select("* FROM seao.swdata LIMIT #{offset},#{STEP}").each_with_index do |record,i|
    puts "Scraping #{record['uri']}"
    parser = DetailPageParser.new record['uri']
    extra = {}

    # Already have:
    # * No (no)
    # * No. Ref. (id)
    # * Statut (statut)
    # * Titre / Titre de l'avis (titre)
    # * Date de publication (publication)
    # * Type de l'avis (type)
    # * Date limite de réception des offres (fermeture)
    # * Organisation (organisation)
    #
    # Can scrape category number, if necessary.

    # Délai pour la réception des offres
    parser.add 'MainUserControl_lblReceptionDelay', :delai_pour_la_reception_des_offres # "X jours et Y heures"
    # Nature du contrat
    parser.add 'MainUserControl_lbContractType', :nature_du_contrat
    # Région(s) de livraison
    parser.add 'MainUserControl_lbDeliveryArea', :regions_de_livraison
    # Type d'adjudicataire
    parser.add 'MainUserControl_lblTendererType', :type_d_adjudicataire
    # Accord(s) applicable(s)
    parser.add 'MainUserControl_lbAccordType', :accords_applicables
    # Valeur estimée
    parser.add 'ContractValueTextvalue', :valeur_estimee
    # Montant estimé de la dépense
    parser.add_float 'MainUserControl_lblEstAmount', :montant_estime
    # Montant total estimé de la dépense incluant les options de renouvellement
    parser.add_float 'MainUserControl_lblRenewalAmount', :montant_total_estime

    # Adresse
    parser.add 'OrganizationAddressTextvalue', :organisation_adresse
    # Site Web
    parser.add_row 'WebSiteUrlTexttext', :organisation_uri
    # Responsable(s)
    # @todo extract name, tel, fax, email separately
    # Can be multiple, e.g. http://seao.ca/OpportunityPublication/avisconsultes.aspx?ItemId=5c30c588-314b-48cb-9ab7-f06d7032ce91&COpp=Search&SubCategoryCode=&callingPage=3
    parser.add_row 'MainUserControl_lbResponsable', :organisation_responsable

    # Description UNSPSC
    node = parser.parser.at_css('#MainUserControl_dgUNSPSC')
    if node
      extra[:unspsc] = []
      node.css('tr:gt(1)').each do |tr|
        extra[:unspsc] << {
          numero: tr.at_css('td:eq(1)').text.strip,
          description: tr.at_css('td:eq(2)').text.strip,
        }
      end
      if extra[:unspsc].empty? 
        extra.delete :unspsc
      else
        extra[:unspsc] = extra[:unspsc].to_json
      end
    end

    # Description
    parser.add_raw 'MainUserControl_lbDescription'

    # Fournisseur
    node = parser.parser.at_css('#MainUserControl_dgFournisseurs')
    if node
      extra[:fournisseurs] = []
      headers = node.at_css('tr:eq(1)').css('td:gt(1)').map{|x| x.text.strip.squeeze ' '}
      node.css('tr:gt(1)').each do |tr|
        hash = {
          adjudicataire_du_contrat: !!tr.at_css('td:eq(1) img'),
        }
        headers.each_with_index do |header,j|
          td = tr.at_css("td:eq(#{j + 2})")
          case header
          when 'Organisation'
            hash[:nom] = td.at_css('.titreAvis').text.strip
            value = td.at_css('a')[:href]
            hash[:uri] = value if value
            value = td.children.reject{|child|
              ['span', 'a'].include?(child.name) || child.text.strip.empty? 
            }.map{|child|
              child.text.strip
            }.join("\n")
            hash[:adresse] = value unless value.empty? 
          when 'Contact'
            value = td.text.gsub(/[[:space:]]+/, ' ').strip
            hash[:contact] = value unless value.empty? 
          when 'Conformité'
            value = td.text.gsub(/[[:space:]]+/, ' ').strip
            hash[:conformite] = value unless value.empty? 
          when 'Montant soumis',
               'Prix soumis'
            value = td.text.strip
            hash[:prix_soumis] = value.sub(',', '.').sub(/[^\d.]/, '').to_f unless value.empty? 
          when 'Montant du contrat',
               'Prix du contrat'
            value = td.text.strip
            hash[:prix_du_contrat] = value.sub(',', '.').sub(/[^\d.]/, '').to_f unless value.empty? 
          when 'Montant total de la dépense incluant les options de renouvellement',
               'Montant total de la dépense prévue incluant les options de renouvellement'
            value = td.text.gsub(/[[:space:]]+/, ' ').strip
            hash[:montant_total] = value.sub(',', '.').sub(/[^\d.]/, '').to_f unless value.empty? 
          else
            raise "Unknown fournisseur column #{header}"
          end
        end
        extra[:fournisseurs] << hash
      end
      extra[:fournisseurs] = extra[:fournisseurs].to_json
    end

    # Documents
    node = parser.parser.at_css('#MainUserControl_headerDocuments')
    if node
      node = node.next_element until node.name == 'table'
      last = {}
      extra[:documents] = []
      node.css('tr:gt(1)').each do |tr|
        size = tr.css('td').size
        next if size.zero? 
        # There will be partial rows if the table lists English and French documents separately.
        partial = size == 3
        index = partial ? 0 : 2

        unless partial
          last = {
            titre: tr.at_css('td:eq(1)').text.strip,
            description: tr.at_css('td:eq(2)').text.strip,
          }
        end

        extra[:documents] << last.merge({
          langue: tr.at_css("td:eq(#{index + 1})").text.strip,
          dimension: tr.at_css("td:eq(#{index + 2})").text.strip,
          nombre: tr.at_css("td:eq(#{index + 3})").text[/\d+/].to_i,
        })
      end
      extra[:documents] = extra[:documents].to_json
    end

    # Addenda
    node = parser.parser.at_css('#MainUserControl_headerAddendas')
    if node
      node = node.next_element until node.name == 'table'
      last = {}
      extra[:addenda] = []
      node.css('tr:gt(1)').each do |tr|
        size = tr.css('td').size
        next if size.zero? 
        # There will be partial rows if the table lists English and French addenda separately.
        partial = size == 4
        index = partial ? 0 : 2

        unless partial
          last = {
            titre: tr.at_css('td:eq(1)').text.strip,
            description: tr.at_css('td:eq(2)').text.strip,
          }
        end

        extra[:addenda] << last.merge({
          langue: tr.at_css("td:eq(#{index + 1})").text.strip,
          dimension: tr.at_css("td:eq(#{index + 2})").text.strip,
          nombre: tr.at_css("td:eq(#{index + 3})").text[/\d+/].to_i,
          publication: Time.parse(tr.at_css("td:eq(#{index + 4})").text.strip),
        })
      end
      if extra[:addenda].empty? 
        extra.delete :addenda
      else
        extra[:addenda] = extra[:addenda].to_json
      end
    end
    
    # @todo Disposition de la loi ou du règlement
    # e.g. http://seao.ca/OpportunityPublication/avisconsultes.aspx?ItemId=e76198bd-f83b-4f7b-a68f-ded0592290ae&COpp=Search&SubCategoryCode=&callingPage=3

    # @todo Conditions et critères d'admissibilité
    # Can be complex, e.g. http://seao.ca/OpportunityPublication/avisconsultes.aspx?ItemId=6e536680-8303-45dd-8163-393cab0f7318&COpp=Search&SubCategoryCode=&callingPage=3

    ScraperWiki.save_sqlite([:id], record.merge(extra).merge(parser.attributes).merge({
      updated_at: Time.now,
    }))
    ScraperWiki.save_var('offset', offset + i)
  end
end
