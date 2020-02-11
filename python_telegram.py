from telegram.ext import  Updater, PreCheckoutQueryHandler, CommandHandler,MessageHandler,CallbackQueryHandler,Filters
from telegram import InlineKeyboardButton,InlineKeyboardMarkup
from dbase import DB
import utils
from pydub import AudioSegment
import os
import  cv2
from PIL import Image, ImageDraw
import numpy as np
from shutil import copyfile

class TestTelegramBot():

    def __init__(self):
        self.telegram_key = 'ВАШ ТОКЕН'
        self.db = DB()

    
   
     

    def handle_users_reply(self,bot, update):
        chat_id =update.message.chat_id 
        if update.message:
            user_reply = update.message.text
        elif update.callback_query:
            user_reply = update.callback_query.data
            chat_id = update.callback_query.message.chat_id
        else:
            return

        if user_reply == '/start':
            user_state = 'START' 
        elif update.message.voice:
            user_state = 'HANDLE_VOICE'
        elif update.message.photo:
            user_state = 'HANDLE_PHOTO'
        else:
            user_state = self.db.get_state(chat_id)
        print(user_state)   
        states_functions = {
          'START': self.start,
          'HANDLE_ECHO': self.echo,
          'HANDLE_VOICE': self.handle_voice,
          'HANDLE_PHOTO': self.handle_photo,
        }
        
        state_handler = states_functions[user_state]
        next_state = state_handler(bot,update)
        self.db.set_state(chat_id,next_state)


    def echo(self, bot, update):
        bot.send_message(chat_id= update.message.chat_id,
                        text= 'Пришлите аудио запись и я схраню её в формате wav \n Или изображение ' \
               'постараюсь найти лицо на нём , если оно есть я сохраню изображение.')
        return 'HANDLE_ECHO'


    def start(self, bot, update):
        text = 'Пришлите аудио запись и я схраню её в формате wav \n Или изображение ' \
               'постараюсь найти лицо на нём , если оно есть я сохраню изображение.'
        bot.send_message(chat_id= update.message.chat_id,
                         text= text )
        
        return 'HANDLE_ECHO'


    def handle_voice(self, bot, update):
        folder = 'voice'
        chat_id = update.message.chat_id

        file_info = bot.get_file(update.message.voice.file_id)
        file_info.download('{}.ogg'.format(chat_id))

        message_count = self.db.get_message_count('audio_path', chat_id)

        file_name = utils.get_file_name(folder, chat_id, message_count)
        voice = AudioSegment.from_file('{}.ogg'.format(chat_id), format='ogg')
        voice = voice.set_frame_rate(16000)
        voice.export(file_name, format='wav')
        voice_name = file_name.split('/')[-1].split('.')[0]
        m_count, value = self.db.set_path_value('audio_path', voice_name, chat_id)
        os.remove('{}.ogg'.format(chat_id))
        text = 'У Вас {} аудио сообщений с именами\n{}'.format(m_count, value.replace(',', '\n'))
        bot.send_message(chat_id= update.message.chat_id,
                        text= text)
        return 'HANDLE_ECHO'


    def handle_photo(self, bot, update):
        folder = 'photo'
        chat_id = update.message.chat_id
        cascad_file = 'haarcascade_frontalface_default.xml'
        file_info = bot.get_file(update.message.photo[-1].file_id)
        file_info.download('{}.jpg'.format(chat_id))

        face_cascad = cv2.CascadeClassifier(cascad_file)
        gray = Image.open('{}.jpg'.format(chat_id)).convert('L')
        image = np.array(gray, 'uint8')
        faces = face_cascad.detectMultiScale(image, scaleFactor=1.3, minNeighbors=7, minSize=(50, 50))

        if len(faces) > 0:

            message_count = self.db.get_message_count('image_path', chat_id)
            file_name = utils.get_file_name(folder, chat_id, message_count)
            copyfile('{}.jpg'.format(chat_id), file_name)
            img = Image.open('{}.jpg'.format(chat_id))

            for (x, y, w, h) in faces:
               # img = Image.open('{}.jpg'.format(chat_id))
                draw = ImageDraw.Draw(img)
                draw.rectangle((x,y,x+w,y+h), outline='green', width=5)

            img.save('{}.jpg'.format(chat_id))
            with(open('{}.jpg'.format(chat_id), 'rb')) as file:
                bot.send_photo(chat_id, file )

            image_name = file_name.split('/')[-1].split('.')[0]
            i_count, image_names = self.db.set_path_value('image_path', image_name, chat_id)
            bot.send_message(chat_id=chat_id, text='На изображении найдено лицо {} шт\n'
                                                   'Изображение сохранено\n'
                                                   'У Вас {} фото сообщений с именами\n{}'.format(len(faces),
                                                                                                  i_count,
                                                                                            image_names.replace(',', '\n')))
        else:
            message_info = ''
            image_names = self.db.get_image_names(chat_id)

            if image_names:
                count_image = len(image_names.split(','))
                message_info = 'У Вас {} фото сообщений с именами\n{}'.format(count_image, image_names.replace(',','\n'))

            bot.send_message(chat_id=chat_id,
                             text='На изображении лицо не найдено \n{}'.format(message_info))
        os.remove('{}.jpg'.format(chat_id))
        return 'HANDLE_ECHO'

    def run_telebot(self):
        REQUEST_KWARGS = {
            'proxy_url': 'socks4://',

            'urllib3_proxy_kwargs': {
                'assert_hostname': 'False',
                'cert_reqs': 'CERT_NONE'}

            }
        
        token = self.telegram_key
        updater = Updater(token=token)#  request_kwargs=REQUEST_KWARGS)
        dispatcher = updater.dispatcher

        dispatcher.add_handler(MessageHandler(Filters.text,self.handle_users_reply))
        dispatcher.add_handler(CommandHandler('start',self.handle_users_reply))
        dispatcher.add_handler(MessageHandler(Filters.voice, self.handle_users_reply))
        dispatcher.add_handler(MessageHandler(Filters.photo, self.handle_users_reply))
    
        updater.start_polling()
        


   