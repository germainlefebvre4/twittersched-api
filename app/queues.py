from flask import Flask, redirect, url_for, request, render_template, current_app
from flask import jsonify
from flask import Blueprint
from flask_cors import CORS
from flask_api import status
import logging
import sys
import datetime as dt
import inspect
import json

from app.models import User, Queue, Queue
from app.database import db_session

bp = Blueprint("queues", __name__)


@bp.route("/api/queues", methods=["GET"])
def getQueues():
    data = []
    #queueId = request.args.get("queue_id", type=int)
    userId = 1
    page_offset = request.args.get("page", default=0, type=int)
    page_limit = 10

    with db_session() as s:
        data_queues = s.query(Queue).filter(
            Queue.user_id == userId
        ).limit(page_limit).offset(page_offset)
        for queue in data_queues:
            print(queue.id)
        data = [
            {
                "id": x.id,
                "title": x.name,
                "message": x.cron,
                "user": x.user_id
            }
            for x in data_queues
        ]

    return jsonify(data)


@bp.route("/api/queues", methods=["POST"])
def queueQueues():
    queueName = request.form.get("queue_name", type=str)
    queueCron = request.form.get("queue_cron", type=str)
    userId = 1

    if queueName and queueCron and userId:
        with db_session() as s:
            newQueue = Queue(
                name = queueName,
                cron = queueCron,
                user_id = userId
            )
            s.add(newQueue)
            s.commit()

            return { "msg": f"Queue '{queueName}' created." }, status.HTTP_201_CREATED

    return { f"msg": "An error occured on creating queue." }, status.HTTP_401_BAD_REQUEST


@bp.route("/api/queues/<int:queueId>", methods=["PUT"])
def putQueues(queueId):
    queueName = request.form.get("queue_name", type=str)
    queueCron = request.form.get("queue_cron", type=str)
    userId = 1

    if queueName and queueCron and userId:
        with db_session() as s:
            s.query(Queue).filter(
                Queue.id == queueId,
                Queue.user_id == userId
            ).update({
                Queue.name: queueName,
                Queue.cron: queueCron
            })
            s.commit()

            return { "msg": f"Queue '{queueId}' updated." }, status.HTTP_200_OK

    return { f"msg": "An error occured on updating queue." }, status.HTTP_401_BAD_REQUEST


@bp.route("/api/queues/<int:queueId>", methods=["DELETE"])
def deleteQueues(queueId):
    userId = 1

    if queueId: 
        with db_session() as s:
            s.query(Queue).filter(
                Queue.id == queueId,
                Queue.user_id == userId
            ).delete()
            s.commit()

            return { "msg": f"Queue '{queueId}' deleted." }, status.HTTP_200_OK

    return { f"msg": "An error occured on deleting queue." }, status.HTTP_401_BAD_REQUEST
