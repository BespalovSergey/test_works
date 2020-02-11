import os

def get_file_name(folder, chat_id, message_count):
    type_dict = {'voice': ['audio_message_', 'wav'], 'photo': ['photo_message_', 'jpg']}
    user_folder = '{}/{}'.format(folder, chat_id)

    if not os.path.exists(user_folder):
        os.makedirs(user_folder)
    file_name = '{}/{}{}.{}'.format(user_folder,type_dict[folder][0], message_count, type_dict[folder][1])

    return file_name