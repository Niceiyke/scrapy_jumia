import scrapy
from ..items import JumiaItem
from scrapy.loader import ItemLoader


class jumiaLaptopSpyder(scrapy.Spider):
    name ='jumialaptop'
    start_urls =['https://www.jumia.com.ng/mlp-working-from-anywhere/laptops/?rating=4-5&seller_score=4-5#catalog-listing',]


    custom_settings= {
          'FEEDS':{
        'jumialaptop.json':{
            'format':'json','overwrite': True
        }
    },

            "ITEM_PIPELINES" :{
                "jumia.pipelines.Remove_Items_withNoDiscount_Pipeline": 100,
                "jumia.pipelines.Remove_Items_NotinStock_Pipeline": 200,
                "jumia.pipelines.SavingToDbpostgres": 300,

                }

    }
   

    def parse(self, response):
        products =response.css('article.c-prd')

        for product in products:
              
            l= ItemLoader(item=JumiaItem(),selector=product) 
            l.add_css('url','a.core ::attr(href)')           
            l.add_css('name','h3.name ::text'),
            l.add_css('discount_price','div.prc ::text'),
            l.add_css('original_price','div.old ::text'),
            l.add_css('discount_percent','div.bdg._dsct._sm ::text'),
            l.add_css('stock','button.add.btn._md ::text'),
            l.add_value('category','laptops'),
            l.add_value('store','Jumia'),
            l.add_css('image','img.img ::attr(data-src)'),

            yield l.load_item()
            
            
        next_page= response.css('a.pg::attr(href)').getall()[-2]
        print(next_page)

        if next_page is not None:
                yield response.follow(f'https://www.jumia.com.ng{next_page}',callback=self.parse)


    def product_detail(self,response):
            
            
            l= ItemLoader(item=JumiaItem(),selector=response)            
            l.add_css('name','h1.-pbxs'),
            l.add_css('discount_price','span.-b.-ltr.-tal.-fs24'),
            l.add_css('original_price','span.-tal.-gy5.-lthr.-fs16'),
            l.add_css('dicount_percent','span.bdg._dsct._dyn.-mls'),
            l.add_css('stock','button.add ::text'),
            l.add_css('category','a.cbs ::text'),
            l.add_css('image','img.-fw.-fh ::attr(data-src)'),

            yield l.load_item()
            
        