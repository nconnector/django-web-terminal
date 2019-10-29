import configparser
import socket
import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import ReplyKeyboardMarkup
from pprint import pprint
from time import sleep, strftime
from datetime import datetime
import ctypes


ctypes.windll.kernel32.SetConsoleTitleW('Garage Door - ESP8266')
config = configparser.ConfigParser()
config.read('config.ini')

API_TOKEN = config['TELEGRAM']['API_TOKEN']
TRUSTED_USERS = [int(x) for x in config['TELEGRAM']['TRUSTED_USERS'].split(',')]
ADMIN = int(config['TELEGRAM']['ADMIN'])
ESP8266_IP = config['LOCAL']['ESP8266_IP']


def auth_user(chat_id):
    TRUSTED_USERS.append(chat_id)  # todo: add config functionality


def to_esp8266(message, chat_id):
    s = socket.socket()
    s.connect((ESP8266_IP, 80))
    s.sendall(message.encode())  # to bytes with utf-8
    while True:
        response = s.recv(1024).decode("utf-8")
        if response:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
            print(f'{timestamp}  #  {chat_id}  #  {response}')
            bot.sendMessage(chat_id, response, reply_markup=keyboard)  # send messages as they appear
        else:
            break
    s.close()


def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type == 'text':
        if msg['text'] == '/start':
            bot.sendMessage(chat_id, 'Hello! If you are not registered yet, press "register".', reply_markup=keyboard)

        elif msg['text'] == "I'm home" or msg['text'] == "Click":
            if chat_id in TRUSTED_USERS:
                try:
                    cmd = msg['text']

                    to_esp8266(cmd, chat_id)
                    sleep(1)

                except Exception as e:
                    print(e)
                    bot.sendMessage(chat_id, 'there has been an error')
                    bot.sendMessage(chat_id, e, reply_markup=keyboard)

        elif msg['text'] == "Register":
            # apply for registration
            if chat_id not in TRUSTED_USERS:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
                print(f'{timestamp}  #  {chat_id}  #  Requested access.')
                bot.sendMessage(ADMIN, f'{chat_id} has requested access')
                bot.sendMessage(chat_id, f'Attempting registration. Your id: {chat_id}.', reply_markup=keyboard)
            else:
                bot.sendMessage(chat_id, f'Already registered. Your id: {chat_id}.', reply_markup=keyboard)

        elif msg['text'] == "Knock":
            # check user's own authorization
            resp = ':)' if chat_id in TRUSTED_USERS else ':('
            bot.sendMessage(chat_id, resp, reply_markup=keyboard)

        elif msg['text'].split(' ')[-1] == "access" and chat_id == ADMIN:
            # approve registrations as ADMIN
            user = int(msg['text'].split(' ')[0])
            auth_user(user)
            bot.sendMessage(ADMIN, f'{user} has been TRUSTED', reply_markup=keyboard)
            bot.sendMessage(user, 'You were authorized!', reply_markup=keyboard)

    else:
        bot.sendMessage(chat_id, f'not text', reply_markup=keyboard)
        pprint(msg)


keyboard = ReplyKeyboardMarkup(keyboard=[["I'm home", "Click"], ["Register", "Knock"]])
bot = telepot.Bot(API_TOKEN)
info = bot.getMe()

MessageLoop(bot, handle).run_as_thread()  # handle incoming messages
print('Garage Door bot is now active....')
input()
