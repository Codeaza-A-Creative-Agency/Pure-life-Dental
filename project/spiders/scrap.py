import scrapy
import pandas as pd
df= pd.read_csv(r'C:\Users\admin\Categories.csv')
links= df['Links'].tolist()
links= links[:30]
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
            yield scrapy.Request(url=url, callback=self.parse)
        # .............
        
       
        
    
    def parse(self,response):
        for r in response.xpath('//div[@class="product-add-form"]'):
            yield{
                "Seller Platform":"Pure life dental",
                "Seller SKU": r.xpath('//td[@data-th="Item #"]/text()').extract_first(),
                "Manufacture": response.xpath("//div[@class='attr__manufacturer']/text()").extract(),
                "Manufacture Code": r.xpath('//td[@data-th="Mfg #"]/text()').extract_first(),
                "Product Title": response.xpath('//span[@itemprop="name"]/text()').extract(),
                "Description": response.css('div.features__detail ::text').extract(),
                "Packaging": r.xpath('//td[@data-th="Packaging"]/text()').extract_first(),
                "Qty":r.xpath('//td[@data-th="Packaging"]/text()').extract_first(),
                'Categories':response.xpath("(//ul[@class='items']//li/a)[2]/text()").extract(),
                "Subcategories": "-1" ,# response.xpath("//li[@class='item cms_page']/strong/text()").extract(),
                "Product Page link": response.url,
                "Attachment URL": '-1',
                "Image link": response.css('img.gallery-placeholder__image ::attr(src)').extract(),
                "Attributes":'-1'
            }
            




