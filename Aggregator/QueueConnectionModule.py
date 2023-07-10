from datetime import datetime

import pika
import json
from LocalState import LocalState
from parsers import BaseParser2
from parsers.MasterParser import MasterParser


class QueueConnectionModule:
    def __init__(self, local_state: LocalState, parser: MasterParser):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='crawlers')
        self.local_state = local_state
        self.parser = parser

    def callback(self, ch, method, properties, body):
        print(" [x] Received %r..." % body[:200])
        payload = json.loads(body)
        payload['received_date'] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.local_state.append_message(json.dumps(payload, indent=4))
        parsed_object = self.parser.parse(payload)
        self.local_state.save_parsed_entry(parsed_object)

    def listen(self):
        self.channel.basic_consume(queue='crawlers',
                              auto_ack=True,
                              on_message_callback=self.callback)
        self.channel.start_consuming()

