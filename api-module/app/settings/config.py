from pathlib import Path
import os
import configparser
import datetime
import pytz 


cfg = configparser.ConfigParser()

env_path = os.path.join(str(Path(__file__).parent.absolute()), 'environment.ini')
print(env_path)
cfg.read(env_path)

#=========================================================================
#                           TIMING CONFIG
#=========================================================================
u = datetime.datetime.utcnow()
u = u.replace(tzinfo=pytz.timezone("Asia/Ho_Chi_Minh"))


#=========================================================================
#                          PROJECT INFORMATION 
#=========================================================================
PROJECT = cfg['project']
PROJECT_NAME = PROJECT['name']
ENVIRONMENT = PROJECT['environment']
HOST = PROJECT['host']
PORT = PROJECT['port']
USER = PROJECT['user']
PASSWORD = PROJECT['password']

NGINX = cfg['nginx']
NGINX_HOST = NGINX['host']
FE_PORT = 3000



#=========================================================================
#                          AUTHENTICATE INFORMATION 
#=========================================================================
AUTHENTICATE = cfg['authenticate']
ENCODE_TYPE = AUTHENTICATE['encode']
DIGEST = AUTHENTICATE['digest']    
ALGORITHM = AUTHENTICATE['algorithm']
ROUNDS = AUTHENTICATE.getint('rounds')
SALT_SIZE = AUTHENTICATE.getint('salt_size')
SALT = bytes(AUTHENTICATE['salt'], "utf-8").decode('unicode_escape')
ACCESS_TOKEN_EXPIRE_MINUTES = AUTHENTICATE.getint('access_expire')
FRESH_TOKEN_EXPIRE_MINUTES = AUTHENTICATE.getint('fresh_expire')
SECRET_KEY = AUTHENTICATE['secret_key']


#=========================================================================
#                          DATABASE INFORMATION 
#=========================================================================
DATABASE = cfg['database']

SQLALCHEMY_DATABASE_URL = "{type}://{user}:{pw}@{host}:{port}/{db_name}" \
    .format(
        type = DATABASE['type'],
        user = DATABASE['user'],
        pw = DATABASE['pass'],
        host = DATABASE['host'],
        port = DATABASE['port'],
        db_name = DATABASE['database'],
    )
DATABASE_SCHEMA = DATABASE['schema']

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

#=========================================================================
#                          ML INFORMATION 
#=========================================================================
DL = cfg['dl']
DL_IMAGE_TYPE = DL['image_type']
DL_STORAGE_PATH = DL['storage_path']
DL_STORAGE_UPLOAD_PATH = DL['storage_upload_path']
DL_OBJECT_DETECTION_TASK = DL['object_detection_task']
DL_QUERY_NAME = DL['query_name']


