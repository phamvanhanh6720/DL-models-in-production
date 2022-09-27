import os
import configparser
import datetime
import pytz 
from pathlib import Path

cfg = configparser.ConfigParser()
env_path = os.path.join(str(Path(__file__).parent.absolute()), 'environment.ini')
cfg.read(env_path)


#=========================================================================
#                           TIMING CONFIG
#=========================================================================
u = datetime.datetime.utcnow()
u = u.replace(tzinfo=pytz.timezone("Asia/Ho_Chi_Minh"))

#=========================================================================
#                          REDIS INFORMATION 
#=========================================================================
REDIS = cfg['redis']
REDIS_BACKEND = "redis://:{password}@{hostname}:{port}/{db}".format(
    hostname=REDIS['host'],
    password=REDIS['pass'],
    port=REDIS['port'],
    db=REDIS['db']
)

#=========================================================================
#                          BROKER INFORMATION 
#=========================================================================
RABBITMQ = cfg['rabbitmq']
BROKER = "amqp://{user}:{pw}@{hostname}:{port}/{vhost}".format(
    user=RABBITMQ['user'],
    pw=RABBITMQ['pass'],
    hostname=RABBITMQ['host'],
    port=RABBITMQ['post'],
    vhost=RABBITMQ['vhost']
)
