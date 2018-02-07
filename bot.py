import socket

HOST = 'irc.twitch.tv'
PORT = 6667
NAME = 'squat_bot'
PASS = ''
CHANNEL = 'thebasementintern'

CONNECT_MESSAGE = 'Come on ladies move those muscles!'

CHEERS = [ 'cheer', 'Kappa', 'DansGame', 'EleGiggle', 'TriHard', 'Kreygasm', '4Head', 'SwiftRage', 'NotLikeThis', 'FailFish', 'VoHiYo', 'PJSalt', 'MrDestructoid', 'bday', 'RIPCheer' ]


def write_to_system(message):
    s.send(bytes(message + '\r\n', 'UTF-8'))


def write_to_chat(message):
    s.send(bytes('PRIVMSG #' + CHANNEL + ' :' + message + '\r\n', 'UTF-8'))


def stop():
    write_to_chat("I've gotten a new PR, see y'all later!")
    write_to_system('PART #' + CHANNEL)
    write_to_system('QUIT')


def is_cheer(message):
    message = str(message)

    for cheer in CHEERS:
        if cheer in message:
            if message.split(cheer)[1].split(' ')[0].isdigit():
                return True

    return False


def get_cheer_contents(message):
    return 0, ''


s = socket.socket()
s.connect((HOST, PORT))
write_to_system('PASS ' + PASS)
write_to_system('NICK ' + NAME)
write_to_system('USER ' + NAME + ' 0 * ' + NAME)
write_to_system('JOIN #' + CHANNEL)

connectBuffer = ""
buffer = ""

while True:
    connectBuffer += str(s.recv(1024))

    if ':End of /NAMES list' in connectBuffer:
        connectBuffer = connectBuffer.replace('\'b\'', '').replace('b\'', '').replace('\\r\\n\'', '')
        for line in connectBuffer.split('\\r\\n'):
            print(line)
        write_to_chat(CONNECT_MESSAGE)
        break

while True:
    line = str(s.recv(1024)).replace('b\'', '').replace('\\r\\n\'', '')

    if line == 'PING :tmi.twitch.tv':
        write_to_system('PONG :tmi.twitch.tv')
    elif 'PRIVMSG' in line:
        username = line.split('!')[1].split('@')[0]
        message = line.split(':')[2]
        if message == '!squats':
            write_to_chat('This boy has 1324234 squats left!')
        elif is_cheer(message):
            bits, message = get_cheer_contents(message)
            pass

    print(line)

