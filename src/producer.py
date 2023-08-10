import pika
import requests
from bs4 import BeautifulSoup as soup
from src.manticore import insert


def send_to_queue(message: str):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    
    channel = connection.channel()

    channel.queue_declare(
        queue='cocos', 
        durable=True
        )
    
    channel.basic_publish(
        exchange='',
        routing_key='cocos',
        body=message,
        properties=pika.BasicProperties(
            delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
        ))
    connection.close()

def get_news(url: str, page_num: int, counter: int = 1):
    resp = requests.get(f"{url}{page_num}")
    
    match resp.status_code:
        case 200:
            bs = soup(resp.content, 'html.parser')
            news_block = bs.find('div', class_='cnt posts__cnt')
            news = news_block.find_all('div', class_='post-mini-b')
            for i in news:
                link = f"https://gotennis.ru{i.find('a').get('href')}"
                send_to_queue(link)
        case 404:
            insert(
                document={
                    "url": url,
                    "code": resp.status_code
                },
                index="errors"
            )
        case _:
            match counter:
                case 1:
                    get_news(
                        url=url,
                        page_num=page_num,
                        counter=2
                    )
                case 2:
                    insert(
                        document={
                            "url": url,
                            "code": resp.status_code
                        },
                        index="errors"
                    )


def producer():
    pages_range = 4
    url = "https://gotennis.ru/read?page="
    for page_num in range(2, pages_range):
        get_news(
            url=url,
            page_num=page_num
            )

    