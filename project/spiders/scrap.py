import scrapy
import pandas as pd
from bs4 import BeautifulSoup
import re

df= pd.read_csv(r'project\spiders\Categories.csv')
links= df['Links'].tolist()
links= links[:100]
class ScrapSpider(scrapy.Spider):
    name = 'scrap'
    # allowed_domains =['https://www.purelifedental.com/']
    def start_requests(self):     
        for url in links:
            url = str(url)
            yield scrapy.Request(url=url, callback=self.parse_links)

    def parse_links(self, response):
        p_links={"Product_link":[]}
        
        r1= response.xpath("//a[@class='action tocart primary']/@href").extract()
        cat= response.xpath("//span[@data-ui-id='page-title-wrapper']/text()").extract_first()
        # since r1 is a list of links, we need to iterate over it and append it to the dictionary
        for i in r1:
            p_links.get("Product_link").append(str(i))
        # .............
        

        
        # for handling pagination 
        next_page= response.xpath("//a[@class='page']/@href").extract_first()    
        if next_page is not None:
            yield response.follow(url=next_page, callback=self.parse_links)
        #...........
        
        # sending the dictionary to the parse function
        for url in  p_links['Product_link']:
            yield scrapy.Request(url=url, callback=self.parse, meta={'cat': cat})
        # .............

       
        
    
    def parse(self,response):
        total_rows = response.xpath('//div[@class="product-add-form"]//tbody//tr').extract()
        if total_rows:
            # total_rows= total_rows[1:]
            for r in total_rows:
                soup = BeautifulSoup(r)
                packaging = soup.find('td', {'data-th':"Packaging"}).text.strip()
                try:
                    packaging = packaging.replace('"', "")
                    if packaging:
                        searchObj = re.search(r'([\d\./]+)/([a-zA-Z]+)', packaging)
                    if not searchObj:
                        searchObj = re.search(r'([\dx\s\./]*)\s*(ml|gm)', packaging)
                    if not searchObj:
                        searchObj = re.search(r'([\d\./oz]*)\s*([a-zA-Z]+)', packaging)
                    if not searchObj:
                        searchObj = re.search(r'([\d\./]+) ([a-zA-Z]+)', packaging)
                    if searchObj:
                        qty = searchObj.group(1)
                        pkg = searchObj.group(2)
                    else:
                        qty = ""
                        pkg = ""
                    
                    yield{
                        "Seller Platform":"Pure life dental",
                        "Seller SKU": soup.find('td', {'data-th':"Item #"}).text.strip(),
                        "Manufacture": response.xpath("//div[@class='attr__manufacturer']/text()").extract_first(),
                        "Manufacture Code": soup.find('td', {'data-th':"Mfg #"}).text.strip(),
                        "Product Title": response.xpath('//span[@itemprop="name"]/text()').extract_first() + " ({})".format(soup.find('td', {'data-th':"Description"}).text.strip()),
                        "Description": response.css('div.features__detail ::text').extract(),
                        "Packaging": pkg,
                        "Qty": qty.strip().replace('\"', ""),
                        "Categories": response.meta.get('cat'),
                        # 'Categories':response.xpath("(//ul[@class='items']//li/a)[2]/text()").extract(),
                        "Subcategories": "-1" ,# response.xpath("//li[@class='item cms_page']/strong/text()").extract(),
                        "Product Page link": response.url,
                        "Attachment URL": '-1',
                        "Image link": response.css('img.gallery-placeholder__image ::attr(src)').extract(),
                    }
                except Exception as e:
                    print(f"ERROR: at{e} at {response.url}")
                
