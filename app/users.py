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


bp = Blueprint("users", __name__)


@bp.route("/api/users", methods=["GET"])
def getUsers():
    data = []
    page_offset = request.args.get("page", default=0, type=int)
    page_limit = 2

    # Database select
    with db_session() as s:
        data_queues = s.query(Queue)
        for queue in data_queues:
            print(queue.id)

    return jsonify(data)

@bp.route("/api/users", methods=["POST"])
def postUsers():
    paramUserName = request.form.get("username")

    userName = "{}".format(paramUserName)

    return { "msg": "User '{}' created.".format(userName) }, status.HTTP_201_CREATED

@bp.route("/api/users/<int:id>", methods=["PUT"])
def putUsers():
    return jsonify({})

@bp.route("/api/users/<int:id>", methods=["DELETE"])
def deleteUsers():
    return jsonify({})
