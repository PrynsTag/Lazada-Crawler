import smtplib
import ssl

import scrapy
from scrapy.crawler import CrawlerProcess

from info import *


def send_email():
    port = 465
    smtp_server = "smtp.gmail.com"
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(SENDER_EMAIL, SENDER_EMAIL_PASS)
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, MESSAGE)


def check_price(price):
    if price < 2100:
        send_email()


class ShoppingNotifier(scrapy.Spider):
    name = "shop"
    start_urls = [URL]

    def parse(self, response, **kwargs):
        price = response.css('#module_product_price_1 > div > div > span::text').extract_first()
        price = price.replace("₱", "").replace(",", "").split(".")[0]
        check_price(int(price))
        print(price)
        yield price


if __name__ == "__main__":
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })
    process.crawl(ShoppingNotifier)
    process.start()
