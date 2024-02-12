from scrapy.exceptions import DropItem 

import aiofiles
import json
import scrapy


class ProductSpider(scrapy.Spider):
    name = "products"
    start_urls = ["https://www.ebay.com/sch/garlandcomputer/m.html"]

    def start_requests(self):
        url = "https://www.ebay.com/sch/garlandcomputer/m.html"
        condition = getattr(self, "condition", None)
        condition_params = { 'USED': 4, 'NEW': 3 }
        
        if condition is not None:
            condition = condition.upper()
            url = f"https://www.ebay.com/sch/i.html?_ssn=garlandcomputer&LH_ItemCondition={condition_params[condition]}"

        yield scrapy.Request(url, self.parse)

    def parse(self, response):
        return response.follow_all(css='.s-item__info > a', callback=self.parse_product)

    async def parse_product(self, response):
        product_id = response.xpath('//*[text() = \'eBay item number:\']/following-sibling::span/text()').get()
        product_data = {
            "title": response.css('h1.x-item-title__mainTitle span::text').get(),
            "condition": response.css('div.x-item-condition-text span::text').get(),
            "price": response.css('div.x-price-primary span::text').re_first(r"(?<=\$).*\.[0-9][0-9]"),
            "product_url": response.url
        }

        try:
            if product_data['title'] is None:
                raise DropItem("Missing data in %s" % product_data)
            
            if product_data['condition'] is None:
                raise DropItem("Missing data in %s" % product_data)
                 
            if product_data['price'] is None:
                raise DropItem("Missing data in %s" % product_data)

        except KeyError:
            raise DropItem("Missing data in %s" % product_data)

        file_name = f"{product_id}.json"
        await self.write_file(file_name, product_data)
        self.log(f"Saved file {file_name}")

    async def write_file(self, file_name, file_content):
        try:
            async with aiofiles.open(file_name, mode='w') as handle:
                await handle.write(json.dumps(file_content))
        except Exception as e:
            print(f"Unexpected error ocurred: {e}")

