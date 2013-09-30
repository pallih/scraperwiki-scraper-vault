require 'scraperwiki'
require 'json'

module GASP
    # wrap save with a local method, inject timestamp
    module Datastore
        def self.save(unique_keys, data, table_name='swdata')
            data = data.merge(:updated_at => Time.now)
            ScraperWiki.save_sqlite unique_keys, data.merge({:updated_at => Time.now}), table_name
        end
    end

    module Utils
        def format_phone_for(str)
            str.split(/[()\-\. ]/).collect {|part| part.empty? ? nil : part }.compact.join('-')
        end

        def parse_linklist(url, selector)
          html = ScraperWiki.scrape(url)
          doc = Nokogiri::HTML(html)
          links = doc.css(selector).collect {|link| link.attr('href')}
        end
    end

    module Helper
        attr_accessor :api_key, :bioguide_id

        def initialize(api_key, bioguide_id)
            @api_key = api_key
            @bioguide_id = bioguide_id
        end

        #send heartbeat
        def finish()
            scrapername = JSON.parse(File.open('launch.json', 'rb').read)['scrapername']
            puts ScraperWiki.scrape("http://services.sunlightlabs.com/gasp/heartbeat/?apikey=#{api_key}&bioguide_id=#{bioguide_id}&scraper_id=#{scrapername}")
        end

        # generic methods
        def add_issue(title, content, options={})
            issue = {:title => title, :content => content, :extra => JSON.dump(options)}
            Datastore.save [:title], issue, 'issues'
        end

        def add_office(address, phone, fax='', options={})
            office = {:address => address, :phone => phone, :fax => fax, :extra => JSON.dump(options)}
            Datastore.save [:address, :phone, :fax], office, 'offices'
        end

        def add_biography(content, options={})
            biography = {:content => content, :extra => JSON.dump(options)}
            Datastore.save [:content], biography, 'biography' 
        end

        def add_event(title, date, location, options={})
            event = {:title => title, :date => date, :location => location, :extra => JSON.dump(options)}
            Datastore.save [:title, :date, :location], event, 'events'
        end

        def add_social_media(service_name, url, options={})
            sm = {:service => service_name, :url => url, :extra => JSON.dump(options)}
            Datastore.save [:service], sm, 'social_media'
        end

        # convenience methods
        def add_press_release(title, date, content, options={})
            add_update 'press_release', title, date, content, options
        end

        def add_news_update(title, date, content, options={})
            add_update 'news_update', title, date, content, options
        end

        def add_blog_post(title, date, content, options={})
            add_update 'blog_post', title, date, content, options
        end

        def add_other_post(title, date, content, options={})
            add_update 'other', title, date, content, options
        end

        def add_facebook(url, options={})
            add_social_media 'facebook', url, options
        end

        def add_flickr(url, options={})
            add_social_media 'flickr', url, options
        end

        def add_twitter(url, options={})
            add_social_media 'twitter', url, options
        end

        def add_youtube(url, options={})
            add_social_media 'youtube', url, options
        end

        protected

        def add_update(type, title, date, content, options={})
            update = {:update_type => type, :title => title, :date => date, :content => content, :extra => JSON.dump(options)}
            Datastore.save [:title, :date, :content, :update_type], update, 'updates'
        end

    end
endrequire 'scraperwiki'
require 'json'

module GASP
    # wrap save with a local method, inject timestamp
    module Datastore
        def self.save(unique_keys, data, table_name='swdata')
            data = data.merge(:updated_at => Time.now)
            ScraperWiki.save_sqlite unique_keys, data.merge({:updated_at => Time.now}), table_name
        end
    end

    module Utils
        def format_phone_for(str)
            str.split(/[()\-\. ]/).collect {|part| part.empty? ? nil : part }.compact.join('-')
        end

        def parse_linklist(url, selector)
          html = ScraperWiki.scrape(url)
          doc = Nokogiri::HTML(html)
          links = doc.css(selector).collect {|link| link.attr('href')}
        end
    end

    module Helper
        attr_accessor :api_key, :bioguide_id

        def initialize(api_key, bioguide_id)
            @api_key = api_key
            @bioguide_id = bioguide_id
        end

        #send heartbeat
        def finish()
            scrapername = JSON.parse(File.open('launch.json', 'rb').read)['scrapername']
            puts ScraperWiki.scrape("http://services.sunlightlabs.com/gasp/heartbeat/?apikey=#{api_key}&bioguide_id=#{bioguide_id}&scraper_id=#{scrapername}")
        end

        # generic methods
        def add_issue(title, content, options={})
            issue = {:title => title, :content => content, :extra => JSON.dump(options)}
            Datastore.save [:title], issue, 'issues'
        end

        def add_office(address, phone, fax='', options={})
            office = {:address => address, :phone => phone, :fax => fax, :extra => JSON.dump(options)}
            Datastore.save [:address, :phone, :fax], office, 'offices'
        end

        def add_biography(content, options={})
            biography = {:content => content, :extra => JSON.dump(options)}
            Datastore.save [:content], biography, 'biography' 
        end

        def add_event(title, date, location, options={})
            event = {:title => title, :date => date, :location => location, :extra => JSON.dump(options)}
            Datastore.save [:title, :date, :location], event, 'events'
        end

        def add_social_media(service_name, url, options={})
            sm = {:service => service_name, :url => url, :extra => JSON.dump(options)}
            Datastore.save [:service], sm, 'social_media'
        end

        # convenience methods
        def add_press_release(title, date, content, options={})
            add_update 'press_release', title, date, content, options
        end

        def add_news_update(title, date, content, options={})
            add_update 'news_update', title, date, content, options
        end

        def add_blog_post(title, date, content, options={})
            add_update 'blog_post', title, date, content, options
        end

        def add_other_post(title, date, content, options={})
            add_update 'other', title, date, content, options
        end

        def add_facebook(url, options={})
            add_social_media 'facebook', url, options
        end

        def add_flickr(url, options={})
            add_social_media 'flickr', url, options
        end

        def add_twitter(url, options={})
            add_social_media 'twitter', url, options
        end

        def add_youtube(url, options={})
            add_social_media 'youtube', url, options
        end

        protected

        def add_update(type, title, date, content, options={})
            update = {:update_type => type, :title => title, :date => date, :content => content, :extra => JSON.dump(options)}
            Datastore.save [:title, :date, :content, :update_type], update, 'updates'
        end

    end
end