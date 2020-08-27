from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView
import sys
import inspect

from app import bcrypt, db_session
from app.models import User, BlacklistToken

bp = Blueprint('auth', __name__)


class RegisterAPI(MethodView):
    """
    User Registration Resource
    """

    def post(self):
        # get the post data
        #userName = request.form.get("username", type=str)
        #userEmail = request.form.get("email", type=str)
        #userPassword = request.form.get("password", type=str)
        userEmail = request.json["email"]
        userPassword = request.json["password"]

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
                # generate the auth token
                auth_token = user.encode_auth_token(user.id)
                responseObject = {
                    'status': 'success',
                    'message': 'Successfully registered.',
                    'auth_token': auth_token.decode()
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


class LoginAPI(MethodView):
    """
    User Login Resource
    """
    def post(self):
        #userEmail = request.form.get("email", type=str)
        #userPassword = request.form.get("password", type=str)
        userEmail = request.json["email"]
        userPassword = request.json["password"]
        with db_session() as s:
            try:
                # fetch the user data
                user = s.query(User).filter_by(
                    email=userEmail
                ).first()
                if user and bcrypt.check_password_hash(
                    user.password, userPassword
                ):
                    auth_token = user.encode_auth_token(user.id)
                    if auth_token:
                        responseObject = {
                            'status': 'success',
                            'message': 'Successfully logged in.',
                            'auth_token': auth_token.decode()
                        }
                        return make_response(jsonify(responseObject)), 200
                else:
                    responseObject = {
                        'status': 'fail',
                        'message': 'User does not exist.'
                    }
                    return make_response(jsonify(responseObject)), 404
            except Exception as e:
                print(e)
                responseObject = {
                    'status': 'fail',
                    'message': 'Try again'
                }
                return make_response(jsonify(responseObject)), 500


class UserAPI(MethodView):
    """
    User Resource
    """
    def get(self):
        # get the auth token
        auth_header = request.headers.get('Authorization')
        if auth_header:
            try:
                auth_token = auth_header.split(" ")[1]
            except IndexError:
                responseObject = {
                    'status': 'fail',
                    'message': 'Bearer token malformed.'
                }
                return make_response(jsonify(responseObject)), 401
        else:
            auth_token = ''
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                with db_session() as s:
                    user = s.query(User).filter_by(id=resp).first()
                    responseObject = {
                        'status': 'success',
                        'data': {
                            'user_id': user.id,
                            'email': user.email,
                            'admin': user.admin,
                            'registered_on': user.registered_on
                        }
                    }
                    return make_response(jsonify(responseObject)), 200
            responseObject = {
                'status': 'fail',
                'message': resp
            }
            return make_response(jsonify(responseObject)), 401
        else:
            responseObject = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return make_response(jsonify(responseObject)), 401


class LogoutAPI(MethodView):
    """
    Logout Resource
    """
    def post(self):
        # get auth token
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ''
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                # mark the token as blacklisted
                blacklist_token = BlacklistToken(token=auth_token)
                try:
                    # insert the token
                    with db_session() as s:
                        s.add(blacklist_token)
                        s.commit()
                    responseObject = {
                        'status': 'success',
                        'message': 'Successfully logged out.'
                    }
                    return make_response(jsonify(responseObject)), 200
                except Exception as e:
                    responseObject = {
                        'status': 'fail',
                        'message': e
                    }
                    return make_response(jsonify(responseObject)), 200
            else:
                responseObject = {
                    'status': 'fail',
                    'message': resp
                }
                return make_response(jsonify(responseObject)), 401
        else:
            responseObject = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return make_response(jsonify(responseObject)), 403

# define the API resources
registration_view = RegisterAPI.as_view('register_api')
login_view = LoginAPI.as_view('login_api')
user_view = UserAPI.as_view('user_api')
logout_view = LogoutAPI.as_view('logout_api')

# add Rules for API Endpoints
bp.add_url_rule(
    '/auth/register',
    view_func=registration_view,
    methods=['POST']
)
bp.add_url_rule(
    '/auth/login',
    view_func=login_view,
    methods=['POST']
)
bp.add_url_rule(
    '/auth/status',
    view_func=user_view,
    methods=['GET']
)
bp.add_url_rule(
    '/auth/logout',
    view_func=logout_view,
    methods=['POST']
)

