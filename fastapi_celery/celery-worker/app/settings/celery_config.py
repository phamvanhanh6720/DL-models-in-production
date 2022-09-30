import os
from kombu import Queue
import configparser
from pathlib import Path


cfg = configparser.ConfigParser()
env_path = os.path.join(str(Path(__file__).parent.absolute()), 'environment.ini')
cfg.read(env_path)

#=========================================================================
#                          CELERY INFORMATION 
#=========================================================================
CELERY = cfg['celery']

# Set worker to ack only when return or failing (unhandled expection)
task_acks_late = True

# Worker only gets one task at a time
worker_prefetch_multiplier = 1

QUERY_NAME = CELERY["query"]

# Create queue for worker
task_queues = [Queue(name=QUERY_NAME)]

# Set Redis key TTL (Time to live)
result_expires = 60 * 60 * 48  # 48 hours in seconds


# #=========================================================================
# #                          ML INFORMATION 
# #=========================================================================
DL_TASK_NAME = CELERY['task_name']
DL_STORAGE_RESULT_PATH = CELERY['storage_result_path']
DL_IMAGE_TYPE = CELERY['image_type']
