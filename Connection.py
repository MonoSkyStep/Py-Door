import socket



class Connection():


    def __init__(self, ip, port):
        self.ip, self.port = ip, port
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)



    def connect(self):
        print('connecting')
        try:
            self.connection.connect((self.ip, self.port))
            return True
        except ConnectionRefusedError:
            return False



    def write(self, text, encoding='utf-8'):
        if encoding == 'utf-8':
            self.connection.sendall(str.encode(text)+b'<NON>\n')
        elif encoding == 'b':
            self.connection.sendall(text+b'<NON>\n')



    def writeln(self, text, encoding='utf-8'):
        if encoding == 'utf-8':
            self.connection.sendall(str.encode(text)+b'\n')
        elif encoding == 'b':
            self.connection.sendall(text+b'\n')



    def read(self, buffersize):
        text = self.connection.recv(buffersize)
        return text.decode('utf-8').splitlines()[0]
