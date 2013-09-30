require 'nokogiri'

@voluntary_sectors =  ['/Charity-and-Voluntary-Jobs/sector-28']

@private_sectors = ['/Accountancy-Finance-Jobs/sector-1', '/Banking-Financial-services-Insurance-Jobs/sector-2', '/Beauty-Hair-Care-Leisure-Jobs/sector-3', '/Childcare-Social-Work-Jobs/sector-4', '/Construction-Architecture-Jobs/sector-5', '/Customer-Service-Call-Centre-Jobs/sector-6', '/Education-Training-Jobs/sector-7', '/Engineering-Jobs/sector-8', '/Environmental-Health-Safety-Jobs/sector-9', '/General-Management-Jobs/sector-10', '/Hotel-Catering-Jobs/sector-11', '/Human-Resource-Jobs/sector-12', '/IT-Jobs/sector-13', '/Legal-Jobs/sector-14']

@public_sectors = ['/Public-Sector-Jobs/sector-19']

@urlroot = "http://www.nijobfinder.co.uk"


#def innerText(element)
#    # Note: I have just used Nokogiri's inner_text method
#    # Perhaps something similar exists for lxml, I simply
#    # haven't looked to see if there is
#end


def sanatize_salary(salary)

    salary = salary.gsub(/[^\d-]/) {''}
    salary_range = salary.split('-')

    begin
        if salary_range.size == 2
            salary = (salary_range[0].to_i + salary_range[1].to_i)/2
        else
            salary = salary_range[0]
        end
    rescue Exception => e
        return nil
    end

    begin
        salary = salary.to_i
    rescue Exception => e
        salary = nil
    end

    salary
end


def summed_salary_with_count(root)
    num_parsed = 0
    summed_salary = 0

    # place your cssselection case here and extract the values
    root.search('div.result-item span.salary').each do |tr|
        #puts tr

        salary = sanatize_salary(tr.inner_text.strip)
        if salary
            num_parsed += 1
            summed_salary += salary
        end
    end

    [summed_salary, num_parsed]
end


def find_next_button(root)
    # place your cssselection case here and extract the values
    buttons = root.search('li.next a')

    if buttons.size > 0
        return buttons[0]
    else
        return nil
    end
end


def do_it_for_category(sectors)
    category_num_parsed = 0
    category_summed_salary = 0

    sectors.each do |sector|
        sector_summed_salary, sector_num_parsed = do_it_for_sector(sector)
        category_num_parsed += sector_num_parsed
        category_summed_salary += sector_summed_salary
    end

    [category_summed_salary, category_num_parsed]
end


def do_it_for_sector(sector)
    sector_num_parsed = 0
    sector_summed_salary = 0

    url = @urlroot + sector


    # Sorry, I'm tired - if the url is longer than 0 chars then continue
    while url.size > 0
        html = ScraperWiki.scrape(url)
        root = Nokogiri::HTML(html)

        summed_salary, num_parsed = summed_salary_with_count(root)

        sector_num_parsed += num_parsed
        sector_summed_salary += summed_salary

        next_button = find_next_button(root)
        #puts next_button

        unless next_button
            url = '' # Wow! How hacky!
        else
            url = @urlroot + next_button['href']
        end
    end

    [sector_summed_salary, sector_num_parsed]
end


def main

    summed_private_salary, num_private_parsed = do_it_for_category(@private_sectors)
    summed_public_salary, num_public_parsed = do_it_for_category(@public_sectors)
    summed_voluntary_salary, num_voluntary_parsed = do_it_for_category(@voluntary_sectors)
    

    avg_private_salary = summed_private_salary / num_private_parsed
    avg_public_salary = summed_public_salary / num_public_parsed
    avg_voluntary_salary = summed_voluntary_salary / num_voluntary_parsed

    # Here is a simple Ruby hash which will go into our datastore
    data = {
       'num_private_parsed' => num_private_parsed,
       'num_public_parsed' => num_public_parsed,
       'num_voluntary_parsed' => num_voluntary_parsed,

       'avg_private_salary' => avg_private_salary,
       'avg_public_salary' => avg_public_salary,
       'avg_voluntary_salary' => avg_voluntary_salary
    }

    # We save the data using the datastore API - it can then be used by a view
    # (in this case http://scraperwiki.com/views/example_shops_view )
    # If a hash key is present in unique_keys it means that the value for key will be overwritten
    # every time this scraper is run - otherwise the key will occur twice.
    # In the case I want a overwrite the values for all keys on every scraper run.
    ScraperWiki.save(data.keys, data)
end


mainrequire 'nokogiri'

@voluntary_sectors =  ['/Charity-and-Voluntary-Jobs/sector-28']

@private_sectors = ['/Accountancy-Finance-Jobs/sector-1', '/Banking-Financial-services-Insurance-Jobs/sector-2', '/Beauty-Hair-Care-Leisure-Jobs/sector-3', '/Childcare-Social-Work-Jobs/sector-4', '/Construction-Architecture-Jobs/sector-5', '/Customer-Service-Call-Centre-Jobs/sector-6', '/Education-Training-Jobs/sector-7', '/Engineering-Jobs/sector-8', '/Environmental-Health-Safety-Jobs/sector-9', '/General-Management-Jobs/sector-10', '/Hotel-Catering-Jobs/sector-11', '/Human-Resource-Jobs/sector-12', '/IT-Jobs/sector-13', '/Legal-Jobs/sector-14']

@public_sectors = ['/Public-Sector-Jobs/sector-19']

@urlroot = "http://www.nijobfinder.co.uk"


#def innerText(element)
#    # Note: I have just used Nokogiri's inner_text method
#    # Perhaps something similar exists for lxml, I simply
#    # haven't looked to see if there is
#end


def sanatize_salary(salary)

    salary = salary.gsub(/[^\d-]/) {''}
    salary_range = salary.split('-')

    begin
        if salary_range.size == 2
            salary = (salary_range[0].to_i + salary_range[1].to_i)/2
        else
            salary = salary_range[0]
        end
    rescue Exception => e
        return nil
    end

    begin
        salary = salary.to_i
    rescue Exception => e
        salary = nil
    end

    salary
end


def summed_salary_with_count(root)
    num_parsed = 0
    summed_salary = 0

    # place your cssselection case here and extract the values
    root.search('div.result-item span.salary').each do |tr|
        #puts tr

        salary = sanatize_salary(tr.inner_text.strip)
        if salary
            num_parsed += 1
            summed_salary += salary
        end
    end

    [summed_salary, num_parsed]
end


def find_next_button(root)
    # place your cssselection case here and extract the values
    buttons = root.search('li.next a')

    if buttons.size > 0
        return buttons[0]
    else
        return nil
    end
end


def do_it_for_category(sectors)
    category_num_parsed = 0
    category_summed_salary = 0

    sectors.each do |sector|
        sector_summed_salary, sector_num_parsed = do_it_for_sector(sector)
        category_num_parsed += sector_num_parsed
        category_summed_salary += sector_summed_salary
    end

    [category_summed_salary, category_num_parsed]
end


def do_it_for_sector(sector)
    sector_num_parsed = 0
    sector_summed_salary = 0

    url = @urlroot + sector


    # Sorry, I'm tired - if the url is longer than 0 chars then continue
    while url.size > 0
        html = ScraperWiki.scrape(url)
        root = Nokogiri::HTML(html)

        summed_salary, num_parsed = summed_salary_with_count(root)

        sector_num_parsed += num_parsed
        sector_summed_salary += summed_salary

        next_button = find_next_button(root)
        #puts next_button

        unless next_button
            url = '' # Wow! How hacky!
        else
            url = @urlroot + next_button['href']
        end
    end

    [sector_summed_salary, sector_num_parsed]
end


def main

    summed_private_salary, num_private_parsed = do_it_for_category(@private_sectors)
    summed_public_salary, num_public_parsed = do_it_for_category(@public_sectors)
    summed_voluntary_salary, num_voluntary_parsed = do_it_for_category(@voluntary_sectors)
    

    avg_private_salary = summed_private_salary / num_private_parsed
    avg_public_salary = summed_public_salary / num_public_parsed
    avg_voluntary_salary = summed_voluntary_salary / num_voluntary_parsed

    # Here is a simple Ruby hash which will go into our datastore
    data = {
       'num_private_parsed' => num_private_parsed,
       'num_public_parsed' => num_public_parsed,
       'num_voluntary_parsed' => num_voluntary_parsed,

       'avg_private_salary' => avg_private_salary,
       'avg_public_salary' => avg_public_salary,
       'avg_voluntary_salary' => avg_voluntary_salary
    }

    # We save the data using the datastore API - it can then be used by a view
    # (in this case http://scraperwiki.com/views/example_shops_view )
    # If a hash key is present in unique_keys it means that the value for key will be overwritten
    # every time this scraper is run - otherwise the key will occur twice.
    # In the case I want a overwrite the values for all keys on every scraper run.
    ScraperWiki.save(data.keys, data)
end


main