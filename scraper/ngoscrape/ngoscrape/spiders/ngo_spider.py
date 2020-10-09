import scrapy

class NGOSpider(scrapy.Spider):
    name = "ngos"

    start_urls =[
        'https://ngosindia.org/andaman-nicobar/',
        'https://ngosindia.org/#'

    ]
    def parse(self, response):
        for state in response.css('.npos-layout-cell ul li'):
            state_link = state.css('a::attr(href)').get()
            state_ngo_page = response.urljoin(state_link)
            yield scrapy.Request(state_ngo_page, callback=self.state_dive)

    def state_dive(self, response):
        for ngo in response.css('.lcp_catlist li'):
            info_link =  ngo.css('a::attr(href)').get()
            ##  scrape the name and link to NGO
            building_yield = {
                'state': response.url.split('/')[-2],
                'name': ngo.css('a::text').get(),
                'info_link': ngo.css('a::attr(href)').get()
            } 

            if info_link  is not None:
                info_link = response.urljoin(info_link)
                request = scrapy.Request(info_link, callback=self.dig_ngo_info)
                request.cb_kwargs['building_yield'] = building_yield
                yield request
            else:
                yield  building_yield


    def dig_ngo_info(self, response, building_yield):
        #  return the raw content
        raw_content_scraped = response.css('.npos-postcontent p::text').getall()
        building_yield['raw_content'] = raw_content_scraped
        processed_dict = self.token_ngosindia(raw_content_scraped)
        building_yield.update(processed_dict)
        yield building_yield

    def token_ngosindia(self, raw_content_scraped):
        building_yield = {}
        current_key = ""
        ## Go through each element in the raw content
        for element in raw_content_scraped:
            delimiter = ":"
            if delimiter in element:
                csv = element.split(delimiter)
                current_key = csv[0].replace('\n','').strip()

                ## count delimiter to  determine if it's a website
                if element.count(delimiter) > 1: 
                    building_yield[current_key] = delimiter.join(csv[1:]).replace('\n','').strip()
                else:
                    building_yield[current_key] = csv[1].replace('\n','').strip()
            else:
                ## extend if needed, i.e. for Add
                building_yield[current_key] += ", " +  element.replace('\n','').strip()
        return building_yield
            