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

from app.models import User, Queue, Post
from app.database import db_session

bp = Blueprint("queues", __name__)


@bp.route("/api/queues", methods=["GET"])
def getQueues():
    data = []
    queueId = request.args.get("queue_id", type=int)
    page_offset = request.args.get("page", default=0, type=int)
    page_limit = 10

    with db_session() as s:
        data_queues = s.query(Queue).filter(
            Queue.user_id == 1
        ).limit(page_limit).offset(page_offset)
        for queue in data_queues:
            print(queue.id)
        data = [
            {
                "id": x.id,
                "name": x.name
            }
            for x in data_queues
        ]

    return jsonify(data)

@bp.route("/api/queues", methods=["POST"])
def postQueues():
    queueName = request.form.get("queue_name")
    userId = request.form.get("user_id", default=1, type=int)

    return { "msg": "Queue '{}' created.".format(queueName) }, status.HTTP_201_CREATED


@bp.route("/api/queues/<int:id>", methods=["PUT"])
def putQueues():
    return jsonify({})

@bp.route("/api/queues/<int:id>", methods=["DELETE"])
def deleteQueues():
    return jsonify({})
