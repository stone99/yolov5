from __future__ import print_function
import traceback
from twisted.internet import protocol
from twisted.internet import reactor
import re


class MyPP(protocol.ProcessProtocol):
    def __init__(self, verses):
        self.verses = verses
        self.data = ""

    def connectionMade(self):
        print("connectionMade!")
        for i in range(self.verses):
            self.transport.write(b"Aleph-null bottles of beer on the wall,\n" +
                                 b"Aleph-null bottles of beer,\n" +
                                 b"Take one down and pass it around,\n" +
                                 b"Aleph-null bottles of beer on the wall.\n")
        self.transport.closeStdin()  # tell them we're done

    def outReceived(self, data):
        print("outReceived! with %s bytes!" % data.decode())
        self.data = self.data + data.decode()

    def errReceived(self, data):
        print("errReceived! with %s bytes!" % data.decode())

    def inConnectionLost(self):
        print("inConnectionLost! stdin is closed! (we probably did it)")

    def outConnectionLost(self):
        print("outConnectionLost! The child closed their stdout!")
        # now is the time to examine what they wrote
        # print("I saw them write:", self.data)
        (dummy, lines, words, chars, file) = re.split(r'\s+', self.data)
        print("I saw %s lines" % lines)

    def errConnectionLost(self):
        print("errConnectionLost! The child closed their stderr.")

    def processExited(self, reason):
        print("processExited, status %d" % (reason.value.exitCode,))

    def processEnded(self, reason):
        print("processEnded, status %d" % (reason.value.exitCode,))
        print("quitting")
        reactor.stop()

if __name__ == "__main__":
    pp = MyPP(10)
    reactor.spawnProcess(pp, "detect.py", ["detect.py", "--source", "test.mp4"], {})
    reactor.run()




