
import utils
from webdav3.client import Client

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

if not vault.check(root_dir):
    print(f'Folder "{root_dir}" does not exist at WebDav vault')

def look_dirs(base_dir: str):
    items = vault.list(base_dir)
    # print(f'Look up in "{base_dir}": {items}')
    for item in items:
        # item is note
        # need to download and look up for tags
        # print(item[-3::])
        if item[-3::] == '.md':
            print(f'Found .md file: {item}')
            check_notifications(vault, base_dir + item)
        # item is directory
        if item[-1] == '/':
            print(f'Found directory: {item}')
            look_dirs(base_dir + item)

def check_notifications(server, filename: str):
    server.download_sync(remote_path=filename, local_path=tmp_file_name)
    exit()

look_dirs(root_dir)

#TODO: download file and search tags in there

#TODO: send messages

#TODO: проверка существования временного каталога
