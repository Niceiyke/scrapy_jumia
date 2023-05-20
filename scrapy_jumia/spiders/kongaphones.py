import scrapy
from ..items import KongaItem
from scrapy.loader import ItemLoader
from scrapy_splash import SplashRequest

lua_script = """
function main(splash, args)
    assert(splash:go(args.url))

  while not splash:select('li.bbe45_3oExY._22339_3gQb9') do
    splash:wait(0.1)
    print('waiting...')
  end
  return {html=splash:html()}
end
"""

class kongaPhoneSpyder(scrapy.Spider):
    name ='kongaphone'
    page_num=1
    
    def start_requests(self):
        url = 'https://www.konga.com/category/phones-tablets-5294?konga_fulfilment_type=CWK'
        yield SplashRequest(
            url,
            callback=self.parse,
            endpoint='execute', 
            args={'wait': 5, 'lua_source': lua_script,  url:'https://www.konga.com/category/phones-tablets-5294?konga_fulfilment_type=CWK'}
            
            )

    def parse(self, response):
        
        products =response.css('li.bbe45_3oExY._22339_3gQb9')

        for product in products:
              
            l= ItemLoader(item=KongaItem(),selector=product) 
            l.add_css('url',' div._4941f_1HCZm ::attr(href)')           
            l.add_css('name','div.af885_1iPzH ::text'),
            l.add_css('discount_price','span.d7c0f_sJAqi'),
            l.add_css('original_price','span.f6eb3_1MyTu'),
            l.add_css('dicount_percent','span._4472a_zYlL-._6c244_q2qap ::text'),
            l.add_value('category','smartphones'),
            l.add_value('store','Konga'),
            l.add_css('image','img.f5e10_VzEXF _59c59_3-MyH lazyloaded ::attr(src)'),

            yield l.load_item()
        
        self.page_num+=1

        next_page =response.css('a._08932_1bhTj._4c4d8_1SOeS')
        if next_page is not None:
            url=f'https://www.konga.com/category/phones-tablets-5294?konga_fulfilment_type=CWK&page={self.page_num}'
            yield SplashRequest(
            url,
            callback=self.parse,
            endpoint='execute', 
            args={'wait': 5, 'lua_source': lua_script, 'url':url}
            )


            
            



            
        