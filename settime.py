import configparser
import platform
import itertools
import time
from sucks import *
import json

_LOGGER = logging.getLogger(__name__)

#_LOGGER.parent.setLevel(logging.DEBUG)

def config_file():
    if platform.system() == 'Windows':
        return os.path.join(os.getenv('APPDATA'), 'sucks.conf')
    else:
        return os.path.expanduser('~/.config/sucks.conf')

def read_config():
    parser = configparser.ConfigParser()
    with open(config_file()) as fp:
        parser.read_file(itertools.chain(['[global]'], fp), source=config_file())
    return parser['global']

config = read_config()

api = EcoVacsAPI(config['device_id'], config['email'], config['password_hash'],
                         config['country'], config['continent'], config['verify_ssl'])
my_vac = api.devices()[0]
vacbot = VacBot(api.uid, api.REALM, api.resource, api.user_access_token, my_vac, config['continent'], '192.168.0.239', False, config['verify_ssl'])
#vacbot.connect_and_wait_until_ready()
ts = time.time()
vacbot.run(VacBotCommand("GetMapSet", {"tp":"sa"}))
vacbot.run(SetTime(str(ts), '+7')) # return to the charger