from django.core import management
from time import sleep

import threading

def conjob():
    t = threading.Thread(target=init_conjob)
    t.daemon = True
    t.start()

def init_conjob():
    while True:
        sleep(5)
        management.call_command('process_uploads')
