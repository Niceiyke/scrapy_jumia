# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
import psycopg2
import os
from dotenv import load_dotenv
load_dotenv()


class JumiaPipeline:
    def process_item(self, item, spider):
        print("pipeline" + item["name"])
        return item


class Remove_Items_NotinStock_Pipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        if adapter["stock"] == "Add To Cart":
            return item

        else:
            raise DropItem(f" {item!r} sold out")


class Remove_Items_withNoDiscount_Pipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        if adapter["original_price"] is not None:
            return item

        else:
            raise DropItem(f"No Discount found for {item!r}")
        
class Remove_Duplicate_item_Pipeline:
    def __init__(self):
        self.names_seen =set()

    def process_item(self,item,spider):
        adapter = ItemAdapter(item)

        if adapter['name'] in self.names_seen:

            raise DropItem(f'Duplicate item {item!r} found')
        
        else:
            self.names_seen.add(adapter['name'])
            return item



class SavingToDbpostgres:
    def __init__(self):
        self.con = psycopg2.connect(
            database=os.environ.get('database'),
            user=os.environ.get('user'),
            password=os.environ.get('password'),
            host=os.environ.get('host'),
            port=os.environ.get('port'),
        )

        self.cur = self.con.cursor()

        print("connected")


    def process_item(self,item,spider):
        try:
            self.cur.execute(""" insert into products_product (name,stock,store,category,image,product_url,discount_percent,original_price,discount_price) values (%s,%s,%s,%s,%s,%s,%s,%s,%s) on conflict(name) do nothing""",
                            (item['name'],item['stock'],item['store'],item['category'],item['image'],item['url'],item['discount_percent'],item['original_price'],item['discount_price'],))
            #print(item)
            self.con.commit()

        except Exception as e:
            print('db_err',e)
            
 
        return item
  
