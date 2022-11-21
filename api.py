import json
from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel
import pika

completed_tasks = 0


class Task(BaseModel):
    taskid: str
    description: str
    params: Union[dict, None] = None


app = FastAPI()


@app.post("/AddTask")
def add_task(task: Task):
    global completed_tasks
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()
    channel.queue_declare(queue='tasks')
    channel.basic_publish(
        exchange='',
        routing_key='tasks',
        body=task.json(),
        properties=pika.BasicProperties(content_type='application/json')
    )
    connection.close()
    completed_tasks += 1
    return {"result": "success"}


@app.get("/GetStats")
def get_stats():
    global completed_tasks
    return {"tasks_completed": completed_tasks}
