import json, os

def load_pass_file(filename: str):
    '''
    Loads config as dictionary form "./filename" file

    Exit program when file or key is not provided
    '''

    if not os.path.isfile("pass.json"):
        print(f'No "{filename}" file provided')
        exit()

    with open(filename, 'r') as file:
        conf = json.load(file)
    
    keys = ['vault_name', 'bot_id', 'user_id', 'server', 'login', 'password']

    error_flag = False
    for key in keys:
        if key not in conf.keys():
            print(f'No "{key}" provided in "{filename}"')
            error_flag = True

    if error_flag: exit()

    return conf
