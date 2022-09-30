import json
from api.entities.model import DlResult
from settings import config
from mq_main import redis, celery_execute


def process_background(task_id: str,
                       data: DlResult
                       ):

    try:
        data_dump = json.dumps(data.__dict__)
        redis.set(task_id, data_dump)
        # print(config.ML_QUERY_NAME, config.ML_OBJECT_DETECTION_TASK)
        celery_execute.send_task(
            name="{}.{}".format(config.DL_QUERY_NAME, config.DL_TASK_NAME),
            kwargs={
                'task_id': task_id,
                'data': data_dump,
            },
            queue=config.DL_QUERY_NAME
        )
    except Exception as e:
        data.status = "FAILED"
        data.error = str(e)
        redis.set(task_id, json.dumps(data.__dict__))