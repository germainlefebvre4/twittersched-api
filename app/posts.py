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

bp = Blueprint("posts", __name__)


@bp.route("/api/posts", methods=["GET"])
def getPosts():
    data = []
    queueId = request.args.get("queue_id", type=int)
    page_offset = request.args.get("page", default=0, type=int)
    page_limit = 10

    with db_session() as s:
        data_posts = s.query(Post).filter(
            Post.queue_id == queueId
        ).limit(page_limit).offset(page_offset)
        for post in data_posts:
            print(post.id)
        data = [
            {
                "id": x.id,
                "title": x.title,
                "message": x.message,
                "queue": x.queue_id
            }
            for x in data_posts
        ]

    return jsonify(data)


@bp.route("/api/posts", methods=["POST"])
def postPosts():
    postTitle = request.form.get("post_title", type=str)
    postMessage = request.form.get("post_message", type=str)
    queueId = request.form.get("queue_id", type=int)
    #userId = request.form.get("user_id", default=1, type=int)

    if postTitle and postMessage and queueId:
        with db_session() as s:
            newPost = Post(
                title = postTitle,
                message = postMessage,
                queue_id = queueId
            )
            s.add(newPost)
            s.commit()

            return { "msg": f"Post '{postTitle}' created." }, status.HTTP_201_CREATED

    return { f"msg": "An error occured on creating post." }, status.HTTP_401_BAD_REQUEST

@bp.route("/api/posts/<int:postId>", methods=["PUT"])
def putPosts(postId):
    postTitle = request.form.get("post_title", type=str)
    postMessage = request.form.get("post_message", type=str)
    #queueId = request.form.get("queue_id", type=int)
    #userId = request.form.get("user_id", default=1, type=int)

    if postId and postTitle and postMessage:
        with db_session() as s:
            s.query(Post).filter(
                Post.id == postId
            ).update({
                Post.title: postTitle,
                Post.message: postMessage
            })
            s.commit()

            return { "msg": f"Post '{postId}' updated." }, status.HTTP_200_OK

    return { f"msg": "An error occured on updating post." }, status.HTTP_401_BAD_REQUEST

@bp.route("/api/posts/<int:postId>", methods=["DELETE"])
def deletePosts(postId):
    #queueId = request.form.get("queue_id", type=int)
    #userId = request.form.get("user_id", default=1, type=int)

    if postId: 
        with db_session() as s:
            s.query(Post).filter(
                Post.id == postId
            ).delete()
            s.commit()

            return { "msg": f"Post '{postId}' deleted." }, status.HTTP_200_OK

    return { f"msg": "An error occured on deleting post." }, status.HTTP_401_BAD_REQUEST
