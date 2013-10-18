import socket
import mpd
import ssl

MPD_HOST = "127.0.0.1"
MPD_PORT = 6600

HOST = "irc.rizon.net"
HOME_CHANNEL = "#AcuallyOS"
NICK = "JiyuuRadio"
PORT = 9999
SSL = True

mpc = mpd.MPDClient()
mpc.connect(MPD_HOST, MPD_PORT)

if(SSL):
    s = ssl.wrap_socket(socket.socket( ))
else:
    s = socket.socket( )
s.connect((HOST, PORT))
s.send("USER "+ NICK +" "+ NICK +" "+ NICK +" :"+NICK+"\n")
s.send("NICK "+ NICK +"\r\n")
s.send("JOIN "+ HOME_CHANNEL +"\r\n")


def parse_command(command):
    if command.startswith("add"):
        args = command[4:]
        mpc.searchadd("any", args)
    elif command == "play":
        mpc.play()
    elif command == "next":
        mpc.next()
    elif command == "current":
        return_output(mpc.currentsong())
    elif command == "queue":
        queue = "Next 4 tracks:\n"
        for track in mpc.playlist()[:4]:
            queue += str(track)+"\n"
        return_output(queue)
    elif command == "stats":
        return_output(mpc.stats())
    elif command == "help":
        return_output(".add - adds tracks | .play - starts playing (useful for when the stream dies due to lack of queued tracks)\n.next - next track | .current - prints infor about current track\n.queue - shows next 4 songs | .stats - shows stats")

def return_output(text):
    text=str(text)
    for msg in text.split("\n"):
        s.send("PRIVMSG "+HOME_CHANNEL+" :"+str(msg)+"\r\n")



print "*** Connecting... ***"
while 1:
    line = s.recv(2048)
    line = line.strip("\r\n")
    if("End of /NAMES list." in line):
	print "\n*** Connected! ***\n"
	break
    else:
	print line

while 1:
    try:
        line = s.recv(2048)
        line = line.strip("\r\n")
        print line
        if "PING" in line:
            s.send("PONG :"+line[6:])
        elif "PRIVMSG" in line and not "NOTICE" in line and HOME_CHANNEL in line:
            command = line[line.rindex(":")+1:]
            if "*" in command:
                return_output("NOPE")
            elif command.startswith("."):
                parse_command(command[1:])
    except:
        return_output("I dun goofed, soz aye m80.")
