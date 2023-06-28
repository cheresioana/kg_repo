import pika
class QueueConnectionModule:
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='hello')

    def send_message(self, message):
        self.channel.basic_publish(exchange='',
                              routing_key='hello',
                              body='Hello World!')
        print(" [x] Sent 'Hello World!'")

    def callback(self, ch, method, properties, body):
        print(" [x] Received %r" % body)

    def listen(self):
        self.channel.basic_consume(queue='hello',
                              auto_ack=True,
                              on_message_callback=self.callback)
        self.channel.start_consuming()

