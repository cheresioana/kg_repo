from LocalState import LocalState
from QueueConnectionModule import QueueConnectionModule
import time

from parsers.MasterParser import MasterParser
from parsers.MindBugsParser import MindBugsParser

def start_listening():
    local_state = LocalState()
    master_parser = MasterParser()
    queue = QueueConnectionModule(local_state, master_parser)
    queue.listen()
    while 1:
        time.sleep(3)
    exit(0)

if __name__ == '__main__':
    start_listening()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
