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

from app.models import User, User, User
from app.database import db_session

bp = Blueprint("users", __name__)


@bp.route("/api/users", methods=["GET"])
def getUsers():
    data = []
    page_offset = request.args.get("page", default=0, type=int)
    page_limit = 10

    with db_session() as s:
        data_users = s.query(User).filter() \
            .limit(page_limit) \
            .offset(page_offset)
        for user in data_users:
            print(user.id)
        data = [
            {
                "id": x.id,
                "username": x.username
            }
            for x in data_users
        ]

    return jsonify(data)


@bp.route("/api/users", methods=["POST"])
def userUsers():
    userName = request.form.get("user_name", type=str)

    if userName:
        with db_session() as s:
            newUser = User(
                username = userName,
            )
            s.add(newUser)
            s.commit()

            return { "msg": f"User '{userName}' created." }, status.HTTP_201_CREATED

    return { f"msg": "An error occured on creating user." }, status.HTTP_401_BAD_REQUEST


@bp.route("/api/users/<int:userId>", methods=["PUT"])
def putUsers(userId):
    userName = request.form.get("user_name", type=str)

    if userName:
        with db_session() as s:
            s.query(User).filter(
                User.id == userId,
            ).update({
                User.username: userName,
            })
            s.commit()

            return { "msg": f"User '{userId}' updated." }, status.HTTP_200_OK

    return { f"msg": "An error occured on updating user." }, status.HTTP_401_BAD_REQUEST


@bp.route("/api/users/<int:userId>", methods=["DELETE"])
def deleteUsers(userId):
    if userId: 
        with db_session() as s:
            s.query(User).filter(
                User.id == userId,
            ).delete()
            s.commit()

            return { "msg": f"User '{userId}' deleted." }, status.HTTP_200_OK

    return { f"msg": "An error occured on deleting user." }, status.HTTP_401_BAD_REQUEST
