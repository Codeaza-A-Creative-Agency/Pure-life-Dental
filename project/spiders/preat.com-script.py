import json
import requests
import pandas as pd
from bs4 import BeautifulSoup
df= pd.read_csv('Preat.com-product-links.csv')  
links = df['Links'].tolist()
class scrap:
    Title= []
    Seller_Platform= []
    Seller_SKU= []
    Manufacture_Name=[]
    Manufacture_Code=[]
    Packaging=[]
    Qty=[]
    Att_url=[]
    Product_Page_URL=[]
    Categories= []
    Sub_Categories=[]
    Description=[]
    Image_URL=[]
    Attributes= []
    baseurl= 'https://www.preat.com'
    def __init__(self):
        for link in links:
            self.parse(link)
        self.save_data()
        
    def parse(self,url):
        images=[]
        r= requests.get(url)
        print(r.status_code)
        bs = BeautifulSoup(r.content,'lxml')
        tag= bs.find('script', id="__NEXT_DATA__")
        resp= json.loads(tag.text)
        name = resp['props']['pageProps']['product']['name']
        price = resp['props']['pageProps']['product']['price_range']
        sku = resp['props']['pageProps']['product']['sku']
        image= resp['props']['pageProps']['product']['media_gallery']
        s_description = resp['props']['pageProps']['product']['short_description']
        l_description =resp['props']['pageProps']['product']['description']
        cat = resp['props']['pageProps']['product']['categories']
        for i in image:
            images.append(i['url'])
        self.Title.append(name)
        data=resp['props']['pageProps']['product']
        self.Seller_Platform.append('Preat')
        self.Manufacture_Name.append('-1')
        self.Manufacture_Code.append('-1')
        self.Packaging.append('-1')
        self.Qty.append('-1')
        self.Sub_Categories.append('Misc')
        self.Attributes.append('-1')
        self.Product_Page_URL.append(r.url)
        self.Seller_SKU.append(sku)
        self.Categories.append(cat[0]['name'])
        self.Image_URL.append(images)
        bs= BeautifulSoup(l_description['html'],'lxml')
        descrip = bs.find('html')
        try:
            descrip= descrip.text
        except:
            descrip=''
        final_descript= descrip+s_description['html']
        self.Description.append(final_descript)
        bs =BeautifulSoup(r.content, 'lxml')
        try:
            attachment=bs.find('div',class_='product__description').find('a').get('href')
        except:
            attachment=''
        self.Att_url.append(self.baseurl+attachment)
    def save_data(self):
        data_dict={"Seller Platform":self.Seller_Platform, "Seller SKU":self.Seller_SKU, "Manufacture":self.Seller_Platform,"Manufacture Code":self.Seller_SKU,
          "Product Title":self.Title,"Description":self.Description, "Packaging":self.Packaging,"Categories":self.Categories, "Subcategories":self.Sub_Categories,
           "Product Page URL":self.Product_Page_URL,"Attachment URL":self.Att_url[0],"Image URL":self.Image_URL, "Attributes":self.Attributes }
        df= pd.DataFrame.from_dict(data_dict)
        df.to_csv("Preat-Sample-data.csv", index=False)
        
        


if __name__ =='__main__':
    scrap=scrap()

