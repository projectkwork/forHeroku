import telebot
import firebase_admin
import sys
import time
from threading import Thread
import logging
import datetime as dt
from time import sleep
from firebase_admin import credentials
from firebase_admin import firestore
from openpyxl import Workbook
import openpyxl
from datetime import date
from datetime import timedelta
from telebot import types
import schedule
cred = credentials.Certificate("system.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
var_to_stop_sending = 0
token = '5233386973:AAHwA29T0WlUuWhNC91Xp8VB-JV2BIoqHjs'
bot = telebot.TeleBot(token)
def schedule_checker():
    while True:
        schedule.run_pending()
        sleep(1)

@bot.message_handler(commands=['start'])


def start_message(message):
    if str(message.chat.id) in db.collection('users').document('admin').get().to_dict().values():
        send = bot.send_message(message.chat.id,'Распознал вас, Сэр. Буду отправлять таблицу каждое утро. Для получения отчета нажмите на кнопку.')
        bot.register_next_step_handler(send,admin)

            
    else:
        if message.text == '/start':
            doc_ref = db.collection(u'users').document('ID')
            doc_ref.update({str(message.chat.id):[False]})
            send = bot.send_message(message.chat.id, 'Здравстуйте, для продолжения введите ваше ФИО')
            bot.register_next_step_handler(send,fio)
        
@bot.message_handler(func=lambda message: True)

def fio(message):
    if message.text != '/start':
        doc_ref = db.collection(u'users').document(u'ID')
        doc_ref.update({str(message.chat.id):[True,str(message.text)]})
        print(message.chat.id)
        send = bot.send_message(message.chat.id, 'Поздравляем с успешной регистрацией. Просим писать только по поводу отчета и не засорять бота')
        while (str(dt.datetime.now()).split()[1].split('.')[0]) != '15:46:50':
            pass
        sleep(1)
        bot.send_message(message.chat.id,'Ответьте на вопросы:')
        doc_ref = db.collection(u'users').document(u'questions')
        a = sorted(doc_ref.get().to_dict().items())
        for i in a:
            bot.send_message(message.chat.id,i[1])
        bot.send_message(message.chat.id,'ВНИМАНИЕ! Ответы на вопросы присылать строго через знак ";"')
        bot.register_next_step_handler(send,answers)
        timing = time.time()
        doc_ref = db.collection(u'users').document('ID')
        while True:
            for i in db.collection('users').document('ID').get().to_dict().items():
                if i[0] == str(message.chat.id):
                    if i[1][0] == False:
                        break
            if time.time() - timing > 3600:
                bot.send_message(message.chat.id,'ВНИМАНИЕ! Вы не ответили на вопросы!')
                timing = time.time()
            sleep(10)
            
def admin(message):
    
    markup = types.ReplyKeyboardMarkup()
    button = types.KeyboardButton('Получить отчет')
    markup.row(button)
    send = bot.send_message(message.chat.id,'Вот ваш отчет',reply_markup=markup)
    bot.send_document(message.chat.id,document=open('top.xlsx','rb'))
    bot.register_next_step_handler(send,admin)
    
def answers(message):
    
    schedule.clear(str(message.chat.id))
    for i in db.collection('users').document('ID').get().to_dict().items():
        if i[0] == str(message.chat.id):
            mas = i[1]
            break
    if len(mas) > 2:
        mas[2] = message.text
    else:
        mas.append(message.text)
    mas[0] = False
    doc_ref = db.collection(u'users').document('ID')
    doc_ref.update({str(message.chat.id):mas})
    send = bot.send_message(message.chat.id,'Спасибо за ваши ответы! Не забудьте завтра ответить снова')
    while (str(dt.datetime.now()).split()[1].split('.')[0]) != '15:47:00':
            pass
    sleep(1)
    bot.send_message(message.chat.id,'Ответьте на вопросы:')
    doc_ref = db.collection(u'users').document(u'questions')
    a = sorted(doc_ref.get().to_dict().items())
    for i in a:
        bot.send_message(message.chat.id,i[1])
    send = bot.send_message(message.chat.id,'ВНИМАНИЕ! Ответы на вопросы присылать строго через знак ";"')
    for i in db.collection('users').document('ID').get().to_dict().items():
        if i[0] == str(message.chat.id):
            mas = i[1]
    mas[0] = True
    doc_ref = db.collection(u'users').document('ID')
    doc_ref.update({str(message.chat.id):mas})
    bot.register_next_step_handler(send,answers1)
    doc_ref = db.collection(u'users').document('ID')
    schedule.every(3).seconds.do(get_sending_function(message.chat.id)).tag(message.chat.id)
    
    
            
def answers1(message):
    schedule.clear(str(message.chat.id))
    for i in db.collection('users').document('ID').get().to_dict().items():
        if i[0] == str(message.chat.id):
            mas = i[1]
            break
    if len(mas) > 2:
        mas[2] = message.text
    else:
        mas.append(message.text)
    mas[0] = False
    doc_ref = db.collection(u'users').document('ID')
    doc_ref.update({str(message.chat.id):mas})
    send = bot.send_message(message.chat.id,'Спасибо за ваши ответы! Не забудьте завтра ответить снова')
    while (str(dt.datetime.now()).split()[1].split('.')[0]) != '23:37:20':
            pass
    sleep(1)
    bot.send_message(message.chat.id,'Ответьте на вопросы:')
    doc_ref = db.collection(u'users').document(u'questions')
    a = sorted(doc_ref.get().to_dict().items())
    for i in a:
        bot.send_message(message.chat.id,i[1])
    send = bot.send_message(message.chat.id,'ВНИМАНИЕ! Ответы на вопросы присылать строго через знак ";"')
    for i in db.collection('users').document('ID').get().to_dict().items():
        if i[0] == str(message.chat.id):
            mas = i[1]
    mas[0] = True
    doc_ref = db.collection(u'users').document('ID')
    doc_ref.update({str(message.chat.id):mas})
    bot.register_next_step_handler(send,answers)
    doc_ref = db.collection(u'users').document('ID')
    schedule.every(3).seconds.do(get_sending_function(message.chat.id)).tag(message.chat.id)
def get_sending_function(chatId):
    def send_function():
        bot.send_message(chatId, "ВНИМАНИЕ! Вы не ответили на вопросы!")
        for i in db.collection('users').document('ID').get().to_dict().items():
            if i[0] == str(chatId):
                mas = i[1]
                break
        if mas[0] == False:
            return schedule.CancelJob
        else:
            return 0
    return send_function

if __name__ == "__main__":
    scheduleThread = Thread(target=schedule_checker)
    scheduleThread.daemon = True
    scheduleThread.start()
    bot.polling(none_stop=False,interval=1)
