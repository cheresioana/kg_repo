import time

import pika

'''
The class sends data to RabbitMQ, from where it is read by the Aggregator component
'''


class QueueConnectionModule:
    def __init__(self):
        self.connection_params = pika.ConnectionParameters('localhost')
        self.queue_name = 'crawlers'
        self.connect()

    def connect(self):
        """Metoda pentru a stabili conexiunea și canalul."""
        print("Connect Rabbit MQ")
        self.connection = pika.BlockingConnection(self.connection_params)
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue_name)

    def send_message(self, message):
        try:
            self.channel.basic_publish(exchange='',
                                       routing_key='crawlers',
                                       body=message)
            print(" [crawler] Sent " + message[:200])
        except (pika.exceptions.StreamLostError, pika.exceptions.ChannelClosedByBroker) as e:
            print("Eroare la trimiterea mesajului, încerc reconectarea: ", e)
            print("Reconectare la RabbitMQ...")
            self.connect()
            self.channel.basic_publish(exchange='',
                                       routing_key='crawlers',
                                       body=message)
            print(" [crawler] Sent after reconnect " + message[:200])
