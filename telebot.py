#!/usr/bin/env python

import telepot
import sys
import datetime
from config import chat_list, TOKEN



def format_chat(raw):
    if len(raw) > 0:
        out = ''
        for i in raw:
            date = datetime.datetime.fromtimestamp(i['message']['date']).strftime('%d.%m.%y %H:%M:%S')
            out += '{0}: "{1}" [{2}]\n'.format(date, i['message']['from']['username'], i['message']['chat']['id'])
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


def get_chats():
    bot = telepot.Bot(TOKEN)
    response = bot.getUpdates()
    print format_chat(response)

def send_mssg(mssg, chat=None):
    bot = telepot.Bot(TOKEN)
    if not chat:
        for chat in chat_list:
            bot.sendMessage(chat, mssg)
        return len(chat_list)
    bot.sendMessage(chat, mssg)
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

