import pexpect

class player():
    def play(self, url):
        self.pl = None
        self.pl = pexpect.spawn('cvlc ' + url + ' --intf rc')

    def volDown(self):
        self.pl.sendline('voldown')

    def volUp(self):
        self.pl.sendline('volup')

    def stop(self):
        self.pl.sendline('q')