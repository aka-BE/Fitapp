import sys

sys.path.insert(0, '/var/www/fitapp')

activate_this = '/home/akabe/.local/share/virtualenvs/fitapp-U_asuPSo/bin/activate_this.py'
with open(activate_this) as file:
    exec(file.read(), dict(__file__=activate_this))

from wsgi import app as application
