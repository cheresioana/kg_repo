import pika
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

