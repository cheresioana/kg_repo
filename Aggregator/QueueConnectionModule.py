from datetime import datetime

import pika
import json
from LocalState import LocalState
from format_conversion.MainConvertor import MainConvertor
from parsers import BaseParser2
from parsers.MasterParser import MasterParser
import traceback

class QueueConnectionModule:
    def __init__(self, local_state: LocalState, parser: MasterParser, main_convertor: MainConvertor):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='crawlers')
        self.local_state = local_state
        self.parser = parser
        self.convertor = main_convertor

    def callback(self, ch, method, properties, body):
        print(f" [x] Received {body[:200]}...")
        payload = json.loads(body)
        payload['received_date'] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.local_state.append_message(json.dumps(payload, indent=4))
        try:
            parsed_object = self.parser.parse(body)
            self.local_state.save_parsed_entry(parsed_object, payload['crawler_name'] + "_data.csv")
            #self.convertor.convert_csv('data2.csv')
        except Exception as e:
            payload = json.loads(body)
            print(f"Error occurred for: {payload['statement']}")
            print(e)
            traceback.print_exc()


    def listen(self):
        self.channel.basic_consume(queue='crawlers',
                              auto_ack=True,
                              on_message_callback=self.callback)
        self.channel.start_consuming()

