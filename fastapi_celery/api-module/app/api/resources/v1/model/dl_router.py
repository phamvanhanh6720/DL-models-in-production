from fastapi import APIRouter, UploadFile, File, Form, BackgroundTasks, HTTPException, Depends
from starlette.status import (
    HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR
)
import uuid
import json
from mq_main import redis
from helpers import time as time_helper
from settings import config
from api.entities.model import DLTimeHandle, DlResult, DlResponse
from api.resources.v1.model.background import process_background


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
    redis.set(task_id, json.dumps(data.__dict__))

    background_tasks.add_task(process_background, task_id, data)

    return DlResponse(status="PENDING", time=time, status_code=HTTP_200_OK, task_id=task_id, prompt_text=prompt_text)


@router.get("/status/{task_id}", response_model=DlResult)
def ml_status(
    *,
    task_id: str,
):
    data = redis.get(task_id)
    if data is None:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail='task id not found!')
    message = json.loads(data)

    return message
