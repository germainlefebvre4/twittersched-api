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
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity, get_jwt_claims
)

from app.models import User, Queue
from app.database import db_session

bp = Blueprint("queues", __name__)


@bp.route("/api/queues", methods=["GET"])
@jwt_required
def getQueues():
    current_user = get_jwt_identity()
    current_user_claims = get_jwt_claims()

    data = []
    userId = current_user_claims.get('id', None)
    page_offset = request.args.get("page", default=0, type=int)
    page_limit = 10


    with db_session() as s:
        data_queues = s.query(Queue).filter(
            Queue.user_id == userId
        ).limit(page_limit).offset(page_offset)
        #for queue in data_queues:
        #    print(queue.id)
        data = [
            {
                "id": x.id,
                "name": x.name,
                "cron": x.cron,
                "user": x.user_id
            }
            for x in data_queues
        ]

    return jsonify(data)

@bp.route("/api/queues/<int:queueId>", methods=["GET"])
@jwt_required
def getQueuesById(queueId):
    current_user = get_jwt_identity()
    current_user_claims = get_jwt_claims()

    data = []
    userId = current_user_claims.get('id', None)
    page_offset = request.args.get("page", default=0, type=int)
    page_limit = 10


    with db_session() as s:
        data_queues = s.query(Queue).filter(
            Queue.user_id == userId
        ).limit(page_limit).offset(page_offset)
        #for queue in data_queues:
        #    print(queue.id)
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
@jwt_required
def queueQueues():
    current_user = get_jwt_identity()
    current_user_claims = get_jwt_claims()

    queueName = request.json.get("name", None)
    queueCron = request.json.get("cron", None)
    userId = current_user_claims.get('id', None)

    if queueName and queueCron and userId:
        with db_session() as s:
            newQueue = Queue(
                name = queueName,
                cron = queueCron,
                user_id = userId
            )
            s.add(newQueue)

            return { "msg": f"Queue '{queueName}' created." }, status.HTTP_201_CREATED

    return { f"msg": "An error occured on creating queue." }, status.HTTP_400_BAD_REQUEST


@bp.route("/api/queues/<int:queueId>", methods=["PUT"])
@jwt_required
def putQueues(queueId):
    current_user = get_jwt_identity()
    current_user_claims = get_jwt_claims()

    queueName = request.json.get("name", None)
    queueCron = request.json.get("cron", None)
    userId = current_user_claims.get('id', None)

    if (queueName or queueCron) and userId:
        with db_session() as s:
            if queueName:
                s.query(Queue).filter(
                    Queue.id == queueId,
                    Queue.user_id == userId
                ).update({
                    Queue.name: queueName
                })
            if queueCron:
                s.query(Queue).filter(
                    Queue.id == queueId,
                    Queue.user_id == userId
                ).update({
                    Queue.cron: queueCron
                })

        return { "msg": f"Queue '{queueId}' updated." }, status.HTTP_200_OK

    return { f"msg": "An error occured on updating queue." }, status.HTTP_400_BAD_REQUEST


@bp.route("/api/queues/<int:queueId>", methods=["DELETE"])
@jwt_required
def deleteQueues(queueId):
    current_user = get_jwt_identity()
    current_user_claims = get_jwt_claims()

    userId = current_user_claims.get('id')

    if queueId: 
        with db_session() as s:
            s.query(Queue).filter(
                Queue.id == queueId,
                Queue.user_id == userId
            ).delete()

            return { "msg": f"Queue '{queueId}' deleted." }, status.HTTP_200_OK

    return { f"msg": "An error occured on deleting queue." }, status.HTTP_400_BAD_REQUEST
