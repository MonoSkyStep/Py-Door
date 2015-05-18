from ctypes import windll
import Connection
import os



conn = None

def run(connection):
    global running
    global conn
    connection = conn

    connection.writeln('power module started.')
    running = True
    while running:
        connection.write('>>')
        text = connection.read(1024)
        if text == 'quit' or text == 'exit':
            running = False
        else:
            parse(text)




running = False
def parse(text):

    cmd, *args = text.split(' ')

    if cmd == 'shutdown':

        if args is None:
            shutdown()
            return

        t= None
        m = None
        hast = False
        hasm = False


        for pos, arg in enumerate(args):
            if '-t' in arg:
                hast = True
                t = int(args[pos+1])
            if '-m' in arg:
                hasm = True
                m = args[pos+1]

        shutdown(time=(hast if t else None),message=(hasm if m else None))
        return

    elif cmd == 'logoff':
        logoff()
        return

    elif cmd == 'lock':
        lock()
        return



def shutdown(time=None, message=None):

    conn.writeln('shutting computer down')
    cmd = 'shutdown -s -f '

    if time is not None:
        cmd += '-t ' + time + ' '
    if message is not None:
        cmd += '-c ' + message + ' '

    os.system(cmd)


def logoff():

    conn.writeln('logging off computer')
    os.system('shutdown -l -f')


def lock():

    conn.writeln('locking computer')
    x = windll.user32
    x.LockWorkStation()