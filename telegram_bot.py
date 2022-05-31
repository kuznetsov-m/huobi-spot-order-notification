import os
import telebot
from telebot import types


def send_text(reciver_user_id: int, text: str):
    """
    Send text message to reciver_user_id
    """

    API_TOKEN = os.environ.get('TELEGRAM_API_TOKEN')
    
    bot = telebot.TeleBot(API_TOKEN)
    
    try:
        bot.send_message(reciver_user_id, text)
    except Exception as e:
        print(f'ERROR [{__name__}]: {str(e)}')