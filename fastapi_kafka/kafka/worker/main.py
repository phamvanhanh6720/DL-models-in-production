import json
import os
import asyncio
import logging
from logging.handlers import TimedRotatingFileHandler


import torch
# from torch import autocast
from aiokafka import AIOKafkaConsumer
from diffusers import StableDiffusionPipeline

import config
from helpers import time as time_helper
from helpers.storage import create_path

from main_kafka import redis_object

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler = TimedRotatingFileHandler('{}{}-{}-{}_{}h-00p-00.log'.format(
    config.DL_LOG,
    config.u.year, config.u.month, config.u.day, config.u.hour),
    when="midnight", interval=1, encoding='utf8'
)
handler.suffix = "%Y-%m-%d"
handler.setFormatter(formatter)
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(handler)


access_token = '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'
logger.info('Loading model ...')
print('Loading model....')
model = StableDiffusionPipeline.from_pretrained(
                "CompVis/stable-diffusion-v1-4",
                use_auth_token=access_token)
CUDA_ID = os.getenv('CUDA_ID')
device = 'cuda:{}'.format(CUDA_ID) if torch.cuda.is_available() else 'cpu'
logger.info(device)
if 'cuda' in device:
     model = model.to(device)

logger.info("Model loaded")
print('Model loaded')


def infer(prompt_text):

    if 'cuda' in device:
        # with autocast(device):
        with torch.cuda.amp.autocast(True):
            image = model(prompt_text).images[0]
    else:
        image = model(prompt_text).images[0]

    return image


async def consume():
    consumer = AIOKafkaConsumer(
        config.KAFKA_TOPIC,
        bootstrap_servers=config.KAFKA_CONNECTION,
        group_id=config.KAFKA_GROUP_ID
    )
    await consumer.start()
    try:
        # Consume messages
        async for msg in consumer:
            data_dump = msg.value.decode()
            data = json.loads(data_dump)
            logger.info('Consumed: topic {} partition {} offset {} task-id {}'
                        .format(msg.topic, msg.partition, msg.offset, data['task_id']))

            time = time_helper.now_utc()
            data['time']['start_inference'] = str(time_helper.now_utc().timestamp())
            string_time = time_helper.str_yyyy_mm_dd(time)

            prompt_text = data['prompt_text']
            task_id = data['task_id']

            try:
                dir_path = config.DL_STORAGE_PATH + string_time
                img_path = os.path.join(dir_path, str(task_id) + config.DL_IMAGE_TYPE)
                create_path(dir_path)

                image = infer(prompt_text)
                image.save(img_path)

                data['inference_result_uri'] = "/api/v1/show-image/?path_image={}".format(img_path)
                data['time']['end_inference'] = str(time_helper.now_utc().timestamp())
                data['status'] = "SUCCESS"
                data_dump = json.dumps(data)
                redis_object.set(task_id, data_dump)
                logger.info('Task: {} done'.format(task_id))

            except Exception as e:
                data['time']['end_inference'] = str(time_helper.now_utc().timestamp())
                data['status'] = "FAILED"
                data['error'] = str(e)
                data_dump = json.dumps(data)
                redis_object.set(task_id, data_dump)
                logger.info('Task: {} failed'.format(task_id))

    finally:
        # Will leave consumer group; perform autocommit if enabled.
        await consumer.stop()

asyncio.run(consume())
