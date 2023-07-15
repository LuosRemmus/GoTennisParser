import pika
import requests
from bs4 import BeautifulSoup as soup
from manticore import insert, write_to_file


def consumer():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(
        queue='kos_queue', 
        durable=True
        )
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(
        queue='cocos', 
        on_message_callback=get_data, 
        auto_ack=False
        )
    channel.start_consuming()

def get_data(
        channel, 
        method, 
        properties, 
        url, 
        counter: int = 1):
    link = url.decode('utf-8')
    resp = requests.get(link)
    match resp.status_code:
        case 200:
            bs = soup(resp.content, 'html.parser')
            try:
                title = bs.find('h1', class_='post-card__title').text.strip()
            except AttributeError:
                title = 'No title'
            try:
                art_text = bs.find('div', class_='post-card__text').find_all('p')
                art_text = " ".join([p.text.strip() for p in art_text])
            except AttributeError:
                art_text = "No text"

            print(title, art_text, "\n", sep='\n')
            data = {
                    "title": title,
                    "art_text": art_text
                }
            a = insert(data)
            print(a)
            write_to_file(data)
            channel.basic_ack(delivery_tag=method.delivery_tag)
        case 404:
            insert(
                document={
                    "url": link,
                    "code": resp.status_code
                },
                index="errors"
            )
        case _:
            match counter:
                case 1:
                    get_data(
                        channel=channel,
                        method=method,
                        properties=properties,
                        url=url,
                        counter=2
                        )
                case 2:
                    insert(
                        document={
                            "url": link,
                            "code": resp.status_code
                        },
                        index="errors"
                    )
