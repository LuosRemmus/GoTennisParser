from producer import producer
from consumer import consumer
import threading


def main():
    thread_1 = threading.Thread(target=producer).start()
    thread_2 = threading.Thread(target=consumer).start()


if __name__ == '__main__':
    main()