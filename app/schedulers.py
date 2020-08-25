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

bp = Blueprint("schedules", __name__)


@bp.route("/api/schedules", methods=["GET"])
def getSchedules():
    data = []
    page_offset = request.args.get("page", default=0, type=int)
    page_limit = 2

    # Database select
    db = get_db()
    table = db.table('schedules')
    Schedule = Query()
    data = table.search(Schedule.user == 1)[page_offset*page_limit:page_offset*page_limit + page_limit]

    return jsonify(data)

# ONLY FOR TESTS
@bp.route("/api/schedules", methods=["POST"])
def postSchedules():
    scheduleName = request.form.get("schedule_name")
    userId = request.form.get("user_id", default=1, type=int)

    db = get_db()
    Schedule = Query()
    table = db.table('schedules')
    rows = table.search(
      (Schedule.user == userId) &
      (Schedule.name == scheduleName)
    )
    if len(rows) > 0:
        current_app.logger.info("Schedule '{}' already exists.".format(scheduleName))
        return { "msg": "Schedule '{}' already exists.".format(scheduleName) }, status.HTTP_409_CONFLICT

    table.insert(
      {
        "name": scheduleName,
        "user": userId
      }
    )

    return { "msg": "Schedule '{}' created.".format(scheduleName) }, status.HTTP_201_CREATED


@bp.route("/api/schedules/<int:id>", methods=["PUT"])
def putSchedules():
    return jsonify({})

@bp.route("/api/schedules/<int:id>", methods=["DELETE"])
def deleteSchedules():
    return jsonify({})
