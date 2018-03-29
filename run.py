#!/usr/bin/python
import urlbot

HOST='irc.freenode.net'
PORT=6667
NICK='phyx-bot'
IDENT='phyx-bot'
REALNAME='url botty'
CHANNEL='#phyx'

bot = urlbot.URLBot(HOST, PORT, NICK, IDENT, REALNAME, CHANNEL)
bot.run()
