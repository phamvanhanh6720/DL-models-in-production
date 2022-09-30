import json
from api.v1.entities.model import DlResult
import config
from main_kafka import redis_object, producer


async def process_background(
        task_id: str,
        data: DlResult
):

    try:
        data_dump = json.dumps(data.__dict__)
        redis_object.set(task_id, data_dump)
        # print(config.ML_QUERY_NAME, config.ML_OBJECT_DETECTION_TASK)
        await producer.send_and_wait(config.KAFKA_TOPIC, json.dumps(data.__dict__, ensure_ascii=False).encode('utf-8'))

    except Exception as e:
        data.status = "FAILED"
        data.error = str(e)
        redis_object.set(task_id, json.dumps(data.__dict__))