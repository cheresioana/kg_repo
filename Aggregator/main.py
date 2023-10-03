from LocalState import LocalState
from QueueConnectionModule import QueueConnectionModule
import time

from format_conversion.MainConvertor import MainConvertor
from parsers.MasterParser import MasterParser

def start_listening():
    local_state = LocalState()
    master_parser = MasterParser()
    main_convertor = MainConvertor()
    queue = QueueConnectionModule(local_state, master_parser, main_convertor)
    queue.listen()
    while 1:
        time.sleep(3)
    exit(0)

if __name__ == '__main__':
    start_listening()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
