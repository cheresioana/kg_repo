from QueueConnectionModule import QueueConnectionModule
import time


if __name__ == '__main__':
    queue = QueueConnectionModule()
    queue.listen()
    while 1:
        time.sleep(3)
    exit(0)
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
