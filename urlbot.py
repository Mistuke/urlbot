#!/usr/bin/python
import sys
import socket
import string
from urlparse import urlparse
import time
import urllogger
import urldescription
import re

class URLBot():
    def __init__(self, host, port, nick, ident, name, chan):
        self.host = host
        self.port = port
        self.nick = nick
        self.ident = ident
        self.name = name
        self.chan = chan
        self.desc = urldescription.URLdescription()
        self.welcome = 'Welcome to' #FIXME
        self.sock = socket.socket( )

    def parsemsg(self):
        complete=self.line[1:].split(':',1)
        info=complete[0].split(' ')
        msgpart=complete[1]
        sender=info[0].split('!')

        msgpart = re.sub(r'[^\x20-\x7e]', '', msgpart)

        for w in msgpart.split(' '):
            # Check if phabricator diff
            if w.startswith ('D'):
               w='https://phabricator.haskell.org/' + w

            # Check if trac issue
            if w.startswith ('#'):
               w='https://ghc.haskell.org/trac/ghc/ticket/' + w[1:]

            # Check if git commit hash
            match = re.match ("[a-fA-F0-9]{40}|[a-fA-F0-9]{7}", w)
            if match and not w.startswith ("http"):
                w='https://github.com/ghc/ghc/commit/' + match.group(0)
                # doesn't seem to put commit title in.
                # w='https://git.haskell.org/ghc.git/commit/' + match.group(0)

            o = urlparse(w)
            if len(o.netloc)!=0:
                print int(time.time()),'checking url: "'+w.strip()+'"'
                title = self.desc.fetchtitle(w.strip())
                if len(title)!=0:
                    urllogger.URLlogger(w, title, sender[0]).start()
                    title_decoded = self.desc.unescape(title)  # Remove '&#8226;' etc
                    title_decoded = title_decoded + " - " + w
                    print int(time.time()),'PRIVMSG '+info[2]+' :'+title_decoded
                    if w.strip() != title_decoded:
                        self.sock.send('PRIVMSG '+info[2]+' :'+title_decoded+'\n')

    def run(self):
        readbuffer=''
        self.sock.connect((self.host, self.port))
        print int(time.time()),self.sock.recv(4096)

        print int(time.time()),'NICK '+self.nick
        self.sock.send('NICK '+self.nick+'\n')
        print int(time.time()),'USER '+self.ident+' '+self.host+' bla :'+self.name
        self.sock.send('USER '+self.ident+' '+self.host+' bla :'+self.name+'\n')

        timer = time.time()
        while True:
            self.line=self.sock.recv(512)
            print int(time.time()),self.line.rstrip('\n')
            if self.line.find('Closing Link')!=-1:
                print int(time.time()),'closing link, exiting..'
                sys.exit(1)
            if self.line.find(self.welcome)!=-1:
                print int(time.time()),'JOIN '+self.chan
                self.sock.send('JOIN '+self.chan+'\n')
            if self.line.find('PRIVMSG')!=-1:
                try:
                    self.parsemsg()
                except Exception, e:
                    print e
            self.line=self.line.rstrip()
            self.line=self.line.split()
            if(self.line[0]=='PING'):
                timer = time.time()
                print int(time.time()),'PONG '+self.line[1]
                self.sock.send('PONG '+self.line[1]+'\n')
            if(time.time()-timer>900):
                print int(time.time()),'no PING for 15 min, exiting..'
                sys.exit(1)
