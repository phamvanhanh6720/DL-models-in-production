import json
import logging
import os.path
from abc import ABC

from celery import Celery, Task
from init_broker import is_broker_running
from init_redis import is_backend_running

import torch
from torch import autocast
from diffusers import StableDiffusionPipeline


from helpers import time as time_helper
from settings import celery_config, config
from helpers.storage import create_path
from mq_main import redis


if not is_backend_running():
    exit()
if not is_broker_running():
    exit()


app = Celery(celery_config.QUERY_NAME, broker=config.BROKER, backend=config.REDIS_BACKEND)
app.config_from_object('settings.celery_config')


class PredictTask(Task, ABC):
    """
    Abstraction of Celery's Task class to support loading ML model.
    """
    abstract = True

    def __init__(self):
        super().__init__()
        self.model = None
        self.access_token = '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'
        self.device = 'cuda:0' if torch.cuda.is_available() else 'cpu'

    def __call__(self, *args, **kwargs):
        """
        Load model on first call (i.e. first task processed)
        Avoids the need to load model on each task request
        """
        if self.model is None:
            logging.info('Loading Model...')
            self.model = StableDiffusionPipeline.from_pretrained(
                "CompVis/stable-diffusion-v1-4",
                use_auth_token=self.access_token)
            if 'cuda' in self.device:
                self.model.to(self.device)
            logging.info('Model loaded')

        return self.run(*args, **kwargs)


@app.task(bind=True,
          base=PredictTask,
          name="{query}.{task_name}".format(
              query=celery_config.QUERY_NAME, 
              task_name=celery_config.DL_TASK_NAME))
def inference(self, task_id: str, data: bytes):
    """_summary_: object_detection by efi d2 model

    Args:
        task_id (str): _description_
        data (bytes): _description_

    Returns:
        _type_: _description_
    """
    data = json.loads(data)
    print(data)

    time = time_helper.now_utc()
    data['time']['start_inference'] = str(time_helper.now_utc().timestamp())
    string_time = time_helper.str_yyyy_mm_dd(time)

    prompt_text = data['prompt_text']
    try:
        dir_path = celery_config.DL_STORAGE_RESULT_PATH + string_time
        img_path = os.path.join(dir_path, str(task_id) + celery_config.DL_IMAGE_TYPE)
        create_path(dir_path)

        # inference
        if 'cuda' in self.device:
            with autocast(self.device):
                image = self.model(prompt_text).images[0]
                image.save(img_path)
        else:
            image = self.model(prompt_text).images[0]
            image.save(img_path)

        data['inference_result_uri'] = "/api/v1/show-image/?path_image={}".format(img_path)

        data['time']['end_inference'] = str(time_helper.now_utc().timestamp())
        data['status'] = "SUCCESS"
        data_dump = json.dumps(data)
        redis.set(task_id, data_dump)

    except Exception as e:
        data['time']['end_inference'] = str(time_helper.now_utc().timestamp())
        data['status'] = "FAILED"
        data['error'] = str(e)
        data_dump = json.dumps(data)
        redis.set(task_id, data_dump)
        