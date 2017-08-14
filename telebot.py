#!/usr/bin/env python

import telepot
import sys
import datetime


try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser

config = ConfigParser()
config.read('config.ini')

TOKEN = config.get('config', 'token')
CHATS = config.items('chats')


def format_chat(raw):
    if len(raw) > 0:
        out = ''
        print(raw)
        for i in raw:
            date = datetime.datetime.fromtimestamp(i['message']['date']).strftime('%d.%m.%y %H:%M:%S')
            username = None
            if 'username' in i['message']['from'].keys():
                username = i['message']['from']['username']
            else:
                username = i['message']['from']['first_name']
            out += u'{0}: "{1}" [{2}]\n'.format(date, username, i['message']['chat']['id'])
        return out
    return 'No chats yet'

def usage():
    print '''
        Usage: telebot.py MSSG
               telebot.py MSSG chat_id
               telebot.py info
               telebot.py chats
    '''


def info():
    bot = telepot.Bot(TOKEN)
    print(bot.getMe())


def get_updates():
    bot = telepot.Bot(TOKEN)
    response = bot.getUpdates()
    print format_chat(response)

def send_mssg(mssg, chat=None):
    bot = telepot.Bot(TOKEN)
    if not chat:
        for chat in CHATS:
            bot.sendMessage(chat[1], mssg, parse_mode='Markdown')
        return len(chat_list)
    bot.sendMessage(chat, mssg, parse_mode='Markdown')
    return 1


if __name__ == '__main__':
    if len(sys.argv) == 2:
        if sys.argv[1] == 'info':
            info()
        elif sys.argv[1] == 'chats':
            get_chats()
        else:
            send_mssg(sys.argv[1])
    elif len(sys.argv) == 3:
        send_mssg(sys.argv[1], sys.argv[2])
    else:
        usage()

