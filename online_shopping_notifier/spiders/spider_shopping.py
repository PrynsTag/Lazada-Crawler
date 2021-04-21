import os
import smtplib
import ssl

import scrapy
from scrapy.crawler import CrawlerProcess


def send_email():
    port = 465
    smtp_server = "smtp.gmail.com"
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(os.environ["SENDER_EMAIL"], os.environ["SENDER_EMAIL_PASS"])
        server.sendmail(os.environ["SENDER_EMAIL"], os.environ["RECEIVER_EMAIL"], os.environ["MESSAGE"])


def check_price(price):
    if price < 2100:
        send_email()


class ShoppingNotifier(scrapy.Spider):
    name = "shop"

    def start_requests(self):
        yield scrapy.Request(url=os.environ["URL"], callback=self.parse)

    def parse(self, response, **kwargs):
        price = response.css('#module_product_price_1 > div > div > span::text').extract_first()
        price = price.replace("₱", "").replace(",", "").split(".")[0]
        check_price(int(price))
        print(price)
        yield price


if __name__ == "__main__":
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 '
                      'Safari/537.36 OPR/75.0.3969.218 '
    })
    process.crawl(ShoppingNotifier)
    process.start()
