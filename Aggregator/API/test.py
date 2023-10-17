from data_formats_pb2 import Statement
if __name__=='__main__':
    statement = Statement()
    statement.type = "Here is whatever Ioana Russia Mihai 1000 euros in Romania or Europe"
    string_ser = statement.SerializeToString()
    with open("sa_imi_testez2", 'wb') as file:
        file.write(string_ser)
