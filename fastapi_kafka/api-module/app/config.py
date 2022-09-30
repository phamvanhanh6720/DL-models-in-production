from pathlib import Path
import os
import configparser
import datetime
import pytz 


cfg = configparser.ConfigParser()

env_path = os.path.join(str(Path(__file__).parent.absolute()), 'environment.ini')
cfg.read(env_path)


u = datetime.datetime.utcnow()
u = u.replace(tzinfo=pytz.timezone("Asia/Ho_Chi_Minh"))


PROJECT = cfg['project']
PROJECT_NAME = PROJECT['name']

# REDIS INFORMATION
REDIS = cfg['redis']
REDIS_BACKEND = "redis://:{password}@{hostname}:{port}/{db}".format(
    hostname=REDIS['host'],
    password=REDIS['pass'],
    port=REDIS['port'],
    db=REDIS['db']
)


KAFKA = cfg['kafka']
KAFKA_TOPIC = KAFKA['topic']
KAFKA_CONNECTION = '{}:{}'.format(
    KAFKA['host'],
    KAFKA['port']
)


# DL INFORMATION
DL = cfg['dl']
DL_IMAGE_TYPE = DL['image_type']
DL_STORAGE_PATH = DL['storage_path']
DL_TASK_NAME = DL['task_name']
DL_QUERY_NAME = DL['query_name']
DL_LOG = DL['logs']

