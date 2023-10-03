import pika

'''
The class sends data to RabbitMQ, from where it is read by the Aggregator component
'''


class QueueConnectionModule:
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='crawlers')

    def send_message(self, message):
        self.channel.basic_publish(exchange='',
                                   routing_key='crawlers',
                                   body=message)
        print(" [crawler] Sent " + message[:200])
