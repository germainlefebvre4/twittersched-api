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

bp = Blueprint("dashboard", __name__)


@bp.route("/api/dashboard", methods=["GET"])
def getDashboard():
    return { "msg": "Dashboard" }

