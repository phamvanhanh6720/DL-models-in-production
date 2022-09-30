from fastapi import APIRouter, BackgroundTasks, HTTPException
from starlette.status import (
    HTTP_200_OK, HTTP_400_BAD_REQUEST
)
import uuid
import json
from main_kafka import redis_object
from helpers import time as time_helper
import config
from api.v1.entities.model import DLTimeHandle, DlResult, DlResponse
from api.v1.resources.background import process_background


router = APIRouter()


@router.post("/process")
async def ml_process(
    *,
    prompt_text: str,
    background_tasks: BackgroundTasks
):
    if not len(prompt_text):
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="prompt is empty")

    time = time_helper.now_utc()
    task_id = str(uuid.uuid5(uuid.NAMESPACE_OID, config.DL_QUERY_NAME + "_" + str(time)))

    time_handle = DLTimeHandle(request_time=str(time.timestamp())).__dict__
    data = DlResult(task_id=task_id, time=time_handle, prompt_text=prompt_text)
    redis_object.set(task_id, json.dumps(data.__dict__))

    background_tasks.add_task(process_background, task_id, data)

    return DlResponse(status="PENDING", time=time, status_code=HTTP_200_OK, task_id=task_id, prompt_text=prompt_text)


@router.get("/status/{task_id}", response_model=DlResult)
def ml_status(
    *,
    task_id: str,
):
    data = redis_object.get(task_id)
    if data is None:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail='task id not found!')
    message = json.loads(data)

    return message
