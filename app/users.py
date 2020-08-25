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

bp = Blueprint("users", __name__)


@bp.route("/api/users", methods=["GET"])
def getUsers():
    data = []
    page_offset = request.args.get("page", default=0, type=int)
    page_limit = 2

    # Database select
    db = get_db()
    table = db.table('users')
    User = Query()
    data = table.get(doc_id=1)

    return jsonify(data)

@bp.route("/api/users", methods=["POST"])
def postUsers():
    paramUserName = request.form.get("username")

    userName = "{}".format(paramUserName)

    db = get_db()
    User = Query()
    table = db.table('users')
    rows = table.search(
      (User.username == userName)
    )
    if len(rows) > 0:
        current_app.logger.info("User '{}' already exists.".format(userName))
        return { "msg": "User '{}' already exists.".format(userName) }, status.HTTP_409_CONFLICT

    table.insert(
      {
        "username": userName,
      }
    )

    return { "msg": "User '{}' created.".format(userName) }, status.HTTP_201_CREATED

@bp.route("/api/users/<int:id>", methods=["PUT"])
def putUsers():
    return jsonify({})

@bp.route("/api/users/<int:id>", methods=["DELETE"])
def deleteUsers():
    return jsonify({})
