from src.producer import producer
from src.consumer import consumer
import threading


def main():
    threading.Thread(target=producer).start()
    threading.Thread(target=consumer).start()


if __name__ == '__main__':
    main()