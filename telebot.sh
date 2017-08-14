#!/bin/bash
cd /opt/telebot
. venv/bin/activate
./telebot.py "$@"
