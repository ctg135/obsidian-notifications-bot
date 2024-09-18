from webdav3.client import Client
from datetime import datetime
from telebot import TeleBot
from random_unicode_emoji import random_emoji
import re, os
import utils

# Loading configuration file
conf = utils.load_pass_file("pass.json")

utils.check_tmp_folder_exists(conf['tmp_dir'])
tmp_file_name = conf['tmp_dir'] + 'temp_file'
# Connection options for Webdav server
options = {
    'webdav_hostname': conf['server'],
    'webdav_login': conf['login'],
    'webdav_password': conf['password']
}

root_dir = conf['vault_name'] + '/'
vault = Client(options)
notfications = []
today = datetime.today().strftime('%Y-%m-%d')

# Check that root folder exists
if not vault.check(root_dir):
    print(f'Folder "{root_dir}" does not exist at WebDav vault')

def look_dirs(base_dir: str):
    '''
    Function for recursively looking for .md files in folders
    '''
    items = vault.list(base_dir)
    for item in items:
        # item is .md file
        if item[-3::] == '.md':
            # print(f'Found .md file: {item}')
            check_notifications(vault, base_dir + item)
        # item is directory
        if item[-1] == '/':
            # print(f'Found directory: {item}')
            look_dirs(base_dir + item)

def check_notifications(server, filename: str):
    '''
    Downloads file and look up notification template in them
    '''
    server.download_sync(remote_path=filename, local_path=tmp_file_name)

    with open(tmp_file_name, 'r', encoding="utf8") as file: lines = file.read()
    result = re.findall(
        r"- \[r\](.*)\(@(\d{4}-\d{2}-\d{2})\)",
        lines
    )

    for notify in result:
        if notify[1] == today:
            notfications.append(notify[0].strip())

    os.remove(tmp_file_name)

look_dirs(root_dir)

# print(notfications)

# Sending messages via Telegram
bot = TeleBot(conf['bot_id'])

for notify in notfications: 
    bot.send_message(chat_id=conf['user_id'], text=random_emoji()[0] + ' ' + notify)
