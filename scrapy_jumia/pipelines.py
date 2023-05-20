# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
import sqlite3
import psycopg2


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

class SavingToDb:
    def __init__(self):
        self.con = sqlite3.connect("scrapy.db")

        self.cur = self.con.cursor()
        self.create_table()

    def create_table(self):
        self.cur.execute(
            """CREATE TABLE IF NOT EXISTS products(
        name TEXT PRIMARY KEY,stock text,category text,store text,image text,url text,discount REAL,original_price REAL,discount_price REAL)"""
        )

    def process_item(self, item, spider):
        self.cur.execute(
            """ INSERT INTO products VALUES (?,?,?,?,?,?,?,?,?)""",
            (
                item["name"],
                item["stock"],
                item["category"],
                item["store"],
                item["image"],
                item["url"],
                item["discount_percent"],
                item["original_price"],
                item["discount_price"],
            ),
        )

        self.con.commit()

        return item


class SavingToDbpostgres:
    def __init__(self):
        self.con = psycopg2.connect(
            database="postgresec2",
            user="postgresec2",
            password="postgresec2",
            host="3.23.130.169",
            port="5432",
        )

        self.cur = self.con.cursor()

        print("connected")


    def process_item(self,item,spider):
        try:
            self.cur.execute(""" insert into products_product (name,stock,category,image,product_url,discount_percent,original_price,discount_price) values (%s,%s,%s,%s,%s,%s,%s,%s) on conflict(name) do nothing""",
                            (item['name'],item['stock'],item['category'],item['image'],item['url'],item['discount_percent'],item['original_price'],item['discount_price'],))
            
            self.con.commit()
            print('ADDED')

        except Exception as e:
            print('db_err',e)

        return item
  
