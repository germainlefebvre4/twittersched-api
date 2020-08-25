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
from tinydb import Query

from app.db import get_db

bp = Blueprint("queues", __name__)


@bp.route("/api/queues", methods=["GET"])
def getQueues():
    data = []
    page_offset = request.args.get("page", default=0, type=int)
    page_limit = 2

    # Database select
    db = get_db()
    table = db.table('queues')
    Queue = Query()
    data = table.search(Queue.user == 1)[page_offset*page_limit:page_offset*page_limit + page_limit]

    return jsonify(data)

@bp.route("/api/queues", methods=["POST"])
def postQueues():
    queueName = request.form.get("queue_name")
    userId = request.form.get("user_id", default=1, type=int)

    db = get_db()
    Queue = Query()
    table = db.table('queues')
    rows = table.search(
      (Queue.user == userId) &
      (Queue.name == queueName)
    )
    if len(rows) > 0:
        current_app.logger.info("Queue '{}' already exists.".format(queueName))
        return { "msg": "Queue '{}' already exists.".format(queueName) }, status.HTTP_409_CONFLICT

    table.insert(
      {
        "name": queueName,
        "user": userId
      }
    )

    return { "msg": "Queue '{}' created.".format(queueName) }, status.HTTP_201_CREATED


@bp.route("/api/queues/<int:id>", methods=["PUT"])
def putQueues():
    return jsonify({})

@bp.route("/api/queues/<int:id>", methods=["DELETE"])
def deleteQueues():
    return jsonify({})
