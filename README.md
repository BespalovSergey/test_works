# test_works

Бот сохраняет аудиосообщения из диалогов  на диск по идентификаторам пользователей.
Конвертирует все аудиосообщения в формат wav с частотой дискретизации 16kHz
Записывает в БД адреса файлов в формате: uid —> [audio_message_0, audio_message_1, ..., audio_message_N].
Определяет есть ли лицо на отправляемых фотографиях или нет, сохраняет только те, где оно есть,
Если лицо есть в ответном сообщении отправляет фотографию с лицом выделенным рамкой

Установите все зависимости из  файла requirements.txt
Также необходимо установить библиотеку ffmpeg , open-cv
ffmpeg для линукс sudo apt-get install ffmpeg 
opencv для линукс sudo apt install python3-opencv

В файле python-telegram.py Заменить "ВАШ ТОКЕН" на Токен вашего бота телеграм