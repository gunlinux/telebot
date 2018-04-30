#!/usr/bin/env python

import sys
import datetime
import requests
import hashlib


try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser

config = ConfigParser()
config.read('config.ini')

SECRET = config.get('config', 'secret')
CHATS = config.items('chats')
TGATE = config.get('config','tgate')


def usage():
    print('''
        Usage: telebot.py MSSG
               telebot.py MSSG chat_id
    ''')

def get_token(mssg):
    test_hash = hashlib.sha1(mssg.encode()).hexdigest()
    temp = test_hash + hashlib.sha1(SECRET.encode()).hexdigest()
    return hashlib.sha1(temp.encode()).hexdigest()

def send_mssg(mssg, chat_id=None):
    token = get_token(mssg)
    params = {'mssg': mssg, 'token': token}
    if not chat_id:
        params['chats'] = ','.join([i[1] for i in CHATS])
        r = requests.get('{}/send'.format(TGATE), params=params)
    else:
        r = requests.get('{}/send/{}'.format(TGATE, chat_id), params=params)


if __name__ == '__main__':
    if len(sys.argv) == 2:
        # send all from config
        send_mssg(sys.argv[1])
    elif len(sys.argv) == 3:
        # send sing message for someone
        send_mssg(sys.argv[1], sys.argv[2])
    else:
        usage()
