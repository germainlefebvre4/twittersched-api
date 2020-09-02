from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView
import sys
import inspect

from app import bcrypt, db_session, jwt
from app.models import User

from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    jwt_refresh_token_required, create_refresh_token,
    get_jwt_identity, 
)

bp = Blueprint('auth', __name__)

@bp.route('/auth/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    userEmail = request.json.get('email', None)
    userPassword = request.json.get('password', None)
    if not userEmail:
        return jsonify({"msg": "Missing email parameter"}), 400
    if not userPassword:
        return jsonify({"msg": "Missing password parameter"}), 400

    with db_session() as s:
        user = s.query(User) \
            .filter_by(
                email=userEmail
            ) \
            .first()
                #password=userPassword
        if not user:
            return jsonify({"msg": "Failed to login"}), 403
        
    #if userEmail != 'germain.lefebvre4@gmail.com' or userPassword != 'password':
    #    return jsonify({"msg": "Bad email or password"}), 401

    # Identity can be any data that is json serializable
    ret = {
        'access_token': create_access_token(identity=userEmail),
        'refresh_token': create_refresh_token(identity=userEmail)
    }
    return jsonify(ret), 200


@bp.route('/auth/register', methods=['POST'])
def register():
    userEmail = request.json.get("email", None)
    userPassword = request.json.get("password", None)

    with db_session() as s:
      user = s.query(User).filter_by(email=userEmail).first()
      if not user:
        try:
            user = User(
                email=userEmail,
                password=userPassword
            )
            # insert the user
            s.add(user)
            s.commit()
            # generate auth token
            access_token = create_access_token(identity=userEmail)
            # response data
            responseObject = {
                'status': 'success',
                'message': 'Successfully registered.',
                'access_token': access_token
            }
            return make_response(jsonify(responseObject)), 201
        except Exception as e:
            responseObject = {
                'status': 'fail',
                'message': 'Some error occurred. Please try again.'
            }
            return make_response(jsonify(responseObject)), 401
      else:
        responseObject = {
            'status': 'fail',
            'message': 'User already exists. Please Log in.',
        }
        return make_response(jsonify(responseObject)), 202

@jwt.user_claims_loader
def add_claims_to_access_token(identity):
    with db_session() as s:
        user = s.query(User).filter_by(email=identity).first()

    roles = ['user']
    if user.admin:
        roles += ['admin']

    return {
        'id': user.id,
        'roles': roles
    }

@bp.route('/auth/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    current_user = get_jwt_identity()
    ret = {
        'access_token': create_access_token(identity=current_user)
    }
    return jsonify(ret), 200
