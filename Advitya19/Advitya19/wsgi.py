"""
WSGI config for Advitya19 project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os
import time 
import traceback 
import signal 
import sys 
from django.core.wsgi import get_wsgi_application 

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Advitya19.settings')

sys.path.append('/var/www/vhosts/Advitya19') 
# adjust the Python version in the line below as needed 
sys.path.append('/home/ubuntu/.local/share/virtualenvs/Advitya19-fYUrhkM7/Lib/site-packages')

try: 
    application = get_wsgi_application() 
except Exception: 
    # Error loading applications 
    if 'mod_wsgi' in sys.modules: 
        traceback.print_exc() 
        os.kill(os.getpid(), signal.SIGINT) 
        time.sleep(2.5)


 

 
 
 
