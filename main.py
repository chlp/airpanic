import requests
import os
import time
from pathlib import Path

file_name = str(Path(__file__).parent.absolute()) + '/panic.txt'
panic_number_max = 20
panic_number_min = int(panic_number_max * .7)
bot_credentials = ''
chat_id = ''

prev_air = 0
if os.path.isfile(file_name):
    f = open(file_name, 'r')
    prev_air = int(f.readline())
    f.close()

r = requests.get('https://aircms.online/php/guiapi.php?graph&fwid=14970961')
data = r.json()['data'][0][-1]
lastTs = data[0]
air = data[1]

if int(time.time()) - lastTs < 300 and panic_number_min <= air >= panic_number_max:
    f = open(file_name, 'w')
    f.write('%d' % air)
    f.close()

    if prev_air < panic_number_max <= air:
        r = requests.post('https://api.telegram.org/bot' + bot_credentials + '/sendMessage',
                          data={'chat_id': chat_id, 'text': 'air panic:' + str(air)})

    if prev_air >= panic_number_min > air:
        r = requests.post('https://api.telegram.org/bot' + bot_credentials + '/sendMessage',
                          data={'chat_id': chat_id, 'text': 'cancel air panic:' + str(air)})
