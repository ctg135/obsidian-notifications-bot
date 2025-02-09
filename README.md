# Telegram bot for sending notifications from Obsidian

## Overview

This script uses format of plugin Tasks to remind you about tasks, that have due date today

So, script searchs in your webdav folder any file, that contents this template:

```
- [ ] Task to do 📅 2025-02-09
```

And than sends you a message between `- [ ]` and `📅 2025-02-09`

## Instalation

### Configuration file

File `pass.json` with authorization data for WebDav server looks like this:

```json
{
    "vault_name": "name",
    "bot_id": "###",
    "user_id": "###",
    "server": "https://webdav.server.net",
    "login": "username",
    "password": "###"
}
```

### Edit webdav library

Sometimes `webdav3` library not works properly when downloading files than need to fix some code:

```python
#.venv\Lib\site-packages\webdav3\client.py
class Client:
    ...
    def download_file(self, remote_path, local_path, progress=None, progress_args=()):
    ... 
    
    # 456 line original:
    with open(local_path, 'wb') as local_file:
        response = self.execute_request('download', urn.quote())
        total = int(response.headers['content-length'])
        current = 0

    # to new:
    with open(local_path, 'wb') as local_file:
        response = self.execute_request('download', urn.quote())
        if 'content-length' in response.headers.keys():
            total = int(response.headers['content-length'])
        else: total = 0
        current = 0

```