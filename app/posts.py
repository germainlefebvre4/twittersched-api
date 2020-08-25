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

bp = Blueprint("posts", __name__)


@bp.route("/api/posts", methods=["GET"])
def getPosts():
    data = []
    queueId = request.args.get("queue_id", type=int)
    page_offset = request.args.get("page", default=0, type=int)
    page_limit = 10

    # Database select
    db = get_db()
    table = db.table('posts')
    Post = Query()
    data = table.search(Post.queue == queueId)[page_offset*page_limit:page_offset*page_limit + page_limit]

    return jsonify(data)

@bp.route("/api/posts", methods=["POST"])
def postPosts():
    postTitle = request.form.get("post_title", type=str)
    postMessage = request.form.get("post_message", type=str)
    queueId = request.form.get("queue_id", type=int)
    userId = request.form.get("user_id", default=1, type=int)

    db = get_db()
    Post = Query()
    table = db.table('posts')

    table.insert(
      {
        "queue": queueId,
        "user": userId,
        "title": postTitle,
        "message": postMessage
      }
    )

    return { "msg": "Post '{}' created.".format(postTitle) }, status.HTTP_201_CREATED

@bp.route("/api/posts/<int:id>", methods=["PUT"])
def putPosts():
    return jsonify({})

@bp.route("/api/posts/<int:id>", methods=["DELETE"])
def deletePosts():
    return jsonify({})
