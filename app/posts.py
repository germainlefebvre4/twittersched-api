from sqlalchemy.dialects import postgresql

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

from app.models import User, Queue, Post
from app.database import db_session

bp = Blueprint("posts", __name__)


@bp.route("/api/posts", methods=["GET"])
@jwt_required
def getPosts():
    current_user = get_jwt_identity()
    current_user_claims = get_jwt_claims()

    data = []
    queueId = request.args.get("queue_id", None)
    userId = current_user_claims.get('id', None)
    page_offset = request.args.get("page", None)
    page_limit = 10

    with db_session() as s:
        data_posts = s.query(Post) \
        .join(Queue) \
        .filter(
            #Post.queue_id == queueId,
            Queue.user_id == userId
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


@bp.route("/api/posts/<int:postId>", methods=["GET"])
@jwt_required
def getPostsById(postId):
    current_user = get_jwt_identity()
    current_user_claims = get_jwt_claims()

    data = []
    page_offset = request.args.get("page", None)
    page_limit = 10

    with db_session() as s:
        data_posts = s.query(Post).filter(
            Post.id == postId
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


@bp.route("/api/queues/<int:queueId>/posts", methods=["GET"])
@jwt_required
def getPostsByQueueId(queueId):
    current_user = get_jwt_identity()
    current_user_claims = get_jwt_claims()

    data = []
    page_offset = request.args.get("page", 0)
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


#@bp.route("/api/posts", methods=["POST"])
@bp.route("/api/queues/<int:queueId>/posts", methods=["POST"])
@jwt_required
def postPostByQueueId(queueId):
    current_user = get_jwt_identity()
    current_user_claims = get_jwt_claims()

    postTitle = request.json.get("title", None)
    postMessage = request.json.get("message", None)
    #queueId = request.json.get("queue_id", None)
    userId = current_user_claims.get('id', None)

    if postTitle and postMessage and queueId:
        with db_session() as s:
            newPost = Post(
                title = postTitle,
                message = postMessage,
                queue_id = queueId
            )
            s.add(newPost)

            return { "msg": f"Post '{postTitle}' created." }, status.HTTP_201_CREATED

    return { f"msg": "An error occured on creating post." }, status.HTTP_400_BAD_REQUEST


@bp.route("/api/posts/<int:postId>", methods=["PUT"])
@jwt_required
def putPosts(postId):
    current_user = get_jwt_identity()
    current_user_claims = get_jwt_claims()

    postTitle = request.json.get("title", None)
    postMessage = request.json.get("message", None)
    queueId = request.json.get("queue_id", None)
    userId = request.json.get("user_id", None)

    if postId and postTitle and postMessage:
        with db_session() as s:
            s.query(Post).filter(
                Post.id == postId
            ).update({
                Post.title: postTitle,
                Post.message: postMessage
            })

            return { "msg": f"Post '{postId}' updated." }, status.HTTP_200_OK

    return { f"msg": "An error occured on updating post." }, status.HTTP_400_BAD_REQUEST


@bp.route("/api/posts/<int:postId>", methods=["DELETE"])
def deletePosts(postId):
    #queueId = request.json.get("queue_id", type=int)
    #userId = request.json.get("user_id", default=1, type=int)

    if postId: 
        with db_session() as s:
            s.query(Post).filter(
                Post.id == postId
            ).delete()
            s.commit()

            return { "msg": f"Post '{postId}' deleted." }, status.HTTP_200_OK

    return { f"msg": "An error occured on deleting post." }, status.HTTP_400_BAD_REQUEST
